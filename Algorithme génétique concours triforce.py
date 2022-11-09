from math import *
from cmath import *
import numpy as np
import random as rd

##############
# PARAMETRES #
##############
NB_INDIVIDUS = 20       # Nombre d'individus par génération
PC_ENJAMBEMENT = 0.15   # Pourcentage de gènes passées entre les parents pour créer les enfants
CHANCE_DE_MUTER = 1     # Chance entre 0 et 1 qu'un gène soit muté au hasard
GENE_BLQ_MAX = 500      # Nombre de générations d'affilé max avec le même meilleur individu à sa tête
NB_BEST_KEEP = 1        # Nombre de couples d'individus parmi les meilleurs qui sont conservés d'une génération à l'autre
NB_COUPLE_ALEA = 0      # Nombre de couples tirés aléatoirement pour remplacer les plus mauvais
NB_BEST = 0             # Nombre de "bons individus" à inclure dans la génération de départ

###################
# INITIALISATIONS #
###################
NB_PTS = 82			# Choix purement arbitraire mais nécessaire car la solution optimale semble comporter de nombreuses gênes. Il vaut mieux trop que pas assez...
I_SCORE = NB_PTS		# Le score associé à chaque individu est ajouté à cet indice, à la suite de ses gènes
I_BEST = 0				# Indice de l'individu avec le meilleur core lorsque les individus sont classés
I_WORST = NB_INDIVIDUS-1# Indice de l'individu avec le moins bons core lorsque les individus sont classés
best = -10000			# Score du meilleur individu actuel
old_best = -10000		# Valeur de l'ancien meilleur score
i_generation = 0		# Indice de la génération actuelle
nb_gene_bloq = 0		# Nombre de générations consécutives avec le même meilleur individu
Pop_Best = []  			# Pour sauvegarder la meilleure population
NB_GENES = int(NB_PTS*PC_ENJAMBEMENT)  # Nombre de gènes qui vont être permutés de mère à père pour créer fils et fille

w = 65537  
a = 31

# Création du vecteur contenant les fameuses Dragon Balls !
dbz = [0j]
for i in range(1, 9):
  a = (75*a)%w
  dbz += [((8*a/w-4)/3)]
  a = (75*a)%w
  dbz[i] += 1j*(2*a/w-1)
  dbz[i] = abs(dbz[i])+1j*phase(dbz[i])*pi/phase(-1)
#print(dbz)

