'''
Genetic algorithm on magic numbers --magic2
'''
import os
import threading
import subprocess
import time
import heapq
import numpy as np
from matplotlib import pyplot as plt

#Number of rounds
rounds = 10
server_file = '/home/hollan/Desktop/mj-1.14-linux-x86_64/mj-server'
player_file = '/home/hollan/Desktop/mj-1.14-linux-x86_64/mj-player'
round_scores = []
new_round_scores = dict()
all_genomes = []
#genomes = {1:[0.1,0.4,0.3,0.8],2:[0.5,0.5,0.1,0.2],3:[0.9,0.9,0.3,0.1],4:[0.2,0.6,0.8,0.0]}
psize = 4
glength = 4
nservers = 10
np.random.seed(1234)
best_strategy = []

rstrat = dict()

os.mkdir('plfiles')
#os.system('cp ga_player.py* _ga* plfiles/')
base_path = os.getcwd()
#start = False

def worker(num,nums):
	#print(str(nums)+str(num))
	#f = open(base_path + '/plfiles/pl'+str(nums)+str(num+1)+'.py','w')
	#f.write('import ga_player\nimport sys\n')
	#f.write('ga_player.get_inits(float(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]))\n')
	#f.write('ga_player.get_address(\'localhost:500'+str(nums)+'\')\n')
	#f.write('ga_player.ga_player_run('+str(num+1)+',\'player'+str(nums)+str(num+1)+'\')')
	#f.close()
	os.system('python plfiles/pl'+str(nums)+str(num+1)+'.py '+str(all_genomes[nums][num+1][0])+' '+str(all_genomes[nums][num+1][1])+' '+str(all_genomes[nums][num+1][2])+' '+str(all_genomes[nums][num+1][3]))
	time.sleep(2)
	#start = True
	#print('thread'+str(num+1)+' started')
	return

def gworker(num,nums):
	p=subprocess.Popen([player_file,'--id',str(num+1),'--name', 'magic'+str(nums)+str(num+1),'--server','localhost:500'+str(nums),'--magic2',base_path + '/plfiles/magicfile'+str(nums)+str(num+1)+'.txt'],stdout=subprocess.PIPE,shell=False)
	#(output,err) = p.communicate()
	#p_status = p.wait()
	while True:
		line = p.stdout.readline()
		if line == '':
			break
		#round_scores.append(line.strip())
	time.sleep(2)
	#round_scores=output
	#round_scores = subprocess.check_output([server_file,'--server','localhost:5000'],stderr=subprocess.STDOUT)
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

def serv2(num):
	p=subprocess.Popen([server_file,'--server','localhost:500'+str(num)],stdout=subprocess.PIPE,shell=False)
	#(output,err) = p.communicate()
	#p_status = p.wait()
	_scores = []
	while True:
		line = p.stdout.readline()
		if line == '':
			break
		_scores.append(line.strip())
	new_round_scores[num]=_scores
	return

def createFiles(psize,nservers):
	for nums in range(nservers):
		for num in range(psize):
			f = open(base_path + '/plfiles/magicfile'+str(nums)+str(num+1)+'.txt','w')
			f.write(str(np.random.uniform(0,1,13).tolist())[1:-1].replace(', ',' '))
			f.close()

'''
Selects the top n performing gonomes for crossover and mutation.
Input is a dictionary with key: 'Name'+'id' and value:'cummulative round score'
Return value is a list of keys starting with the highest to the lowest performing.
'''
def selection(scores_dict,g):
	temp = dict()
	for i in scores_dict.keys():
		if int(i[-2]) == g: temp[i] = scores_dict[i]
	return heapq.nlargest(4,temp,key=temp.get)
