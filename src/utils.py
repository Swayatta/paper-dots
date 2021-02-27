from IPython.core.display import display, HTML
import re
import fitz
import urllib.request, urllib.parse, urllib.error

def render(cleaned_spans, tok_tags, colour='yellow', debug=False):
    html_string_components = []
    flat_spans = sum(cleaned_spans, [])
    
    extra_info = '<sup style="background-color:yellow">{}</sup>' if debug else ''

    for idx, tok in enumerate(tok_tags):
        if idx not in flat_spans:
            html_string_components.append(str(tok[0])+extra_info.format(tok[1]))
        else:
            html_string_components.append(f'<span style="background-color:{colour}">{tok[0]}</span>'+extra_info.format(tok[1]))

    html_to_render = '<p> '+' '.join(html_string_components) + ' </p>'
    display(HTML(html_to_render))

def search_and_annotate(rect, phrases, page):
    for phrase in phrases:
        text_instances = page.searchFor(phrase)   # TODO: Use clip parameter to bring down noise
        for inst in text_instances:
            page.addHighlightAnnot(inst, )        # highlight the found text
            # TODO: annotate based on the type/importance of phrase

def sanitize_phrases(phrases):
    for idx, phrase in enumerate(phrases):
        phrase = re.sub('\s*\-\s*', '', phrase) # "represent- ation model" -> "representation model"
        phrase = phrase.strip()                 # remove spaces from end 
        phrases[idx] = phrase
    
    phrases = [x for x in phrases if x]         # discard empty phrases
    return phrases

def read_file(filepath):
    if filepath.startswith('https'):
        if not filepath.endswith('pdf'):
            # if not a pdf link, process and convert the url to point to pdf url
            paper_id = filepath.split('/')[-1]
            filepath =  f'https://arxiv.org/pdf/{paper_id}.pdf'
            
        pdf_stream = urllib.request.urlopen(filepath).read()
        pages = fitz.open(stream=pdf_stream, filetype='pdf')
    else:
        pages = fitz.open(filepath)
    
    return pages