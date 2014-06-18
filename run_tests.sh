#!/bin/bash

echo "Testing bash execution on travis"

nosetests tests/test_parsers.py
