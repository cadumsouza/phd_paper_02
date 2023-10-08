"""
                    Project MOSASAUR - rules.py

[MO]del-based [S]ystem [A]pplied to [S]ubsea [AU]tonomous [R]obotics

Rules file for the Situation Awareness Model (SAM) prototype applied
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

NOTE: NO RULE IS PROVIDED IN THIS FILE SINCE THEY ARE INTELLECTUAL PROPERTY.
"""

from project.robot_db.python.typeDB_main.builder import BuildModel
from typedb.client import SessionType, TransactionType
from project.robot_db.python.typeDB_main.color_text import Color, Box
import pprint

color = Color()
box = Box()


class RuleBuilder:
    def __init__(self):
        self.db_name = "robot_db"
        self.client = BuildModel.Client().client
        self.session_type = SessionType.SCHEMA
        self.transaction_type = TransactionType.WRITE
        self.rule_set = \
            {'rule-name': {'when': "{ condition }", 'then': "{ consequence }"}, }

    def rule_builder(self, rule_name, erase=False, commitment=False):
        rule_set = self.rule_set
        condition = rule_set[rule_name]['when']
        conclusion = rule_set[rule_name]['then']
        session_type = SessionType.SCHEMA
        with self.client.session(self.db_name, session_type) as sch_session:
            with sch_session.transaction(TransactionType.WRITE) as transaction:
                if erase is False:
                    msg = box.cyan(f'\u26A0\u0009 > BUILD ({rule_name})')
                    print(msg)
                    query = f'define rule {rule_name}: when {condition} then {conclusion};'
                    print(f'{color.c6(f"rule {rule_name}:")}' + '\n\u0009' +
                          f'{color.c7(f"when {condition}")}' + '\n\u0009' +
                          f'{color.c4(f"then {conclusion}")}')
                    transaction.query().define(query)
                    transaction.commit() if commitment else None
                else:
                    msg = box.red(f'\u26A0\u0009 > ERASE ({rule_name})')
                    print(msg)
                    query = f'undefine rule {rule_name};'
                    transaction.query().undefine(query)
                    transaction.commit() if commitment else None
            transaction.close()

