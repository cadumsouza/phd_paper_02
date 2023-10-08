"""
                    Project MOSASAUR - inquirer.py

[MO]del-based [S]ystem [A]pplied to [S]ubsea [AU]tonomous [R]obotics

Inquirer file for the Situation Awareness Model (SAM) prototype applied
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

from typedb.client import SessionType, TransactionType, TypeDBOptions
from project.robot_db.python.typeDB_main.builder import BuildModel
from project.robot_db.python.typeDB_main.auxiliary import *
from project.robot_db.python.typeDB_main.color_text import Color, Box
from project.robot_db.python.typeDB_main.decider import DecisionMaker
import copy
color = Color()
box = Box()


class QueryModel:
    """
    The objective of this class is to provide a simple interface to the user to query the database.
    Most of the time we are going to use "match" queries.
    Example:
        match $s isa sensor; get $s;
        match $t isa physical-dimension, has unit $u, has measure-value $m; get $t, $u, $m;

    """
    def __init__(self):
        self.db_name = None
        self.client = BuildModel.Client().client
        self.session_type = SessionType.DATA
        self.schema = BuildModel.Schema()
        self.decision = DecisionMaker()
        options = TypeDBOptions.core()
        options.infer = True
        options.explain = True
        self.options = options
        self.copy = copy
        self.count = 0

    def open_tx(self):
        db_name = "robot_db"
        with self.client.session(db_name, self.session_type) as session:
            with session.transaction(TransactionType.READ, options=self.options) as tx:
                print(tx.is_open())
                return tx

    def valid_input_phrase(self, p, reset_tx=''):
        """
        This function checks if the input phrase is valid.
        NOTE: On the gRPC side, when an error occurs, the remote call is stopped.
        Unfortunately a transaction is a single call in gRPC, so this means the whole
        transaction is aborted (even on syntax errors)
        :param reset_tx:
        :param p: input phrase p
        :return p_dict: phrase in dictionary format
        """
        db_name = "robot_db"
        with self.client.session(db_name, self.session_type) as session:
            with session.transaction(TransactionType.READ, options=self.options) as tx:

                if reset_tx != '':                                      # RESET TRANSACTION
                    new_phrase = p                                      # RESET PHRASE
                    p_dict = phrase2dict(tx, new_phrase)                # RESET PHRASE DICTIONARY
                else:
                    p_dict = phrase2dict(tx, p)                         # PHRASE DICTIONARY

                if p_dict != {} and len(p_dict) > 1:                    # VALIDATE PHRASE IF NOT EMPTY
                    return p_dict
                else:
                    new_phrase = input(f'INPUT NEW PHRASE \u25B6 ')     # ASK FOR NEW PHRASE
                return self.valid_input_phrase(new_phrase, 'reset')     # RECURSIVE FUNCTION

    def command_line(self, phrase=None, test_title=None):
        """
        This function is the main function of the class. It receives a phrase and returns the query.
        :param test_title:
        :param phrase:
        :return:
        """

        if test_title:
            division_line(f'INPUT ERROR TESTING \u25B6 {test_title}', 'test')

        phrase = '' if phrase is None else phrase           # SOLVES ERROR NUMBER 1 - NO INPUT PHRASE
        tab = '\u0009'                                      # ASCII TAB CHARACTER
        db_name = "robot_db"                                # DATABASE NAME
        qn = 0
        with self.client.session(db_name, self.session_type) as session:
            # with session.transaction(TransactionType.READ) as transaction:  # TO TESTE WITHOUT INFERENCE
            with session.transaction(TransactionType.READ, options=self.options) as transaction:

                d_phrase = self.valid_input_phrase(phrase)  # VALIDATE INPUT PHRASE (ERROR HANDLING)

                print(box.c0(f'(INPUT PHRASE) > {phrase}', tab=5, division=True))
                #      ╭──────────────────────╮
                # ━━━━━┥ INPUT PHRASE ▶ phase ┝━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                #      ╰──────────────────────╯

                print(box.c1(f'Command Line > {d_phrase}')) if d_phrase is not None else 0
                print(color.c3('\n \u25B6 STARTING SITUATION AWARENESS PROCEDURE\n'))
                '''
                ╭──────────────────────────────────────────────────────────────────────────╮
                │ Command Line ▶ {'command': '', element:, '', prep: '', 'pair': ['', '']} │
                ╰──────────────────────────────────────────────────────────────────────────╯
                '''
                question0 = f'Q{qn}. What is my actual location (latitude, longitude) ?'
                print(f' \u25B6 {question0}')
                answer0 = 'location > (ACTUAL - from navigation system)'
                complement_answer0 = 'name | latitude | longitude | Water Depth'
                print(box.c1(answer0, complement_answer0, 0))

                ''' ▶ Q0. What is my actual location (latitude, longitude) ?
                ╭────────────────────────────────────────────╮ ╭───────────────────────────────────────────╮
                │ location ▶ ACTUAL - from navigation system ├─┤ name | latitude | longitude | Water Depth │
                ╰────────────────────────────────────────────╯ ╰───────────────────────────────────────────╯
                '''
                def return_element(name):
                    return d_phrase.get(name, 0) if d_phrase is not None else 0

                # Extract all elements from the phrase dictionary
                command = return_element('command')
                element1 = return_element('element-1')
                pair1 = return_element('pair-1')
                prep1 = return_element('prep-1')
                element2 = return_element('element-2')
                pair2 = return_element('pair-2')
                prep2 = return_element('prep-2')
                element3 = return_element('element-3')

                # ━━┥ 1. COMMAND INQUIRE ┝━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                qn += 1
                if command != 0:
                    command_type = find_type(transaction, command).split(":")[1]
                    command_list = goal_list(transaction, command, 'function', 'attribute')

                    # print(link(transaction, command, pair1, pair2, linking=False)) NOT FOR HERE --> FOR EXECUTING

                    if 'function' in command_list:
                        use_tool = True
                        a_name = "command-type"

                        # QUESTION 1 - COMMAND
                        question1f = f'Q{qn}. What kind of command is {color.c3(command)} ?'
                        print(f'{tab * 2}\u25B6 {question1f}')
                        answer1f = f'{command} > is a (tool function) and {goal_list(transaction, command, a_name)}'
                        print(box.c3(answer1f, '\u25B6 Requires TOOL', 2))

                        ''' ▶ Q1. What kind of command is command ?
                            ╭───────────────────────────────────────────────────────╮ ╭─────────────────╮
                            │ command ▶ is a tool function and ['A-goal', 'B-goal'] ├─┤ ▶ Requires TOOL │
                            ╰───────────────────────────────────────────────────────╯ ╰─────────────────╯
                        '''
                        c_answer1f = f'Q{qn}a.What {color.c4("TOOL(s)")} are available for "{command}" command:'
                        print(f'{tab * 4}' + '\u25B6 ' + c_answer1f)
                        query_tool = f'match $x isa tool, has function "{str(command)}", ' \
                                     f'has element-type $y; get $y;'
                        tool_list = [e.map().get('y').as_attribute().get_value()
                                     for e in list(match_query(transaction, query_tool))]
                        print(box.c4(f'Tool list > ({tool_list})', '', 4))

                        '''     ▶ TOOL(s) available for "clean" command:
                                ╭────────────────────────────────────────────╮
                                │ Tool list ▶ ['tool-A', 'tool-B', 'tool-C'] │
                                ╰────────────────────────────────────────────╯
                        '''
                    else:
                        use_tool = False

                        # QUESTION 1 - COMMAND
                        question1 = f'Q{qn}. What kind of command is {color.c3(command)} ?'
                        print(f'{tab * 2}\u25B6 {question1}')
                        answer1 = f'{command} > is a {goal_list(transaction, command, command_type)}'
                        print(box.c3(answer1, '', 2))

                        ''' ▶ Q1. What kind of command is command ?
                            ╭───────────────────────────╮
                            │ command ▶ is a ['A-goal'] │
                            ╰───────────────────────────╯
                        '''
                else:
                    print(color.yellow(f" \u25B6\u0009INPUT A COMMAND (look at inquirer.py in COMMAND)"))

                # Verify if command requires more than one element - attribute 'goal-location'
                # TEST TO SEE IF THE COMMAND REQUIRES 1 OR 2 ELEMENTS

                prep_q = f'match $x isa goal, has command-type "{command}", has goal-location $gl; get $gl;'
                prep_iter = list(match_query(transaction, prep_q))
                prep_test = prep_iter[0].map().get('gl').as_attribute().get_value() if prep_iter != [] else ''

                # ━━┥ 2. ELEMENT / PAIR INQUIRE ┝━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                qn += 1

                def inquiry_element(e):
                    # Verifies if element is a list or a pair of elements
                    tag_number = None
                    if isinstance(e, list):
                        element = e[0]
                        tag_number = e[1]
                    else:
                        element = e

                    e_type = element_type(transaction, element)
                    g_list = goal_list(transaction, command, command_type)

                    def inquiry_answer():
                        relations_dicts = get_relations(transaction, element, e_type, tag_number, pair2, prep1)
                        f_rxy_dict, f_rxz_dict, f_rwz_dict, l_pair1, l_pair2, l_dict, coord_list = relations_dicts

                        def build_question(tx, e, p_tag=None, pair2=False):
                            tab = '\u0009'
                            question2 = f'Q{qn}.What kind of element is {color.c3(e)} ?'
                            print(color.c3(f'{tab * 2}' + f'{"─" * 120}'))
                            print(f'{tab * 2}\u25B6 {question2}')
                            e_type = element_type(tx, e)

                            if pair2:
                                c_tag = f'has tag-number: {p_tag}'
                            else:
                                c_tag = f'has tag-number: {tag_number}' if tag_number is not None else ''

                            '''     ▶ Q2. What kind of element is element?     '''

                            if e_type[1] == 'entity':
                                query_entity = f'match $e type {e}; get $e;'
                                iterator = next(match_query(tx, query_entity)).map()
                                superclass = iterator.get('e').as_remote(tx).get_supertype().get_label()
                                type_el = e
                                print(box.c3(f'{e} > is a ({superclass}) {e_type[1]} ', f'{c_tag}', 2))
                                '''     ╭───────────────────────────╮ ╭─────────────────╮
                                        │ element ▶ is a e_type[1]  ├─┤ tag-number: T-N │
                                        ╰───────────────────────────╯ ╰─────────────────╯
                                '''
                                question2a = f'Q{qn}a. What kind of relations {color.c4(e)} has ?'
                                print(f'{tab * 4}\u25B6 {question2a}')

                            else:
                                superclass = e_type[1]
                                type_el = e_type[1]
                                print(box.c3(f'{e} > is a ({e_type[1]}) attribute',
                                             f'attribute name: {e_type[0]} | {c_tag}', 2))
                                '''     ╭──────────────────────────╮ ╭────────────────────────────────────────╮
                                        │ element ▶ is a e_type[1] ├─┤ attribute name: name | tag-number: T-N │
                                        ╰──────────────────────────╯ ╰────────────────────────────────────────╯
                                '''
                                check_command_compliance(command, element, use_tool, superclass, g_list)
                                question2a = f'Q{qn}a. What kind of relations {color.c4(e)} ' \
                                             f'{color.c4(type_el)} has ?'
                                print(f'{tab * 4}\u25B6 {question2a}')

                        def map_relations(e, f_dict, ld, p2=None):
                            p_test = None
                            if p2 is not None:
                                if isinstance(p2, list):
                                    p_test = p2[0]
                            else:
                                p_test = e
                            loc_list = []
                            for key, value in ld.items():
                                loc_list = f'{key} {value[1]}'
                            for rel in list(f_dict.keys()):
                                print(box.c4(rel, f'{e}', 4))
                                if loc_list:
                                    match_loc = list(filter(lambda l: loc_list in l, f_dict[rel]))
                                    if match_loc and e == p_test:
                                        l_value = match_loc[0]
                                        loc_index = f_dict[rel].index(l_value)
                                        f_dict[rel][0], f_dict[rel][loc_index] = f_dict[rel][loc_index], f_dict[rel][0]
                                    else:
                                        l_value = ''
                                    if rel == 'assembling':
                                        msg = 'GRAB ACTION - MANUAL TASK'
                                        print(box.c5(f_dict[rel], f_dict[rel][0], 6, True, msg, 5))
                                    else:
                                        msg = 'TARGET LOCATION'
                                        print(box.c5(f_dict[rel], l_value, 6, True, msg, 5))
                                else:
                                    print(box.c5(f_dict[rel], '', 6, True, '', 5))
                            return ld

                        def target_location(lp1, lp2, p2=None):

                            if lp1:
                                if len(lp1) > 1:
                                    location_1 = f'SAME AS ▶ {p2}'
                                    coord = f'SAME AS ▶ {p2}'
                                    return coord, location_1
                                else:
                                    location_1 = lp1[0]
                                    l1 = find_location(transaction, lp1[0])
                                    if l1:
                                        coord = f'name: {l1[0]} | latitude: {l1[1]} ' \
                                                f'| longitude: {l1[2]} | water-depth: {l1[3]}'
                                    else:
                                        # coord = 'UNDEFINED'
                                        raise LocationError
                                    return coord, location_1
                            else:
                                if lp2:
                                    location_2 = p2
                                    coord = lp2
                                else:
                                    location_2 = 'UNDEFINED'
                                    coord = 'UNDEFINED'
                                return coord, location_2

                        def retrieve_coordinates(c, loc, el):
                            if isinstance(c, list):
                                print(f'{tab * 2}\u25B6 {color.c3("Possible locations to")} {el}. '
                                      f'{color.c3("PROBABLY NOT:")} {loc}')
                                c2, l2 = target_location(l_pair2, coord_list, pair2)
                                print(box.c3(c, c2, 2, True, 'TARGET LOCATION - PROBABLY NOT HERE'))
                                return c, loc
                            else:
                                print(box.c1(f'Location > (TARGET)', c, 0))
                                return c, loc

                        def retrieve_target_information(tx, loc):
                            if loc != 'UNDEFINED':
                                target_element = loc[0]
                                target_tag = loc[1]
                                target_type = element_type(transaction, target_element)
                                question2a = f'Q{qn}a. What kind of relations {color.c4(target_element)} has ?'
                                print(f'{tab * 4}\u25B6 {question2a}')
                                rel_dicts = get_relations(tx, target_element, target_type, target_tag)
                                t_dict = rel_dicts[0]
                                map_relations(target_element, t_dict, l_dict)
                                # return target_element, target_tag, target_type, f_rxy_d
                                return t_dict
                            else:
                                return None

                        def find_common_elements(d1, d2):
                            if d1 and d2 is not None:
                                question2a = f'Q{qn}a. Which are the common elements between target and local ?'
                                print(f'{tab * 2}\u25B6 {question2a}')

                                s1 = set(i.split('▶')[0] for sl in d1.values() for i in sl)
                                s2 = set(i.split('▶')[0] for sl in d2.values() for i in sl)
                                c_elements = s1.intersection(s2)
                                if isinstance(c_elements, set):
                                    print(box.c3(list(c_elements), '', 2, True))
                                else:
                                    print(box.c3(c_elements, '', 2))

                        if pair2:

                            # ELEMENT 1 OR PAIR 1 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                            build_question(transaction, element, pair2=False)
                            map_relations(element, f_rxy_dict, l_dict)
                            coordinates1, local1 = target_location(l_pair1, coord_list, pair2)
                            retrieve_coordinates(coordinates1, local1, element)

                            # PAIR 2 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                            build_question(transaction, pair2[0], pair2[1], pair2=True)
                            map_relations(pair2[0], f_rwz_dict, l_dict, pair2)
                            coordinates, local = target_location(l_pair2, coord_list, pair2)
                            retrieve_coordinates(coordinates, local, element)
                            target_dict = retrieve_target_information(transaction, local)
                            find_common_elements(target_dict, f_rwz_dict)

                        else:

                            build_question(transaction, element, pair2=False)
                            map_relations(element, f_rxy_dict, l_dict)
                            coordinates, local = target_location(l_pair1, coord_list)
                            retrieve_coordinates(coordinates, local, element)
                            target_dict = retrieve_target_information(transaction, local)
                            find_common_elements(target_dict, f_rxy_dict)

                    return inquiry_answer()

                try:
                    if element1 != 0:
                        inquiry_element(element1)
                    else:
                        inquiry_element(pair1)

                    # ━━┥ 3. PREP-1 INQUIRE ┝━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                    # the preposition confirms the association... if there is no association, need to ask if
                    # it is necessary to associate... like in:
                    # operate mechanism OF tool TOOL-CLAMP-MANU-AT-UN-03

                    print(color.cyan('\n' + "\u2501" * 175 + '\n'))

                except ComplianceError:
                    print(color.e1(f'{tab * 2}' + f'{"─" * 120}'))
                    p = input(color.e1(f'\n{tab * 2}PLEASE ENTER A VALID COMMAND LINE \u25B6 '))
                    self.command_line(p)

                except LocationError:
                    print(color.e1(f'{tab * 2}' + f'{"─" * 120}'))
                    p = input(color.e1(f'\n{tab * 2}MISSING LOCATION - PLEASE ENTER A COMPLETE COMMAND LINE \u25B6 '))
                    self.command_line(p)
