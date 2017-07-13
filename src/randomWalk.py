#!/usr/bin/env python
# -*- coding: utf-8 -*-

# *********************************************************************
# Run randomWalk.py to get random walks for each vertex.
# This code is a revised version for node2vec of author Aditya Grover. 
# For more details of node2vec, refer to the paper: 
# node2vec: Scalable Feature Learning for Networks.
# Knowledge Discovery and Data Mining (KDD), 2016.
# *********************************************************************

# import the modules needed to run the script
import os, sys, subprocess



import argparse
import numpy as np
import networkx as nx
import node2vec, os
from gensim.models import Word2Vec

if not os.path.exists('./../data/randomWalks/'):
	os.makedirs('./../data/randomWalks/')
# if not os.path.exists('./../data/embs/'):
# 	os.makedirs('./../data/embs/')

inputDir = './../data/rawData/'
fl=os.listdir(inputDir)  # input file list
for f in fl:
	if f.endswith('.txt'):
		# print f
		def parse_args():
			'''
			Parses the node2vec arguments.
			'''
			parser = argparse.ArgumentParser(description="Run node2vec.")

			parser.add_argument('--input', nargs='?', default=inputDir+f,
			                    help='Input graph path')

			# parser.add_argument('--output', nargs='?', default='./../data/embs/'+f.replace('.txt', '.embs'),
			#                     help='Embeddings path')

			parser.add_argument('--randomWalks', nargs='?', default='./../data/randomWalks/'+f.replace('.txt', '.walks'),
		                    	help='random walks path')

			parser.add_argument('--dimensions', type=int, default=128,
			                    help='Number of dimensions. Default is 128.')

			parser.add_argument('--l', type=int, default=30,
			                    help='Length of walk per source. Default is 80.')  # length of walk per node

			parser.add_argument('--r', type=int, default=5,
			                    help='Number of walks per source. Default is 10.')  # number of walks per node

			parser.add_argument('--window-size', type=int, default=10,
		                    	help='Context size for optimization. Default is 10.')

			parser.add_argument('--iter', default=1, type=int,
		                      help='Number of epochs in SGD')

			parser.add_argument('--workers', type=int, default=8,
			                    help='Number of parallel workers. Default is 8.')

			parser.add_argument('--p', type=float, default=1,
			                    help='Return hyperparameter. Default is 1.')

			parser.add_argument('--h', type=float, default=1,
			                    help='Inout hyperparameter. Default is 1.')

			parser.add_argument('--weighted', dest='weighted', action='store_true',
			                    help='Boolean specifying (un)weighted. Default is unweighted.')
			parser.add_argument('--unweighted', dest='unweighted', action='store_false')
			parser.set_defaults(weighted=True)

			parser.add_argument('--directed', dest='directed', action='store_true',
			                    help='Graph is (un)directed. Default is undirected.')
			parser.add_argument('--undirected', dest='undirected', action='store_false')
			parser.set_defaults(directed=False)

			return parser.parse_args()

		def read_graph():
			'''
			Reads the input network in networkx.
			'''
			if args.weighted:
				G = nx.read_edgelist(args.input, nodetype=int, data=(('weight',float),), create_using=nx.DiGraph())
			else:
				G = nx.read_edgelist(args.input, nodetype=int, create_using=nx.DiGraph())
				for edge in G.edges():
					G[edge[0]][edge[1]]['weight'] = 1
					# print edge

			if not args.directed:
				G = G.to_undirected()

			return G

		def learn_embeddings(walks):
			'''
			Learn embeddings by optimizing the Skipgram objective using SGD.
			'''

			# print '=============================\n'  # zj add
			# # print walks  # zj add
			# print 'length of walks: ' + str(len(walks))
			# # print args.randomWalks
			# print '\n============================='  # zj add
			
			walks = [map(str, walk) for walk in walks]
			# model = Word2Vec(walks, size=args.dimensions, window=args.window_size, min_count=0, sg=1, workers=args.workers, iter=args.iter)
			# model.save_word2vec_format(args.output)
			# model.wv.save_word2vec_format(args.output)  # changed line88 to line 89, according to the warning error
			
			# zj add
			with open(args.randomWalks, 'w') as fw:
				for e_walk in walks:
					# print e_walk
					for e_node in e_walk:
						# print e_node
						fw.write(e_node + ' ')
					fw.write('. ')
			fw.close()


			return

		def main(args):
			'''
			Pipeline for representational learning for all nodes in a graph.
			'''
			nx_G = read_graph()
			G = node2vec.Graph(nx_G, args.directed, args.p, args.h)
			G.preprocess_transition_probs()
			walks = G.simulate_walks(args.r, args.l)
			learn_embeddings(walks)



		if __name__ == "__main__":
			args = parse_args()
			main(args)
