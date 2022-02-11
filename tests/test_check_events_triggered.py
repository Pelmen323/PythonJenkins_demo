##########################
# Test script to check if "is_triggered_only = yes" events are triggered from somewhere
# If they not - they'll never be triggered
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
from .imports.file_functions import open_text_file
import logging


def test_check_triggered_events(test_runner: object):
    filepath_events = f'{test_runner.full_path_to_mod}events\\'
    filepath_global = test_runner.full_path_to_mod
    filepath_history = f'{test_runner.full_path_to_mod}history\\'
    all_events = []
    triggered_events_id = dict()
    invoked_events_id = []
    
    for filename in glob.iglob(filepath_events + '**/*.txt', recursive=True):
        try:
            text_file = open_text_file(filename)
            text_file = text_file.lower()
        except Exception as ex:
            logging.warning(f'Skipping the file {filename}')
            logging.warning(ex)
            continue
    #1. Get list of all events in events files
        # pattern_matches = re.findall('((?<=\n)country_event.*?\n(.|\n*?)*?\n\})', text_file)
        pattern_matches = re.findall('((?<=\n)country_event = \{.*\n(.|\n*?)*\n\})', text_file)
        if len(pattern_matches) > 0:
            for match in pattern_matches:
                match = match[0]                                            # Counter empty capture groups
                all_events.append(match)

    #2. Get the "triggered only events"
    print(len(all_events))
    for event in all_events:
        # print(event)
        if "is_triggered_only = yes" in event:
            # Extract event ID:
            pattern_matches = re.findall('id = .*', event)
            event_id = pattern_matches[0].strip('\t').strip()                   # Only first match is taken
            if '#' in event_id:
                event_id = event_id[:event_id.index('#')].strip()               # Clean up comments
            event_id = event_id[5:].strip()                                     # Remove "id =" part
            triggered_events_id[event_id] = 0                                   # Default value is set to zero

    #3. Time to roll out - NO HISTORY FILES HERE
    for filename in glob.iglob(filepath_global + '**/*.txt', recursive=True):
        if '\\history\\' in filename: continue
        try:
            text_file = open_text_file(filename)
            text_file = text_file.lower()
        except Exception as ex:
            logging.warning(f'Skipping the file {filename}')
            logging.warning(ex)
            continue
 
        if "country_event =" in text_file:
            #3.0 One-liners w/o brackets
            pattern_matches = re.findall('([\t| ]country_event = ((?!\{).)*\n)', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[0]
                    match = match[16:].strip().strip('}').strip().strip('}').strip()
                    if '#' in match:
                        match = match[:match.index('#')].strip().strip('}').strip()    # Clean up comments
                    invoked_events_id.append(match)
    
            # 3.1 One-liners with brackets
            pattern_matches = re.findall('[\t| ]country_event = \{.*\}', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    event_id_match = re.findall('id = [a-zA-Z0-9\._]*', match)
                    match = ''.join(event_id_match)[4:].strip()
                    invoked_events_id.append(match)


            # 3.2 Multiliners        
            pattern_matches = re.findall('([\t| ]country_event = \{((?!\}).)*\n(.|\n*?)*\n\t*\})', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    if '' in match:
                        match = match[0]                                            # Counter empty capture groups
                    event_id_match = re.findall('id = [a-zA-Z0-9\._]*', match)
                    match = ''.join(event_id_match)[4:].strip()
                    invoked_events_id.append(match)
            
    for filename in glob.iglob(filepath_history + '**/*.txt', recursive=True):
        try:
            text_file = open_text_file(filename)
            text_file = text_file.lower()
        except Exception as ex:
            logging.warning(f'Skipping the file {filename}')
            logging.warning(ex)
            continue
        
        
        if "country_event =" in text_file:
            # 4.0 One-liners w/o brackets
            pattern_matches = re.findall('(country_event = ((?!\{).)*\n)', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[0]
                    match = match[16:].strip().strip('}').strip().strip('}').strip()
                    if '#' in match:
                        match = match[:match.index('#')].strip().strip('}').strip()    # Clean up comments
                    invoked_events_id.append(match)
    
            #4.1 One-liners with brackets
            pattern_matches = re.findall('country_event = \{.*\}', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    event_id_match = re.findall('id = [a-zA-Z0-9\._]*', match)
                    match = ''.join(event_id_match)[4:].strip()
                    invoked_events_id.append(match)

            #4.2 Multiliners        
            pattern_matches = re.findall('(country_event = \{((?!\}).)*\n(.|\n*?)*\n\t*\})', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    if '' in match:
                        match = match[0]                                            # Counter empty capture groups
                    event_id_match = re.findall('id = [a-zA-Z0-9\._]*', match)
                    match = ''.join(event_id_match)[4:].strip()
                    invoked_events_id.append(match)


    for event in invoked_events_id:
        if event in triggered_events_id.keys():
            triggered_events_id[event] += 1
            
    
    results = [i for i in triggered_events_id.keys() if triggered_events_id[i] == 0]
    # with open(f"C:\\Users\\{test_runner.username}\\Desktop\\events_DEBUG.txt", "a") as create_var:
    #     for i in results:
    #         create_var.write(f"\n- [ ] {i}")
    #         # print(i)

    if results != []:
        logging.warning("Following events have 'is_triggered_only = yes' attr but are never triggered from outside:")
        for i in results:
            logging.error(f'- [ ] {i}')
        logging.warning(f"{len(results)} 'is_triggered_only = yes' events are not triggered from somewhere.")
        raise AssertionError("Following events have 'is_triggered_only = yes' attr but are not triggered! Check console output")
