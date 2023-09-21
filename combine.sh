#!/bin/bash
printf "<HTML><BODY><BR>" > preview.html
ls -1 *.png | awk -F : '{ print $1":"$2"\n<BR><IMG SRC=\""$1""$2"\" width=400><BR><BR>"}' >> preview.html
printf "</BODY></HTML>" >> preview.html
