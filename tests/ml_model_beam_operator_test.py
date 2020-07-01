import unittest
from ml_model_abc import MLModel
from model_beam_job.ml_model_operator import MLModelPredictOperation


# creating an MLModel class to test with
class MLModelMock(MLModel):
    # accessing the package metadata
    display_name = "display name"
    qualified_name = "qualified_name"
    description = "description"
    major_version = 1
    minor_version = 1
    input_schema = None
    output_schema = None

    def __init__(self):
        pass

    def predict(self, data):
        return {"prediction": 123}


# creating a mockup class to test with
class SomeClass(object):
    pass


class MLModelZeroRPCEndpointTests(unittest.TestCase):

    def test1(self):
        """testing the __init__() method"""
        # arrange

        # act

        # assert


if __name__ == '__main__':
    unittest.main()