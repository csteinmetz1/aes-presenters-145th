import os
import sys
import numpy as np
import pandas as pd
from collections import OrderedDict

import clean

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

    generate_csv(sorted_affiliation_name_cnt, "data/affiliation_counts.csv")
    generate_csv(sorted_affiliation_location_cnt, "data/location_counts.csv")
    generate_csv(sorted_affiliation_country_cnt, "data/country_counts.csv")

    top_names = sorted_affiliation_name_cnt[0:top_limit]
    top_locations = sorted_affiliation_location_cnt[0:top_limit]
    top_countries = sorted_affiliation_country_cnt[0:top_limit]

    statistics = {}
    statistics['presenters'] = n_presenters
    statistics['names'] = top_names
    statistics['locations'] = top_locations
    statistics['countries'] = top_countries

    return statistics

def analyze_papers(papers, top_limit=10):

    ### Authors ###
    authors = []
    authors_cnt = {}

    for paper in papers:
        for author in paper['authors']:
            if author not in authors:
                authors.append(author)
                authors_cnt[author] = 1
            else:
                authors_cnt[author] += 1

    sorted_authors_cnt = sorted(authors_cnt.items(), key=lambda kv: kv[1], reverse=True)
    #print(sorted_authors_cnt)

    ### Affiliations ###
    affiliations = []
    affiliations_cnt = {}

    for paper in papers:
        for affiliation in paper['affiliation']:
            affiliation = affiliation.split(',')[0]
            if affiliation not in affiliations:
                affiliations.append(affiliation)
                affiliations_cnt[affiliation] = 1
            else:
                affiliations_cnt[affiliation] += 1

    sorted_affiliations_cnt = sorted(affiliations_cnt.items(), key=lambda kv: kv[1], reverse=True)
    #for aff in sorted_affiliations_cnt:
    #    print(aff)

    ### Subjects ###

    subjects = []
    subjects_cnt = {}

    for paper in papers:
        if paper['subject'] not in subjects:
            subjects.append(paper['subject'])
            subjects_cnt[paper['subject']] = 1
        else:
            subjects_cnt[paper['subject']] += 1

    sorted_subjects_cnt = sorted(subjects_cnt.items(), key=lambda kv: kv[1], reverse=True)
    for sub in sorted_subjects_cnt:
        print(sub)

    ### Title/Abtract ###
    words = []
    words_cnt = {}

    for paper in papers:
        abstract_words = paper['abstract']
        filtered_abstract_words = clean.remove_stopwords(abstract_words)
        for word in filtered_abstract_words:
            if word not in words:
                words.append(word)
                words_cnt[word] = 1
            else:
                words_cnt[word] += 1
    
    sorted_words_cnt = sorted(words_cnt.items(), key=lambda kv: kv[1], reverse=True)
    #print(sorted_words_cnt)

def generate_csv(data_list, filename):
    dataframe = pd.DataFrame(data_list)
    dataframe.to_csv(filename, sep=',')