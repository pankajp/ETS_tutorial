# -*- coding: utf-8 -*-

import numpy as np

from traits.api import (Either, HasTraits, List, Str, Range, Instance, Float,
        Array, Property, cached_property)

from traitsui.api import View, Item, RangeEditor

class ODE(HasTraits):
    """ An ODE of the form dX/dt = f(X) """
    name = Str
    vars = Either(List(Str), Str, 
                  desc='The names of variables')
    def eval(self, X, t):
        """ Evaluate the derivative, f(X). 
        """
        raise NotImplementedError

class LorenzEquation(ODE):
    name = 'Lorenz Equation'
    vars = ['x', 'y', 'z']
    s = Range(0.0, 20.0, 10.0, 
              desc='the parameter s')
    r = Float(28.0)
    b = Float(8./3)

    view = View(Item('s'),
                Item('r'),
                Item('b'),
                title='Lorenz equation')

    def eval(self, X, t):
        x, y, z = X[0], X[1], X[2]
        u = self.s*(y-x)
        v = self.r*x - y - x*z
        w = x*y - self.b*z
        return np.array([u, v, w])

lorentz_view = View(Item('s'),
                    Item('r', editor=RangeEditor(low=20.0, high=36.0)),
                    Item('b'),
                    title='Lorenz equation')


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
        return odeint(self.ode.eval, self.initial_state, self.t)


if __name__ == '__main__':
    ode = LorenzEquation()
    ode.configure_traits()
    ode.configure_traits(view=lorentz_view)
    solver = ODESolver(ode=ode, initial_state=[10.,50.,50.], t=np.linspace(0,10,1001))
