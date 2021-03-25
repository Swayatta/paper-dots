<p align="center">
  <br>
  <img  src="docs/logo3.png" width=500>
  </br>
</p>

<p align="center">
  <br>
    <a href="https://travis-ci.com/harshit158/paper-insights">
        <img alt="Build" src="https://travis-ci.com/harshit158/paper-insights.svg?branch=main">
    </a>
    <a href="https://img.shields.io/github/issues/harshit158/paper-insights">
        <img alt="Issues" src="https://img.shields.io/github/issues/harshit158/paper-insights">
    </a>
    <a href="https://img.shields.io/github/license/harshit158/paper-insights">
        <img alt="License" src="https://img.shields.io/github/license/harshit158/paper-insights">
    </a>
  </br>
</p>

## What is Paper Dots ?
Paper Dots is an automatic insights extraction tool from research papers, which 
* Automatically annotates a research paper PDF with important keyphrases, ensuring faster skim-reading of papers
* Builds cumulative Knowledge Graph on top of papers read so far, helping in tracking important concepts
* Delivers relevant papers continuously through mail, promoting consistent and directed learning

The end-to-end pipeline is shown below:

<p align="center">
  <img  src="docs/pipeline.png">
</p>

## Approach
There are 3 main components to the project:
* **Keyphrase Extraction**
* **Knowledge Graph construction**
* **Paper sampling**

The papers are sampled from [Arxiv corpus](https://www.kaggle.com/Cornell-University/arxiv) (hosted on Kaggle). To enable semantic search over the papers, we had to first obtain the embeddings for each of the papers in the corpus, for which we used [Sentence-Transformers](https://github.com/UKPLab/sentence-transformers).  
The corpus embeddings are available and can be downloaded from [here](https://drive.google.com/file/d/1EDdcti5J0y4L1jvuiEdpKAHDkGfJf7LT/view?usp=sharing) for research purposes.  
Once the corpus embeddings are in place, a new paper can be sampled from the corpus using the seed paper as follows:  


<p align="center">
  <img  src="docs/paper-sampling.png">
</p>

## How to use ?
Currently, the end-to-end pipeline is not open for public use (coming very soon) but individual components can be used as follows:

## How to contribute ?
Feel free to raise requests for new features :)

## Contact

## References

## License