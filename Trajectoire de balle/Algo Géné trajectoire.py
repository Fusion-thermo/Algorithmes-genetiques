import random as rd
from math import pi, cos, tan


#Initialisation

nb_individus=30
taux_crossing_over=0.2
#ici taux de mutation très élevé. Sans les mutations on serait limité par la meilleure version de chaque gène
#créée lors de la genèse. Les mutations permettent de donner des allèles encore meilleur.
taux_mutation=0.1
score_max=2.5
meilleur_score=0
prec_meilleur_score=0
vitesse_depart_max=5

#Genèse
#Chaque individu possède deux gènes : son angle de départ compris entre 0 et pi/2, et sa vitesse initiale comprise entre 0 et 5
#la première case est le score, c'est juste pour pouvoir trier grâce aux listes
population=[]
for i in range(nb_individus):
	population.append([0,rd.random()*pi/2,rd.random()*vitesse_depart_max])


#équation de trajectoire avec angle et vitesse initiale, mais position initiale à (0,0)
#g=10
#la courbe est sur l'axe des abscisse en x=0 et x=b/a
#représentation en pourcentage, plus clair
def score(individu):
	a= 5 /(individu[2]**2 * cos(individu[1])**2)
	b=tan(individu[1])
	return 100*b/(score_max*a)


#générations
iteration=0
while meilleur_score<99.99:
	iteration+=1
	#on calcule leur score
	for individu in population:
		individu[0]=score(individu)
	#on supprime la moitié la moins performante
	"""for i in range(nb_individus//2):
		population.pop(min(population))"""
	population.sort()
	population=population[nb_individus//2:]
	meilleur_score=population[-1][0]
	if meilleur_score>prec_meilleur_score:
		prec_meilleur_score=meilleur_score
		print(iteration,"\n", meilleur_score, ":\n",population[-1],"\n",[100,pi/4,5],'\n')
	#on fait les enfants par croisement
	#on prendre chaque individu 2 à 2, le père (gauche) a une probabilité de taux_crossing_over de donner ses gènes à l'enfant
	#la mutation donne une valeur de gène au hasard, comme dans la genèse
	for rang in range(nb_individus//2):
		r1=rd.random()
		r2=rd.random()
		if r1<taux_mutation:
			angle=rd.random()*pi/2
		elif r1<taux_crossing_over:
			angle=population[rang][1]
		else:
			angle=population[rang+1][1]

		if r2<taux_mutation:
			vitesse=rd.random()*vitesse_depart_max
		elif r2<taux_crossing_over:
			vitesse=population[rang][2]
		else:
			vitesse=population[rang+1][2]

		population.append([0,angle,vitesse])