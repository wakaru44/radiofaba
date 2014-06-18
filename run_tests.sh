#!/bin/bash

echo "Testing bash execution on travis"

nosetests tests/test_parsers.py

echo "testing environment"


if [ $(grep "^version:" app.yaml | cut -d " " -f 2) -eq 2 ]
then
	echo "Dev version"
	cd google_appengine
	ls -lart
	# oauth code:
	token="4/9JwInYmiQAdaLh9xqDSHDavVyYfL.kqeQpM1lKmofOl05ti8ZT3a3FIpajQI"
	python appcfg.py update --oauth2 --noauth_local_webserver --oauth2_access_token=$token ..
else
	echo "Non dev version"
fi
