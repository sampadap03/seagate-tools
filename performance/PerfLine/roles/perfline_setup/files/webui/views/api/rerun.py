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

import yaml
from flask import make_response

from app_global_data import *
from core import pl_api


@app.route('/api/results/rerun/<string:taskid>')
def rerun(taskid: str):
    response = {}
    location = cache.get_location(taskid)
    with open(f'{location}/result_{taskid}/workload.yaml', 'r') as taskfile:
      try:
          config = yaml.safe_load(taskfile)
          result = pl_api.add_task(str(config))
          response = make_response(f'{result}')
      except Exception as e:
          result = { 'Error': "File not found" }
          response = make_response(f'{result}')
    return response