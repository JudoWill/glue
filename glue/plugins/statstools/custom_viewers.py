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
        positions = np.arange(len(width))-0.4
        sig_mask = res.pvalues.values < alpha

        axes.barh(left=ci[0].values[sig_mask],
                  width=width.values[sig_mask],
                  bottom=positions[sig_mask],
                  height=0.8,
                  alpha=1)

        axes.barh(left=ci[0].values[~sig_mask],
                  width=width.values[~sig_mask],
                  bottom=positions[~sig_mask],
                  height=0.8,
                  alpha=0.3)

        axes.set_yticks(range(len(ci)))
        axes.set_yticklabels(ci.index)