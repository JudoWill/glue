from ... import custom_viewer
from ...qt.custom_viewer import ComponenentElement
from data import StatsModelsComponent
import numpy as np

class StatsModelComponenentElement(ComponenentElement):

    def _list_components(self):

        comps = []
        for layer in self.container.layers:
            for c in layer.data.components:
                comp = layer.data.get_component(c)
                if not c._hidden and isinstance(comp, StatsModelsComponent):
                    comps.append(c)
        comps = sorted(comps, key=lambda x: x.label)
        return comps

    @classmethod
    def recognizes(cls, params):
        return params == 'StatsComp'


effect_size_viewer = custom_viewer('Effect Sizes',
                                   prediction='StatsComp',
                                   confidence_interval=0.95,
                                   alpha=0.05)

@effect_size_viewer.plot_data
def plot_data(axes, prediction, alpha, confidence_interval):
    if prediction._component:
        res = prediction._component._result
        ci = res.conf_int(confidence_interval)

        width = ci[1]-ci[0]
        alphas = np.ones_like(width.values)
        alphas[res.pvalues < alpha] = 0.3

        axes.barh(left=ci[0],
                  width=width,
                  bottom=np.arange(len(width))-0.4,
                  height=0.8,
                  alpha=alphas)
        axes.set_yticks(range(len(ci)))
        axes.set_yticklabels(ci.index)
        res.params.plot(kind='barh', ax=axes, grid=False)