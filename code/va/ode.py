
import numpy
from functools import wraps
from scipy.integrate import odeint
from traits.api import (HasTraits, Str, List, Instance, Float, Array, Int, 
        Property, cached_property, Expression, on_trait_change, Event, Bool)
from traitsui.api import View, Item, RangeEditor


class ODE(HasTraits):
    """ An ODE of the form dX/dt = f(X).
    """
    name = Str
    num_vars = Int(0)
    vars = List(Str, desc='The names of the variables of X vector')
    changed = Event
    error = Bool(False)

    def eval(self, X, t):
        """ Evaluate the derivative function f(X). """
        raise NotImplementedError

    def default_domain(self):
        return [(0.0,10.0) for i in range(len(self.vars))]

class EpidemicODE(ODE):
    """ The spread of an epidemic in a population
        $\frac{dy}{dt} = ky(L-y)$
    where $L$ is the total population
    """
    name = 'Epidemic ODE'
    num_vars = 1
    vars = ['Epidemic Spread']
    L = Float(2.5e5)
    k = Float(3e-5)

    @on_trait_change('L,k')
    def _on_params_changed(self):
        self.changed = True

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

    @on_trait_change('s,r,b')
    def _on_params_changed(self):
        self.changed = True

    def eval(self, X, t):
        x, y, z = X[0], X[1], X[2]
        return numpy.array([self.s*(y-x),
                             self.r*x - y - x*z,
                             x*y - self.b*z])

def check_error(func):
    @wraps(func)
    def wrapper(self, X, t):
        error = False
        try:
            return func(self, X, t)
        except Exception as e:
            print(e)
            error = True
        finally:
            self.error = error
    return wrapper


class ODE1D(ODE):
    """ A generic 1D ODE """
    name = '1D ODE'
    num_vars = 1
    vars = List(['x'])
    equation = Expression('1-x')

    def eval(self, X, t):
        return eval(self.equation_, numpy.__dict__, locals())

class ODE2D(ODE):
    """ A generic 2D ODE """
    name = '2D ODE'
    num_vars = 2
    vars = List(['x', 'y'])
    equations = List(Expression, value=['-y', 'x'])

    def eval(self, X, t):
        return numpy.array([eval(self.equations[0], numpy.__dict__, locals()),
                             eval(self.equation[1], numpy.__dict__, locals())])

class ODE3D(ODE):
    """ A generic 3D ODE """
    name = '3D ODE'
    num_vars = 3
    vars = List(['x', 'y', 'z'])
    equations = List(Expression, value=['-y', 'x', 'y-x'])

    def eval(self, X, t):
        return numpy.array([eval(self.equations[0], numpy.__dict__, locals()),
                             eval(self.equation[1], numpy.__dict__, locals()),
                             eval(self.equation[2], numpy.__dict__, locals())])

class GenericODE(ODE):
    name = "Generic ODE"
    num_vars = Int(1)
    vars = List(Str)
    equations = List(Str)
    initial_state = Array

    view = View(Item('name'),
                Item('num_vars', label='Number of variables'),
                Item('equations'),
                resizable=True)

    @check_error
    def eval(self, X, t):
        localdict = {'t':t}
        for i, var in enumerate(self.vars):
            localdict[var] = X[..., i]
        return numpy.array([eval(self.equations[i], numpy.__dict__, localdict)
                            for i in range(self.num_vars)])

    @on_trait_change('equations[]')
    def _on_equations_changed(self):
        self.changed = True

    @on_trait_change('num_vars')
    def _on_num_vars_changed(self, object, name, old, new):
        if old > new:
            self.vars = self.vars[:new]
            self.equations = self.equations[:new]
        else:
            extend = ['x%d'%(i) for i in range(old, new)]
            self.vars.extend(extend)
            self.equations.extend(extend)

    def _vars_default(self):
        return ['x%d'%(i) for i in range(self.num_vars)]

    def _equations_default(self):
        return ['-%s' % var for var in self.vars]


class ODESolver(HasTraits):
    """ A single solution state of the ODE (fixed initial condn.) """
    ode = Instance(ODE)
    initial_state = List
    t = Array
    solution = Property(Array, depends_on='initial_state, t, ode.changed')

    t_low = Float(0)
    t_high = Float(10)
    t_num = Int(1000)

    view = View('initial_state',
                't_low',
                't_high',
                't_num',
                Item('object.ode.error', style='readonly'),
                resizable=True)

    @on_trait_change('ode.num_vars')
    def _on_num_vars_changed(self, new):
        defaults = self.ode.default_domain()
        self.initial_state = [(d[0]+d[1])/2.0 for d in defaults]

    @cached_property
    def _get_solution(self):
        try:
            return self.solve()
        except Exception as e:
            print(e)
            self.ode.error = True

    def solve(self):
        """ Solve the ODE and return the values of the solution vector at
        specified times t. """
        return odeint(self.ode.eval,
                       numpy.array(self.initial_state, dtype='float'),
                       self.t)

    def _t_default(self):
        return numpy.linspace(self.t_low, self.t_high, self.t_num+1) 

    @on_trait_change('t_low, t_high, t_num')
    def _change_t(self):
        self.t = self._t_default()


if __name__ == '__main__':
    ode = GenericODE()
    ode.configure_traits()
    solver = ODESolver(ode=ode, initial_state=[250])
    from matplotlib import pyplot
    fig = pyplot.plot(solver.t, solver.solution)
    pyplot.show()