'''
Performs crossover of the genomes by crossing the two most performing genomes
and producing two offsprings which replaces the 2 least performing genomes. 
crossover point is the centre of the length of the genome.
Input is the return value of the selection function.
'''
def crossover(selected,g):
	#chop_greater = lambda x:
	#g_old = all_genomes[g].copy()
	s1= int(selected[0][-1])#strong genomes
	s2 = int(selected[1][-1])
	w1 = int(selected[2][-1])#weak genomes
	w2 = int(selected[3][-1])
	s_1 = open(base_path + '/plfiles/magicfile'+str(g)+str(s1)+'.txt')
	s_2 = open(base_path + '/plfiles/magicfile'+str(g)+str(s2)+'.txt')
	w_1 = open(base_path + '/plfiles/magicfile'+str(g)+str(w1)+'.txt','w')
	w_2 = open(base_path + '/plfiles/magicfile'+str(g)+str(w2)+'.txt','w')
	c1 = s_1.readlines()
	c2 = s_2.readlines()
	#c3 = w_1.readlines()
	#c4 = w_2.readlines()
	i_c1 = map(float,c1[0].split(' '))
	i_c2 = map(float,c2[0].split(' '))

	#save best strategy
	#best_strategy.append(all_genomes[g][s1])
	rstrat[g] = c1[0].split(' ')

	#compute mean and variance
	mu = np.mean([i_c1,i_c2],axis=0)
	sigma = np.std([i_c1,i_c2],axis=0)
	i=0
	off1 = []
	off2 = []
	for (u,s) in zip(mu,sigma):
		params = np.random.normal(u,s,2)
		# if i == 0:
		# 	chop_greater = lambda x:1 if x >1 else x
		# 	chop_less = lambda x:-1 if x <-1 else x
		# 	params = map(chop_greater,params)
		# 	params = map(chop_less,params)
		# elif i == 1:
		# 	chop_greater = lambda x:1 if x >1 else x
		# 	chop_less = lambda x:0 if x <0 else x
		# 	params = map(chop_greater,params)
		# 	params = map(chop_less,params)
		# elif i == 2:
		# 	chop_greater = lambda x:1 if x >1 else x
		# 	chop_less = lambda x:0 if x <0 else x
		# 	params = map(chop_greater,params)
		# 	params = map(chop_less,params)
		# elif i == 3:
		# 	chop_greater = lambda x:1 if x >1 else x
		# 	chop_less = lambda x:0 if x <0 else x
		# 	params = map(chop_greater,params)
		# 	params = map(chop_less,params)
		#else: pass
		off1.append(params[0])
		off2.append(params[1])
		#genomes[w1][i] = params[0]
		#genomes[w2][i] = params[1]
		i+=1
	#all_genomes[g][w1] = off1
	#all_genomes[g][w2] = off2
	w_1.write(str(off1)[1:-1].replace(', ',' '))
	w_2.write(str(off2)[1:-1].replace(', ',' '))
	s_1.close()
	s_2.close()
	w_1.close()
	w_2.close()

	#genomes[w1] = genomes[s1][:-2]+genomes[s2][2:]
	#genomes[w2] = genomes[s2][:-2]+genomes[s1][2:]
	#print(g_old)
	#print(all_genomes[g])
	return

def initpop():
	for i in range(nservers):
		genomes = {1:[0.1,0.4,0.3,0.8],2:[0.5,0.5,0.1,0.2],3:[0.9,0.9,0.3,0.1],4:[0.2,0.6,0.8,0.0]}
		for g in range(psize):
			genomes[g+1][0] = np.random.uniform(-1,1)
			genomes[g+1][1] = np.random.uniform(0,1)
			genomes[g+1][2] = np.random.uniform(0,1)
			genomes[g+1][3] = np.random.uniform(0,1)
		all_genomes.append(genomes.copy())

def newplot():
	chowness = {k: [] for k in range(nservers)}
	hiddenness = {k: [] for k in range(nservers)}
	majorness = {k: [] for k in range(nservers)}
	suitness = {k: [] for k in range(nservers)}
	xvals = range(1,rounds+1)
	for s in best_strategy:
		for i in range(nservers):
			chowness[i].append(s[i][0])
			hiddenness[i].append(s[i][1])
			majorness[i].append(s[i][2])
			suitness[i].append(s[i][3])

	f,((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2)
	for i in range(nservers):
		ax1.plot(xvals,chowness[i])
		ax2.plot(xvals,hiddenness[i])
		ax3.plot(xvals,majorness[i])
		ax4.plot(xvals,suitness[i])
	ax1.set_xlabel('Rounds')
	ax1.set_ylabel('Chowness')
	ax2.set_xlabel('Rounds')
	ax2.set_ylabel('Hiddenness')
	ax3.set_xlabel('Rounds')
	ax3.set_ylabel('Majorness')
	ax4.set_xlabel('Rounds')
	ax4.set_ylabel('Suitness')
	plt.tight_layout()
	plt.show()

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

#initpop()
createFiles(psize,nservers)
f = open('Magic_strategies.txt','w')
for r in range(rounds):
	print('Round {}'.format(r+1))
	#s = threading.Thread(target=server)
	#round_scores = []
	servers = []#new added
	new_round_scores = dict()#added now
	for i in range(nservers):#added
		v = threading.Thread(target=serv2,args=(i,))#
		servers.append(v)#
		v.start()#
		#print(i)
	scores = dict()
	#s.start()
	threads = dict()
	for j in range(nservers):
		ts = []
		for i in range(4):
			t = threading.Thread(target=gworker,args=(i,j))
			#threads.append(t)
			ts.append(t)
			t.start()
		threads[j]=ts
	for m in range(nservers):
		for k in threads[m]:
			k.join()
		servers[m].join()
	#s.join()
	for p in range(nservers):
		for l in new_round_scores[p][2:]:
			l= l.split()
			scores[l[1][1:]]=int(l[3])#STOPPED HERE
	#printing round results
		for key in scores.keys():
			print('name: {}\tscore: {}'.format(key,scores[key]))
		crossover(selection(scores,p),p)
	#print(rstrat)
	best_strategy.append(rstrat.copy())
#plotstrategy()
#print('ALL VALUES HERE')
#print(best_strategy)
for i in best_strategy[r-1].keys():
	f.write(best_strategy[r-1][i].__str__()+'\n')
f.close()
newplot()