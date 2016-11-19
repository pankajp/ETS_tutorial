import numpy as np
from traits.api import HasTraits, Instance, on_trait_change, Range
from traitsui.api import View, Item
from mayavi.core.ui.api import MayaviScene, \
    MlabSceneModel, SceneEditor

class Plot3D(HasTraits):
    scene = Instance(MlabSceneModel, args=())
    factor = Range(0.0, 20.0, 1.0)
    plot = Instance(HasTraits)
    view = View(Item(name='scene',
                     editor=SceneEditor(
                         scene_class=MayaviScene),
                     show_label=False, resizable=True,
                     height=500, width=500),
                Item(name='factor'),
                resizable=True)

    @on_trait_change('scene.activated, factor')
    def generate_data(self):
        # Create some data
        X, Y = np.mgrid[-2:2:100j, -2:2:100j]
        R = self.factor*np.sqrt(X**2 + Y**2)
        Z = np.sin(R)/R
        if self.plot is None:
            self.plot = self.scene.mlab.surf(X,Y,Z,colormap='gist_earth')
        else:
            self.plot.mlab_source.reset(x=X, y=Y, scalars=Z)

if __name__ == '__main__':
    p = Plot3D()
    p.configure_traits()

