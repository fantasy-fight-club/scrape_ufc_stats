# Scrape UFC Stats (Forked)

Rescraped on 2026-05-04 and added URLs to the stats csv so they can be linked without using names

Scrape all available UFC events data, fights stats, and fighter details from [ufcstats.com](http://ufcstats.com/) and save in CSV format.

## Prerequisites

Python 3

Install requirements with `pip install -r requirements.txt`

## Introduction

Data for all events, fights, and fighters have been scraped and saved as the following data files:

- ufc_events.csv
- ufc_fight_details.csv
- ufc_fight_results.csv
- ufc_fight_stats.csv
- ufc_fighter_details.csv
- ufc_fighter_tott.csv

To download the CSV files without running any code, click `Code` > `Download ZIP` or clone the repo.

You can also scrape all the data for fight stats again using the notebook `scrape_ufc_stats_all_historical_data.ipynb`, and all data for fighter tale of the tape again using the notebook `scrape_ufc_stats_fighter_tott.ipynb`.
Do note that these will each take a few hours to complete.

Once you have the up-to-date historical data for fight stats, you can run the notebook `scrape_ufc_stats_unparsed_data.ipynb` or the script `scrape_ufc_stats_unparsed_data.py` to scrape only the latest fights and refresh the data.

The notebook `scrape_ufc_stats_working_example.ipynb` can be used for testing or debugging. The code here is broken down into sections which can be executed to scrape single data points, e.g. scraping stats for one fight only.

Do [feel free to reach out](https://www.linkedin.com/in/russellchanws/) with any comments, suggestions, or issues.

## Data Refresh

The script `scrape_ufc_stats_unparsed_data.py` has been deployed to Google Cloud Platform (GCP) as a Cloud Run Job and will run daily via Cloud Scheduler to check and scrape new fights and fighters, then push the refreshed data files to this repository.

This keeps the data files up to date with the latest fight and fighter stats, and you can quickly download and use the CSV files above without running any code.
