"""Launch Beam job."""
from __future__ import absolute_import
import argparse
import logging
import json

import apache_beam as beam
from apache_beam.coders import Coder
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions


from model_beam_job.ml_model_operator import MLModelPredictOperation


class JsonCoder(Coder):
    """JSON coder interpreting each line as a JSON string."""

    def encode(self, x):
        """Serialize object to JSON string and encode to UTF-8."""
        return json.dumps(x).encode("utf-8")

    def decode(self, x):
        """Deserialize JSON string to object."""
        return json.loads(x)


def run(argv=None):
    """Build beam pipeline and run it."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='Input file to process.')
    parser.add_argument('--output', required=True, help='Output file to write results to.')
    known_args, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = True

    with beam.Pipeline(options=pipeline_options) as p:
        (
            p
            | 'read_input' >> ReadFromText(known_args.input, coder=JsonCoder())
            | 'apply_model' >> beam.ParDo(MLModelPredictOperation(module_name="iris_model.iris_predict",
                                                                  class_name="IrisModel"))
            | 'write_output' >> WriteToText(known_args.output, coder=JsonCoder())
        )

        result = p.run()
        result.wait_until_finish()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
