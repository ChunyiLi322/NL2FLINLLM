# coding: utf-8

import numpy as np
import argparse
from helper import getData, writeData, set_gpu
from random import choices
from time import time

class promtGeneration():
    def __init__(self,args):
        self.embedding_file = args.embedding_file
        self.embedding_dict = dict()
        self.embedding_dict2 = dict()
        self.id_conf = dict()
        self.emd_size = args.embed_dim
        self.type_dict = dict()
        self.dirpath = args.dirpath
        self.id_lf = dict()
        self.id_paper = dict()
        self.paper_conf = dict()
        self.paper_lf = dict()
        self.conf_paper = dict()
        self.lf_paper = dict()
        self.max_id = 0
        self.search_word=args.search_word
        self.step = args.step


    def mask_adj_matrix(self, dict):
        for key in dict:
            value = dict[key]
            for i in value:
               self.adj_matrix[int(key)][int(i)] = 1

    # create adj_matrix
    def load_embedding_dict(self):
        # reading embedding to dictionary
        with open(self.embedding_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip().split(" ")
                key = line[0][1:]
                key2 = line[0]
                vector = [float(x) for x in line[1:]]
                self.embedding_dict[key] = vector
                self.embedding_dict2[key2] = vector

        # node type dict
        for key in self.embedding_dict2.keys():
            first_letter = key[0]
            number_value = int(key[1:])
            if first_letter in self.type_dict:
                self.type_dict[first_letter].append(number_value)
            else:
                self.type_dict[first_letter] = [number_value]
        # print("-------------self.type_dict--------------",self.type_dict)

        # adj_matrix
        self.max_id = max(int(val) for val in self.id_conf.keys())
        self.adj_matrix = np.zeros((self.max_id+1, self.max_id+1), dtype=int)

        self.mask_adj_matrix(self.paper_conf)
        self.mask_adj_matrix(self.paper_lf)
        self.mask_adj_matrix(self.conf_paper)
        self.mask_adj_matrix(self.lf_paper)
        # print("-------------self.adj_matrix--------------", self.adj_matrix.shape)
        # print("-------------self.adj_matrix--------------", self.adj_matrix)

        # count adj_matrix linkage
        # count = 0
        # for row in self.adj_matrix:
        #     for element in row:
        #         if element > 0:
        #             count += 1
        # print("-------------count--------------", count)

    def compute_embedding_cos_matrix(self):
        #embedding dict to matrix
        self.cos_matrix = np.zeros((self.max_id+1, self.emd_size), dtype=float)
        for key in self.embedding_dict:
            values = self.embedding_dict[key]
            for index,value in enumerate(values):
                self.cos_matrix[int(key)][index] = value
        self.similarity_matrix = np.dot(self.cos_matrix, self.cos_matrix.T)
        norms = np.linalg.norm(self.cos_matrix, axis=1, keepdims=True)
        zero_indices = np.where(norms == 0)[0]
        norms[zero_indices] = 1
        self.similarity_matrix /= np.dot(norms, norms.T)
        self.similarity_matrix = (self.similarity_matrix + 1) / 2
        # print("-------------self.similarity_matrix--------------", self.similarity_matrix[10][128], self.similarity_matrix[128][10], self.similarity_matrix[106][10])




    def load_dataset(self):
        with open(self.dirpath + "/id_conf.txt", errors='ignore') as cdictfile:
            for line in cdictfile:
                toks = line.strip().split("\t")
                if len(toks) == 2:
                    newconf = toks[1].replace(" ", "")
                    self.id_conf[toks[0]] = newconf
        with open(self.dirpath + "/paper_fl.txt", errors='ignore') as pafile:
            for line in pafile:
                toks = line.strip().split("\t")
                if len(toks) == 2:
                    p, a = toks[0], toks[1]
                    if p not in self.paper_lf:
                        self.paper_lf[p] = []
                    self.paper_lf[p].append(a)
                    if a not in self.lf_paper:
                        self.lf_paper[a] = []
                    self.lf_paper[a].append(p)
        with open(self.dirpath + "/paper_conf.txt", errors='ignore') as pcfile:
            for line in pcfile:
                toks = line.strip().split("\t")
                if len(toks) == 2:
                    p, c = toks[0], toks[1]
                    if p not in self.paper_conf:
                        self.paper_conf[p] = []
                    self.paper_conf[p].append(c)
                    if c not in self.conf_paper:
                        self.conf_paper[c] = []
                    self.conf_paper[c].append(p)

        with open(self.dirpath + "/id_fl.txt", errors='ignore') as adictfile:
            for line in adictfile:
                toks = line.strip().split("\t")
                if len(toks) == 2:
                    self.id_lf[toks[1]] = toks[0]

        with open(self.dirpath + "/paper.txt", errors='ignore') as adictfile:
            for line in adictfile:
                toks = line.strip().split("\t")
                if len(toks) == 2:
                    self.id_paper[toks[0]] = toks[1]




    def get_similar_nodes_sorted(self, begin_word_id):
        linked_nodes = []
        for i in range(len(self.adj_matrix[begin_word_id])):
            if self.adj_matrix[begin_word_id][i] == 1:
                linked_nodes.append(i)
        linked_nodes.sort(key=lambda x: self.similarity_matrix[begin_word_id][x], reverse=True)
        return linked_nodes


    def generate_prompt(self):
        begin_word_id = int(self.id_lf[self.search_word])
        prompt = 'You are a mature formal professional scholar with knowledge of ' + self.search_word + '.'
        record_word_list =  []
        for step_i in range(self.step):
            get_similar_nodes_list = self.get_similar_nodes_sorted(begin_word_id)
            for i in get_similar_nodes_list:
                # print("-------------self.type_dict--------------", self.type_dict)
                if i in self.type_dict['p'] and self.id_paper[str(i)] not in record_word_list:
                    prompt = prompt + "You are knowledgeable in " + self.id_paper[str(i)] + '.'
                    record_word_list.append(self.id_paper[str(i)])
                    break
        with open("output/prompts.txt", "w") as file:
            file.write(prompt + "Please answer the " + self.search_word + " logical formula of the requirement text, the formulas are all wrapped in $ $, and explain the meaning of the logic formula.")




if __name__=='__main__':
    parser = argparse.ArgumentParser(description='promtGeneration')

    parser.add_argument('-embed_dim',   dest='embed_dim',   default=64,   type=int, help='The length of latent embedding')
    parser.add_argument('-gpu', dest='gpu', default='0', help='Run the model on gpu')
    parser.add_argument('-search_word',  dest='search_word', default='Linear Temporal Logic', type=str, help='Word to search for')
    parser.add_argument('-embedding_file',      dest='embedding_file',    default='output/embeddings', help='Name of the output file.')
    parser.add_argument('-dirpath',      dest='dirpath', default='fl_kg', help='Name of the dataset file.')
    parser.add_argument('-step', dest='step', default=4, type=int, help='Number of the prompts.')

    args = parser.parse_args()
    set_gpu(args.gpu)
    promtGeneratior = promtGeneration(args)

    promtGeneratior.load_dataset()
    promtGeneratior.load_embedding_dict()
    promtGeneratior.compute_embedding_cos_matrix()
    promtGeneratior.generate_prompt()
