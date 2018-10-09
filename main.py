import argparse

import analyze
import parse
import clean
import plot

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--presenters', help='Path to HTML file containing presenter list.', required=False)
    parser.add_argument('--papers', help='Path to HTML file containing papers list.', required=False)
    return parser

if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    if args.presenters:
        presenters = parse.parse_presenters_list(args.presenters)
        presenters = clean.clean_presenters_list(presenters)
        analyze.generate_csv(presenters, "data/presenters.csv")
        stats = analyze.analyze_presenters(presenters, top_limit=15)
        plot.plot_top_presenter_data(stats)
    if args.papers:	
        papers = parse.parse_papers_list(args.papers)
        analyze.generate_csv(papers, "data/papers.csv")