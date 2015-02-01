# coding=utf-8
import os
import copy
import argparse

from import_sorter_libs import std_lib_modules


def parse_args():
    """Preparing & parsing arguments"""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '-A', '--all_files', type=bool, default=False, const=True, nargs='?',
        help=u'Run script on all *.py files in current directory.')
    parser.add_argument(
        '-f', '--files', metavar='files', type=str, default='', nargs='+',
        help=u'Run script on specified file.')
    return parser.parse_args()


def get_file_imports(path):
    imports = []
    pos = 0
    start_pos = None
    last_import_position = 0
    non_imports = []
    try_block = []
    with open(path, mode='r') as fts:
        while True:
            file_pos = fts.tell()
            line = fts.readline()
            if _is_import_line(line):
                imports.append(line)
                if start_pos is None:
                    start_pos = pos
                last_import_position = pos
            pos += 1
            if line.split() and line.split()[0] in ['def', 'class']:
                break
            if file_pos == fts.tell():
                break
            if 'try:' in line:
                try_block.append(line)
                #pos += 1
                while True:
                    line = fts.readline()
                    pos += 1
                    if line.strip() in ['except:', 'finally:'] or line.startswith(' '):
                        try_block.append(line)
                    else:
                        last_import_position = pos
                        break
    return (imports, start_pos, last_import_position, try_block)


def _is_import_line(line):
    if line.split() and not line.startswith(' '):
        line_prefix = line.split()[0]
        if line_prefix in ['import', 'from']:
            return True
    return False


def get_beautiful_imports(all_imports, non_imports, try_block):
    std_imports = get_standard_imports(all_imports)
    all_imports = list(set(all_imports) - set(std_imports))
    local_imports = get_third_party_imports(all_imports)
    third_party_imports = set(all_imports) - set(std_imports) - set(
                                                               local_imports)

    ok_imports = get_import_the_right_way(std_imports, third_party_imports,
                                         local_imports, non_imports, try_block)
    return ok_imports


def get_from_and_import_separately(imports):
    from_imports = []
    import_imports = []
    for import_ in imports:
        if import_.split() and import_.split()[0] == 'from':
            from_imports.append(import_)
        else:
            import_imports.append(import_)
    import_imports.extend(from_imports)
    return import_imports


def get_import_the_right_way(std_imports, third_party_imports, local_imports, non_imports, try_block):
    std_imports = sorted(std_imports, key=len)
    std_imports = get_from_and_import_separately(std_imports)
    third_party_imports = sorted(third_party_imports, key=len)
    third_party_imports = get_from_and_import_separately(third_party_imports)
    local_imports = non_imports + sorted(local_imports, key=len) + try_block
    local_imports = get_from_and_import_separately(local_imports)
    if std_imports and (third_party_imports or local_imports):
        std_imports.append('\n')
    if third_party_imports and local_imports:
        third_party_imports.append('\n')
    return std_imports + third_party_imports + local_imports

def get_standard_imports(all_imports):
    imports = []
    for x in all_imports:
        mod_name = get_module_name(x)
        if mod_name in std_lib_modules:
            imports.append(x.lstrip())
    return imports

def get_third_party_imports(all_imports):
    imports = []
    ctm_imports = get_curent_dir_modules()
    try:
        ctm_imports.remove('modules')
    except ValueError:
        pass
    for x in all_imports:
        mod_name = get_module_name(x)
        if mod_name in ctm_imports or 'security' in x:
            imports.append(x.lstrip())
    return imports

def get_module_name(mod_import):
    import_separated = mod_import.split()
    import_prefix = import_separated[0]
    mod = import_separated[1]
    if import_prefix == 'from':
        if '.' in mod:
            mod_name = mod.split('.')[0]
        else:
            mod_name = mod
    else:
        mod_name = mod
    return mod_name

def get_curent_dir_modules():
    a_dir = os.getcwd()
    dir_mods = os.listdir('.')
    modules = []
    for mod in dir_mods:
        if not os.path.isdir(mod) and len(mod.split('.')) == 2 and mod.split('.')[1] == 'py':
            modules.append(mod.split('.')[0])
    while True:
        if '__init__.py' not in os.listdir(a_dir):
            break
        a_dir = '/'.join(os.getcwd().split('/')[:-1])
    return modules + [name for name in os.listdir(a_dir)
                if os.path.isdir(os.path.join(a_dir, name)) and '.' not in name]

def get_files_to_sort(files=None, recursive=True):
    if files:
        return files
    else:
        path = os.getcwd()
        result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(path)
                  for f in filenames if os.path.splitext(f)[1] == '.py'
                  and '__' not in os.path.splitext(f)[0] and 'modules' not in dp]
    return result

def get_non_imports(path, start_pos, end_pos):
    non_imports = []
    pos = 0
    with open(path, mode='r') as fts:
        while True:
            file_pos = fts.tell()
            line = fts.readline()
            if pos == end_pos or (line.split() and line.split()[0] in ['def', 'class']):
                break
            if pos >= start_pos and _is_non_import(line):
                non_imports.append(line)
            pos += 1
    return non_imports

def _is_non_import(line):
    return (line.split()
            and line.split()[0] not in ['import', 'from']
            and '#' not in line
            and line.strip() not in ['try:', 'except:', 'finally:']
            and not (line.startswith('"""') or line.startswith("'''"))
    )

def main():
    nspace = parse_args()
    files_to_sort = get_files_to_sort(nspace.files)

    for file_path in files_to_sort:
        imports_, start_pos, end_pos, try_block = get_file_imports(file_path)
        non_imports = get_non_imports(file_path, start_pos, end_pos)
        beautiful_imports = get_beautiful_imports(
            imports_, non_imports, try_block)
        with open(file_path, mode='r') as fts:
            all_lines = fts.readlines()
        with open(file_path, mode='w') as fts:
            if beautiful_imports:
                all_lines[start_pos:end_pos + 1] = beautiful_imports
                fts.writelines(all_lines)


if __name__ == '__main__':
    main()


"""
TODO:
Hight priority:
- multi-line imports with commas or brackets
- make sure std_lib modules list is complete
Low priority:
- expand file paths (e.g. ~/file to /home/user/file)
- option to collapse all imports from ... into one
- line length checking
- checking if two blank lines between class and last import

FIXED:
+ imports first, later from

FIX:
- webapp2_extras recognized as local module, but webapp2_extras.auth is ok (in
services/sync_service.py is recognized ok, but not in models/user.py)
- module cgi not recognized as std_lib module
- 'from testcase_534 import TestCase534' recognized as third party module
"""