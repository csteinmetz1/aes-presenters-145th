import os
import sys
import numpy as np
import pandas as pd
from collections import OrderedDict

import clean

def analyze_presenters(presenters):

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
    
    print("Presenter Statistics Summary:")
    print("Number of presenters:", n_presenters)
    print("Number of affiliations:", n_affiliation_names)
    print("Number of locations:", n_affiliation_locations)
    print("Number of countries:", n_affiliation_countries)
    print("\n")

    # sort affiliations by count
    sorted_affiliation_name_cnt = sorted(affiliation_name_cnt.items(), key=lambda kv: kv[1], reverse=True)
    sorted_affiliation_location_cnt = sorted(affiliation_location_cnt.items(), key=lambda kv: kv[1], reverse=True)
    sorted_affiliation_country_cnt = sorted(affiliation_country_cnt.items(), key=lambda kv: kv[1], reverse=True)

    generate_csv(sorted_affiliation_name_cnt, "data/presenter_names.csv")
    generate_csv(sorted_affiliation_location_cnt, "data/presenter_locations.csv")
    generate_csv(sorted_affiliation_country_cnt, "data/presenter_countries.csv")

    statistics = {}
    statistics['presenters'] = n_presenters
    statistics['names'] = [i for i in sorted_affiliation_name_cnt if i[0] != 'None']
    statistics['locations'] = [i for i in sorted_affiliation_location_cnt if i[0] != 'None'] 
    statistics['countries'] = [i for i in sorted_affiliation_country_cnt if i[0] != 'None'] 

    return statistics

def analyze_papers(papers):

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

    ### Title/Abtract ###
    words = []
    words_cnt = {}

    for paper in papers:
        abstract_words = paper['abstract'].lower()
        filtered_abstract_words = clean.remove_stopwords(abstract_words)
        for word in filtered_abstract_words:
            if word not in words:
                words.append(word)
                words_cnt[word] = 1
            else:
                words_cnt[word] += 1
    
    sorted_words_cnt = sorted(words_cnt.items(), key=lambda kv: kv[1], reverse=True)

    n_papers = len(papers)

    print("Paper Statistics Summary:")
    print("Number of papers:", n_papers)
    print("Number of subjects:", len(sorted_subjects_cnt))
    print("Number of unique words:", len(sorted_words_cnt))
    print("Number of affiliation:", len(sorted_affiliations_cnt))

    generate_csv(sorted_words_cnt, "data/abstract_words.csv")
    generate_csv(sorted_authors_cnt, "data/paper_authors.csv")
    generate_csv(sorted_subjects_cnt, "data/paper_subjects.csv")
    generate_csv(sorted_affiliations_cnt, "data/paper_affiliations.csv")

    statistics = {}
    statistics['papers'] = n_papers
    statistics['authors'] = sorted_authors_cnt
    statistics['subjects'] = sorted_subjects_cnt
    statistics['words'] = sorted_words_cnt
    statistics['affiliations'] = sorted_affiliations_cnt

    return statistics

def generate_csv(data_list, filename):
    dataframe = pd.DataFrame(data_list)
    dataframe.to_csv(filename, sep=',')