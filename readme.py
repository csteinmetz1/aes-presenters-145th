import textwrap

def format_paper_data(stats):

	papers_text = """
	## Papers
	This section outlines statistics related to papers accepted to the convention. This includes papers that are presented in the form of talks as well as posters. 

	Total number of accepted papers: {0:0d}<br/>
	Total number of affiliations: {1:0d}<br/>
	Total number of subjects: {2:0d}<br/>
	Total number of unqiue abstract words: {3:0d}<br/>

	### Top Authors

	![authors](img/paper_authors.png) 

	### Top Affiliations
	![affiliations](img/paper_affiliations.png) 

	### Top Subjects

	![subjects](img/paper_subjects.png) 

	### Top Abstract Words

	![authors](img/abstract_words.png) 
	""".format(stats['papers'], len(stats['affiliations']),
			   len(stats['subjects']), len(stats['words']))

	with open("markdown/papers.md", "w") as papers_fp:
		papers_fp.write(textwrap.dedent(papers_text))

def format_presenter_data(stats):
	presenters_text = """
	## Presenters
	This section outlines statistics about all of the presenters at the convention. It it not limited to just accepted papers.

	Total number of presenters: {0:0d}<br/>
	Total number of affiliations:  {1:0d}<br/>
	Total number of cities: {2:0d}<br/>
	Total number of countries: {3:0d}<br/>

	### Top Affiliations

	![names](img/presenter_names.png) 

	### Top Cities

	![locations](img/presenter_locations.png)

	### Top Countries

	![countries](img/presenter_countries.png)

	## Disclaimer
	These statistics are only estimates. Formatting discrepancies in the scrapped data may skew some of these metrics.  

	""".format(stats['presenters'], len(stats['names']),
			   len(stats['locations']), len(stats['countries']))
	
	with open("markdown/presenters.md", "w") as presenters_fp:
		presenters_fp.write(textwrap.dedent(presenters_text))

def compile_readme():
	# load markdown source files
	with open("markdown/intro.md", "r") as intro_fp:
		intro = intro_fp.read()
	with open("markdown/papers.md", "r") as papers_fp:
		papers = papers_fp.read()
	with open("markdown/presenters.md", "r") as presenters_fp:
		presenters = presenters_fp.read()

	# load README.md file
	with open("README.md", "w") as readme_fp:
		readme_fp.write(intro)
		readme_fp.write(papers)
		readme_fp.write(presenters)