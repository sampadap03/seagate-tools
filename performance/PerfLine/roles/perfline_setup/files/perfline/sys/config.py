#
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

from huey import SqliteHuey

huey = SqliteHuey(filename='sys/s3cluster_queue.db')
artifacts_dir = f'/var/perfline'
pack_artifacts = False
nodes = 'sm13-r2.pun.seagate.com,sm14-r2.pun.seagate.com'
ha_type = 'pcs'
# TODO: Pass parameter of type: HARE or Pacemaker