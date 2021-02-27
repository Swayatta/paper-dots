import argparse

import fitz
from tqdm import tqdm

import config
import constituency_parser
from utils import search_and_annotate


def main(args, filepath):
    # Initializing Parser
    parser = constituency_parser.Parser()
    
    # Reading input and process the pages
    pages = fitz.open(filepath)
    for page in tqdm(pages):
        page_bbox = page.cropbox  # bounding box of full page
        
        text_blocks = page.get_text("blocks")
        for block in text_blocks:
            x0, y0, x1, y1, text, block_no, block_type = block
            if block_no!=10:
                continue
            
            rect = [x0, y0, x1, y1]                     
            phrases = parser.parse(text)                
            search_and_annotate(rect, phrases, page)
            
            if args['clip_abstract']:
                # keep the area from starting of page till the end of abstract
                page.set_cropbox(fitz.Rect([0,0,page_bbox[2],y1+20]))
                zoom = 3    # zoom factor to increase resolution
                mat = fitz.Matrix(zoom, zoom)
                pix = page.getPixmap(matrix = mat)
                pix.writeImage(config.ANNOTATED_FILEPATH+"abstract.png")
                
        
        # Since we are interested only in highlighting "Abstract", we process just the "first page"
        # TODO: Process all the pages in a research paper
        break
    
    # save the annotated document
    pages.save(config.ANNOTATED_FILEPATH+"annotated.pdf", garbage=4, deflate=True, clean=True)
    

if __name__=="__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-ca', '--clip_abstract',
                        action='store_true',
                        default=True,
                        help='If true, clips and saves the annotated abstract as an image file')

    args = vars(parser.parse_args())
    
    filepath="/home/hs/Desktop/Projects/study-buddy/input/1706.03762.pdf"
    main(args, filepath)