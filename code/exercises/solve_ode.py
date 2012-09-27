import numpy as np
from traits.api import (HasTraits, Str, Int, List,  Float, Instance, Either, 
    Array, Property, cached_property)

class ODE(HasTraits):
    """ An ODE of the form dX/dt = f(X).
    """
    name = Str
    num_vars = Int(0)
    vars = List(Str, desc='The names of the variables of X vector')

    def eval(self, X, t):
        """ Evaluate the derivative function f(X). """
        raise NotImplementedError

    def default_domain(self):
        return [(0.0,10.0) for i in range(len(self.vars))]

class LorenzEquation(ODE):
    name = 'Lorenz Equation'
    num_vars = 3
    vars = ['x', 'y', 'z']
    s = Float(10)
    r = Float(28)
    b = Float(8./3)

    def eval(self, X, t):
        x, y, z = X[0], X[1], X[2]
        return np.array([self.s*(y-x),
                             self.r*x - y - x*z,
                             x*y - self.b*z])

class ODESolver(HasTraits):
    ode = Instance(ODE)
    initial_state = Either(Float, Array)
    t = Array
    solution = Property(Array, depends_on='initial_state, t, ode')
            
    @cached_property
    def _get_solution(self):
        return self.solve()

    def solve(self):
        """ Solve the ODE and return the values 
        of the solution vector at specified times t. 
        """
        from scipy.integrate import odeint
        return odeint(self.ode.eval, self.initial_state, 
                      self.t)

###############################################################################
# Find the solution of the ODE.
# Hint: you can use an initial state of [1,1,1] and a t = [1, 2, 4] or so.
