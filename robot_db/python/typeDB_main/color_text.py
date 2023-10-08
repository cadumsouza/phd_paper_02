"""
                Project MOSASAUR - color_text.py

[MO]del-based [S]ystem [A]pplied to [S]ubsea [AU]tonomous [R]obotics

Cosmetics file for the Situation Awareness Model (SAM) prototype applied
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


from project.robot_db.python.typeDB_main.auxiliary import *


class Color:
    def __init__(self):
        pass

    @staticmethod
    def color(c):
        cor = {
            'e1': "\033[38;5;197m",
            'e2': "\033[38;5;196m",
            'e3': "\033[38;5;160m",
            'e4': "\033[0;31m",
            'e5': "\033[38;5;203m",
            'e6': "\033[38;5;202m",
            'e7': "\033[38;5;208m",
            'e8': "\033[38;5;214m",
            'e9': "\033[38;5;220m",
            'e10': "\033[38;5;226m",
            'e11': "\033[38;5;227m",
            'e12': "\033[38;5;228m",
            'c12': "\033[38;5;22m",
            'c11': "\033[38;5;28m",
            'c10': "\033[38;5;40m",
            'c9': "\033[38;5;46m",
            'c8': "\033[38;5;118m",
            'c7': "\033[38;5;121m",
            'c6': "\033[38;5;123m",
            'c5': "\033[38;5;44m",
            'c4': "\033[38;5;38m",
            'c3': "\033[38;5;31m",
            'c2': "\033[38;5;25m",
            'c1': "\033[38;5;24m",
            'c0': "\033[38;5;23m",
            'white': "\033[0;28m",
            'yellow': "\033[38;5;220m",
            'gold': "\033[0;33m",
            'green': "\033[0;32m",
            'navy': "\033[38;5;27m",
            'blue': "\033[0;34m",
            'cyan': "\033[0;36m",
            'red': "\033[0;31m",
            'neon': "\033[38;5;46m",
            'brow': "\033[38;5;130m",
            'pink': "\033[38;5;219m",
            'violet': "\033[38;5;5m",
            'orange': "\033[38;5;208m",
            'black': "\033[0;30m",
            'gray': "\033[0;90m",
            'd_white': "\033[1;37m",
            'd_yellow': "\033[1;33m",
            'd_green': "\033[1;32m",
            'd_blue': "\033[1;34m",
            'd_cyan': "\033[1;36m",
            'd_red': "\033[1;31m",
            'd_violet': "\033[1;35m",
            'd_black': "\033[1;30m",
            'l_black': "\033[0;90m",
            'l_red': "\033[0;91m",
            'l_green': "\033[0;92m",
            'l_yellow': "\033[0;93m",
            'l_blue': "\033[0;94m",
            'l_violet': "\033[0;95m",
            'l_cyan': "\033[0;96m",
            'l_white': "\033[0;97m",
            'l_orange': "\033[38;5;202m",
            'l_pink': "\033[38;5;219m",
            'l_neon': "\033[38;5;46m",
            'l_brow': "\033[38;5;130m",
            'l_navy': "\033[38;5;27m",
            'l_gold': "\033[38;5;220m",
            'l_gray': "\033[0;37m",
            'off': "\033[1;0m",
            'bg_black': "\033[40m",
            'bg_red': "\033[41m",
            'bg_green': "\033[42m\033[30m",
            'bg_yellow': "\033[43m\033[30m",
            'bg_orange': "\033[48;5;208m\033[30m",
            'bg_blue': "\033[44m\033[30m",
            'bg_navy': "\033[48;5;27m\033[30m",
            'bg_neon': "\033[48;5;46m\033[30m",
            'bg_pink': "\033[45m\033[30m",
            'bg_cyan': "\033[46m\033[30m",
            'bg_white': "\033[47m\033[30m"
        }
        return f'{cor[c]}'

    def create_color_method(self, color_name):
        def color_method(text):
            return self.color(color_name) + f'{text}' + self.color("off")
        return color_method

    def __getattr__(self, color_name):
        return self.create_color_method(color_name)


class Box:
    def __init__(self):
        self.color = Color().color

    def create_color_method(self, color_name):

        def highlight(text):
            return self.color(color_name) + f'{text}' + self.color("off")

        def color_method(text_input, opt='', tab=0, is_list=False, msg1=None, limit=None, division=False):
            text = text_input
            ht = text.split('(')[1].split(')')[0].strip() if '(' in text else None
            opt_h = opt.split('(')[1].split(')')[0].strip() if '(' in opt else None

            h_opt = highlight(opt_h)
            h_text = highlight(ht)

            s = self.color(color_name)
            e = self.color("off")
            cl = len(s) + len(e) if '(' in text else 0
            cl_opt = len(s) + len(e) if '(' in opt else 0

            tab_space = '\u0009' * tab

            if is_list:
                o_length = len(text_input)
                l_text = text_input[:limit]
                modified_list = []
                for i, item in enumerate(l_text):
                    modified_list.append(item)
                    if item:
                        modified_list.append('-')

                # print(modified_list)
                l_text = modified_list
                if l_text:
                    max_text_length = max(map(len, l_text)) + 2
                else:
                    max_text_length = len(l_text) + 2
                    return s + f'{tab_space}\u25B6 NO MATCHES FOUND WITH ' + e + f'[ {opt} ]'

                h_line = "\u2500" * (max_text_length + 3)
                t_line = f'{tab_space}' + s + f'\u256D{h_line}\u256E' + e
                d_line = f'{tab_space}' + s + f'\u251C{h_line}\u2524' + e
                b_line = f'{tab_space}' + s + f'\u2570{h_line}\u256F' + e
                m_line = f'{tab_space}' + s + '\u2502 \u25CB ' + e

                t_opt = f'\u25C0 {msg1}'
                # isa_match = len(l_text)/2

                max_opt_length = len(t_opt) + 2
                for i in range(len(l_text) - 1):
                    if opt == l_text[i]:
                        top_eline = s + f' \u256D{"─" * max_opt_length}\u256E' + e
                        middle_eline = '\u251C\u2500\u2524 ' + e + t_opt.ljust(max_opt_length - 1) + s + '\u2502' + e
                        bottom_eline = s + f' \u2570{"─" * max_opt_length}\u256F' + e
                        if i == 0:
                            print(t_line + top_eline)
                            print(m_line + l_text[i].ljust(max_text_length) + s + middle_eline)
                        else:
                            print(m_line + l_text[i].ljust(max_text_length) + s + middle_eline)
                        if i == len(l_text) - 2:
                            print(b_line + bottom_eline)
                    else:
                        if i == 0:
                            print(t_line)
                            print(m_line + l_text[i].ljust(max_text_length) + s + '\u2502' + e)
                        else:
                            if l_text[i] == '-':
                                if l_text[i - 1] == opt:
                                    print(d_line + s + f' \u2570{"─" * max_opt_length}\u256F' + e)
                                elif l_text[i + 1] == opt:
                                    print(d_line + s + f' \u256D{"─" * max_opt_length}\u256E' + e)
                                else:
                                    print(d_line + '')
                            else:
                                print(m_line + l_text[i].ljust(max_text_length) + s + '\u2502' + e)
                        if i == len(l_text) - 2:
                            print(b_line)
                if limit is not None and limit < o_length:
                    return s + f'{tab_space}\u25B6 Showing: ' + e + \
                        f'{limit}' + s + f' of a total of ' + e + \
                        f'{o_length}' + s + ' items' + e
                else:
                    return s + f'{tab_space}\u25B6 Total items in list: ' + e + f'{int(len(l_text) / 2)}'

            else:
                if division:
                    opt = opt.replace(f'({opt_h})', h_opt)
                    text = text.replace(f'({ht})', h_text)
                    text1 = text.split('> ')[0] if '>' in text else ''
                    text2 = text.split('> ')[1] if '>' in text else text

                    t = f" {text1}" + s + "\u25B6" + e + f" {text2} "

                    horizontal_line = "\u2500" * (len(text1) + len(text2) - cl + 4)
                    horizontal_line2 = "\u2500" * (len(opt) - cl_opt + 2) if opt else 'end list'
                    extra_line1 = f' \u256D{horizontal_line2}\u256E' if opt else ''
                    extra_line2 = f' \u2570{horizontal_line2}\u256F' if opt else ''

                    line1 = ' ' * tab + s + f'\u256D{horizontal_line}\u256E' + extra_line1 + '\n' + e
                    line2 = s + '\u2501' * tab + \
                                '\u2525' + e + t.center(len(text)) + s + '\u251D' + \
                                '\u2501' * (168 - (len(horizontal_line))) + '\n'
                    line3 = ' ' * tab + f'\u2570{horizontal_line}\u256F' + extra_line2 + e
                    return line1 + line2 + line3
                else:
                    opt = opt.replace(f'({opt_h})', h_opt)
                    text = text.replace(f'({ht})', h_text)
                    text1 = text.split('> ')[0] if '>' in text else ''
                    text2 = text.split('> ')[1] if '>' in text else text

                    t = f" {text1}" + s + "\u25B6" + e + f" {text2} "
                    extra_box = '\u2500\u2524 ' + e + opt.center(len(opt) - cl_opt + 0) + s + \
                                ' \u2502' + e if opt else ''

                    horizontal_line = "\u2500" * (len(text1) + len(text2) - cl + 4)
                    horizontal_line2 = "\u2500" * (len(opt) - cl_opt + 2) if opt else 'end list'
                    extra_line1 = f' \u256D{horizontal_line2}\u256E' if opt else ''
                    extra_line2 = f' \u2570{horizontal_line2}\u256F' if opt else ''
                    vl1 = '\u251C' if opt else '\u2502'

                    line1 = f'{tab_space}' + s + f'\u256D{horizontal_line}\u256E' + extra_line1 + '\n' + e
                    line2 = f'{tab_space}' + s + '\u2502' + e + t.center(len(text)) + s + vl1 + extra_box + '\n' + e
                    line3 = f'{tab_space}' + s + f'\u2570{horizontal_line}\u256F' + extra_line2 + e
                    return line1 + line2 + line3

        return color_method

    def __getattr__(self, color_name):
        return self.create_color_method(color_name)
