import pandas as pd
import h5py
from sentence_transformers import SentenceTransformer, util


class Sample():
    """Samples a relevant paper given an input, using corpus_embeddings
    """
    
    def __init__(self):
        # Reading corpus_embeddings
        data=h5py.File('./data/corpus_embeddings.hdf5', 'r')
        self.corpus_embeddings=data['corpus_embeddings'][()]
        
        # Loading model to encode input text
        self.model = SentenceTransformer('allenai-specter')

    def sample(self, paper_text):
        """Given paper_text( = paper_abstract+paper_title), samples out the most relevant paper

        Args:
            paper_text (str): concatenated string of paper_title & paper_abstract

        Returns:
            [type]: [description]
        """
        query_embedding = self.model.encode(paper_text, convert_to_tensor=True)

        search_hits = util.semantic_search(query_embedding, self.corpus_embeddings)
        return search_hits[0]
        


if __name__=='__main__':
    paper_text = '''A fully differential calculation in perturbative quantum chromodynamics is presented for 
                the production of massive photon pairs at hadron colliders. All next-to-leading order perturbative 
                contributions from quark-antiquark, gluon-(anti)quark, and gluon-gluon subprocesses are included, 
                as well as all-orders resummation of initial-state gluon radiation valid at next-to-next-to-leading 
                logarithmic accuracy. The region of phase space is specified in which the calculation is most reliable. 
                Good agreement is demonstrated with data from the Fermilab Tevatron, and predictions are made for more 
                detailed tests with CDF and DO data. Predictions are shown for distributions of diphoton pairs produced 
                at the energy of the Large Hadron Collider (LHC). Distributions of the diphoton pairs from the decay of
                a Higgs boson are contrasted with those produced from QCD processes at the LHC, showing that enhanced 
                sensitivity to the signal can be obtained with judicious selection of events. Calculation of prompt 
                diphoton production cross sections at Tevatron and LHC energies'''
    
    sample = Sample()
    result = sample.sample(paper_text)
    print(result)