##########
# GENESE #
##########
# Création de la génération originelle : Adam, Eve et leurs amis (complètement au hasard)
Pop = np.random.uniform(low=-1, high=1, size=(NB_INDIVIDUS, NB_PTS+1))
#print(Pop[0])
#en partant d'un résultat d'un autre concurrent :
#Pop[0]=[0.14511,0.001,0.001,-0.001,0.51,0.001,0.508,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,-0.329,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.41,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,-0.619,0.001,0.001,.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,-0.148,0.001,0.001,0.001,0.001,0.001,0.001,0.001,-0.219,0.001,0.001,0.0042,0.416,0,0,0,0,0,0,0]
#Pop[1]=[0.142578125,0.001953125,0.001953125,0.080078125,0.09375,0.294921875,0.556640625,-0.03125,-0.01953125,-0.087890625,-0.0546875,-0.05859375,-0.041015625,-0.01953125,-0.00390625,-0.01953125,-0.015625,0.0,-0.009765625,-0.001953125,0.00390625,0.001953125,0.0078125,0.025390625,0.0,0.005859375,0.015625,0.013671875,0.0078125,0.0078125,0.03515625,0.0546875,0.041015625,0.029296875,0.01171875,0.08984375,0.119140625,-0.171875,-0.119140625,-0.025390625,-0.12890625,-0.076171875,-0.037109375,-0.05859375,-0.056640625,-0.0078125,-0.009765625,-0.0390625,-0.013671875,-0.009765625,-0.00390625,-0.0078125,-0.001953125,0.001953125,-0.009765625,-0.0078125,0.0,0.001953125,0.0078125,0.005859375,0.00390625,0.0234375,0.025390625,0.03125,0.0234375,0.060546875,0.009765625,-0.36328125,-0.326171875]
#Pop[2]=[0,0,0,0,0,0,0,0.0009,0.0001,0.0034,0.0058,0.132,0.0472,0.0494,0.0191,0.1857,0.5506,0.1786,-0.0727,-0.0374,-0.0566,-0.0242,-0.0253,-0.028,-0.0067,-0.0338,-0.0261,-0.0142,-0.0066,-0.0031,-0.0102,-0.0039,0.0021,0.0034,0.0024,0.016,0.0043,0.0149,0.0203,0.0058,0.0428,0.0408,0.0304,0.0611,0.0722,0.0189,0.0164,0.1039,-0.2058,-0.1009,-0.0508,-0.0953,-0.0558,-0.0286,-0.039,-0.0412,-0.0075,-0.0231,-0.0383,-0.0124,-0.0062,-0.0284,-0.0166,-0.0113,-0.0044,-0.0034,0.0002,0.0004,0.0108,0.0009,0.0078,0.0083,0.003,0.0153,0.0043,0.0058,0.0131,0.0088,0.0413,0.0241,0.0462,-0.3781,-0.322900001]
while(True):
    ##############
    # EVALUATION #
    ##############
    # Calcul du score pour chaque individu de la population
    scores = [0]*NB_INDIVIDUS
    for i_IND in range(NB_INDIVIDUS):
       db = np.copy(dbz)
       a = 62916
       z = 0j
       best_ind = -10000;
       
       for i_PTS in range(NB_PTS):  
          
          t = z
          a = (75*a)%w
          z = z + Pop[i_IND][i_PTS] + 1j*(.04+a/w)/(9*abs(z.real)+1)
          scores[i_IND] -= 500*abs(z.real*e**(1j*z.imag)-t.real*e**(1j*t.imag))

          for i in range(9):
            if i==0 and db[0].imag==8 and z.real*t.real<=0 or i>0 and pi>=db[i].imag and .085>=abs(z.real*e**(1j*z.imag)-db[i].real*e**(1j*db[i].imag)):
              if i>0:
                db[i] = db[i].real+1j*(2*pi+db[i].imag)
              db[0] = 1j+1j*db[0].imag
              scores[i_IND] += 500*(3-min(1,abs(z.real*e**(1j*z.imag)-db[i].real*e**(1j*db[i].imag)))-min(1,abs(z.real-db[i].real))) 

		  # Détection d'un nouveau meilleur score. Celui-ci peut ne pas utiliser toutes les gènes d'un individu
          if scores[i_IND] > old_best:
            old_best = scores[i_IND]
            print("G#"+str(i_generation) +" SCORE=" + str(scores[i_IND]))
            #print(*Pop[i_IND,0:(i_PTS+1)], sep = ", ")  
          if scores[i_IND] > best_ind:
            best_ind = scores[i_IND]
			
	   # Sauvegarde du meilleur score d'un individu parmi tous les scores calculés avec ses gènes successives	
       scores[i_IND] = best_ind
	   
    # Tri de la population du meilleur individu au moins bon, en fonction de son score
    Pop = Pop[np.argsort(scores)[::-1]]
    
    # Le meilleur score de la population est sauvegardé
    best = scores[I_BEST]
    
    # Les scores sont récupérés et décalés de sorte que le moins bon vale 0 (pas de score négatif)
    scores = [x-scores[I_WORST] for x in scores]

    # Un certain nombre des meilleurs/pires couples sont gardés, les autres sont remplacés par leur descendance
    for i_couple in range(NB_BEST_KEEP, int(NB_INDIVIDUS/2)):
        if i_couple < int(NB_INDIVIDUS/2)-NB_COUPLE_ALEA:
           ####################################
           # SELECTION PAR ROUE DE LA FORTUNE #
           ####################################
           # Tirage aléatoire de deux parents, proportionnelement à leur score (plus le score est élevé, plus le parent a de chance d'être tiré)
           tirage_m = rd.random()*sum(scores)
           tirage_f = rd.random()*sum(scores)
           i_mother = -1
           i_father = -1
           for i_ind in range(NB_INDIVIDUS):
              if ((i_mother==-1) and (tirage_m > scores[i_ind])):
                 i_mother = i_ind
              if ((i_father==-1) and (tirage_f > scores[i_ind])):
                 i_father = i_ind
              if (i_mother!=-1) and (i_father!=1):
                 break
           father = Pop[i_father]
           mother = Pop[i_mother]
           
           ##############
           # CROISEMENT #
           ##############
           # Tirage aléatoire de l'indice du premier gène qui sera permuté
           i_jambe  = rd.randint(0,NB_PTS)
           #Création et ajout à la nouvelle génération des fils et filles à partir des parents
           if i_jambe+NB_GENES<=NB_PTS:
              Pop[2*i_couple  ][0:NB_PTS] = np.append(father[0:i_jambe], np.append(mother[i_jambe:i_jambe+NB_GENES], father[i_jambe+NB_GENES:NB_PTS]))
              Pop[2*i_couple+1][0:NB_PTS] = np.append(mother[0:i_jambe], np.append(father[i_jambe:i_jambe+NB_GENES], mother[i_jambe+NB_GENES:NB_PTS]))
           else:
              Pop[2*i_couple  ][0:NB_PTS] = np.append(mother[0:NB_GENES-NB_PTS+i_jambe], np.append(father[NB_GENES-NB_PTS+i_jambe:i_jambe], mother[i_jambe:NB_PTS]))
              Pop[2*i_couple+1][0:NB_PTS] = np.append(father[0:NB_GENES-NB_PTS+i_jambe], np.append(mother[NB_GENES-NB_PTS+i_jambe:i_jambe], father[i_jambe:NB_PTS]))
              
           ############
           # MUTATION #
           ############
           # Certains enfants ont de la chance et l'un de leurs gènes mute à une valeur au hasard
           if (rd.random() < CHANCE_DE_MUTER):
              Pop[2*i_couple  ][rd.randint(0,NB_PTS)] = rd.random()*2-1
              Pop[2*i_couple+1][rd.randint(0,NB_PTS)] = rd.random()*2-1
              
        else:
           # Les derniers couples de la génération actuelle sont remplacés par des individus aléatoires
           Pop[2*i_couple  ] = np.random.uniform(low=-1, high=1, size=(1, NB_PTS+1))
           Pop[2*i_couple+1] = np.random.uniform(low=-1, high=1, size=(1, NB_PTS+1))
     
    #############################
    # CONTROLE DE LA POPULATION #
    #############################
    # Le nombre de générations gouvernées par le même individu est compté. S'il reste plus de X générations au pouvoir, on l'y laisse mais change tous les autres
    if (old_best == best):
        nb_gene_bloq += 1
        
        if nb_gene_bloq >= GENE_BLQ_MAX:     
           Best = Pop[I_BEST]
           Pop = np.random.uniform(low=-1, high=1, size=(NB_INDIVIDUS, NB_PTS+1))
           Pop[I_BEST] = Best;
           nb_gene_bloq = 0
           #print('BIM')      

    else:
        nb_gene_bloq = 0
		
    i_generation += 1
