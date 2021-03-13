from flask import Flask, request, render_template
flask_app = Flask(__name__)

from paper_sampler import Sample
sample = Sample()

@flask_app.route('/', methods=['GET'])
def index_page():
    paper_text = request.args.get('text')
    return paper_text

@flask_app.route('/nextpaper',methods=['GET'])
def get_next_paper():
    paper_text = request.args.get('text')
    next_paper = sample.sample(paper_text)
    print(next_paper)
    return next_paper

@flask_app.route('/encode',methods=['GET'])
def encode():
    pass

if __name__=='__main__':
    flask_app.run(host ='0.0.0.0',port=8081, debug=True)