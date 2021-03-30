import re
import argparse
from collections import defaultdict

import fitz
from tqdm import tqdm
from PIL import Image
import pandas as pd
from pyvis.network import Network
import pprint
pp = pprint.PrettyPrinter(indent=4)

import config
from model_loader import Model
from utils import search_and_annotate, read_file, get_block_containing_abstract
from extractor import extract_author, extract_year

def get_ARGS(result):
    ARGS_overall=[]
    for item in result['verbs']:
        to_parse=item['description']
        ARGS=re.findall('\[.*?\]', to_parse)
        ARGS_overall.append(ARGS)

    return ARGS_overall

def get_svo_triplets(ARGS):
    svo_triplets=[]
    for triplet in ARGS:
        svo=defaultdict(list)
        for arg in triplet:
            parts=arg.split(':')
            if 'ARG0' in parts[0]:
                svo['subject']=parts[1][:-1]
            elif 'ARG1' in parts[0]:
                svo['object']=parts[1][:-1]
            elif 'V' in parts[0]:
                svo['relation'].append(parts[1][:-1])
    
        svo['relation']=' '.join(svo['relation'])
        svo_triplets.append(svo)
    return svo_triplets

def build_graph(triplets, net):
    for triplet in triplets:
        if not all([triplet['subject'], triplet['object'], triplet['relation']]):
            continue
        net.add_node(triplet['subject'])
        net.add_node(triplet['object'])    
        net.add_edge(triplet['subject'], triplet['object'], label=triplet['relation'])
    return net
    
def main(args):
    # Initializing Parser
    model_path = config.OPENIE['local_path']
    model = Model(model_path)

    # Reading input and process the pages
    pages = read_file(args['filepath'])
    
    # Process each page
    for page in tqdm(pages):
        page_bbox = page.cropbox  # bounding box of full page
        text_blocks = page.get_text("blocks")
        
        # Text block containing the "Abstract"
        abstract_block = get_block_containing_abstract(text_blocks)
        
        x0, y0, x1, y1, text, abstract_block_no, block_type = abstract_block

        # Running OPENIE prediction on abstract text        
        result = model.predict(sentence=text)
        
        # Extracting SVO triplets
        ARGS=get_ARGS(result)
        svo_triplets=get_svo_triplets(ARGS)

        # Initializing graph
        net = Network(height=1500, width=1500)
        net=build_graph(svo_triplets, net)
        
        net.show('../output/graph.html')
        
        break


if __name__=="__main__":
    text = '''A fully differential calculation in perturbative quantum chromodynamics is presented for 
                the production of massive photon pairs at hadron colliders. All next-to-leading order perturbative 
                contributions from quark-antiquark, gluon-(anti)quark, and gluon-gluon subprocesses are included, 
                as well as all-orders resummation of initial-state gluon radiation valid at next-to-next-to-leading 
                logarithmic accuracy. The region of phase space is specified in which the calculation is most reliable. 
                Good agreement is demonstrated with data from the Fermilab Tevatron, and predictions are made for more 
                detailed tests with CDF and DO data. Predictions are shown for distributions of diphoton pairs produced 
                at the energy of the Large Hadron Collider (LHC). Distributions of the diphoton pairs from the decay of
                a Higgs boson are contrasted with those produced from QCD processes at the LHC, showing that enhanced 
                sensitivity to the signal can be obtained with judicious selection of events.'''
        
    filepath = 'https://arxiv.org/abs/0704.0001'
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-fp', '--filepath',
                        type=str,
                        required=True,
                        help="Filepath - can be path on local disk or a URL")

    args = vars(parser.parse_args())
    
    main(args)