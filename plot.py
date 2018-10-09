import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_top_presenter_data(statistics):
    
    sns.set()

    # plot top affiliation names
    names = [name[0] for name in statistics['names']]
    cnt = [name[1] for name in statistics['names']]
    x_pos = np.arange(len(names))

    fig, ax = plt.subplots(figsize=(10, 10))
    plt.barh(x_pos, cnt[::-1], align='center')
    plt.yticks(x_pos, names[::-1]) 
    plt.xlabel('Count')
    ax.set_xlim(0, 12)

    for i, v in enumerate(cnt[::-1]):
        ax.text(v + 0.125, i, "{:0.01f}%".format((v*100)/statistics['presenters']), va='center')

    fig.subplots_adjust(left=0.3)
    plt.savefig("img/names.png")

    # plot top affiliation locations by city
    locations = [location[0] for location in statistics['locations']]
    cnt = [location[1] for location in statistics['locations']]
    x_pos = np.arange(len(locations))

    fig, ax = plt.subplots(figsize=(10, 10))
    plt.barh(x_pos, cnt[::-1], align='center')
    plt.yticks(x_pos, locations[::-1]) 
    plt.xlabel('Count')
    ax.set_xlim(0, 36)

    for i, v in enumerate(cnt[::-1]):
        ax.text(v + 0.25, i, "{:0.01f}%".format((v*100)/statistics['presenters']), va='center')

    fig.subplots_adjust(left=0.3)
    plt.savefig("img/locations.png")

    # plot top affiliation locations by country
    countries = [country[0] for country in statistics['countries']]
    cnt = [country[1] for country in statistics['countries']]
    x_pos = np.arange(len(countries))

    fig, ax = plt.subplots(figsize=(10, 10))
    plt.barh(x_pos, cnt[::-1], align='center')
    plt.yticks(x_pos, countries[::-1]) 
    plt.xlabel('Count')
    ax.set_xlim(0, 275)

    for i, v in enumerate(cnt[::-1]):
        ax.text(v + 1, i, "{:0.01f}%".format((v*100)/statistics['presenters']), va='center')

    fig.subplots_adjust(left=0.3)
    plt.savefig("img/countries.png")