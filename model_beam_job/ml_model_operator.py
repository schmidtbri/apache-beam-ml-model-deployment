"""Make predictions with an MlModel object in a Beam pipeline."""
import importlib
import logging
import apache_beam as beam
from ml_model_abc import MLModel

logger = logging.getLogger(__name__)


class MLModelPredictOperation(beam.DoFn):
    """Class for make predictions with an MLModel.

    :param module_name: path of module containing MLModel-derived class
    :type module_name: str
    :param class_name: name of MLModel-derived class
    :type class_name: str
    :returns: An instance of MLModelPredictOperation.
    :rtype: MLModelPredictOperation

    """

    def __init__(self, module_name, class_name):
        """Initialize object."""
        beam.DoFn.__init__(self)
        model_module = importlib.import_module(module_name)
        model_class = getattr(model_module, class_name)
        model_object = model_class()

        if issubclass(type(model_object), MLModel) is None:
            raise ValueError("The model object is not a subclass of MLModel.")

        self._model = model_object

        logger.info("Initializing pipeline operator for model: {}".format(self._model.qualified_name))

    def process(self, data, **kwargs):
        """Make prediction with model and return result."""
        yield self._model.predict(data=data)
