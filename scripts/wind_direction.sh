#!/bin/bash
if [ "$1" -gt "326" ] && [ "$1" -lt "11" ]; then #NNW to NNE
	echo "Nordlig"
elif [ "$1" -gt "11" ] && [ "$1" -lt "56" ]; then #NNE to ENE
	echo "Nordostlig"
elif [ "$1" -gt "56" ] && [ "$1" -lt "101" ]; then #ENE to ESE
	echo "Ostlig"
elif [ "$1" -gt "101" ] && [ "$1" -lt "146" ]; then #ESE to SSE
	echo "Sydostlig"
elif [ "$1" -gt "146" ] && [ "$1" -lt "191" ]; then #SSE to SSW
	echo "Sydlig"
elif [ "$1" -gt "191" ] && [ "$1" -lt "236" ]; then #SSW to WSW
	echo "Sydvästlig"
elif [ "$1" -gt "236" ] && [ "$1" -lt "281" ]; then #WSW to WNW
	echo "Västlig"
elif [ "$1" -gt "281" ] && [ "$1" -lt "326" ]; then #WNW to NNW
	echo "Nordvästlig"
fi