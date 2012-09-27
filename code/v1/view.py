
from traits.api import HasTraits, Instance, Str, Property, Array, on_trait_change, cached_property, List, DelegatesTo
from traitsui.api import View, Item, EnumEditor, HGroup, VGroup, HSplit, VSplit, Tabbed
from enable.api import Component, ComponentEditor
from chaco.api import Plot, ArrayPlotData
from chaco.tools.api import TraitsTool, ZoomTool, PanTool

from ode import ODE, ODESolver, GenericODE
from plot2d import ODEPlot
from plot3d import ODEPlot3D

class ODEApp(HasTraits):
    ode = Instance(ODE)
    solver = Instance(ODESolver)
    plot = Instance(ODEPlot)
    plot3d = Instance(ODEPlot3D)

    traits_view = View(HSplit(VSplit(Item('ode', style='custom'),
                                     Item('solver', style='custom')),
                              Tabbed(Item('plot', style='custom'),
                                     Item('plot3d', style='custom')),
                              show_labels=False),
                       width=800, height=700, resizable=True,
                       title="ODE Solution")

    def _ode_default(self):
        return GenericODE()

    def _solver_default(self):
        return ODESolver(ode=self.ode)

    def _plot_default(self):
        return ODEPlot(ode_soln=self.solver)

    def _plot3d_default(self):
        return ODEPlot3D(ode_soln=self.solver)

if __name__ == '__main__':
    from ode import LorenzEquation
    odeapp = ODEApp(ode=LorenzEquation())
    odeapp.configure_traits()
