
from traits.api import HasTraits, Instance
from traitsui.api import View, Item, HSplit, VSplit, Tabbed, Group

from ode import ODE, ODESolver, GenericODE
from plot2d import ODEPlot
from plot3d import ODEPlot3D

class ODEApp(HasTraits):
    ode = Instance(ODE)
    solver = Instance(ODESolver)
    plot = Instance(ODEPlot)
    plot3d = Instance(ODEPlot3D)

    traits_view = View(HSplit(VSplit([Group(Item('ode', style='custom', 
                                                show_label=False),
                                           label='ODE'),
                                     Group(Item('solver', style='custom',
                                                show_label=False),
                                                label='Solver')],
                                    ),
                              Tabbed(Item('plot', style='custom'),
                                     Item('plot3d', style='custom'),
                                     dock='tab',
                                     show_labels=False),
                              id='example.ODEAPP.panels',
                              show_labels=False),
                       width=800, height=700, resizable=True,
                       id='example.ODEApp',
                       title="ODE Solution")

    def _ode_default(self):
        return GenericODE()

    def _solver_default(self):
        return ODESolver(ode=self.ode)

    def _plot_default(self):
        return ODEPlot(solver=self.solver)

    def _plot3d_default(self):
        return ODEPlot3D(solver=self.solver)

if __name__ == '__main__':
    from ode import LorenzEquation
    odeapp = ODEApp(ode=LorenzEquation())
    odeapp.configure_traits()
