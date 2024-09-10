#!/bin/bash

for file in data/*.xlsx; do
  for sheet in palabras "no palabras"; do
    in2csv -f xlsx -I --skip-lines 1 --sheet "$sheet" "$file" \
      > "$(md5sum "$file" | awk '{ print $1 }')_${sheet/ /}.csv"
  done
done

mv ./*_{no,}palabras.csv converted
