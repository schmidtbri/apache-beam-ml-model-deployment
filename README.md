# apache-beam-ml-model-deployment
Deploying an ML model in an Apache Beam job.


# Apache Beam ML Model Deployment

![Test and Build](https://github.com/schmidtbri/apache-beam-ml-model-deployment/workflows/Test%20and%20Build/badge.svg)

Deploying an ML model in a Apache Beam service.

This code is used in this [blog post](https://medium.com/@brianschmidt_78145/an-apache-beam-ml-model-deployment-ac31c6f2d9b2).

## Requirements
Python 3

## Installation 
The Makefile included with this project contains targets that help to automate several tasks.

To download the source code execute this command:

```bash
git clone https://github.com/schmidtbri/apache-beam-ml-model-deployment
```

Then create a virtual environment and activate it:

```bash
# go into the project directory
cd apache-beam-ml-model-deployment

make venv

source venv/bin/activate
```

Install the dependencies:

```bash
make dependencies
```

## Running the Unit Tests
To run the unit test suite execute these commands:

```bash
# first install the test dependencies
make test-dependencies

# run the test suite
make test

# clean up the unit tests
make clean-test
```
