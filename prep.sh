#!/bin/bash
set -e

PDF="$1"
TMP="/tmp/$(date +"%s")"
SCHEDULE="${TMP}/schedule.pdf"

if [ -f "$PDF" ];
then
    mkdir -p "$TMP"
    cp "$PDF" "$SCHEDULE"
    pushd $TMP
    convert -density 300 schedule.pdf schedule.png
    for f in schedule-*.png
    do
        tesseract --psm 4 $f - >>out.txt
    done
    popd
    cat "${TMP}/out.txt" >> ~/git/clm-schedule-parser/schedule.txt
else
    echo "Can't find ${PDF}!"
    exit 1
fi

