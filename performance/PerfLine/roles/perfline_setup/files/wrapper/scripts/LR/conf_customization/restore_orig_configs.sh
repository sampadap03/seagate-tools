#!/usr/bin/env bash
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

set -e
set -x

SCRIPT_NAME=`echo $0 | awk -F "/" '{print $NF}'`
SCRIPT_PATH="$(readlink -f $0)"
SCRIPT_DIR="${SCRIPT_PATH%/*}"

source "$SCRIPT_DIR/../../../perfline.conf"

EX_SRV="pdsh -S -w $NODES"

HARE_CONF_LOCATION="/var/lib/hare"
HARE_CONFIG="$HARE_CONF_LOCATION/cluster.yaml"
HARE_CONFIG_BACKUP="$HARE_CONF_LOCATION/.perfline__cluster.yaml__backup"

MOTR_CONFIG="/etc/sysconfig/motr"
MOTR_CONFIG_BACKUP="/etc/sysconfig/.perfline__motr__backup"

HAPROXY_CONFIG="/etc/haproxy/haproxy.cfg"
HAPROXY_CONFIG_BACKUP="/etc/haproxy/.perfline__haproxy.cfg__backup"

S3_CONFIG="/opt/seagate/cortx/s3/conf/s3config.yaml"
S3_CONFIG_BACKUP="/opt/seagate/cortx/s3/conf/.perfline__s3config.yaml__backup"

LNET_CONFIG="/etc/modprobe.d/lnet.conf"
LNET_CONFIG_BACKUP="/etc/modprobe.d/.perfline__lnet.conf__backup"

IB_CONFIG="/etc/modprobe.d/ko2iblnd.conf"
IB_CONFIG_BACKUP="/etc/modprobe.d/.perfline__ko2iblnd.conf__backup"

function restore_hare_config()
{
    $EX_SRV "if [[ -e $HARE_CONFIG_BACKUP ]]; then mv -f $HARE_CONFIG_BACKUP $HARE_CONFIG; fi"
}

function restore_motr_config()
{
    $EX_SRV "if [[ -e $MOTR_CONFIG_BACKUP ]]; then mv -f $MOTR_CONFIG_BACKUP $MOTR_CONFIG; fi"
}

function restore_haproxy_config()
{
    $EX_SRV "if [[ -e $HAPROXY_CONFIG_BACKUP ]]; then mv -f $HAPROXY_CONFIG_BACKUP $HAPROXY_CONFIG; fi"
}

function restore_s3_config()
{
    $EX_SRV "if [[ -e $S3_CONFIG_BACKUP ]]; then mv -f $S3_CONFIG_BACKUP $S3_CONFIG; fi"
}

function restore_lnet_config()
{
    $EX_SRV "if [[ -e $LNET_CONFIG_BACKUP ]]; then mv -f $LNET_CONFIG_BACKUP $LNET_CONFIG; fi"
}

function restore_ib_config()
{
    $EX_SRV "if [[ -e $IB_CONFIG_BACKUP ]]; then mv -f $IB_CONFIG_BACKUP $IB_CONFIG; fi"
}

function apply_configs()
{
    set +e
    $EX_SRV "systemctl stop lnet"
    $EX_SRV "systemctl start lnet"
    $EX_SRV "systemctl restart haproxy"
    set -e
}

function main()
{
    restore_hare_config
    restore_motr_config
    restore_haproxy_config
    restore_s3_config
    restore_lnet_config
    restore_ib_config
    apply_configs
}

main $@
exit $?