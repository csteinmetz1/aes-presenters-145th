import os
import sys
import glob
import urllib.request
from time import sleep
from bs4 import BeautifulSoup

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

    papers = [] # list to store paper objects

    for idx, paper in enumerate(glob.glob("html/papers/*.html")):
        soup = BeautifulSoup(open(paper), 'html.parser')
        paper_details = soup.find('body').find('div', {'class' : 'c-content-box c-size-md c-bg-white'}).find_all('p')
        title = soup.find('body').find('h2', {'class' : 'c-left c-font-24'}).text

        # extract the goods from each paper page
        abstract = paper_details[0].text
        if paper_details[1].text == "OpenAccess":
            details = paper_details[2].find_all('span')
        else:
            details = paper_details[1].find_all('span')
        authors = details[1].text.split(';')
        affiliation = details[3].text.split(';')
        subject = details[13].text
        if subject.strip() == "Subject:":
            subject = details[14].text

        if   '-' in subject:
            subject = subject.split('-')[0].strip()
        elif '—' in subject:
            subject = subject.split('—')[0].strip()
        elif '–' in subject:
            subject = subject.split('–')[0].strip()

        if 'Posters' in subject:
            paper_type = 'Poster'
            subject = subject.replace('Posters: ', '').strip()
        else:
            paper_type = 'Talk'

        print(subject, paper_type)

        #print(idx, title)
        paper = {}
        paper['title'] = title
        paper['abstract'] = abstract
        paper['authors'] = authors
        paper['affiliation'] = affiliation
        paper['subject'] = subject
        paper['paper_type'] = paper_type

        papers.append(paper)

    return papers