# -----------------------------------------------
#
# Remove files generated by export_schema.py/sh
#
# -----------------------------------------------

import os
import re

for root, dirs, files in os.walk('.'):
    for f in files:
        file_path = os.path.join(root, f)
        if re.search('\.sql$', file_path):
            print("Removing file: {}".format(os.path.abspath(file_path)))
            os.remove(file_path)

