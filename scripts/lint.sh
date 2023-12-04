#!/usr/bin/env bash

set -x

mypy core port targets
black core port targets --check
isort --profile black --check-only core port targets
flake8