import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_presenter_data(statistics, top_limit=10):
    
    sns.set()

    # plot top affiliation names
    names = [name[0] for name in statistics['names'][0:top_limit]]
    cnt = [name[1] for name in statistics['names'][0:top_limit]]
    x_pos = np.arange(len(names))

    fig, ax = plt.subplots(figsize=(10, 6))
    plt.barh(x_pos, cnt[::-1], align='center')
    plt.yticks(x_pos, names[::-1]) 
    plt.xlabel('Count')
    ax.set_xlim(0, 12)

    for i, v in enumerate(cnt[::-1]):
        ax.text(v + 0.125, i, "{:0.01f}%".format((v*100)/statistics['presenters']), va='center')

    fig.subplots_adjust(left=0.3)
    plt.savefig("img/presenter_names.png")

    # plot top affiliation locations by city
    locations = [location[0] for location in statistics['locations'][0:top_limit]]
    cnt = [location[1] for location in statistics['locations'][0:top_limit]]
    x_pos = np.arange(len(locations))

    fig, ax = plt.subplots(figsize=(10, 6))
    plt.barh(x_pos, cnt[::-1], align='center')
    plt.yticks(x_pos, locations[::-1]) 
    plt.xlabel('Count')
    ax.set_xlim(0, 36)

    for i, v in enumerate(cnt[::-1]):
        ax.text(v + 0.25, i, "{:0.01f}%".format((v*100)/statistics['presenters']), va='center')

    fig.subplots_adjust(left=0.3)
    plt.savefig("img/presenter_locations.png")

    # plot top affiliation locations by country
    countries = [country[0] for country in statistics['countries'][0:top_limit]]
    cnt = [country[1] for country in statistics['countries'][0:top_limit]]
    x_pos = np.arange(len(countries))

    fig, ax = plt.subplots(figsize=(10, 6))
    plt.barh(x_pos, cnt[::-1], align='center')
    plt.yticks(x_pos, countries[::-1]) 
    plt.xlabel('Count')
    ax.set_xlim(0, 275)

    for i, v in enumerate(cnt[::-1]):
        ax.text(v + 1, i, "{:0.01f}%".format((v*100)/statistics['presenters']), va='center')

    fig.subplots_adjust(left=0.1)
    plt.savefig("img/presenter_countries.png")

def plot_paper_data(statistics, top_limit=10):
    
    sns.set()

    # plot top paper authors
    authors = [author[0] for author in statistics['authors'][0:top_limit]]
    cnt = [author[1] for author in statistics['authors'][0:top_limit]]
    x_pos = np.arange(len(authors))

    fig, ax = plt.subplots(figsize=(10, 6))
    plt.barh(x_pos, cnt[::-1], align='center')
    plt.yticks(x_pos, authors[::-1]) 
    plt.xlabel('Count')
    ax.set_xlim(0, cnt[0]+1)

    for i, v in enumerate(cnt[::-1]):
        ax.text(v + 0.125, i, "{0:0.01f}%".format((v*100)/statistics['papers']), va='center')
        #ax.text(v - 0.25, i, "{0:0d}".format(v), color='white', va='center')

    fig.subplots_adjust(left=0.2)
    plt.savefig("img/paper_authors.png")

    # plot top paper subjects
    subjects = [subject[0] for subject in statistics['subjects'][0:top_limit]]
    cnt = [subject[1] for subject in statistics['subjects'][0:top_limit]]
    x_pos = np.arange(len(subjects))

    fig, ax = plt.subplots(figsize=(10, 5))
    plt.barh(x_pos, cnt[::-1], align='center')
    plt.yticks(x_pos, subjects[::-1]) 
    plt.xlabel('Count')
    ax.set_xlim(0, cnt[0]+6)

    for i, v in enumerate(cnt[::-1]):
        ax.text(v + 0.5, i, "{0:0.01f}%".format((v*100)/statistics['papers']), va='center')
        #ax.text(v - 1.25, i, "{0:0d}".format(v), color='white', va='center')

    fig.subplots_adjust(left=0.3)
    plt.savefig("img/paper_subjects.png")

    # plot top paper words
    words = [word[0] for word in statistics['words'][0:top_limit]]
    cnt = [word[1] for word in statistics['words'][0:top_limit]]
    x_pos = np.arange(len(words))

    fig, ax = plt.subplots(figsize=(10, 6))
    plt.barh(x_pos, cnt[::-1], align='center')
    plt.yticks(x_pos, words[::-1]) 
    plt.xlabel('Count')
    ax.set_xlim(0, cnt[0]+20)

    for i, v in enumerate(cnt[::-1]):
        ax.text(v + 2.0, i, "{0:0.02f}%".format((v*100)/len(statistics['words'])), va='center')
        #ax.text(v - 4.5, i, "{0:0d}".format(v), color='white', va='center')

    plt.savefig("img/abstract_words.png")

    # plot top paper affiliations
    affs = [aff[0] for aff in statistics['affiliations'][0:top_limit]]
    cnt = [aff[1] for aff in statistics['affiliations'][0:top_limit]]
    x_pos = np.arange(len(words))

    fig, ax = plt.subplots(figsize=(10, 6))
    plt.barh(x_pos, cnt[::-1], align='center')
    plt.yticks(x_pos, affs[::-1]) 
    plt.xlabel('Count')
    ax.set_xlim(0, cnt[0]+1)

    for i, v in enumerate(cnt[::-1]):
        ax.text(v + 0.125, i, "{0:0.01f}%".format((v*100)/statistics['papers']), va='center')
        #ax.text(v - 0.25, i, "{0:0d}".format(v), color='white', va='center')

    fig.subplots_adjust(left=0.4)
    plt.savefig("img/paper_affiliations.png")