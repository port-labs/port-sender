#!/bin/sh -e
set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place core port targets --exclude=__init__.py
black core port targets
isort --profile black core port targets