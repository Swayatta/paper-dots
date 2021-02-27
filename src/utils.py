from IPython.core.display import display, HTML
import re

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