import json
import argparse
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from collections import OrderedDict

def parse_list(presenter_file):
	soup = BeautifulSoup(open(presenter_file), 'html.parser')
	presenter_list = soup.find('body').find('div', {'class' : 'col-md-9'}).find_all('p')
	
	presenters =[]

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

def analyze_presenters(presenters):

	affiliation_names = []
	affiliation_name_cnt = {}
	affiliation_locations = []
	affiliation_location_cnt = {}

	for presenter in presenters:
		for name in presenter['affiliation_names']:
			if name not in affiliation_names:
				affiliation_names.append(name)
				affiliation_name_cnt[name] = 1
			else:
				affiliation_name_cnt[name] += 1
		for location in presenter['affiliation_locations']:
			if location not in affiliation_locations:
				affiliation_locations.append(location)
				affiliation_location_cnt[location] = 1
			else:
				affiliation_location_cnt[location] += 1
	
	n_presenters = len(presenters)
	n_affiliation_names = len(affiliation_names)
	n_affiliation_location = len(affiliation_locations)
	
	print("Number of presenters:", n_presenters)
	print("Number of affiliations:", n_affiliation_names)
	print("Number of locations:", n_affiliation_location)

	# sort affiliations by count
	sorted_affiliation_name_cnt = sorted(affiliation_name_cnt.items(), key=lambda kv: kv[1], reverse=True)
	sorted_affiliation_location_cnt = sorted(affiliation_location_cnt.items(), key=lambda kv: kv[1], reverse=True)

	generate_csv(sorted_affiliation_name_cnt, "affiliations.csv")
	generate_csv(sorted_affiliation_location_cnt, "locations.csv")

	top_15_names = sorted_affiliation_name_cnt[1:16]
	top_15_locations = sorted_affiliation_location_cnt[1:16]

	# plot top affiliation names
	names = [name[0] for name in top_15_names]
	cnt = [name[1] for name in top_15_names]
	x_pos = np.arange(len(names))

	fig, ax = plt.subplots(figsize=(10, 6))
	plt.barh(x_pos, cnt[::-1], align='center')
	plt.yticks(x_pos, names[::-1]) 
	plt.xlabel('Count')
	fig.subplots_adjust(left=0.3)
	plt.savefig("img/names.png")

	# plot top affiliation locations
	locations = [location[0] for location in top_15_locations]
	cnt = [location[1] for location in top_15_locations]
	x_pos = np.arange(len(locations))

	fig, ax = plt.subplots(figsize=(10, 6))
	plt.barh(x_pos, cnt[::-1], align='center')
	plt.yticks(x_pos, locations[::-1]) 
	plt.xlabel('Count')
	fig.subplots_adjust(left=0.3)
	plt.savefig("img/locations.png")

def generate_csv(data_list, filename):
	dataframe = pd.DataFrame(data_list)
	dataframe.to_csv(filename, sep=',')

def create_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument('--file', help='Path to HTML file containing presenter list.', required=True)
	return parser

if __name__ == '__main__':
	parser = create_parser()
	args = parser.parse_args()
	presenters = parse_list(args.file)
	generate_csv(presenters, "presenters.csv")
	analyze_presenters(presenters)
