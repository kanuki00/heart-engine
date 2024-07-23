#!/bin/bash

if [ ! -d venv ] ; then
	echo "Environment does not exist. Creating..."
	python -m venv venv
	venv/bin/pip install numpy
	venv/bin/pip install numpy-quaternion
	venv/bin/pip install numba
else
	echo "Environment already exits. skipping"
fi
source venv/bin/activate
