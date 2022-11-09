import random as rd
import csv
import numpy as np

taille=80
#taille=5
graphe=np.zeros((taille,taille))
with open('p08123_matrix.txt') as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    a=0
    for row in reader:
        b=0
        for i in row:
            graphe[a,b]=int(i)
            b+=1
        a+=1

graphe[taille-1,taille-1]=7981-10**8
#graphe[taille-1,taille-1]=331-10**8
#Initialisation

nb_individus=30
taux_crossing_over=0.2
taux_mutation=0.01
itera_chef=0
itera_chef_max=500
chef=""
prec_chef=""
#score_attendu=2427
score_attendu=427337
meilleur_score=10**10
prec_meilleur_score=10**10
mouvement=[[0,1],[1,0]]

#Genèse
population=[]

for i in range(nb_individus):
	genes=""
	for gene in range(2*taille-2):
		genes+=str(rd.randint(0,1))
	population.append([0,genes])
chef=population[0][1]
prec_chef=population[0][1]


def score(individu):
	x=0
	y=0
	score=graphe[0,0]
	for gene in range(len(individu)):
		x+=mouvement[int(individu[gene])][0]
		y+=mouvement[int(individu[gene])][1]
		if x>taille-1 or y>taille-1:
			score=10**8-gene*10*4
			break
		else:
			score+=graphe[x,y]
	return score

iteration=0
while meilleur_score+10**8!=score_attendu:
	iteration+=1
	#calcul des scores
	for individu in population:
		individu[0]=score(individu[1])
	#élimination des plus mauvais
	population.sort()
	population=population[:nb_individus//2]
	#meilleur_score
	meilleur_score=population[0][0]
	if meilleur_score<prec_meilleur_score:
		prec_meilleur_score=meilleur_score
		print(iteration,":",meilleur_score+10**8,score_attendu)
	#chef
	chef=population[0][1]
	if chef==prec_chef:
		itera_chef+=1
		if itera_chef==itera_chef_max:
			print(iteration,"coup d'etat")
			itera_chef=0
			taux_mutation+=0.01
			actuel_chef=population[0]
			nb_executions=0
			while population.count(actuel_chef)>0:
				nb_executions+=1
				population.remove(actuel_chef)
				genes=""
				for i in range(2*taille-2):
					genes+=str(rd.randint(0,1))
				population.append([0,genes])
			print(nb_executions, len(population))
	else:
		prec_chef=chef
		itera_chef=0
	#on fait les enfants par croisement (crossing-over)
	#on prendre chaque individu 2 à 2, le père (gauche) a une probabilité de taux_crossing_over de donner ses gènes à l'enfant
	#la mutation donne une valeur de gène au hasard, comme dans la genèse
	for rang in range(nb_individus//2):
		genes=population[rang][1]
		nouveau=""
		for ngene in range(len(genes)):
			hasard=rd.random()
			if hasard<taux_mutation:
				nouveau+=str(rd.randint(0,1))
			elif hasard<taux_crossing_over:
				nouveau+=genes[ngene]
			else:
				nouveau+=population[rang+1][1][ngene]
		population.append([0,nouveau])