import re

from model_loader import Model

import config

model_path = config.CONSTITUENCY_PARSING['local_path']

class Parser(Model):
    def __init__(self):
        Model.__init__(self, model_path)
    
    def parse(self, sentence):
        # fetching model's output
        model_output=self.predict(sentence)

        # extracting noun chunks from the model's output
        raw_noun_phrases = self.get_raw_noun_phrases(model_output)

        # cleaning raw_noun_phrases
        noun_phrases = self.get_noun_phrases(raw_noun_phrases)

        return noun_phrases

    def get_noun_phrases(self, raw_noun_phrases):
        noun_phrases=[]
        for phrase in raw_noun_phrases:
            np=' '.join(re.findall(' [A-Za-z0-9\-]+(?=\))', phrase))
            noun_phrases.append(np)
        return noun_phrases

    def get_raw_noun_phrases(self, model_output):
        text=model_output['trees'].replace('NNP', '**')
        searches=re.finditer('\(NP \([^(NP)]+', text)            # 
        noun_phrases=[]                                                 # 
        for search in searches:
            start, end = search.span(0)[0], search.span(0)[1]           # 
            noun_phrases.append(self.parse_brackets(start, text))     # 
        return noun_phrases
    
    def parse_brackets(self, start, result_text):
        arr=[]
        ptr=int(start)
        arr.append(result_text[ptr])
        ptr+=1
        while arr:
            #print(result_text[ptr])
            if result_text[ptr]==')':
                arr.pop(-1)
            elif result_text[ptr]=='(':
                arr.append(result_text[ptr])
                #print(arr)
            ptr+=1
        
        return result_text[start:ptr]