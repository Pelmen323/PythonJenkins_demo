import re
import os

INPUT_FILE_PATH = 'C:\\Users\\' + os.getlogin() + '\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Dev Build\\interface\\kaiserreich\\technology_icons.gfx'
OUTPUT_FILE_PATH = 'C:\\Users\\' + os.getlogin() + '\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Dev Build\\interface\\kaiserreich\\technology_icons.gfx'
HEADER_STR = "### This file is autogenerated. Don't edit it manually. Content is sorted alphabetically. By Pelmen323\n"
INPUT_LIST = [
    ['transport_plane_equipment_1_medium', 'bba_early_transport_plane_medium'],
    ['transport_plane_equipment_2_medium', 'bba_improved_transport_plane_medium'],
    ['transport_plane_equipment_3_medium', 'bba_strategic_airlifter_medium'],
]
SAME_FILE = True


def main(input_list: list[str, str]):
    '''
    This script autogenerates chassis icons based on tank icons
    Input - List
    Input[0] - chassis icon
    Input[1] - tank icon
    Script generates chassis icons for all tags that have relevant tank icons
    '''
    output_list = []

    with open(INPUT_FILE_PATH, 'r', encoding='utf-8') as text_file:
        input_file = text_file.read()

    for item in input_list:
        i = item[0]
        chassis = item[1]
        icon_pattern = 'GFX_..._' + i
        tech_icons = re.findall(icon_pattern, input_file)

        for icon in tech_icons:
            tag = re.findall(r'GFX_(...)_', icon)[0]
            search_result = re.findall('(' + icon + '.*?\n.*?texturefile.*?=.*?"(.*?)"\n\t\})', input_file)[0]
            key = search_result[0]
            icon_path = search_result[1]
            output_str = '\n\tSpriteType = {\n\t\tname = "GFX_' + tag + '_' + chassis + '"\n\t\ttexturefile = "' + icon_path + '"\n\t}'
            if output_str not in input_file:
                if 'GFX_' + tag + '_' + chassis in input_file:
                    print(f'GFX_{tag}_{chassis} is already present, but points to a different texture') 
                output_list.append([key, output_str])

    if SAME_FILE:
        updated_input_file = input_file
        for i in output_list:
            key = i[0]
            value = i[1]
            updated_input_file = updated_input_file.replace(key, key+value)
        with open(OUTPUT_FILE_PATH, 'w', encoding='utf-8') as text_file_write:
            text_file_write.write(updated_input_file)

    else:
        with open(OUTPUT_FILE_PATH, 'w', encoding='utf-8') as text_file_write:
            output_list = sorted(output_list)
            output_file = HEADER_STR + 'spriteTypes = {\n' + ''.join(output_list) + '}\n'
            text_file_write.write(output_file)


if __name__ == '__main__':
    main(INPUT_LIST)
