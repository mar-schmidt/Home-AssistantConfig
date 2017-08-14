#!/bin/bash
ARG="${1%\.*}"

if [ "$ARG" -gt "326" ] && [ "$ARG" -lt "11" ]; then #NNW to NNE
	echo "Nordlig"
elif [ "$ARG" -gt "11" ] && [ "$ARG" -lt "56" ]; then #NNE to ENE
	echo "Nordostlig"
elif [ "$ARG" -gt "56" ] && [ "$ARG" -lt "101" ]; then #ENE to ESE
	echo "Ostlig"
elif [ "$ARG" -gt "101" ] && [ "$ARG" -lt "146" ]; then #ESE to SSE
	echo "Sydostlig"
elif [ "$ARG" -gt "146" ] && [ "$ARG" -lt "191" ]; then #SSE to SSW
	echo "Sydlig"
elif [ "$ARG" -gt "191" ] && [ "$ARG" -lt "236" ]; then #SSW to WSW
	echo "Sydvästlig"
elif [ "$ARG" -gt "236" ] && [ "$ARG" -lt "281" ]; then #WSW to WNW
	echo "Västlig"
elif [ "$ARG" -gt "281" ] && [ "$ARG" -lt "326" ]; then #WNW to NNW
	echo "Nordvästlig"
fi
