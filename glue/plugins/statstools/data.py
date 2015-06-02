from ...core.data import Component
import numpy as np

class StatsModelsComponent(Component):

    def __init__(self, data, formula, model_api, units=None, **kwargs):
        """
        :param data: The data object to use for calculation
        :type data: :class:`~glue.core.data.Data`

        :param formula: Any function parsable by Patsy

        :param model_api: Any function in statsmodels.formula.api

        :param units: Optional unit description
        """
        super(Component, self).__init__()

        data_df = data.to_dataframe()
        self._model = model_api(formula, data=data_df,
                                missing = 'drop', **kwargs)
        self._result = self._model.fit()

        fitted_vals = self._result.fittedvalues
        not_missing = data_df.notnull().all(axis=1)

        self._data = np.nan*np.ones_like(data_df[self._model.endog_names].values)
        self._data[not_missing.values] = self._result.fittedvalues

    @property
    def data(self):
        """ Return the numerical data as a numpy array """
        return self._data

    def __getitem__(self, key):
        return self._result.fittedvalues.values.__get_item__(key)