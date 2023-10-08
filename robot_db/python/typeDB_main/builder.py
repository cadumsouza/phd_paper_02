"""
                    Project MOSASAUR - builder.py

[MO]del-based [S]ystem [A]pplied to [S]ubsea [AU]tonomous [R]obotics

Builder file for the Situation Awareness Model (SAM) prototype applied
to Robotic Underwater Autonomy. This code is part of the author's
PhD research project conducted at Polytechnique Montreal University
and funded by Petróleo Brasileiro S.A. - PETROBRAS.

        Copyright (C) 2023  Carlos Eduardo Maia de Souza

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from typedb.client import TypeDB, SessionType, TransactionType, TypeDBOptions
from subprocess import PIPE, Popen, CREATE_NEW_PROCESS_GROUP
from project.robot_db.python.typeDB_main.auxiliary import *
from project.robot_db.python.typeDB_main.color_text import Color, Box
import os
import time
import pprint
import socket

color = Color()
box = Box()


class BuildModel:
    def __init__(self):
        self.server = self.Server()
        self.database = self.Database()
        self.schema = self.Schema()
        self.datahandling = self.DataHandling()

    class Server:
        def __init__(self):
            t = 4
            if self.check_server():
                print('\n')
                print(box.cyan('\u26A0\u0009 > TypeDB Server is (running!) Hit CTRL+C in cmd window to stop.'))
                print(color.cyan('\n' + "\u2501" * 175 + '\n'))

            else:
                Popen('start typedb server', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)

                text1 = f'Starting TypeDB Server...  Wait {t}s to bootup complete'
                text2 = f'Hit CTRL+C in cmd window to stop'

                horizontal_line = "\u2500" * (len(text1) + 10)
                line1 = f'\u256D{horizontal_line}\u256E'
                line2 = '\u2502' + text1.center(len(text1) + 10) + '\u2502'
                line3 = '\u2502' + text2.center(len(text1) + 10) + '\u2502'
                line4 = f'\u2570{horizontal_line}\u256F'

                print('\n')
                print(color.neon(line1))
                print(color.neon(line2))
                print(color.neon(line3))
                print(color.neon(line4))

                print(color.neon('\n' + "\u2501" * 175 + '\n'))
                time.sleep(t)

        @staticmethod
        def check_server():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', 1729))
            if result == 0:
                sock.close()
                return True
            else:
                sock.close()
                return False

    class Client:
        def __init__(self):
            with TypeDB.core_client(address=TypeDB.DEFAULT_ADDRESS) as client_db:
                self.client = client_db

    class Database:
        def __init__(self):
            self.db_name = None
            self.client = BuildModel.Client().client

        def lists(self):
            """
            List all databases on the server.
            :return: list of all databases on the server
            """
            databases = self.client.databases().all()
            databases_list = [db.name() for db in databases]
            return databases_list

        def check_database(self, db_name):
            check = self.client.databases().contains(db_name)
            if check is True:
                print(f"{color.green('[')}{db_name:^10}{color.green('] --------- on the server.')}")
            else:
                print(f"{color.red('[')}{db_name:^10}{color.red('] ----- not on the server.')}")

        def create_database(self, db_name):
            db_list = self.lists()
            if db_name not in db_list:
                print(f'Creating database \033[36m>>>>\033[0m [\033[36m{db_name:^10}\033[0m]')
                self.client.databases().create(db_name)
            else:
                print(f'Database [{db_name}] already exists.')
            self.db_name = db_name

        def delete_database(self, db_name):
            db_list = self.lists()
            if db_name in db_list:
                print(f'Deleting database \033[33m>>>>\033[0m [\033[33m{db_name:^10}\033[0m]')
                self.client.databases().get(db_name).delete()
            else:
                print(f'Database [{db_name}] does not exist or deleted.')

    class Schema:
        def __init__(self):
            self.db_name = None
            self.client = BuildModel.Client().client
            self.datahandling = BuildModel.DataHandling
            self.session_type = SessionType.SCHEMA

        def print_schema(self, db_name):
            """
            This function returns the entire schema of the database.
            :return: schema
            """
            with self.client.session(db_name, self.session_type) as session:
                db_schema = session.database().schema()
                session.close()
                return db_schema

        def load_schema(self, db_name):
            """
            This function loads the schemas of each module of the framework into the database.
            schema_mod1 - contains the schema for the module 1 PERCEPTION
            schema_mod2 - contains the schema for the module 2 THINKING
            schema_mod3 - contains the schema for the module 3 ACTION
            schema_mod4 - contains the schema for the module 4 TASK KNOWLEDGE
            :param db_name: name of the database.
            :return: commits the schemas to the database.
            """
            # Loads the files of each schema module individualy.
            with open("project/robot_db/schemas/schema_mod1.tql", "r") as f1:
                tql1 = f1.read()
            with open("project/robot_db/schemas/schema_mod2.tql", "r") as f2:
                tql2 = f2.read()
            with open("project/robot_db/schemas/schema_mod3.tql", "r") as f3:
                tql3 = f3.read()
            with open("project/robot_db/schemas/schema_mod4.tql", "r") as f4:
                tql4 = f4.read()

            # TEMPORARY - REMOVE AFTER EVERYTHING IS WORKING !!!!!
            with open("schema_cell_test.tql", "r") as temp:
                tql_temp = temp.read()

            print(box.cyan(f'\u26A0\u0009 > (WARNING!) SCHEMA IS NOW BEING LOADED'))
            with self.client.session(db_name, self.session_type) as session:
                with session.transaction(TransactionType.WRITE) as transaction:
                    # print(transaction.is_open())
                    # transaction.query().define(tql1)                      # uncomment after testing
                    # transaction.query().define(tql2)                      # uncomment after testing
                    # transaction.query().define(tql3)                      # uncomment after testing
                    # transaction.query().define(tql4)                      # uncomment after testing
                    transaction.query().define(tql_temp)
                    print(f'\033[31mWARNING!!! TEMPORARY SCHEMA - REMOVE THIS WARNING AFTER!!!\033[0m')
                    transaction.commit()
                    transaction.close()
                session.close()

        def schema_dict(self, thing, tx):
            query = f'match $var sub! {thing}; get $var;'
            iterator = tx.query().match(query)
            result_dict = {}
            for cmap in iterator:
                d = cmap.map()
                for key in d.keys():
                    concept = d[key].get_label().name()
                    concept_d = self.schema_dict(concept, tx)
                    if concept_d:
                        result_dict[concept] = concept_d
                    else:
                        result_dict[concept] = ''
            return result_dict

        def undef_concepts(self, thing, tx):
            # thing = ['entity', 'attribute', 'relation']
            query = f'match $c sub! {thing}; get $c;'
            iterator = tx.query().match(query)
            result_list = []
            for cmap in iterator:
                d = cmap.map()
                for k, v in d.items():
                    concept = v.get_label().name()
                    sub_concept = self.undef_concepts(concept, tx)  # recursive call to get the sub_concept
                    # Check if the sub_concepts list is not empty
                    if sub_concept:
                        result_list.append([concept] + sub_concept)
                    else:
                        # if sub_concept list is empty, then undefine the concept
                        tx.query().undefine(f'undefine {concept} sub {thing};')
            return result_list

        def delete_schema(self, db_name):
            session_type = SessionType.SCHEMA
            print(box.violet(f'\u26A0\u0009 > (WARNING!)   SCHEMA IS BEING DELETED'))
            with self.client.session(db_name, session_type) as sch_session:
                with sch_session.transaction(TransactionType.WRITE) as transaction:
                    things_list = ['entity', 'attribute', 'relation']
                    for concept in things_list:
                        print(f'{color.red(" Deleting... ")}{concept}')
                        self.undef_concepts(concept, transaction)
                    transaction.commit()
                transaction.close()
            print(box.blue(f"({db_name}) > SCHEMA DELETED"))

        def print_schema_dict(self, db_name):
            session_type = SessionType.SCHEMA
            with self.client.session(db_name, session_type) as sch_session:
                with sch_session.transaction(TransactionType.READ) as transaction:
                    things_list = ['entity', 'attribute', 'relation']
                    for concept in things_list:
                        pprint.pprint(self.schema_dict(concept, transaction))
                transaction.close()

    class DataHandling:
        def __init__(self):
            self.db_name = None
            self.client = BuildModel.Client().client
            self.session_type = SessionType.DATA
            self.inputs = None
            self.data_folder = './project/robot_db/data'

        def file_paths(self, concept_type=None):
            file_paths = []
            os_dir = f'{self.data_folder}/{concept_type}_data'
            for f in os.listdir(os_dir):
                if f.endswith(".csv"):
                    path = os.path.join(os_dir, f).replace("\\", "/")
                    file_path = os.path.splitext(path)[0]
                    file_dict = {"data_path": file_path}
                    file_paths.append(file_dict)
            return file_paths

        def load_data(self, db_name, concept_type=None, commitment=False):
            inputs = self.file_paths(concept_type)
            with self.client.session(db_name, self.session_type) as session:
                for i in inputs:
                    print(color.c3('\n' + "\u2501" * 175 + '\n'))
                    print(box.l_cyan(f'DATA FILE: {i["data_path"].split("/")[-1]}.csv'))
                    thing = i["data_path"].split("/")[-1]
                    items = csv_to_dict_list(i)

                    with session.transaction(TransactionType.WRITE) as transaction:
                        if concept_type == 'entity':
                            for item_dict, x in zip(items, range(0, len(items))):
                                q = f'insert $v{x} isa {thing},'
                                for j in range(0, len(item_dict)):
                                    # Query constructors - concepts, attributes and roles
                                    a_key = list(item_dict.keys())[j]           # attribute key j
                                    a_value = list(item_dict.values())[j]       # attribute value j
                                    # SPECIAL CASE ┝━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                                    if ":" in a_value:
                                        attribute = a_key.split(" : ")[1]
                                        a_key = a_value.split(" : ")[0]
                                        if "|" in attribute:
                                            if " | " in a_value.split(" : ")[1]:
                                                a_list = a_value.split(" : ")[1]
                                                q = f'insert $v{x} isa {a_key},'
                                                for n, a in enumerate(a_list.split(" | ")):
                                                    q += f' has {attribute.split(" | ")[n]} "{str(a)}"'
                                                    q += f',' if n < len(a_list.split(" | ")) - 1 else ''
                                            else:
                                                a_list = a_value.split(" : ")[1]
                                                q = f'insert $v{x} isa {a_key},'
                                                q += f' has {attribute.split(" | ")[0]} "{str(a_list)}"'
                                        else:
                                            a_value = a_value.split(" : ")[1]
                                            key_type = find_type(transaction, a_key)
                                            if str(key_type).split(":")[0] == 'entity':
                                                q = f'insert $v{x} isa {a_key},'
                                                q += f' has {attribute} "{str(a_value)}"'
                                            else:
                                                q = query_builder(q, a_key, a_value, 'entity')
                                                q += ';'
                                                q += f' $v{x} "{str(a_key)}"'
                                                q += f',' if j < len(item_dict) - 1 else ''
                                    # NORMAL CASE ┝━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                                    else:
                                        q = query_builder(q, a_key, a_value, concept_type, '')
                                    q += f',' if j < len(item_dict) - 1 else ''
                                q += f';'
                                # FOR SURFACES ┝━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                                if item_dict.get('tag-number', 0) != 0:
                                    s_tag = item_dict['tag-number']
                                    name = item_dict['element-type']
                                    insert_s = f'insert $s{x} isa surface, ' \
                                               f'has name "surface-of-{name}", ' \
                                               f'has tag-number "{s_tag}";'
                                    transaction.query().insert(insert_s)
                                print(f'{color.c4(q)}')
                                print(color.c3(insert_s))
                                transaction.query().insert(q)
                            transaction.commit() if commitment else None
                        elif concept_type == 'relation':
                            for item_dict, x in zip(items, range(0, len(items))):
                                q1 = f'match'
                                q2 = f' insert $rel{x} ('
                                for k in range(0, int(len(item_dict.keys()))):
                                    d_keys = list(item_dict.keys())[k]
                                    d_values = list(item_dict.values())[k]
                                    concept = d_values.split(" : ")[0]
                                    c_type = find_type(transaction, concept)
                                    role = d_keys.split(" : ")[0]
                                    # For multiple roles with same name
                                    role = role.split("*")[0] if "*" in role else role
                                    a_name = d_keys.split(" : ")[1]
                                    a_value = d_values.split(" : ")[1]
                                    if a_value:
                                        q1 += f' $v{x + 1}{k} isa {concept},'
                                        if "|" in a_name:               # For multiple attributes
                                            if "|" in a_value:          # For multiple attributes
                                                for i, a in enumerate(a_value.split(" | ")):
                                                    if a_value.split(" | ")[i] != '-':
                                                        q1 = query_builder(q1, a_name.split(" | ")[i], a, 'entity', '')
                                                        q1 = q1 + ',' if i < len(a_value.split(" | ")) - 1 else q1 + ';'
                                            else:
                                                if c_type.split(":")[0] == 'entity':
                                                    q1 = query_builder(q1, a_name.split(" | ")[0], a_value, 'entity')
                                                    q1 += ';'
                                                else:
                                                    q1 = query_builder(q1, x + 1, a_value)
                                        else:
                                            if c_type.split(":")[0] == 'entity':
                                                # q1 += f' $v{x + 1}{k} isa {concept},'
                                                q1 = query_builder(q1, a_name, a_value, 'entity')
                                                q1 += ';'
                                            else:
                                                # q1 += f' $v{x + 1}{k} isa {concept};'
                                                q1 = query_builder(q1, x + 1, a_value)
                                    else:
                                        q1 += f' $v{x + 1}{k} isa {concept};'
                                    q2 += f'{role}: $v{x + 1}{k}'
                                    q2 += f', ' if k < int(len(item_dict.keys()) - 1) else ')'
                                q3 = f' isa {thing};'
                                insert_query = q1 + q2 + q3
                                print(f'{color.cyan(insert_query)}')
                                transaction.query().insert(insert_query)
                            transaction.commit() if commitment else None
                        transaction.close()

        def unload_data(self, db_name):
            with self.client.session(db_name, self.session_type) as session:
                with session.transaction(TransactionType.WRITE) as transaction:
                    delete_query = f'match $t isa thing; delete $t isa thing;'
                    print(box.e7(f"\u26A0\u0009 > (WARNING!) ALL DATA IS BEING DELETED"))
                    transaction.query().delete(delete_query)
                    transaction.commit()
                print(box.e2(f"\u26A0\u0009 > (WARNING!)   ALL DATA IS NOW DELETED"))
                transaction.close()

        def update_data(self):
            pass
