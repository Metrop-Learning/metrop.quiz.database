# Metrop db compiler

import os
import json

file_list = [os.path.join(dirpath, file) for (dirpath, dirnames, filenames) in os.walk("./content") for file in filenames]
file_list = [i.replace('\\', '/').removeprefix('./content/') for i in file_list]

with open('dbinfo.json', 'r') as f:
    data = json.load(f)

data['QUIZ_LIST'] = file_list

with open('dbinfo.json', 'w') as f:
    json.dump(data, f, indent=4)