#!/bin/bash
cd ~/pyatv
source bin/activate
if [ $1 = "Sovrum" ]; then
	address="192.168.1.7"
	airplay_credentials="D41F69574E18FBC6:2B86A4E7233FCCED2AC084071E23049B7B279CDA98947A8C81748AF8D2871288"
elif [ $1 = "Vardagsrum" ]; then
	address="192.168.1.3"
	airplay_credentials="BC6BD302F03CBBD6:97994153463C2F49DBF2DC4D3F8E1F7DF63018A3566C2DA92550F68060144808"
fi

if [ ! -z $address ] && [ ! -z $airplay_credentials ]; then
	atvremote --address $address --login_id 00000000-1092-dc12-7d1d-158da0c84566 --debug --airplay_credentials=$airplay_credentials play_url=$2
else
	echo "Invalid parameters"
fi
