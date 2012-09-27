
from traits.api import HasTraits, Instance, DelegatesTo, List
from traitsui.api import View, Item, HSplit, VSplit, Tabbed, Group, InstanceEditor

from ode import ODE, ODESolver, GenericODE, LorenzEquation, EpidemicODE, ODE1D, ODE2D, ODE3D
from plot2d import ODEPlot
from plot3d import ODEPlot3D

class ODEApp(HasTraits):
    ode = DelegatesTo('solver')
    ode_list = List(Instance(ODE))
    solver = Instance(ODESolver)
    plot = Instance(ODEPlot)
    plot3d = Instance(ODEPlot3D)

    traits_view = View(HSplit(VSplit([Group(Item('ode', style='custom',
                                                 editor=InstanceEditor(
                                                     name='object.ode_list'),
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

    def _ode_changed(self):
        self.plot = self._plot_default()
        self.plot3d = self._plot3d_default()

    def _solver_default(self):
        return ODESolver(ode=self.ode_list[0])

    def _plot_default(self):
        return ODEPlot(solver=self.solver)

    def _plot3d_default(self):
        return ODEPlot3D(solver=self.solver)

    def _ode_list_default(self):
        return [LorenzEquation(), EpidemicODE(), GenericODE()]

if __name__ == '__main__':
    from ode import LorenzEquation
    odeapp = ODEApp()
    odeapp.configure_traits()
