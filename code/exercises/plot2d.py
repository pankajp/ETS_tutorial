# -*- coding: utf-8 -*-

import numpy as np
from traits.api import HasTraits, Instance, Str, Property, Array, \
    on_trait_change, cached_property, List
from traitsui.api import View, Item, HGroup, EnumEditor
from enable.api import Component, ComponentEditor
from chaco.api import Plot, ArrayPlotData
from chaco.tools.api import TraitsTool, ZoomTool, PanTool

from solve_ode import ODE, ODESolver


class ODEPlot(HasTraits):
    """ A 2D plot of ode solution variables. """
    plot = Instance(Component)
    pd = Instance(ArrayPlotData, args=())

    ode = Property(Instance(ODE), depends_on='solver')
    solver = Instance(ODESolver)
    traits_view = View(Item('plot', editor=ComponentEditor(),
                            show_label=False),
                       Item('ode', style='custom'),
                       width=800, height=700, resizable=True,
                       title="ODE Solution")

    def _get_ode(self):
        return self.solver and self.solver.ode

    @on_trait_change('solver.solution')
    def _on_soln_changed(self):
        self.pd.set_data('index', self.solver.t)
        self.pd.set_data('value', self.solver.solution[:, 0])

    @on_trait_change('index_arr,value_arr')
    def _on_arr_changed(self, obj, name, old, new):
        self.pd.set_data(name[:-4], new)

    def _plot_default(self):
        self.pd.set_data('index', self.solver.t)
        # Set the first array as value array for plot.
        self.pd.set_data('value', self.solver.solution[:,0])
        plot = Plot(self.pd)
        plot.plot(('index', 'value'))
        plot.tools.append(TraitsTool(component=plot))
        plot.tools.append(ZoomTool(component=plot))
        plot.tools.append(PanTool(component=plot))
        plot.x_axis.title = 'time'
        plot.y_axis.title = 'x'
        plot.title = self.ode.name
        return plot


if __name__ == '__main__':
    from solve_ode import LorenzEquation
    ode = LorenzEquation()
    solver = ODESolver(ode=ode, initial_state=[10.,50.,50.], t=np.linspace(0,10,1001))
    plot = ODEPlot(solver=solver)
    plot.configure_traits()

