
from traits.api import HasTraits, Instance, Str, Property, Array, on_trait_change, cached_property, List, DelegatesTo
from traitsui.api import View, Item, EnumEditor, HGroup, VGroup, HSplit, VSplit
from enable.api import Component, ComponentEditor
from chaco.api import Plot, ArrayPlotData
from chaco.tools.api import TraitsTool, ZoomTool, PanTool

from ode import ODE, ODESolver, GenericODE
from plot2d import ODEPlot

class ODEApp(HasTraits):
    ode = DelegatesTo('plot')
    solver = DelegatesTo('plot', prefix='ode_soln')
    plot = Instance(ODEPlot)

    traits_view = View(HSplit(VSplit(Item('ode', style='custom'),
                                     Item('solver', style='custom')),
                              Item('plot', style='custom'),
                              show_labels=False),
                       width=800, height=700, resizable=True,
                       title="ODE Solution")

    def _plot_default(self):
        ode = GenericODE()
        solver = ODESolver(ode=ode)
        return ODEPlot(ode_soln=solver)

if __name__ == '__main__':
    odeapp = ODEApp()
    odeapp.configure_traits()
