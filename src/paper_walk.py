'''
Performs one-step walk over the papers
1. Fetch latest record from db for a user
2. Run Analysis on top of that
3. Mail Delivery
4. Sample next paper and store it in DB
'''
import argparse

import logging
log = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO)

from utils import get_current_time, sample_next_paper, compose_paper_url
from mongo_utils import MongoUtils
from main import main

mongo_obj = MongoUtils(db='paper_dots')

def walk():
    # Fetch most recent record for the intended user (which is also the paper-to-read)
    USER = 'harshit158@gmail.com'
    paper_to_read = mongo_obj.get_recent(USER)
    paper_id = paper_to_read['paper_id']
    print('Found paper_id {}'.format(paper_id))
    
    # Run analysis on paper_to_read (last record from db)
    paper_url = compose_paper_url(paper_id)
    main({"filepath":paper_url})
    print('Processing done')
    
    # Deliver mail containing analysis results
    
    
    # Sample next paper
    next_paper_id = sample_next_paper(paper_id)
    print('Next paper_id {}'.format(next_paper_id))
    
    doc = {'paper_id':next_paper_id,
           'date':get_current_time()}
    mongo_obj.push(USER, doc)


if __name__=="__main__":
    parser = argparse.ArgumentParser()    
    
    parser.add_argument('-r', '--reset',
                        action='store_true',
                        help="If True, inserts the seed paper data in the db")
    
    args = vars(parser.parse_args())
    
    if args['reset']:
        mongo_obj.push('harshit158@gmail.com', doc = {'paper_id':'1810.04805','date':get_current_time()})
    
    walk()