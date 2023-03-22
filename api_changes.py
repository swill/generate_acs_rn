#!/usr/bin/env python

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
Usage:
  api_changes.py <diff.json>
  api_changes.py (-h | --help)
Options:
  -h --help                 Show this screen.
  --col_name_width=<arg>    The width of the Name column [default: 60].
  --col_desc_width=<arg>    The width of the Description column [default: 80].
"""

import docopt
import json
from lib.Table import TableRST
import pprint
import sys

# run the code...
if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    data = {}
    try:
        with open(args['<diff.json>']) as f:
            data = json.load(f)
    except IOError:
      print("Error: File '%s' does not exist." % args['<diff.json>'])
      sys.exit(0)

    # new commands
    if data and 'commands_added' in data and len(data['commands_added']) > 0:
        new_apis_table = ''
        try:
            table = TableRST([
                ("Name", int(args['--col_name_width'])),
                ("Description", int(args['--col_desc_width']))
            ])
            for cmd in data['commands_added']:
                table.add_row(['``%s``' % cmd['name'], cmd['description']])
            new_apis_table = table.draw()
        except IOError as e:
            print('ERROR: %s' % str(e))

        new_commands_title = 'New API Commands'
        print('%s' % new_commands_title)
        print('%s\n' % ('-'*len(new_commands_title)))

        print('.. cssclass:: table-striped table-bordered table-hover\n')
        print(new_apis_table)
        print('')

    # removed commands
    if data and 'commands_removed' in data and len(data['commands_removed']) > 0:
        removed_apis_table = ''
        try:
            table = TableRST([
                ("Name", int(args['--col_name_width'])),
                ("Description", int(args['--col_desc_width']))
            ])
            for cmd in data['commands_removed']:
                table.add_row(['``%s``' % cmd['name'], cmd['description']])
            removed_apis_table = table.draw()
        except IOError as e:
            print('ERROR: %s' % str(e))

        removed_commands_title = 'Removed API Commands'
        print('%s' % removed_commands_title)
        print('%s\n' % ('-'*len(removed_commands_title)))

        print('.. cssclass:: table-striped table-bordered table-hover\n')
        print(removed_apis_table)
        print('')

    # sync changed commands
    if data and 'commands_sync_changed' in data and len(data['commands_sync_changed']) > 0:
        sync_changed_apis_table = ''
        try:
            table = TableRST([
                ("Description", int(args['--col_desc_width']))
            ])
            for cmd in data['commands_sync_changed']:
                table.add_row('``%s`` is now %s' % (cmd['name'], cmd['sync_type']))
            sync_changed_apis_table = table.draw()
        except IOError as e:
            print('ERROR: %s' % str(e))

        sync_change_commands_title = 'Sync Type Changed API Commands'
        print('%s' % sync_change_commands_title)
        print('%s\n' % ('-'*len(sync_change_commands_title)))

        print('.. cssclass:: table-striped table-bordered table-hover\n')
        print(sync_changed_apis_table)
        print('')

    # args changed commands
    if data and 'commands_args_changed' in data and len(data['commands_args_changed']) > 0:
        args_changed_apis_table = ''
        try:
            table = TableRST([
                ("Name", int(args['--col_name_width'])),
                ("Description", int(args['--col_desc_width']))
            ])
            for cmd in data['commands_args_changed']:
                desc = ''
                if 'request' in cmd:
                    desc += '**Request:**\n'
                    if 'params_new' in cmd['request'] and len(cmd['request']['params_new']) > 0:
                        desc += '\n*New Parameters:*\n\n'
                        for param in cmd['request']['params_new']:
                            desc += '- ``%s`` (%s)\n' % (param['name'], 'required' if param['required'] else 'optional')
                    if 'params_removed' in cmd['request'] and len(cmd['request']['params_removed']) > 0:
                        desc += '\n*Removed Parameters:*\n\n'
                        for param in cmd['request']['params_removed']:
                            desc += '- ``%s``\n' % param['name']
                    if 'params_changed' in cmd['request'] and len(cmd['request']['params_changed']) > 0:
                        desc += '\n*Changed Parameters:*\n\n'
                        for param in cmd['request']['params_changed']:
                            old_text = 'required' if param['required_old'] else 'optional'
                            new_text = 'required' if param['required_new'] else 'optional'
                            desc += '- ``%s`` was \'%s\' and is now \'%s\'\n' % (param['name'], old_text, new_text)
                if 'response' in cmd:
                    if len(desc) > 0:
                        desc += '\n'
                    desc += '**Response:**\n'
                    if 'params_new' in cmd['response'] and len(cmd['response']['params_new']) > 0:
                        desc += '\n*New Parameters:*\n\n'
                        for param in cmd['response']['params_new']:
                            desc += '- ``%s``\n' % param['name']
                    if 'params_removed' in cmd['response'] and len(cmd['response']['params_removed']) > 0:
                        desc += '\n*Removed Parameters:*\n\n'
                        for param in cmd['response']['params_removed']:
                            desc += '- ``%s``\n' % param['name']
                table.add_row(['``%s``' % cmd['name'], desc])
            args_changed_apis_table = table.draw()
        except IOError as e:
            print('ERROR: %s' % str(e))

        args_changed_commands_title = 'Parameters Changed API Commands'
        print('%s' % args_changed_commands_title)
        print('%s\n' % ('-'*len(args_changed_commands_title)))

        print('.. cssclass:: table-striped table-bordered table-hover\n')
        print(args_changed_apis_table)
        print('')


