"""
                    Project MOSASAUR - main.py

[MO]del-based [S]ystem [A]pplied to [S]ubsea [AU]tonomous [R]obotics

Main file for the Situation Awareness Model (SAM) prototype applied
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

from project.robot_db.python.typeDB_main.builder import BuildModel
from project.robot_db.python.typeDB_main.inquirer import QueryModel
from project.robot_db.python.typeDB_main.color_text import Color, Box
from project.robot_db.python.typeDB_main.rules import RuleBuilder
import time

color = Color()
box = Box()


class UserCommand:
    """
    This class simulates a user command in NLP
    """
    def __init__(self):
        self.command = None

    def set_command(self, command):
        print(command)
        return command

    def get_command_entities(self):
        pass


if __name__ == '__main__':
    model = BuildModel()
    query = QueryModel()
    rule = RuleBuilder().rule_builder
    db = model.database

    # Database creation and deletion - CORRECT ONE
    # db.create_database("robot_db")
    # db.check_database("robot_db")

    #      ╭──────────────────────────────────╮
    # ━━━━━┥ SECTION - SCHEMA & DATA HANDLING ┝━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #      ╰──────────────────────────────────╯

    # WORKING - TO LOAD SCHEMAS (4 MODULES)
    # temporary modification for testing - change after!
    # model.schema.load_schema("robot_db")

    # schema = model.schema.print_schema("robot_db")
    # schema_dict = concept_dict(schema)

    # model.schema.print_schema_dict("robot_db")

# ╭──────────────────────────────────────────────────────────────────────────╮
    # model.datahandling.load_data("robot_db", 'entity', commitment=True)
    # model.datahandling.load_data("robot_db", 'relation', commitment=True)
# ╰──────────────────────────────────────────────────────────────────────────╯
# ╭──────────────────────────────────────────────╮
    # model.datahandling.unload_data("robot_db")
    # model.schema.delete_schema("robot_db")
# ╰──────────────────────────────────────────────╯

    #      ╭────────────────────────────────╮
    # ━━━━━┥ SECTION - TESTING INPUT ERRORS ┝━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #      ╰────────────────────────────────╯

    # division_line(f' INPUT ERROR TESTING \u25B6 1. NO INPUT PHRASE', 'test')
    # query.command_line()
    # query.command_line('', '2. EMPTY INPUT PHRASE')
    # query.command_line('wrong-comm', '3. WRONG INPUT COMMAND')
    # query.command_line('open valve', '4. MISSING ID')
    # query.command_line('open valve wrong-id', '5. WRONG ID SYNTAX')
    # query.command_line('wrong-comm wrong-elem wrong-id', '6. WRONG INPUT PHRASE')
    # query.command_line('open valve MSLK-HAOS0-UNDF-MB-00-01', '7. WRONG ID FOR ATTRIBUTE')
    # query.command_line('clean surface OF tool MSLK-HAOS0-UNDF-MB-00-01', '8. WRONG ID FOR ENTITY')
    # query.command_line('connect hook HOOK-SHANK-PULL-MB-FE-07', '9. INCOMPLETE INPUT FOR GIVEN COMMAND')

    #      ╭───────────────────────╮
    # ━━━━━┥ SECTION - FINAL TESTS ┝━━━━━━━━━━━━━━━┥╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲╲┝━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #      ╰───────────────────────╯

    start_time = time.time()

    """
    query.command_line('open valve MECH-VALVE-TURN-UN-IN-11')
    query.command_line('open valve MECH-VALVE-TURN-UN-HD-10')
    query.command_line('apply-torque-on interface OF valve MECH-VALVE-TURN-UN-IN-11')
    query.command_line('clean surface OF rov-panel SUBS-ROVPN-UNDF-FX-HD-01')
    query.command_line('clean interface OF valve MECH-VALVE-TURN-UN-IN-11')
    query.command_line('operate mechanism OF tool TOOL-CLAMP-MANU-AT-UN-03')
    query.command_line('cut steel-wire-rope1 OF vessel SHIP-VESSL-UNDF-MB-00-17')
    query.command_line('cut steel-wire-rope1 OF AHTS-vessel-winch EQPT-WINCH-AHTS-MB-00-17')
    query.command_line('plug connector CONN-ELECT-PUSH-MB-HD-01 AT interface INTF-RCELE-SLID-FX-00-21')
    
    """
    end_time = time.time()
    execution_time_ms = (end_time - start_time) * 1000

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    print(box.c1(f'(END OF SITUATION AWARENESS PROCEDURE IN) > {execution_time_ms:.2f} ms', tab=5, division=True))

    print(color.e10("SAM - Situation Awareness Model - Copyright (C) 2023 Carlos E M Souza.\n"
                    "This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.\n"
                    "This is free software, and you are welcome to redistribute it under certain conditions;\n"
                    " type `show c' for details."))
