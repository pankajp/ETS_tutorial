
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

    name_list = Property(List(Str), depends_on='ode.t_var, ode.vars')

    ode = Property(Instance(ODE), depends_on='ode_soln')
    ode_soln = Instance(ODESolver)
    traits_view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                            show_label=False),
                       HGroup(Item('x_name', editor=EnumEditor(name='name_list')),
                              Item('y_name', editor=EnumEditor(name='name_list')),
                              Item('z_name', editor=EnumEditor(name='name_list')),
                              Item('s_name', editor=EnumEditor(name='name_list'))),
                       width=800, height=700, resizable=True,
                       title="ODE Solution")

    def _get_ode(self):
        return self.ode_soln and self.ode_soln.ode

    @cached_property
    def _get_name_list(self):
        names = [self.ode.t_var]
        if isinstance(self.ode.vars, basestring):
            names.append(self.ode.vars)
        else:
            names.extend(self.ode.vars)
        return names

    @on_trait_change('x_name,y_name,z_name,s_name')
    def _on_name_changed(self, obj, name, old, new):
        self._set_arr(new, name[:-5])

    def _set_arr(self, name, key='index'):
        if name == self.ode.t_var:
            arr = self.ode_soln.t_arr
        else:
            arr = self.ode_soln.soln_arr[:, self.ode.vars.index(name)]
        self.trait_set(**{key+'_arr':arr})

    @on_trait_change('ode_soln.soln_arr')
    def _on_soln_changed(self):
        self._set_arr(self.x_name, 'x')
        self._set_arr(self.y_name, 'y')
        self._set_arr(self.z_name, 'z')
        self._set_arr(self.s_name, 's')

    @on_trait_change('x_arr,y_arr,z_arr,s_arr')
    def _on_arr_changed(self, obj, name, old, new):
        self.plot3d.mlab_source.set(x=self.x_arr, y=self.y_arr, z=self.z_arr, s=self.s_arr)

    @on_trait_change('scene.activated')
    def update_flow(self):
        n = len(self.name_list)
        self.x_name = self.name_list[1%n]
        self.y_name = self.name_list[2%n]
        self.z_name = self.name_list[3%n]
        self.s_name = self.name_list[0]
        print self.x_arr.shape, self.y_arr.shape, self.z_arr.shape, self.s_arr.shape
        self.plot3d.mlab_source.set(x=self.x_arr, y=self.y_arr, z=self.z_arr, s=self.s_arr)

    def _plot3d_default(self):
        plot3d = self.scene.mlab.plot3d(self.x_arr, self.y_arr, self.z_arr, self.s_arr, tube_radius=0.1)
        return plot3d

    def _index_name_default(self):
        return self.name_list[0]

    def _value_name_default(self):
        return self.name_list[-1]


if __name__ == '__main__':
    from ode import EpidemicODE, LorenzEquation, GenericODE
    import numpy
    ode = EpidemicODE()
    ode = LorenzEquation()
    #ode = GenericODE()
    #ode.configure_traits()
    soln = ODESolver(ode=ode, initial_state=[10.,50.,50.], t_arr=numpy.linspace(0,10,1001))
    plot = ODEPlot3D(ode_soln=soln)
    plot.configure_traits()

