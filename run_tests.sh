#!/bin/bash

########################################
echo "Launching regular tests"

failures=""
nosetests tests/test_parsers.py
if [ $? -ne 0 ]; then failures="$failures test_parsers";fi
nosetests tests/test_parser_youtube.py
if [ $? -ne 0 ]; then failures="$failures test_parser_youtube";fi
#nosetests tests/test_facebook_integration.py # not working in travis
#if [ $? -ne 0 ]; then failures="$failures test_facebook_integration";fi
#nosetests tests/test_facebook.py  # nothing done yet
#nosetests tests/test_requests.py  # unfinished tests
#nosetests tests/test_querys.py  # unfinished tests


########################################
echo "determining version of appengine instance"

if [ $(grep "^version:" app.yaml | cut -d " " -f 2) -eq 2 ]
then
	echo "  Dev version"
else
	echo "  Non dev version"
fi

########################################
# "Uploading to appengine"

function upload_to_appengine()
{
	echo "  not implemented"

	cd google_appengine
	echo " google_appengine"
	echo "hostname"
	hostname
	appdir=".."
	# oauth code:
	token="4/9JwInYmiQAdaLh9xqDSHDavVyYfL.kqeQpM1lKmofOl05ti8ZT3a3FIpajQI" #invalid
	# how to upload with no interaction:
	#python appcfg.py update --oauth2 --noauth_local_webserver --oauth2_refresh_token=$token $appdir
	# how to get the link to token:
	echo "Uploading now"
	ls -l ../../google_appengine
	python ../appcfg.py update   --oauth2  --noauth_local_webserver   friendtube.testing  << EOF
	$token
EOF

}
# upload_to_appengine. only in travis

########################################
echo "determining machine of build"

local_ip="192.168"
travis_ip="172.30"
machine="undetermined"
for ip in $(sudo ifconfig | grep inet | grep -v "127.0.0" | grep -v inet6 | cut -c21-30 | cut -d "." -f 1,2 | sort | uniq )
do
       	if [ $ip == $local_ip ]; then
		machine="Local"
		break
	elif [ $ip == $travis_ip ]; then
		machine="Travis"
		break
	else
		echo "  detected ip: $ip"
       	fi 
done
echo "  $machine Environment"

if [ $machine == "Travis" ]; then
	echo "upload_to_appengine. only in travis"
	upload_to_appengine
else
	echo "Uploading as exception"
	upload_to_appengine
fi


########################################
echo "final verification of tests"

if [ $failures != "" ];then
	echo "There were some errors with the test files:"
	echo "  $failures"
	exit -1
else
	echo "BUILD SUCCESSFUL"
fi
