#!/bin/bash

set -e

TEST_WORKDIR=$(realpath $(dirname "$0"))
PROTOC_HELPER_DIR=$(realpath $TEST_WORKDIR"/../../ansys-tools-protoc-helper")

# check that we are in a virtualenv..
python -c 'import sys; assert hasattr(sys, "real_prefix") or (hasattr(sys, "base_prefix") and sys.prefix != sys.base_prefix), "Must run the test script from within a virtual environment."'

pushd $TEST_WORKDIR
# ---- INSTALL PREREQUISITES ----
# We need versions of pip and setuptools that understand the 'pyproject.toml' - based build, at least
pip install -U pip setuptools==42

pip install cookiecutter 'click<8'
# pip install git+https://github.com/cookiecutter/cookiecutter.git@2.0.2#egg=cookiecutter # NOTE: using v2 for the '--replay-file' option

# ---- CREATE TEST PACKAGES ----
rm -rf ./ansys-api-*
cookiecutter -f --no-input ..  product_name=hello protos_dir=../hello
# cookiecutter -f --no-input ..  product_name=greeter protos_dir=../greeter proto_dependencies="{'modules'=['ansys-api-hello']}"
cookiecutter ..  < greeter_input.txt

# ---- BUILD 'ansys-tools-protoc-helper' WHEEL ----
# Note that we use a local directory as a 'PyPI replacement', since we don't
# yet want to publish the package, but the subsequent builds need to find
# it for the build-time dependencies.
rm -rf local_dist
mkdir local_dist
pushd $PROTOC_HELPER_DIR
pip wheel -w $TEST_WORKDIR/local_dist/ .
popd

# ---- DOWNLOAD ADDITIONAL DEPENDENCIES TO 'local_dist' ----
# We could instead use PyPI _and_ the local directory, but this is unsafe because
# a package on PyPI could shadow 'ansys-tools-protoc-helper' (see example 10 on
# https://pip.pypa.io/en/stable/cli/pip_install/#examples).
pushd ./local_dist
pip download setuptools wheel grpcio-tools protobuf mypy-protobuf # cython?
popd

# ---- BUILD 'ansys-api-hello' WHEEL, INSTALL 'ansys-api-greeter' ----
pip wheel --no-index --find-links=./local_dist -w ./local_dist ./ansys-api-hello/
pip install --no-index --find-links=./local_dist ./ansys-api-greeter/
python -c "from ansys.api.greeter.v1.greeter_pb2_grpc import GreeterStub"