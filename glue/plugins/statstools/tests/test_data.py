from ..data import StatsModelsComponent
from ....core.data import ComponentID
from ....core.data_factories import panda_process
import statsmodels as sm
import statsmodels.formula.api as smf
from numpy.testing import assert_almost_equal
import numpy as np

class TestComponent(object):

    def setup_method(self, *args, **kwargs):

        df = sm.datasets.fair.load_pandas().data
        self.data_df = df.dropna()
        self.formula = 'affairs ~ age + children'
        self.data = panda_process(self.data_df)

    def test_fit_model(self):

        comp = StatsModelsComponent(self.data,
                                    self.formula,
                                    smf.ols)
        assert_almost_equal(comp.data.sum(),
                            4490.4101, decimal=3)

    def test_comp_adds_to_data(self):

        comp = StatsModelsComponent(self.data,
                                    self.formula,
                                    smf.ols)
        c_id = ComponentID('AffairsPred')
        self.data.add_component(comp, c_id)

        out_comp = self.data.get_component(c_id)
        assert isinstance(out_comp, StatsModelsComponent)

    def test_with_nan_values(self):

        data_cp = self.data_df.copy()
        data_cp['age'].iloc[0] = np.nan
        data = panda_process(data_cp)
        comp = StatsModelsComponent(self.data,
                                    self.formula,
                                    smf.ols)
        assert len(comp.data) == len(self.data_df.index)





