# Formal Specification Generation via Prompt-based Large Language Models

This is a Tensorflow implementation of [Formal Specification Generation via Prompt-based
Large Language Models]. If you want to replicate the experimental results, please use the follow code.    

#### For any clarification, comments or suggestions please create an issue or contact [Incognito mode temporarily.].

## Install necessary dependencies.

​	-> Dependencies can be installed using `requirements.txt`.

​	-> Install the dependencies by `pip3 install -r requirements.txt`.

## Dataset

        -> The dataset for graph learning is located in the "/fl_kg" directory, which contains five files corresponding to:

         1) Keywords commonly appearing in papers along with their indices.
         2) Formal languages along with their indices.
         3) Conferences along with their indices.
         4) The relationship between keywords commonly appearing in papers and formal languages.
         5) The relationship between keywords commonly appearing in papers and conferences.

​	-> The dataset for formal language generation that need to be converted is located in the "/formal_dataset" folder. It encompasses all the natural language requirements utilized in our experiments in this paper.

## Train our model

​	-> Firstly, we should read the graph dataset and generate random walk paths. You can run
​	`python pathgeneration.py 1000 10 fl_kg output.kgfl.w1000.l10.txt`

​	-> Then, we utilize the graph learning model to generate embedding representations of formal knowledge based on the paths. You can run

        `python graphlearn.py -file output.kgfl.w1000.l10.txt -embed_dim 128 -epoch 10 -types lp -outname embeddings`
W
​	where `-file` specifies the walk paths, `-types lq` gives a description of all the types appearing in the dataset (i.e. nodes start with 'l' or 'q'). 

​	-> Finally, we generate prompts for the large model. You can run

        `python promptgeneration.py -search_word 'Linear Temporal Logic' -embed_dim 128 -dirpath 'fl_kg' -step 4 -embedding_file 'output/embeddings'` 

## Output

​	-> The generated prompts will be put in `./output/prompts`.  You can input both the prompts and the natural language requirement texts into the large language model to obtain the final LTL formula.



