#!/usr/bin/env python
# -*- coding: utf-8 -*-

# *********************************************************************
# Run doc2vecInfer.py to infer document vectors from trained doc2vec model
# *********************************************************************

# import the modules needed to run the script
import gensim.models as g
import codecs
# import os, sys, subprocess

# d = int(sys.argv[1])  # feature dimension (vector size)
#parameters
# model="toy_data/model.bin"
# test_docs="toy_data/test_docs.txt"
# output_file="toy_data/test_vectors.txt"

# dim =50
# dimList = [50]
# for dim in dimList:


model='./../data/doc2vec/doc2vecFormat_train.bin'
test_docs='./../data/doc2vec/doc2vecFormat.txt'
output_file='./../data/doc2vec/doc2vecFormat_infer.txt'


#inference hyper-parameters
start_alpha=0.01
infer_epoch=1000

#load model
m = g.Doc2Vec.load(model)
test_docs = [ x.strip().split() for x in codecs.open(test_docs, "r", "utf-8").readlines() ]

#infer test vectors
output = open(output_file, "w")
for d in test_docs:
    output.write( " ".join([str(x) for x in m.infer_vector(d, alpha=start_alpha, steps=infer_epoch)]) + "\n" )
output.flush()
output.close()
