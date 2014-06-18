#!/bin/bash

echo "Testing bash execution on travis"

nosetests tests/test_parsers.py

echo "testing environment"

cd google_appengine
ls -lart

if [ $(grep "^version:" app.yaml | cut -d " " -f 2) -eq 2 ]
then
	echo "Dev version"
	appcfg.py update --oauth2 --noauth_local_webserver ..
else
	echo "Non dev version"
fi
