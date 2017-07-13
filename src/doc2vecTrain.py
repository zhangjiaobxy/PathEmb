#!/usr/bin/env python
# -*- coding: utf-8 -*-

# *********************************************************************
# Run doc2vecTrain.py to train a doc2vec model
# *********************************************************************

# import the modules needed to run the script
import gensim.models as g
import logging
import os, sys, subprocess

u = int(sys.argv[1])  # window size
d = int(sys.argv[2])  # feature dimension (vector size)

# vector_size = 50

#doc2vec parameters
# vector_size = 200  # dimensionality of the feature vectors
# window_size = 15  # the maximum distance between the predicted word and context words used for prediction within a document
seed = 23
min_count = 1  # ignore all words with total frequency lower than this
sampling_threshold = 1e-5  #  threshold for configuring which higher-frequency words are randomly downsampled
negative_size = 5  # negative sampling will be used, the int for negative specifies how many “noise words” should be drawn (usually between 5-20).
train_epoch = 20  # number of iterations (epochs) over the corpus. The default inherited from Word2Vec is 5, but values of 10 or 20 are common in published ‘Paragraph Vector’ experiments
dm = 0 #0 = dbow; 1 = dmpv
worker_count = 1 #number of parallel processes

# vector_size_list = [50]
# for vector_size in vector_size_list:
# vector_size = 50

#pretrained word embeddings
# pretrained_emb = "toy_data/pretrained_word_embeddings.txt" #None if use without pretrained embeddings

#input corpus
# train_corpus = "toy_data/train_docs.txt"
train_corpus = './../data/doc2vec/doc2vecFormat.txt'

#output model
# saved_path = "toy_data/model.bin"

saved_path = './../data/doc2vec/doc2vecFormat_train.bin'

#enable logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#train doc2vec model
docs = g.doc2vec.TaggedLineDocument(train_corpus)
# mode without pretrained_emb
model = g.Doc2Vec(docs, size=d, window=u, seed = seed, min_count=min_count, \
	sample=sampling_threshold, workers=worker_count, hs=0, dm=dm, negative=negative_size, dbow_words=1, \
	dm_concat=1, iter=train_epoch)


#save model
model.save(saved_path)
