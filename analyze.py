import os
import sys
import numpy as np
import pandas as pd
from collections import OrderedDict

def analyze_presenters(presenters, top_limit=10):

    affiliation_names = []
    affiliation_name_cnt = {}
    affiliation_locations = []
    affiliation_location_cnt = {}
    affiliation_countries = []
    affiliation_country_cnt = {}

    for presenter in presenters:
        for name in presenter['affiliation_names']:
            if name not in affiliation_names:
                affiliation_names.append(name)
                affiliation_name_cnt[name] = 1
            else:
                affiliation_name_cnt[name] += 1
        for location in presenter['affiliation_locations']:
            # count cities
            if location not in affiliation_locations:
                affiliation_locations.append(location)
                affiliation_location_cnt[location] = 1
            else:
                affiliation_location_cnt[location] += 1
            # count countries
            country = location.split(',')[-1].strip()
            if country not in affiliation_countries:
                affiliation_countries.append(country)
                affiliation_country_cnt[country] = 1
            else:
                affiliation_country_cnt[country] += 1
    
    n_presenters = len(presenters)
    n_affiliation_names = len(affiliation_names)
    n_affiliation_locations = len(affiliation_locations)
    n_affiliation_countries = len(affiliation_countries)
    
    print("Number of presenters:", n_presenters)
    print("Number of affiliations:", n_affiliation_names)
    print("Number of locations:", n_affiliation_locations)
    print("Number of countries:", n_affiliation_countries)

    # sort affiliations by count
    sorted_affiliation_name_cnt = sorted(affiliation_name_cnt.items(), key=lambda kv: kv[1], reverse=True)
    sorted_affiliation_location_cnt = sorted(affiliation_location_cnt.items(), key=lambda kv: kv[1], reverse=True)
    sorted_affiliation_country_cnt = sorted(affiliation_country_cnt.items(), key=lambda kv: kv[1], reverse=True)

    generate_csv(sorted_affiliation_name_cnt, "data/affiliations.csv")
    generate_csv(sorted_affiliation_location_cnt, "data/locations.csv")
    generate_csv(sorted_affiliation_country_cnt, "data/countries.csv")

    top_names = sorted_affiliation_name_cnt[0:top_limit]
    top_locations = sorted_affiliation_location_cnt[0:top_limit]
    top_countries = sorted_affiliation_country_cnt[0:top_limit]

    statistics = {}
    statistics['presenters'] = n_presenters
    statistics['names'] = top_names
    statistics['locations'] = top_locations
    statistics['countries'] = top_countries

    return statistics

def generate_csv(data_list, filename):
    dataframe = pd.DataFrame(data_list)
    dataframe.to_csv(filename, sep=',')