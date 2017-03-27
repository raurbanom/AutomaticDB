from __future__ import division

import json
import os

from datetime import datetime
from AutomaticDB import settings


def get_name_json():
    now = datetime.utcnow()
    epoch = datetime(1970, 1, 1)
    td = now - epoch

    return 'file_' + str(int(round(td.total_seconds()))) + str('.json')


attributes = "A, B,   C,D, E,   F"
dependencies = "A,B: C; D: E, F; C: A; B, E: C; B, C: D; C,F: B, D; A, C, D: B; C, E: A, F"

dependencies_temp = dependencies.replace(" ", "")
list_attributes = attributes.replace(" ", "").split(",")
list_dependencies = dependencies_temp.split(";")

result = []
for pair in list_dependencies:
    x, y = pair.split(":")
    result.append({"x": x, "y": y})

data = {
    "attributes": list_attributes,
    "functionaldependencies": result
}

json_data = json.dumps(data, indent=4)
print(json_data)

filename = get_name_json()
path = os.path.join(settings.MEDIA_ROOT, filename)

file_io = open(path, 'w+')
file_io.write(json_data)
file_io.close()


