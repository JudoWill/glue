from ..data import StatsModelsComponent
from ....core.data import ComponentID
from ....core.data_factories import panda_process
import statsmodels as sm
import statsmodels.formula.api as smf
from numpy.testing import assert_almost_equal
import numpy as np
from .. import utils

class TestUtils(object):

    def setup_method(self, *args, **kwargs):

        df = sm.datasets.fair.load_pandas().data
        self.data_df = df.dropna()
        self.formula = 'affairs ~ age + children'
        self.data = panda_process(self.data_df)

    def test_basic_usage(self):

        utils.fit_model_to_data(self.data, self.formula, smf.ols,
                                label = 'testing')
        assert self.data.find_component_id('testing') is not None

    def test_no_label_usage(self):

        utils.fit_model_to_data(self.data, self.formula, smf.ols)
        assert self.data.find_component_id('affairs_pred') is not None

    def test_repeated_usage_removes(self):

        utils.fit_model_to_data(self.data, self.formula, smf.ols)
        utils.fit_model_to_data(self.data, self.formula + ' + educ', smf.ols)

        comp_id = self.data.find_component_id('affairs_pred')
        comp = self.data.get_component(comp_id)
        assert comp._model.exog_names == ['Intercept', 'age', 'children', 'educ']