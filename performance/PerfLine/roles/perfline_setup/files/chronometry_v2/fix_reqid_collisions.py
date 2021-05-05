#!/usr/bin/env python3
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

import sys
import argparse
import sqlite3

def parse_args():
    parser = argparse.ArgumentParser(prog=sys.argv[0], description="""
    fix_reqid_collisions.py: change s3 request ids to avoid collisions between s3/motr layers.
    """)
    
    parser.add_argument("-d", "--db", type=str, default="m0play.db",
                        help="Performance database (m0play.db)")
    
    parser.add_argument("-f", "--fix-db", help="fix database",
                        action="store_true")

    return parser.parse_args()

def find_collisions(db_connection):
    select_collisions = """
        SELECT s3r.pid, s3r.id, s3r.type_id, mr.type_id
        FROM request s3r INNER JOIN request mr ON s3r.pid=mr.pid AND s3r.id=mr.id
        WHERE s3r.type_id='s3_request_state'
        AND mr.type_id != 's3_request_state'
        LIMIT 1;
    """

    cursor = db_connection.cursor()
    cursor.execute(select_collisions)
    result = True

    if cursor.fetchone() is None:
        result = False

    cursor.close()
    return result


def calculate_s3reqid_offset(db_connection):
    cursor = db_connection.cursor()
    cursor.execute('SELECT max(id) from request;')
    row = cursor.fetchone()
    max_reqid_value = row[0]
    cursor.close()

    offset = 10

    while offset < max_reqid_value:
        offset *= 10

    return offset

def fix_collisions(db_connection):
    offset_val = calculate_s3reqid_offset(db_connection)

    print(f"update s3 request id's values using offset {offset_val}")

    update_req_table = f"UPDATE request SET id=id+{offset_val} WHERE type_id='s3_request_state';"
    update_rel_table = f"UPDATE relation SET mid1=mid1+{offset_val} WHERE type_id='s3_request_to_client';"
    update_s3uid_table = f"UPDATE s3_request_uid SET id=id+{offset_val};"

    cursor = db_connection.cursor()
    cursor.execute(update_req_table)
    cursor.execute(update_rel_table)
    cursor.execute(update_s3uid_table)
    db_connection.commit()
    cursor.close()


def main():
    args = parse_args()
    db_connection = sqlite3.connect(args.db)

    found_collisons = find_collisions(db_connection)

    if found_collisons:
        print("found collisions of s3 request id")

        if args.fix_db:
            fix_collisions(db_connection)
        else:
            print("database is not changed. Use --fix-db option to fix database")

    db_connection.close()

if __name__ == "__main__":
    main()
