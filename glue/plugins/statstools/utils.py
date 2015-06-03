from data import StatsModelsComponent

def fit_model_to_data(data, formula, model_api, label=None, **kwargs):
    """

    :param data: The data object to use for calculation
        :type data: :class:`~glue.core.data.Data`
    :param label: The label. If this is a string]
    :param formula: Any function parsable by Patsy
    :param model_api: Any function in statsmodels.formula.api
    :param kwargs: All other kwargs are passed to the model_api function call
    :return:
    """

    new_comp = StatsModelsComponent(data, formula, model_api, **kwargs)
    if label is None:
        label = new_comp._model.endog_names + '_pred'

    comp_id = data.find_component_id(label)
    if comp_id is not None:
        data.remove_component(comp_id)

    data.add_component(new_comp, label, hidden=False)
