
from traits.api import HasTraits, Instance, Str, Property, Array, on_trait_change, cached_property, List, Any
from traitsui.api import View, Item, HGroup, EnumEditor
from mayavi import mlab
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, \
    SceneEditor

from ode import ODE, ODESolver


class ODEPlot3D(HasTraits):
    """ A 2D plot of ode solution variables. """
    scene = Instance(MlabSceneModel, args=())

    x_arr = Array
    y_arr = Array
    z_arr = Array
    s_arr = Array

    x_name = Str
    y_name = Str
    z_name = Str
    s_name = Str

    plot3d = Any

    name_list = Property(List(Str), depends_on='ode.vars')

    ode = Property(Instance(ODE), depends_on='solver.ode')
    solver = Instance(ODESolver)
    traits_view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                            show_label=False),
                       HGroup(Item('x_name', editor=EnumEditor(name='name_list')),
                              Item('y_name', editor=EnumEditor(name='name_list')),
                              Item('z_name', editor=EnumEditor(name='name_list')),
                              Item('s_name', editor=EnumEditor(name='name_list'))),
                       width=800, height=700, resizable=True,
                       title="ODE Solution")

    def _get_ode(self):
        return self.solver and self.solver.ode

    @cached_property
    def _get_name_list(self):
        names = ['time']
        if isinstance(self.ode.vars, str):
            names.append(self.ode.vars)
        else:
            names.extend(self.ode.vars)
        return names

    def _name_list_changed(self):
        n = len(self.name_list)
        self.trait_set(x_name=self.name_list[1%n],
                       y_name=self.name_list[2%n],
                       z_name=self.name_list[3%n],
                       s_name=self.name_list[0])

    @on_trait_change('x_name,y_name,z_name,s_name')
    def _on_name_changed(self, obj, name, old, new):
        self._set_arr(new, name[:-5])

    def _set_arr(self, name, key):
        if name in ['t', 'time']:
            arr = self.solver.t
        elif name in self.ode.vars:
            arr = self.solver.solution[:, self.ode.vars.index(name)]
        else:
            return
        self.trait_set(**{key+'_arr':arr})

    @on_trait_change('solver.solution')
    def _on_solution_changed(self):
        if self.s_name == '':
            return
        self._set_arr(self.x_name, 'x')
        self._set_arr(self.y_name, 'y')
        self._set_arr(self.z_name, 'z')
        self._set_arr(self.s_name, 's')

    @on_trait_change('x_arr,y_arr,z_arr,s_arr')
    def _on_arr_changed(self, obj, name, old, new):
        if self.x_arr.shape == self.y_arr.shape == self.z_arr.shape == self.s_arr.shape:
            if old.shape == new.shape:
                self.plot3d.mlab_source.set(x=self.x_arr, y=self.y_arr, 
                                            z=self.z_arr, s=self.s_arr)
            else:
                self.plot3d.mlab_source.reset(x=self.x_arr, y=self.y_arr, 
                                              z=self.z_arr, s=self.s_arr)

    @on_trait_change('scene.activated')
    def update_flow(self):
        self.plot3d.mlab_source.set(x=self.x_arr, y=self.y_arr, z=self.z_arr, s=self.s_arr)

    def _plot3d_default(self):
        plot3d = self.scene.mlab.plot3d(self.x_arr, self.y_arr, self.z_arr, 
                                        self.s_arr, tube_radius=0.1)
        return plot3d

if __name__ == '__main__':
    from ode import EpidemicODE, LorenzEquation, GenericODE
    import numpy
    ode = EpidemicODE()
    ode = LorenzEquation()
    solver = ODESolver(ode=ode, initial_state=[10.,50.,50.], 
                       t=numpy.linspace(0,10,1001))
    plot = ODEPlot3D(solver=solver)
    plot.configure_traits()

