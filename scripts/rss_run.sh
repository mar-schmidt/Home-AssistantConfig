#!/bin/bash
wget --quiet -O nyheter $1
xmlstarlet fo --omit-decl --nocdata nyheter > nyheter.xml

yes | python2 /usr/bin/rpl -q -f '&lt;p&gt;' '' nyheter.xml >/dev/null 2>&1
yes | python2 /usr/bin/rpl -q -f '&lt;/p&gt;' '' nyheter.xml >/dev/null 2>&1
yes | python2 /usr/bin/rpl -q -f '&lt;br&gt;' '' nyheter.xml >/dev/null 2>&1
yes | python2 /usr/bin/rpl -q -f '"' '' nyheter.xml >/dev/null 2>&1
yes | python2 /usr/bin/rpl -q -f '”' '' nyheter.xml >/dev/null 2>&1

touch nyheter2.xml
bash rss.sh nyheter.xml > nyheter2.xml
echo "$(cat nyheter2.xml)"
rm nyheter &> /dev/null
rm nyheter.xml &> /dev/null
