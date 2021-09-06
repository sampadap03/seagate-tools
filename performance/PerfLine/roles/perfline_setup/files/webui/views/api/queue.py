# Copyright (c) 2020 Seagate Technology LLC and/or its Affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# For any questions about this software or licensing,
# please email opensource@seagate.com or cortx-questions@seagate.com.
#

import json
import gzip
import yaml
from flask import make_response

from app_global_data import *
from core import pl_api
from core.utils import tq_task_common_get


def tq_queue_read(limit: int):
    lines = pl_api.get_queue().split('\n')[-limit:]
    lines = filter(None, lines)  # remove empty line

    out = []
    results = [yaml.safe_load(line) for line in lines]

    for r in results:
        elem = {}
        try:
            state = r[1]
            tq_task_common_get(elem, r)
            elem["state"] = state['state']
        except Exception as e:
            print(e)

        out.append(elem)

    return out


@app.route('/api/queue', defaults={'limit': 9999999})
@app.route('/api/queue/<int:limit>')
def queue(limit=9999999):
    data = {
        "queue": tq_queue_read(limit)
    }
    content = gzip.compress(json.dumps(data).encode('utf8'), 5)
    response = make_response(content)
    response.headers['Content-length'] = len(content)
    response.headers['Content-Encoding'] = 'gzip'
    return response