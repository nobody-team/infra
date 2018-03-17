#!/bin/bash

# Requre 2 parameter, both are used to replace the placeholder in test scripts:
# 1. `hub_url`: used to replace `%hub_url%`
# 2. `target_browsers`: elements of `target_browsers` are used to replace `%target_browser%`


OLD_IFS=${IFS}
export IFS=","
hub_url=$1
read -r -a target_browsers <<< "$2"
IFS=${OLD_IFS}
echo "Execute with hub_url=$hub_url, target_browsers=${target_browsers[@]}"

file_list=`find . -name "*.py" -type f`

for entry in ${file_list[@]}
do
  echo "Start processing "${entry}

  echo -e "\tReplace %hub_url% with [${hub_url}]"
  sed -i .origin 's|%hub_url%|'"$hub_url"'|g' ${entry}

  echo -e "\tReplace %target_browser% with elements of [${target_browsers[@]}]"
  for browser in "${target_browsers[@]}"
  do
    browser_specific_file=${entry%.*}'_'${browser}'.py'

    sed 's|%target_browser%|'"${browser}"'|g' ${entry} > ${browser_specific_file}

    echo -e "\n\t\tExecute for browser[$browser]: $browser_specific_file"
#    python ${browser_specific_file}

    if [ "$?" -eq '1' ]; then
      exit 1
    fi;
#    rm ${browser_specific_file}
  done
  echo -e "Finish processing $entry ...\n"
#  mv ${entry}.origin ${entry}
done

exit 0