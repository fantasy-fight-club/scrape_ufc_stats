'''
Overview
scrape all upcoming events and their announced bouts

run the script 'scrape_ufc_stats_unparsed_data.py' first so every fighter on an upcoming card
is already in the fighter details and tale of the tape files

the upcoming files are a snapshot of the current cards and are replaced on every run
cancelled bouts drop out and replaced opponents change in place
once an event has taken place, it moves to the completed files on the next run of 'scrape_ufc_stats_unparsed_data.py'
'''

# imports
import pandas as pd
from tqdm import tqdm

# import library
import scrape_ufc_stats_library as LIB

# import config
import yaml
config = yaml.safe_load(open('scrape_ufc_stats_config.yaml'))



### parse upcoming events ###
print('### Parsing upcoming events... ###')
print('\n')

# get soup
soup = LIB.get_soup(config['upcoming_events_all_url'])
# parse upcoming event details
upcoming_event_details_df = LIB.parse_upcoming_event_details(soup)

# write upcoming event details to file
upcoming_event_details_df.to_csv(config['upcoming_event_details_file_name'], index=False)
print(upcoming_event_details_df)
print('\n')



### parse upcoming fight details ###
print('### Parsing upcoming fight details... ###')
print('\n')

# create list to store upcoming fight details of each event
list_of_upcoming_fight_details_dfs = []

# loop through each upcoming event and parse its bouts
for url in tqdm(list(upcoming_event_details_df['URL'])):
    # get soup
    soup = LIB.get_soup(url)
    # parse upcoming fight details
    list_of_upcoming_fight_details_dfs.append(
        LIB.parse_upcoming_fight_details(soup, url, config['upcoming_fight_details_column_names'])
    )

# combine fight details of all events, keeping bout order within each event
upcoming_fight_details_df = pd.concat(
    list_of_upcoming_fight_details_dfs,
    ignore_index=True
) if list_of_upcoming_fight_details_dfs else pd.DataFrame(columns=config['upcoming_fight_details_column_names'])

# write upcoming fight details to file
upcoming_fight_details_df.to_csv(config['upcoming_fight_details_file_name'], index=False)
print('\n')

# show number of announced bouts per event
for event, url in upcoming_event_details_df[['EVENT', 'URL']].values:
    print(f"{event}: {(upcoming_fight_details_df['EVENT_URL'] == url).sum()} bouts")
print('\n')



### check for fighters missing from fighter files ###
print('### Checking fighters on upcoming cards... ###')
print('\n')

# get list of parsed fighter urls
list_of_parsed_fighter_urls = set(pd.read_csv(config['fighter_details_file_name'])['URL'])
list_of_parsed_tott_urls = set(pd.read_csv(config['fighter_tott_file_name'])['URL'])

# get list of fighter urls on upcoming cards
list_of_upcoming_fighter_urls = sorted(
    set(upcoming_fight_details_df['RED_FIGHTER_URL']) | set(upcoming_fight_details_df['BLUE_FIGHTER_URL'])
)

# get list of fighters missing from either file
list_of_missing_fighter_urls = [url for url in list_of_upcoming_fighter_urls
                                if url not in list_of_parsed_fighter_urls or url not in list_of_parsed_tott_urls]

# check if there are any missing fighters
if not list_of_missing_fighter_urls:
    print(f'### All {len(list_of_upcoming_fighter_urls)} fighters on upcoming cards have been parsed. ###')
else:
    print('### Fighters on upcoming cards missing from fighter details or tale of the tape. ###')
    print("### Run 'scrape_ufc_stats_unparsed_data.py' to parse them. ###")
    print('\n')
    print(list_of_missing_fighter_urls)
print('\n')
