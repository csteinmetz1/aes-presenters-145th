import os
import sys
import json
import glob
import argparse
import numpy as np
import pandas as pd
import urllib.request
import seaborn as sns
from time import sleep
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from collections import OrderedDict

def parse_presenters_list(presenter_file):
    soup = BeautifulSoup(open(presenter_file), 'html.parser')
    presenter_list = soup.find('body').find('div', {'class' : 'col-md-9'}).find_all('p')
    
    presenters = []

    for presenter_text in presenter_list:
        p = presenter_text.a.text
        presenter = {}
        presenter['last_name'] = p.split(',')[0]
        presenter['first_name'] = p.split(',')[1].split()[0]
        if not '(' in p:
            presenter['affiliation_names'] = ['None']
            presenter['affiliation_locations'] = ['None']
        else:
            affiliations = p.split('(')[1].strip(')')
            affiliation_name_list = []
            affiliation_location_list = []
            for n in range(affiliations.count(';')+1):
                affiliation = affiliations.split(';')[n].strip()
                if not ' - ' in affiliation:
                    affiliation_name = affiliation
                    affiliation_location = 'None'
                else:
                    affiliation_name = affiliation.split(' - ')[0].strip()
                    affiliation_location = affiliation.split(' - ')[1].strip()
                
                affiliation_name_list.append(affiliation_name)
                affiliation_location_list.append(affiliation_location)
                
            presenter['affiliation_names'] = affiliation_name_list
            presenter['affiliation_locations'] = affiliation_location_list

        presenters.append(presenter)

    return presenters

def parse_papers_list(papers_file, wait_time=5):
    soup = BeautifulSoup(open(papers_file), 'html.parser')
    papers_list = soup.find('body').find('div', {'class' : 'c-layout-sidebar-content c-align-left'}).find_all('h4')
    
    paper_links = []

    for paper_link in papers_list:
        try:
            url = paper_link.a['href']
            filename = paper_link.a.string
            filename = "".join([c for c in filename if c.isalpha() or c.isdigit() or c==' ']).rstrip()
            paper_links.append((url, filename))
        except Exception as e:
            pass
    
        sys.stdout.write("* Papers found: {0}\r".format(len(paper_links)))
        sys.stdout.flush()

    n_papers = len(paper_links)

    # download data about papers (authors, affiliations, subject)
    if not os.path.isdir("html/papers"):
        os.makedirs("html/papers")
        for idx, paper_link in enumerate(paper_links):
            remaining_time = (n_papers - idx) * wait_time
            sys.stdout.write(100 * " ")
            sys.stdout.write("\r")
            sys.stdout.write("* {0}/{1} - {2} - ~{3} seconds remaining...\r".format(idx, n_papers, paper_link[1], remaining_time))
            sys.stdout.flush()
            urllib.request.urlretrieve(paper_link[0], "html/papers/{}.html".format(paper_link[1]))
            sleep(wait_time) # watch out - don't want to spam server with requests

    for paper in glob.glob("html/papers/*.html"):
        soup = BeautifulSoup(open(paper), 'html.parser')
        paper_details = soup.find('body').find('div', {'class' : 'c-content-box c-size-md c-bg-white'}).find_all('p')

        title = os.path.basename(paper).strip('.html')
        abstract = paper_details[0].text
        details = paper_details[1].find_all('span')
        authors = details[1].text.split(';')
        affiliation = details[3].text
        subject = details[13].text

        print(title)
        print(abstract)
        print(authors)
        print(affiliation)
        print(subject)

    #return papers

def clean_presenters_list(presenters):
    for p_idx, presenter in enumerate(presenters):
        for n_idx, name in enumerate(presenter['affiliation_names']):
            if   name == "Queen Mary University London":
                presenters[p_idx]['affiliation_names'][n_idx] = "Queen Mary University of London"
            elif name == "Dolby Laboratories":
                presenters[p_idx]['affiliation_names'][n_idx] = "Dolby Laboratories, Inc."
            elif name == "Meyer Sound Labs" or name == "Meyer Sound":
                presenters[p_idx]['affiliation_names'][n_idx] = "Meyer Sound Laboratories"
            elif name == "BBC R&D":
                 presenters[p_idx]['affiliation_names'][n_idx] = "BBC Research and Development"
            elif name == "The Centre for Interdisciplinary Research in Music Media and Technology":
                presenters[p_idx]['affiliation_names'][n_idx] = "Centre for Interdisciplinary Research in Music Media and Technology"
    
        for l_idx, location in enumerate(presenter['affiliation_locations']):
            country = location.split(',')[-1].strip()
            if country == "NY USA":
                presenters[p_idx]['affiliation_locations'][l_idx] = ""

    return presenters

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

    top_names = sorted_affiliation_name_cnt[1:30]
    top_locations = sorted_affiliation_location_cnt[1:30]
    top_countries = sorted_affiliation_country_cnt[0:30]

    sns.set()

    # plot top affiliation names
    names = [name[0] for name in top_names]
    cnt = [name[1] for name in top_names]
    x_pos = np.arange(len(names))

    fig, ax = plt.subplots(figsize=(10, 10))
    plt.barh(x_pos, cnt[::-1], align='center')
    plt.yticks(x_pos, names[::-1]) 
    plt.xlabel('Count')
    ax.set_xlim(0, 12)

    for i, v in enumerate(cnt[::-1]):
        ax.text(v + 0.125, i, "{:0.01f}%".format((v*100)/n_presenters), va='center')

    fig.subplots_adjust(left=0.3)
    plt.savefig("img/names.png")

    # plot top affiliation locations by city
    locations = [location[0] for location in top_locations]
    cnt = [location[1] for location in top_locations]
    x_pos = np.arange(len(locations))

    fig, ax = plt.subplots(figsize=(10, 10))
    plt.barh(x_pos, cnt[::-1], align='center')
    plt.yticks(x_pos, locations[::-1]) 
    plt.xlabel('Count')
    ax.set_xlim(0, 36)

    for i, v in enumerate(cnt[::-1]):
        ax.text(v + 0.25, i, "{:0.01f}%".format((v*100)/n_presenters), va='center')

    fig.subplots_adjust(left=0.3)
    plt.savefig("img/locations.png")

    # plot top affiliation locations by country
    countries = [country[0] for country in top_countries]
    cnt = [country[1] for country in top_countries]
    x_pos = np.arange(len(countries))

    fig, ax = plt.subplots(figsize=(10, 10))
    plt.barh(x_pos, cnt[::-1], align='center')
    plt.yticks(x_pos, countries[::-1]) 
    plt.xlabel('Count')
    ax.set_xlim(0, 275)

    for i, v in enumerate(cnt[::-1]):
        ax.text(v + 1, i, "{:0.01f}%".format((v*100)/n_presenters), va='center')

    fig.subplots_adjust(left=0.3)
    plt.savefig("img/countries.png")

def generate_csv(data_list, filename):
    dataframe = pd.DataFrame(data_list)
    dataframe.to_csv(filename, sep=',')

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--presenters', help='Path to HTML file containing presenter list.', required=False)
    parser.add_argument('--papers', help='Path to HTML file containing papers list.', required=False)
    return parser

if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    if args.presenters:
        presenters = parse_presenters_list(args.presenters)
        presenters = clean_presenters_list(presenters)
        generate_csv(presenters, "data/presenters.csv")
        analyze_presenters(presenters)
    if args.papers:	
        papers = parse_papers_list(args.papers)

