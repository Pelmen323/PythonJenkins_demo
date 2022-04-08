import glob
import re
from test_classes.generic_test_class import FileOpener, DataCleaner
from core.runner import TestRunner
FILES_TO_SKIP = ['localisation', 'interface', 'gfx', 'map', 'common\\units', 'names']


def replace_string(filename, pattern, replace_with, encoding="utf-8"):
    text_file = FileOpener.open_text_file(filename, lowercase=False)
    text_file_fixed = re.sub(pattern=pattern, repl=replace_with, string=text_file)

    with open(filename, 'w', encoding=encoding) as text_file_write:
        text_file_write.write(text_file_fixed)


def apply_linting(filename, encoding="utf-8"):
    replace_string(filename=filename, pattern='(?<=[\\w_\\"=\\{\\}])  (?=[\\w_\\"=\\{\\}])', replace_with=' ', encoding=encoding)  # Remove any doublespaces
    replace_string(filename=filename, pattern='=\\b', replace_with='= ', encoding=encoding)                     # Add spaces between symbol and =
    replace_string(filename=filename, pattern='\\b=', replace_with=' =', encoding=encoding)                     # Add spaces between symbol and =
    replace_string(filename=filename, pattern=' \\n', replace_with='\\n', encoding=encoding)                    # Remove trailing whitespaces
    replace_string(filename=filename, pattern='\\{(?=[\\w_\\"=])', replace_with='{ ', encoding=encoding)        # Add spaces between symbol and {
    replace_string(filename=filename, pattern='(?<=[\\w_\\"=])\\}', replace_with=' }', encoding=encoding)       # Add spaces between symbol and }
    replace_string(filename=filename, pattern='(?<=[^\\n])\\Z', replace_with='\\n', encoding=encoding)          # Add last line if file is missing
    replace_string(filename=filename, pattern='[ \t]+$', replace_with="", encoding=encoding)                    # Remove last line spaces


def lint_kaiserreich(username, mod_name):
    runner = TestRunner(username, mod_name)
    filepath_common = f'{runner.full_path_to_mod}common\\'
    filepath_events = f'{runner.full_path_to_mod}events\\'
    filepath_unit_names_divisions = f'{runner.full_path_to_mod}common\\units\\names_divisions\\'
    filepath_unit_names_ships = f'{runner.full_path_to_mod}common\\units\\names_ships\\'
    print(filepath_common)
    for filename in glob.iglob(filepath_common + '**/*.txt', recursive=True):
        if DataCleaner.skip_files(files_to_skip=FILES_TO_SKIP, filename=filename):
            continue
        apply_linting(filename=filename)

    for filename in glob.iglob(filepath_events + '**/*.txt', recursive=True):
        apply_linting(filename=filename, encoding="utf-8-sig")

    for filename in glob.iglob(filepath_unit_names_divisions + '**/*.txt', recursive=True):
        apply_linting(filename=filename, encoding="utf-8-sig")

    for filename in glob.iglob(filepath_unit_names_ships + '**/*.txt', recursive=True):
        apply_linting(filename=filename, encoding="utf-8-sig")


if __name__ == '__main__':
    lint_kaiserreich(username="VADIM", mod_name="Kaiserreich Dev Build")
