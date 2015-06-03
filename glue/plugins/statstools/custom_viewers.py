from ... import custom_viewer
from ...qt.custom_viewer import FormElement
import numpy as np

effect_size_viewer = custom_viewer('Effect Sizes',
                                   abslope = 'float',
                                   slider = [0, 3])

@effect_size_viewer.plot_data
def plot_data(axes, abslope):

    x = np.linspace(0, 40)
    if abslope is None:
        abslope = 1.0
    y = abslope*x

    axes.plot(x, y)