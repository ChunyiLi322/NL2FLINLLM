import sys
import os
import random
from collections import Counter

class MetaPathGenerator:
	def __init__(self):
		self.id_lf = dict()  #id_lf key-id  value-lf_name
		self.id_conf = dict() #id_conf key-id  value-conf_name
		self.id_paper = dict()
		self.conf_lf = dict()
		self.lf_conf = dict()
		self.paper_lf = dict()
		self.lf_paper = dict()
		self.conf_paper = dict()
		self.paper_conf = dict()



	def read_data(self, dirpath):
		with open(dirpath + "/id_fl.txt", errors='ignore') as adictfile:
			for line in adictfile:
				toks = line.strip().split("\t")
				if len(toks) == 2:
					self.id_lf[toks[0]] = toks[1].replace(" ", "")


		with open(dirpath + "/id_conf.txt", errors='ignore') as cdictfile:
			for line in cdictfile:
				toks = line.strip().split("\t")
				if len(toks) == 2:
					newconf = toks[1].replace(" ", "")
					self.id_conf[toks[0]] = newconf

		with open(dirpath + "/paper_fl.txt", errors='ignore') as pafile:
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


		with open(dirpath + "/paper_conf.txt", errors='ignore') as pcfile:
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

		# print("------------self.paper_conf----------", self.paper_conf)

		sumpapersconf, sumlfsconf = 0, 0
		conf_lfs = dict()
		for conf in self.conf_paper:
			papers = self.conf_paper[conf]
			sumpapersconf += len(papers)
			for paper in papers:
				if paper in self.paper_lf:
					lfs = self.paper_lf[paper]
					sumlfsconf += len(lfs)

		# print("------------conf_paper----------", self.conf_paper)
        # paper in conf appearance  paper in lf appearance
		print("#confs  ", len(self.conf_paper))
		print("#papers ", sumpapersconf,  "#papers per conf ", sumpapersconf / len(self.conf_paper))
		print("#lfs", sumlfsconf, "#lfs per conf", sumlfsconf / len(self.conf_paper))





	def generate_random_aca(self, outfilename, numwalks, walklength):

		for conf in self.conf_paper:
			self.conf_lf[conf] = []
			for paper in self.conf_paper[conf]:
				if paper not in self.paper_lf: continue
				for lf in self.paper_lf[paper]:
					self.conf_lf[conf].append(lf)
					if lf not in self.lf_conf:
						self.lf_conf[lf] = []
					self.lf_conf[lf].append(conf)

		outfile = open(outfilename, 'w')



		for conf in self.conf_lf:
			conf0 = conf

			# # path conference -> paper -> conference -> paper ->...
			# for j in list(range(0, numwalks)): #wnum walks
			# 	outline = self.id_conf[conf0]
			# 	for i in list(range(0, walklength)):
			# 		lfs = self.conf_lf[conf]
			# 		numa = len(lfs)
			# 		lfid = random.randrange(numa)
			# 		lf = lfs[lfid]
			# 		outline += " " + self.id_lf[lf]
			# 		confs = self.lf_conf[lf]
			# 		numc = len(confs)
			# 		confid = random.randrange(numc)s
			# 		conf = confs[confid]
			# 		outline += " " + self.id_conf[conf]
			# 	outfile.write(outline + "\n")

        # path formal language -> paper -> formal language -> paper ->...
		for lf_index in self.lf_paper:
			lf0 = lf_index
			for j in list(range(0, numwalks)):
				outline = "l"+lf0
				for i in list(range(0, walklength)):
					papers = self.lf_paper[lf0]
					numa = len(papers)
					paperid = random.randrange(numa)
					paper_id= papers[paperid]
					print()
					outline += " " + "p"+str(paper_id)
					lffs = self.paper_lf[paper_id]
					numl = len(lffs)
					lfid = random.randrange(numl)
					lf = lffs[lfid]
					outline += " " + "l"+str(lf)
				outfile.write(outline + "\n")
		outfile.close()


#python py4genMetaPaths.py 100 10 fl_kg   output.kgfl.w100.l10.txt


numwalks = int(sys.argv[1])
walklength = int(sys.argv[2])

dirpath = sys.argv[3]
outfilename = sys.argv[4]

def main():
	mpg = MetaPathGenerator()
	mpg.read_data(dirpath)
	mpg.generate_random_aca(outfilename, numwalks, walklength)


if __name__ == "__main__":
	main()






























