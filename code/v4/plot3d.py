import numpy as np
from traits.api import HasTraits, Instance, Property, on_trait_change, Any
from traitsui.api import View, Item
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor

from ode import ODE, ODESolver


class ODEPlot3D(HasTraits):
    """ A 2D plot of ode solution variables. """
    scene = Instance(MlabSceneModel, args=())
    plot3d = Any
    ode = Property(Instance(ODE), depends_on='solver.ode')
    solver = Instance(ODESolver)
    traits_view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                            show_label=False),
                       width=800, height=700, resizable=True,
                       title="ODE Solution")

    def _get_ode(self):
        return self.solver and self.solver.ode

    @on_trait_change('solver.solution')
    def _on_solution_changed(self):
        # TODO: an exercise for the reader
        pass

    @on_trait_change('scene.activated')
    def update_flow(self):
        self.plot3d = self.scene.mlab.plot3d(self.solver.solution[:,0],
                                              self.solver.solution[:,1],
                                              self.solver.solution[:,2],
                                              self.solver.t,
                                              tube_radius=0.1)


if __name__ == '__main__':
    from ode import LorenzEquation
    ode = LorenzEquation()
    solver = ODESolver(ode=ode, initial_state=[10.,50.,50.], t=np.linspace(0,10,1001))
    plot3d = ODEPlot3D(solver=solver)
    plot3d.configure_traits()

