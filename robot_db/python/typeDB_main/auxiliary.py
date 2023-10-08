"""
                Project MOSASAUR - auxiliary.py

[MO]del-based [S]ystem [A]pplied to [S]ubsea [AU]tonomous [R]obotics

Auxiliary file for the Situation Awareness Model (SAM) prototype applied
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

from project.robot_db.python.typeDB_main.color_text import Color, Box
import csv
import datetime
import pprint

color = Color()
box = Box()


class ComplianceError(Exception):
    pass


class LocationError(Exception):
    pass


def find_paths(self, d, leaf_key, current_path=None):
    if current_path is None:
        current_path = []
    paths = []
    for key, value in d.items():
        new_path = current_path + [key]
        if key == leaf_key:
            paths.append(new_path)
        elif isinstance(value, dict):
            sub_paths = self.find_paths(value, leaf_key, new_path)
            paths.extend(sub_paths)
    return paths


def concept_map_func(iterator, var):
    result_dict = {}
    for cmap in iterator:
        d = cmap.map()
        for k in d.keys():
            concept = f'{d[k].as_type().get_label()}'
            result_dict[concept] = var
    return result_dict


def concept_dict(db_schema):
    lines = list(filter(lambda l: l.strip() and not l.startswith('//'), db_schema.split('\n')))
    concepts_dict = {'entity': [line.split()[0] for line in lines if 'sub entity' in line],
                     'attribute': [line.split()[0] for line in lines if 'sub attribute' in line],
                     'relation': [line.split()[0] for line in lines if 'sub relation' in line]}
    return concepts_dict


def csv_to_dict_list(i):
    with open(i['data_path'] + ".csv") as csv_file:
        csv_reader = csv.DictReader(csv_file, skipinitialspace=True)
        dict_list = [row for row in csv_reader]
    return dict_list


def match_query(tx, q):
    return tx.query().match(q)


def taxonomy_relation(c_name, a_name, target_element, target_id, relation_name, transaction):

    id_type = find_type(transaction, target_id).split(':')[1]

    id_q0 = f'match '
    id_q1 = f'$x isa {c_name}, '
    id_q2 = f'has {a_name} "{target_element}", '
    id_q3 = f'has {id_type} "{target_id}"; '
    id_q4 = f'$r ($r1:$x, $r2:$y) isa {relation_name}; get $y, $r1, $r2;'

    def get_relation():
        id_list = list(match_query(transaction, id_query))
        list_teste = []
        if id_list:
            x = target_element
            for i in id_list:
                y = i.map().get('y').as_entity().get_type().get_label().name()
                r1 = i.map().get('r1').as_role_type().get_label().name()
                r2 = i.map().get('r2').as_role_type().get_label().name()
                if r1 != 'role' and r2 != 'role':
                    dict_teste = {x: r1, y: r2}
                    list_teste.append(dict_teste)
        return list_teste

    if c_name == target_element:
        id_query = id_q0 + id_q1 + id_q3 + id_q4
        dict_final = get_relation()
    else:
        id_query = id_q0 + id_q1 + id_q2 + id_q3 + id_q4
        dict_final = get_relation()
    return dict_final


def determine_data_type(value):
    """
    This function receives an attribute value and returns the type of data of the element
    :param value: typeDB attribute value
    :return: the attribute value in the correct format: long, double, boolean, string or date-time
    """
    # Check for double representation
    try:
        test_value = float(value)
        if test_value.is_integer():
            return int(test_value)
        else:
            return float(test_value)
    except ValueError:
        pass
    # Check for date-time representation
    date_formats = ["%Y-%m-%d", "%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f"]
    for date_format in date_formats:
        try:
            date_obj = datetime.datetime.strptime(value, date_format)
            return date_obj.astimezone()
        except ValueError:
            pass
    # Check for long representation
    try:
        int_value = int(value)
        if -9223372036854775808 <= int_value <= 9223372036854775807:
            return int(value)
    except ValueError:
        pass
    # Check for boolean representation
    if value.lower() == 'true' or value.lower() == 'false':
        return "boolean"
    return 'string'


def query_builder(q, n, v, c_type=None, k=None):
    k = '' if k is None else k
    data_type = determine_data_type(v)
    if c_type == 'entity':
        if data_type == 'string':
            q += f' has {n}{k} "{v}"'
        else:
            q += f' has {n}{k} {data_type}'
    else:
        if data_type == 'string':
            q += f' $v{n}{k} "{v}";'
        else:
            q += f' $v{n}{k} {data_type};'
    return q


def element_type(transaction, element):

    # element_id = element[1] if isinstance(element, list) else None
    element = element[0] if isinstance(element, list) else element
    concept_type = find_type(transaction, element).split(':')[0]
    label = find_type(transaction, element).split(':')[1]

    if concept_type == 'attribute':
        query = f'match $y isa entity, has {label} "{element}"; get $y;'
        element_list = list(match_query(transaction, query))

        if not element_list:
            return label, concept_type
        else:
            target_type = element_list[0].map().get('y').as_entity().get_type().get_label().name()
            return label, target_type
    else:
        return label, concept_type


def goal_list(tx, a_value, a_name, e_type=None):
    if e_type == 'attribute':
        query = f'match $x "{a_value}"; get $x;'
        q = list(tx.query().match(query))
        q_list = []
        for i in q:
            q_list.append(i.map().get('x').as_attribute().get_type().get_label().name())
    else:
        query = f'match $x isa thing, has {a_name} "{a_value}"; get $x;'
        q = list(tx.query().match(query))
        q_list = []
        for i in q:
            q_list.append(i.map().get('x').as_entity().get_type().get_label().name())
    return q_list


def pair_element_id(e, eid, d_phrase):
    try:
        element = d_phrase[e]
        if element:
            pair_dict = {}
            try:
                element_id = d_phrase[eid]
                if element_id and element:
                    pair_dict[f'pair-{e.split("-")[1]}'] = list((element, element_id))
                    return pair_dict
                else:
                    pair_dict[e] = element
                    return pair_dict
            except KeyError:
                pair_dict[e] = element
                return pair_dict
        else:
            raise KeyError
    except KeyError:
        return None


def phrase2dict(transaction, phrase):

    # phrase_list = [(n, w) for n, w in enumerate(phrase.split())]
    phrase_list = [w for w in phrase.split()]
    p_dict = {}
    i0 = 1
    counter = {'element': 0, 'pair': 0}

    def check_for_tag(p, tag, e1, c):
        """
        This function checks if the element is a tag-number, and in affirmative case,
        it adds it to the dictionary generating a pair with the previous element
        :param p: phrase from the phrase_list
        :param tag: tag-number
        :param e1: element-1 or first element of pair
        :param c: counter
        :return: dictionary with the tag-number
        """
        tn = tag.upper()
        ex = None
        index = 1
        v1 = c['element']                                       # counts number of elements
        v2 = c['pair']                                          # counts number of pairs

        id_type = find_type(transaction, tn)

        # print(color.neon([id_type, tn.lower()]))              # TO BE IMPLEMENT LATER (TAG OR ELEMENT-TYPE)

        if id_type is not None:

            if id_type.split(":")[1] != 'tag-number':           # if id_type is not a tag-number
                index += c['element']                           # starts counting from the first element
                p_dict[f'element-{index}'] = e1
                c.update({'element': v1 + 1})
            else:                                               # if id_type is a tag-number
                if e_type.split(":")[0] == 'attribute':         # if the element is an attribute
                    query = f'match $x isa thing, ' \
                            f'has element-type "{e1}", ' \
                            f'has tag-number "{tn}"; get $x;'
                    q_tag = f'match $x isa thing, ' \
                            f'has element-type "{e1}", ' \
                            f'has tag-number $t; get $t;'
                else:                                           # if the element is an entity
                    query = f'match $x isa {e1}, ' \
                            f'has tag-number "{tn}"; get $x;'
                    q_tag = f'match $x isa {e1}, ' \
                            f'has tag-number $t; get $t;'

                q = list(transaction.query().match(query))
                if not q:                                       # if the tag-number is not found in database
                    if ex == 'exception':                       # here ask for the element correct ID
                        # print(color.yellow(tn))
                        raise IndexError                        # raise IndexError

                    else:                                       # when the tag-number is wrong but exists in database
                        print(box.red(f'ATTENTION ! > TAG NUMBER ({tn}) IS INCORRECT !', 'function check_for_tag'))
                        # q_tag = f'match $x isa {e1}, has tag-number $t; get $t;'
                        # print(color.green(q_tag))
                        print(color.e6('\u0009' * 2 + '\u25B6 LIST OF AVAILABLE TAG-NUMBERS:'))
                        it_tag = transaction.query().match(q_tag)
                        answer_list = []
                        for t in it_tag:
                            answer_list.append(t.map().get('t').as_attribute().get_value())

                        print(box.e6(answer_list, '', 2, True))
                        index_tag = int(input(color.e7(f'PROVIDE CORRECT TAG-NUMBER FROM THE LIST '
                                                       f'(1 - {len(answer_list)}) \u25B6 ')))
                        try:
                            int(index_tag)
                            new_tag = (answer_list[index_tag - 1])
                            new_p = p.replace(tn, new_tag)
                            check_for_tag(new_p, new_tag, e1, c)
                        except ValueError:
                            print('MUST BE A NUMBER')
                            check_for_tag(p, tag, e1, c)
                else:
                    index += (v1 + v2)
                    p_dict[f'pair-{index}'] = [e1, tn]
                    c.update({'pair': v1 + 1})
        else:
            prep_list = ['to', 'at', 'linked-to', 'of']
            # if the tag-number is not found in database
            if tn in prep_list:
                print(box.neon('OK, ---------------> remove latter in check_for_tag', f'PREP - {tn.upper()}'))
                index += c['element']
                p_dict[f'prep-{index}'] = tn.upper()
                c.update({'element': v1 + 1})

            print(box.e8('ATTENTION \u26A0\u0009 TRANSACTION CLOSED', '(RESETING) valid_input_phrase'))
            return phrase2dict(transaction, p)

    for i, e in enumerate(phrase_list):

        e_type = find_type(transaction, e)                      # finds the type of the element

        if e_type is None:
            p_dict = {}
        else:
            # print(e_type.split(":")[1])
            # Verify if the element is a role or a preposition
            if e_type.split(":")[1] == 'role':
                p_dict[f'prep-{i0}'] = e
                i0 += 1
            # Verify if the element is a command
            if e_type.split(":")[1] in ['command-type', 'function']:
                p_dict['command'] = e
            # Verify if the element is an attribute
            if e_type.split(":")[1] == 'element-type' or e_type.split(":")[1] == e:

                try:                                            # Verify if the next element is an id
                    tag_number = phrase_list[i + 1]
                    check_for_tag(phrase, tag_number, e, counter)
                except IndexError:                              # If there is no id next, raise a IndexError
                    print(box.e2(f'ATTENTION ! > ELEMENT ({e}) ID NOT FOUND', 'function phrase2dict'))
                    # THIS FIRST CONDITION SEEMS NOT BEING USED...
                    if i + 1 < len(phrase_list):
                        tag_number = input(f'{color.e5("PROVIDE ID (TAG-NUMBER) OR PREPOSITION")} \u25B6 ')
                        new_phrase = phrase.replace(phrase_list[i + 1], tag_number)
                        check_for_tag(new_phrase, tag_number, e, counter)
                    else:
                        tag_number = input(f'{color.e5("PROVIDE ID (TAG-NUMBER) OR PREPOSITION")} \u25B6 ')
                        new_phrase = phrase + ' ' + tag_number
                        check_for_tag(new_phrase, tag_number, e, counter)
                    phrase = new_phrase
                    (box.blue(phrase, 'function phrase2dict - (IndexError)'))
    return p_dict


# VERY IMPORTANT FUNCTION
def find_type(tx, element):

    prep_position_list = ['TO', 'FROM', 'AT', 'IN', 'ON', 'OF', 'INTO']
    # prep_part_list = ['OF', 'LINKED-TO']
    prep_part_list = ['OF']

    # element = element.lower()     # to be implemented later... not only tag-number
    try:
        test_type = tx.concepts().get_thing_type(element)
        if test_type is None:
            if element.upper() in prep_position_list or element in prep_part_list:
                return f'{element}:role:teste'
            else:
                try:
                    a_query = f'match $x "{str(element)}"; get $x;'
                    iterator = next(match_query(tx, a_query))
                    test_type = iterator.get('x').as_attribute().get_type()
                    return f'attribute:{test_type.get_label()}'
                except StopIteration:
                    r_query = f'match $r relates {element.lower()}; get $r;'
                    relation = next(match_query(tx, r_query)).get('r').get_label()
                    return f'{element.lower()}:role:{relation}'

        elif test_type.is_attribute_type():
            return f'attribute:{test_type.get_label()}'
        elif test_type.is_entity_type():
            return f'entity:{test_type.get_label()}'
        elif test_type.is_relation_type():
            return f'relation:{test_type.get_label()}'

    except Exception as e:
        print(box.e1('\u26A0\u0009 > (ATTENTION WRONG INPUT)', f'{str(e).split("Read:")[1]}'))
        return None


def get_relations(tx, elem, elem_type, tag, pair2=None, prep1=None):

    relations_list = ['forming', 'assembling', 'composing', 'linking', 'positioning']

    coordinates = []
    location_pair1 = []
    location_pair2 = []

    if tag:
        qrx_a = f'match $x isa {elem}, has tag-number "{tag}"; '
        qrx_b = f'match $x isa {elem_type[1]}, has {elem_type[0]} "{elem}", has tag-number "{tag}"; '
    else:
        qrx_a = f'match $x isa {elem}; '
        qrx_b = f'match $x isa {elem_type[1]}, has {elem_type[0]} "{elem}"; '

    # thing = '$z sub $t; {$t type entity;} or {$t type relation;} or {$t type attribute;};'
    qry = '$y has $t; {$t isa tag-number;} or {$t isa element-type;}; '
    qrw = '$w has $s; {$s isa tag-number;} or {$s isa element-type;}; '
    # qr_xy = '$rxy($rx:$x, $ry:$y) isa relation; '    # KEEP JUST IN CASE
    qr_xy = '$rxy($rx:$x, $ry:$y) isa relation; ' \
            'not {$rx type relation:role;}; not {$ry type relation:role;}; '
    q_get = 'get $x, $rx, $y, $ry, $rxy, $t;'

    # $rz type relation:role;

    if pair2:   # If the pair2 element is provided
        e_type2 = find_type(tx, pair2[0])

        if prep1:
            if prep1.lower() == 'of' and elem == 'surface':
                qrx_a = f'match $x isa {elem}, has tag-number "{pair2[1]}"; '

        if pair2[1] == tag:
            qrx_a = 'match '

        qze = f'$z isa {pair2[0]}, has tag-number "{pair2[1]}"; '
        qza = f'$z isa entity, has element-type "{pair2[0]}", has tag-number "{pair2[1]}"; '
        # qr_xz = '$rxz($r2x:$x, $rz:$z) isa relation; '       # KEEP JUST IN CASE

        qr_xz = '$rxz($r2x:$x, $rz:$z) isa relation; ' \
                'not {$r2x type relation:role;}; not {$rz type relation:role;}; '
        # qr_wz = '$rwz($r2z:$z, $rw:$w) isa relation; '       # KEEP JUST IN CASE
        qr_wz = '$rwz($r2z:$z, $rw:$w) isa relation; ' \
                'not {$r2z type relation:role;}; not {$rw type relation:role;}; '

        qr_xz_wz = qr_xz + qr_wz

        q_get2 = 'get $x, $y, $z, $rx, $r2x, $r2z, $rw, $ry, $rz, $rxy, $rwz, $rxz, $t, $s;'

        if elem_type[1] == 'entity':
            if e_type2.split(':')[0] == 'entity':
                query = qrx_a + qry + qrw + qze + qr_xy + qr_xz_wz + q_get2
            else:
                query = qrx_a + qry + qrw + qza + qr_xy + qr_xz_wz + q_get2
        else:
            if e_type2.split(':')[0] == 'entity':
                query = qrx_b + qry + qrw + qze + qr_xy + qr_xz_wz + q_get2
            else:
                query = qrx_b + qry + qrw + qza + qr_xy + qr_xz_wz + q_get2
    else:
        query = qrx_a + qry + qr_xy + q_get if elem_type[1] == 'entity' else qrx_b + qry + qr_xy + q_get

    # To find possible current locations of connector or tool
    if elem == 'connector' or elem == 'tool':

        ql1 = f'$lm isa landmark-point, has name $ln, has latitude $lt, has longitude $lg, has water-depth $wd; '
        ql2 = f'$l(currently-located-at:$x, location:$lm) isa locating; '
        qlg = f'get $lm, $ln, $lt, $lg, $wd;'
        query_l = qrx_a + ql1 + ql2 + qlg if elem_type[1] == 'entity' else qrx_b + ql1 + ql2 + qlg
        iterator_l = list(match_query(tx, query_l))
        for loc in iterator_l:
            # lm = loc.map().get('lm').get_type().get_label().name()
            ln = loc.map().get('ln').as_attribute().get_value()
            lt = loc.map().get('lt').as_attribute().get_value()
            lg = loc.map().get('lg').as_attribute().get_value()
            wd = loc.map().get('wd').as_attribute().get_value()

            coordinates.append(f'name: {ln} | latitude: {lt} | longitude: {lg} | water-depth: {wd}')

    l_dict = {}
    rxy_dict = {}
    rxz_dict = {}
    rwz_dict = {}

    iterator_r = list(match_query(tx, query))

    def retrieve_relations(r, e1, tgl, tgn, re1, re2, r_dict):
        if r in relations_list:
            if r not in r_dict:
                r_dict[r] = {}
            if re1 != 'role' and re2 != 'role':
                v = [e1, tgl, tgn, re1]
                if r in r_dict:
                    if isinstance(r_dict[r], list):
                        if v not in r_dict[r]:
                            match_et = list(filter(lambda lz: 'element-type' in lz[1], r_dict[r]))
                            if match_et:
                                r_dict[r].remove(match_et[0])
                            if tgl == 'tag-number':
                                r_dict[r].append(v)
                    else:
                        r_dict[r] = [v]
        return r_dict

    def retrieve_location(target, e_role, t_role, t_tag, t_type, l_d, l_pair):
        if target == 'equipment' or target == 'vessel' or target == 'storage':
            if e_role != 'role' and t_role != 'role':
                if t_type == 'tag-number':
                    l_d[target] = [t_role, t_tag]               # [role, tag-number]
                    if [target, t_tag] not in l_pair:
                        l_pair.append([target, t_tag])          # [equipment, tag-number]

    for i in iterator_r:

        x = i.map().get('x').get_type().get_label().name()
        y = i.map().get('y').get_type().get_label().name()
        rxy = i.map().get('rxy').as_relation().get_type().get_label().name()
        rx = i.map().get('rx').as_role_type().get_label().name()
        ry = i.map().get('ry').as_role_type().get_label().name()
        t = i.map().get('t').as_attribute().get_value()
        tt = i.map().get('t').as_attribute().get_type().get_label().name()

        retrieve_location(y, rx, ry, t, tt, l_dict, location_pair1)

        if pair2:
            z = i.map().get('z').get_type().get_label().name()
            w = i.map().get('w').get_type().get_label().name()
            rz = i.map().get('rz').as_role_type().get_label().name()
            r2x = i.map().get('r2x').as_role_type().get_label().name()
            rw = i.map().get('rw').as_role_type().get_label().name()
            r2z = i.map().get('r2z').as_role_type().get_label().name()
            s = i.map().get('s').as_attribute().get_value()
            ss = i.map().get('s').as_attribute().get_type().get_label().name()
            rxz = i.map().get('rxz').as_relation().get_type().get_label().name()
            rwz = i.map().get('rwz').as_relation().get_type().get_label().name()

            retrieve_location(w, r2z, rw, s, ss, l_dict, location_pair2)

            # Retrieve all the relations dictionaries
            rxz_dict = retrieve_relations(rxz, x, tt, tag, r2x, rz, rxz_dict)
            rwz_dict = retrieve_relations(rwz, w, ss, s, rw, rw, rwz_dict)

        rxy_dict = retrieve_relations(rxy, y, tt, t, ry, rx, rxy_dict)

    f_rxy_dict = filter_relations(rxy_dict)
    f_rxz_dict = filter_relations(rxz_dict)
    f_rwz_dict = filter_relations(rwz_dict)

    return f_rxy_dict, f_rxz_dict, f_rwz_dict, location_pair1, location_pair2, l_dict, coordinates


def filter_relations(p_dict):
    for k in p_dict.keys():
        p_dict[k] = list(map(lambda i: f'{i[0]} {i[2]} ▶ {i[3]}', p_dict[k]))
    return p_dict


def check_command_compliance(c, e, use_tool, s_class, g_list):
    if use_tool:
        print(box.c3(f'Check compliance > Can {c} {e} ?', f'COMPLIANT ▶ REQUIRES TOOL', 2))
    else:
        try:
            check1 = bool(list(filter(lambda item: str(e) in item, g_list)))
            check2 = bool(list(filter(lambda item: str(s_class) in item, g_list)))
            if check1 or check2:
                print(box.c3(f'Check compliance > Can ({c} {e}) ?', 'YES ▶ COMPLIANT', 2))
            else:
                print(box.e3(f'Check compliance > Can ({c} {e}) ?', f'NO ▶ Cannot {c} {e} !', 2))
                raise ComplianceError
        except ComplianceError:
            raise


def link(tx, c, link1, link2, linking=False):
    test = None

    # if link1 is list:
    if isinstance(link1, list):
        q_link1 = f"$l1 isa {link1[0]}, has tag-number '{link1[1]}'; "
    else:
        q_link1 = f"$l1 isa {link1[0]}, "
    if isinstance(link2, list):
        q_link2 = f"$l2 isa {link2[0]}, has tag-number '{link2[1]}'; "
    else:
        q_link2 = f"$l2 isa {link2[0]}, "

    c_query = f"$c isa goal, has command-type '{c}'; "
    r_query = f"(command:$c, link:$l1, link:$l2) isa linking; "
    g_query = f"get $c, $l1, $l2;"
    link_query = f"match " + q_link1 + q_link2 + c_query + r_query + g_query

    iterator = list(match_query(tx, link_query))
    for i in iterator:
        test = i.map().get('l2').as_thing().get_type()
    return color.orange(test)


def find_location(tx, loc_pair):
    tab = '\u0009'
    q1 = f'match '
    q2 = f'$x isa {loc_pair[0]}, has tag-number "{loc_pair[1]}"; '
    q3 = f'$y isa landmark-point, has name $n, has latitude $lat, has longitude $lon, has water-depth $wdp; '
    q4 = f'($x, location:$y) isa locating; '
    q5 = f'get $n, $lat, $lon, $wdp;'
    l_query = q1 + q2 + q3 + q4 + q5
    iterator = list(match_query(tx, l_query))
    if iterator:
        list_parameters = []
        for i in iterator:
            n = i.map().get('n').as_attribute().get_value()
            lat = i.map().get('lat').as_attribute().get_value()
            lon = i.map().get('lon').as_attribute().get_value()
            wdp = i.map().get('wdp').as_attribute().get_value()
            list_parameters.append([n, lat, lon, wdp])
        return list_parameters[0]
    else:
        # print(color.e2(f'{tab * 6}\u25B6 No location found for {loc_pair}'))
        return None


def division_line(text, test=None):
    if test:
        print(color.e1('\n' + " " * 5 + '\u256D' + '\u2500' * (len(text) + 2) + '\u256E'))
        print(color.e1("\u2501" * 5 + '\u2525' + text.center(len(text) + 2) + '\u251D' + "\u2501" * (166 - len(text))))
        print(color.e1(" " * 5 + '\u2570' + '\u2500' * (len(text) + 2) + '\u256F\n'))
    else:
        print(color.c0('\n' + " " * 5 + '\u256D' + '\u2500' * (len(text) + 2) + '\u256E'))
        print(color.c0("\u2501" * 5 + '\u2525' + text.center(len(text) + 2) + '\u251D' + "\u2501" * (166 - len(text))))
        print(color.c0(" " * 5 + '\u2570' + '\u2500' * (len(text) + 2) + '\u256F\n'))