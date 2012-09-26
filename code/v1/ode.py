
import numpy
from scipy.integrate import odeint
from traits.api import HasTraits, Str, Either, List, Instance, Float, Array, Int, Property, cached_property, Expression, on_trait_change
from traitsui.api import View, Item, RangeEditor


class ODE(HasTraits):
    """ An ODE of the form dX/dt = f(X) """
    name = Str
    num_vars = Int(0)
    vars = Either(List(Str), Str, desc='The names of the variables of X vector')
    t_var = Str('Time')

    def eval(self, X, t):
        """ Evaluate the derivative function f(X). """
        raise NotImplementedError


class EpidemicODE(ODE):
    """ The spread of an epidemic in a population
        $\frac{dy}{dt} = ky(L-y)$
    where $L$ is the total population
    """
    name = 'Epidemic ODE'
    num_vars = 1
    vars = 'Epidemic Spread'
    L = Float(2.5e5)
    k = Float(3e-5)

    def eval(self, y, t):
        return self.k * y * (self.L-y)


class LorenzEquation(ODE):
    name = 'Lorenz Equation'
    num_vars = 3
    vars = ['x', 'y', 'z']
    s = Float(10)
    r = Float(28)
    b = Float(8./3)

    view = View(Item('s', editor=RangeEditor(low=0.0, high=20.0)),
                Item('r', editor=RangeEditor(low=20.0, high=36.0)),
                Item('b', editor=RangeEditor(low=0.0, high=5.0)))

    def eval(self, X, t):
        x, y, z = X[0], X[1], X[2]
        return numpy.array([self.s*(y-x),
                             self.r*x - y - x*z,
                             x*y - self.b*z])

class GenericODE(ODE):
    name = "Generic ODE"
    num_vars = Int(1)
    vars = List(Str)
    equations = List(Expression)

    @on_trait_change('num_vars')
    def _on_num_vars_changed(self, object, name, old, new):
        if old > new:
            self.equations = self.equations[:new]
        else:
            self.equations.extend(['x%d'%(i) for i in range(old, new)])

class ODESolver(HasTraits):
    """ A single solution state of the ODE (fixed initial condn.) """
    ode = Instance(ODE)
    initial_state = Either(Float, Array)
    t_arr = Array
    soln_arr = Property(Array, depends_on='initial_state, t_arr, ode')

    @cached_property
    def _get_soln_arr(self):
        return self.solve()

    def solve(self):
        """ Solve the ODE and return the values of the solution vector at
        specified times t. """
        return odeint(self.ode.eval, self.initial_state, self.t_arr)


if __name__ == '__main__':
    ode = EpidemicODE()
    soln = ODESolver(ode=ode, initial_state=250, t_arr=numpy.linspace(0,10,101))
    from matplotlib import pyplot
    fig = pyplot.plot(soln.t_arr, soln.soln_arr)
    pyplot.show()

