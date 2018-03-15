#!/bin/bash
for entry in `find . -name "*.py" -type f`
do
  echo "$entry"
  python "$entry"
done

exec "$@"