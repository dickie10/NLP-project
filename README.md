# Claim Verification and Evidence Extraction Using BERT

## Description

Welcome to the repository for Claim Verification and Evidence Extraction using BERT. This project aims to provide a robust system for verifying claims and extracting supporting evidence by leveraging advanced natural language processing techniques.

## Instructions

1. **Top Documents Retrieval**: To retrieve top documents, please navigate to the `Top_documents` directory and execute the `data_par2` script. Ensure that SQLite is installed on your system for proper functionality.

2. **Download Wikipedia Dump 2017**:
   - Download the Wikipedia dump from [this link](https://fever.ai/download/fever/wiki-pages.zip). This dataset provides essential background information and context for claim verification and evidence extraction.

3. **Download Noun Phrase Documents**:
   - Access the noun phrase documents from [this source](https://public.ukp.informatik.tu-darmstadt.de/fever-2018-team-athene/document_retrieval_datasets.zip). These documents are crucial for identifying and extracting relevant entities and phrases associated with the claims.
   
## Running the Model

To run the sentence retrieval and claim verification, please execute the `Bert_Final.ipynb` notebook on a GPU for optimal performance.


## tf-iDF Model

NOTE: This model uses the FEVER 1.0 Dataset from 2018

Step 1: Downlaod the Wikipedia dataset from the FEVER website and unpack in "wiki-pages" folder within the repo. [source](https://fever.ai/dataset/fever.html)

Step 2: download the train.jsonl file from the FEVER website in the main repo folder [source](https://fever.ai/dataset/fever.html)

IMPORTANT for Step 3

NOTE: "simplified_wiki.jsonl" is appended, not overwriten. Hence if the file already exists before running the code, it will lead to data duplication!!

Step 3: Run Data_Preprocessing.ipynb to generate "simplified_wiki.jsonl" and "populated_samples.jsonl" files

Step 4: Run Document_and_Sentence_Retrieval.ipynb to generate train and test data.

Step 5: Run MLP_FEVER.ipynb

Step x: To test accuracy without having to generate data, we have provided a stripped down version of the Retrieval code which only calculates the Retrieval Accuracy. This can be found at Retrieval_Accuracy.ipynb

All files have relevant instructions in the first cell of the ipython files.


