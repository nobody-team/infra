#!/bin/bash
for entry in `find . -name "*.py" -type f`
do
  echo "$entry"
  python "$entry"
  if [ "$?" -eq '1' ]; then 
    exit 1
  fi;
done

exit 0