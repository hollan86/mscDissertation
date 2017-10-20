'''
Single play genetic algorithm
'''
import os
import threading
import subprocess
import time
import heapq
import numpy as np
from matplotlib import pyplot as plt

#Number of rounds
rounds = 15
server_file = '/home/hollan/Desktop/mj-1.14-linux-x86_64/mj-server'
round_scores = []
#new_round_scores = dict()
genomes = {1:[0.1,0.4,0.3,0.8],2:[0.5,0.5,0.1,0.2],3:[0.9,0.9,0.3,0.1],4:[0.2,0.6,0.8,0.0]}
psize = 4
glength = 4
np.random.seed(1234)
best_strategy = []
def worker(num):
	os.system('python pl'+str(num+1)+'.py '+str(genomes[num+1][0])+' '+str(genomes[num+1][1])+' '+str(genomes[num+1][2])+' '+str(genomes[num+1][3]))
	time.sleep(2)
	#print('thread'+str(num+1)+' started')
	return

def server():
	p=subprocess.Popen([server_file,'--server','localhost:5000'],stdout=subprocess.PIPE,shell=False)
	#(output,err) = p.communicate()
	#p_status = p.wait()
	while True:
		line = p.stdout.readline()
		if line == '':
			break
		round_scores.append(line.strip())
	#round_scores=output
	#round_scores = subprocess.check_output([server_file,'--server','localhost:5000'],stderr=subprocess.STDOUT)
	return

# def serv2(num):
# 	p=subprocess.Popen([server_file,'--server','localhost:500'+str(num)],stdout=subprocess.PIPE,shell=False)
# 	#(output,err) = p.communicate()
# 	#p_status = p.wait()
# 	_scores = []
# 	while True:
# 		line = p.stdout.readline()
# 		if line == '':
# 			break
# 		round_scores.append(line.strip())
# 	#new_round_scores[num]=_scores
# 	return

'''
Selects the top n performing gonomes for crossover and mutation.
Input is a dictionary with key: 'Name'+'id' and value:'cummulative round score'
Return value is a list of keys starting with the highest to the lowest performing.
'''
def selection(scores_dict):
	return heapq.nlargest(4,scores_dict,key=scores_dict.get)
'''
Performs crossover of the genomes by crossing the two most performing genomes
and producing two offsprings which replaces the 2 least performing genomes. 
crossover point is the centre of the length of the genome.
Input is the return value of the selection function.
'''
def crossover(selected):
	g_old = genomes.copy()

	s1= int(selected[0][-1])#strong genomes
	s2 = int(selected[1][-1])
	w1 = int(selected[2][-1])#weak genomes
	w2 = int(selected[3][-1])

	#save best strategy
	best_strategy.append(genomes[s1])

	#compute mean and variance
	mu = np.mean([genomes[s1],genomes[s2]],axis=0)
	sigma = np.std([genomes[s1],genomes[s2]],axis=0)
	i=0
	off1 = []
	off2 = []
	for (u,s) in zip(mu,sigma):
		params = np.random.normal(u,s,2)
		off1.append(params[0])
		off2.append(params[1])
		#genomes[w1][i] = params[0]
		#genomes[w2][i] = params[1]
		i+=1
	genomes[w1] = off1
	genomes[w2] = off2
	#genomes[w1] = genomes[s1][:-2]+genomes[s2][2:]
	#genomes[w2] = genomes[s2][:-2]+genomes[s1][2:]
	print(g_old)
	print(genomes)
	return

def initpop():
	for g in range(psize):
		genomes[g+1][0] = np.random.uniform(-1,1)
		genomes[g+1][1] = np.random.uniform(0,1)
		genomes[g+1][2] = np.random.uniform(0,1)
		genomes[g+1][3] = np.random.uniform(0,1)

def plotstrategy():
	chowness = []
	hiddenness = []
	majorness = []
	suitness = []
	rounds = []
	i = 1
	for s in best_strategy:
		chowness.append(s[0])
		hiddenness.append(s[1])
		majorness.append(s[2])
		suitness.append(s[3])
		rounds.append(i)
		i+=1
		
	f,((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2)
	ax1.plot(rounds,chowness)
	ax1.set_xlabel('Rounds')
	ax1.set_ylabel('Chowness')
	ax2.plot(rounds,hiddenness)
	ax2.set_xlabel('Rounds')
	ax2.set_ylabel('Hiddenness')
	ax3.plot(rounds,majorness)
	ax3.set_xlabel('Rounds')
	ax3.set_ylabel('Majorness')
	ax4.plot(rounds,suitness)
	ax4.set_xlabel('Rounds')
	ax4.set_ylabel('Suitness')
	plt.tight_layout()
	plt.show()

initpop()
for r in range(rounds):
	print('Round {}'.format(r+1))
	s = threading.Thread(target=server)
	round_scores = []
	# servers = []#new added
	# new_round_scores = dict()#added now
	# for i in range(10):#added
	# 	v = threading.Thread(target=serv2(i))#
	# 	servers.append(v)#
	# 	v.start()#
	scores = dict()
	s.start()
	threads = []
	for i in range(4):
		t = threading.Thread(target=worker,args=(i,))
		threads.append(t)
		t.start()
	for m in threads:
		m.join()
	s.join()
	for l in round_scores[2:]:
		l= l.split()
		scores[l[1][1:]]=int(l[3])
	#printing round results
	for key in scores.keys():
		print('name: {}\tscore: {}'.format(key,scores[key]))
	crossover(selection(scores))
plotstrategy()