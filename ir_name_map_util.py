import os
import sys
import json
import xml.etree.ElementTree as ET
from collections import defaultdict


def get_json_name_map(model_path_before, model_path_after, output_path):
    attrs_to_check = ['type']
    attr_to_map = 'name'

    root_before = ET.parse(model_path_before).getroot()
    root_after = ET.parse(model_path_after).getroot()

    layers_before = root_before[0]
    layers_after = root_after[0]
    assert len(layers_before) == len(layers_after),\
            f'Amount of layer before ({len(layers_before)} is not match amount of layers after ({len(layers_after)})'

    result = {}
    for idx, (l_before, l_after) in enumerate(zip(layers_before, layers_after)):
        before_name = l_before.get(attr_to_map)
        after_name = l_after.get(attr_to_map)
        for attr in attrs_to_check:
            before_attr = l_before.get(attr)
            after_attr = l_after.get(attr)
            assert before_attr == after_attr, \
                    f'for layer {before_name} -> {after_name} attribute {attr} does not match:\n'\
                    f'{before_attr} vs {after_attr}'
        result[before_name] = after_name

    print(f'Saving results to {output_path}')
    with open(output_path, 'w') as f:
        f.write(json.dumps(result))


def map_names(path_to_names, path_to_map, output_path):
    with open(path_to_map, 'r') as f:
        name_map = json.loads('\n'.join(f.readlines()))
    with open(path_to_names) as f:
        names = f.read().splitlines()
    result = []
    for name in names:
        result.append(name_map[name])
    with open(output_path, 'w') as f:
        f.writelines(result)


def get_ignored_scope_by_pattern(model_path, pattern_path, output_path):
    layers = ET.parse(model_path).getroot()[0]
    with open(pattern_path, 'r') as f:
        patterns = json.loads('\n'.join(f.readlines()))

    conf_idx_section = 'idx'
    conf_idx_selection = 'idxs_selection'
    conf_num_matches = 'num_matches'
    conf_pattern_section = 'pattern'
    check_attr = 'type'
    target_attr = 'name'
    matches = defaultdict(list)
    for pattern_name, pattern_info in patterns.items():
        pattern = pattern_info[conf_pattern_section]
        for idx, layer in enumerate(layers):
            for pattern_idx, pattern_elem in enumerate(pattern):
                if layers[idx + pattern_idx].get(check_attr) not in pattern_elem:
                    break
            else:
                matches[pattern_name].append([l.get(target_attr) for l in layers[idx:idx+len(pattern)]])

    print('Match stats:')
    for name, m in matches.items():
        ref_matches = patterns[name][conf_num_matches]
        print(f'{name}: collected={len(m)}, ref={ref_matches}')
        assert len(m) == ref_matches

    if conf_idx_section in pattern_info:
        res = []
        for pattern_name, pattern_info in patterns.items():
            _res = []
            for match in matches[pattern_name]:
                _res.append(match[pattern_info[conf_idx_section]])
            if conf_idx_selection not in pattern_info:
                res.extend(_res)
            else:
                idxs = pattern_info[conf_idx_selection]
                res.extend([_res[idx] for idx in idxs])
                print(f'select indexes {idxs} from {pattern_name} pattern')
        matches = res
    with open(output_path, 'w') as f:
        f.writelines(json.dumps(matches))


if __name__ == '__main__':
    options = ['gen', 'map', 'pattern']
    if len(sys.argv) == 1 or sys.argv[1] not in options:
        print(f'options: {options}')
        exit()
    if sys.argv[1] == options[0]:
        get_json_name_map(*sys.argv[2:])
    if sys.argv[1] == options[1]:
        map_names(*sys.argv[2:])
    if sys.argv[1] == options[2]:
        get_ignored_scope_by_pattern(*sys.argv[2:])
    print('Done!')
