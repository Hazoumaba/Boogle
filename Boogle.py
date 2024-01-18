# -*- coding: utf-8 -*-
"""
Créé le mardi ‎28 ‎février ‎2023, ‏‎19:04:34

@auteurs:       Hippolyte Audet-Lagacé, Ben Amor Hazem

Nom du fichier: Boggle.py

Description:    Jeu de Boggle.

                Les fonctions principales demandés ont étés subdivisés pour
                améliorer la clarté et garder les fonction le plus possible
                focussé sur un objectif singulier.

                La fonction jouer() demandée fait appel à deux fonctions 
                additionnelles, qui visent à mieux subdiviser les tâches
                accomplies. ces fonctions sont:
                    deroulement(nb_de_joueurs), qui se concentre sur le
                    déroulement de la partie, soir les entrés de mots des 
                    joueurs.
                    afficher_fin() 
                    
                La fonction generer_grille(taille) fait appel a une fonction 
                séparée afficher_grille(tableau). La fonction afficher_grille 
                est une série de print qui vise a bien afficher la grille aux 
                joueurs.
                
                La fonction calcul_points(grille,mots) fait appel a une 
                fonction point_mot(mots) pour calculer la valeur en points 
                d'un mot individuel.
                
                La fonction est_valide(grille,mot) fait appel à deux fonctions:
                    est_adjacent(grille, l1, l2), qui évalue l'adjacence de 
                    deux lettres dans la grile fournie et retourne un booléen.
                    mot_sans_accents(mot), qui détecte et enlève les accents
                    dans un mot donné.
                
                
"""
##############################################################################

#Importation des modules nécessaires
import random

##############################################################################
#Définition des valeurs constantes

#25 dés standard, les 11 premiers en double, pour un total de 36 (6x6). 
dices = [['E', 'T', 'U', 'K', 'N', 'O'], ['E', 'V', 'G', 'T', 'I', 'N'], 
         ['D', 'E', 'C', 'A', 'M', 'P'], ['I', 'E', 'L', 'R', 'U', 'W'], 
         ['E', 'H', 'I', 'F', 'S', 'E'], ['R', 'E', 'C', 'A', 'L', 'S'],
         ['E', 'N', 'T', 'D', 'O', 'S'], ['O', 'F', 'X', 'R', 'I', 'A'],
         ['N', 'A', 'V', 'E', 'D', 'Z'], ['E', 'I', 'O', 'A', 'T', 'A'],
         ['G', 'L', 'E', 'N', 'Y', 'U'], ['B', 'M', 'A', 'Q', 'J', 'O'],
         ['T', 'L', 'I', 'B', 'R', 'A'], ['S', 'P', 'U', 'L', 'T', 'E'],
         ['A', 'I', 'M', 'S', 'O', 'R'], ['E', 'N', 'H', 'R', 'I', 'S'],
         ['A', 'T', 'S', 'I', 'O', 'U'], ['W', 'I', 'R', 'E', 'B', 'C'],
         ['Q', 'D', 'A', 'H', 'A', 'U'], ['A', 'C', 'F', 'L', 'N', 'E'],
         ['P', 'R', 'S', 'T', 'U', 'G'], ['J', 'P', 'R', 'X', 'E', 'Z'],
         ['E', 'K', 'V', 'Y', 'B', 'E'], ['A', 'L', 'C', 'H', 'E', 'M'],
         ['E', 'D', 'U', 'F', 'H', 'K'], ['E', 'T', 'U', 'K', 'N', 'O'], 
         ['E', 'V', 'G', 'T', 'I', 'N'], ['D', 'E', 'C', 'A', 'M', 'P'], 
         ['I', 'E', 'L', 'R', 'U', 'W'], ['E', 'H', 'I', 'F', 'S', 'E'], 
         ['R', 'E', 'C', 'A', 'L', 'S'], ['E', 'N', 'T', 'D', 'O', 'S'], 
         ['O', 'F', 'X', 'R', 'I', 'A'], ['N', 'A', 'V', 'E', 'D', 'Z'],
         ['E', 'I', 'O', 'A', 'T', 'A'], ['G', 'L', 'E', 'N', 'Y', 'U']]

#Utilisé pour permettre les parties subséquentes
partie = 'active'
rejouer = 'non'


##############################################################################
#Fonctions

#Cette fonction affiche la grille de jeu
def afficher_grille(grille):
    t=len(grille)
    for i in range (t):
        if t==5:
            print("\n---------------")
        elif t==6:
            print("\n------------------")
        else:
            print("\n------------")
        for j in range (t):
            print ("|"+str(grille[i][j]),end="|")
    if t==5:
        print("\n----------------")
    elif t==6:
        print("\n------------------")
    else:
        print("\n------------")

#genere la grille
def generer_grille(taille):
    '''
    etape 1: choisi un de (random) dans la liste
    etape 2: enleve le de de la liste
    etape 3: choisi une face (random) sur le de choisi
    etape 4: repete 16, 25 ou 36 fois dependament la taille
    note:   Le 'taille -= 1' assure que les des sont choisi parmis ceux adequat 
            pour la grille (soit les 16, 25 premiers dans les cas 4x4 et 5x5).
    '''
    #initialiser le tableau a partir duquel la grille va etre construite.
    indice = random.randint(0,taille-1)
    dice = dices[indice]                                #On choisi un dé.
    dices.remove(dices[indice])                         #on l'enlève
    tableau = dice[random.randint(0,5)]                 #On le roule.
    taille -= 1   
    for i in range(taille):
        indice = random.randint(0,taille-1)
        dice = dices[indice]                            #On choisi un dé.
        dices.remove(dices[indice])                     #on l'enlève
        tableau += dice[random.randint(0,5)]            #On le roule.
        taille -= 1 

    #Grille qui va etre utilisée pour établir la validité des mots
    grille = []
    for i in range(dimension):
        grille += [tableau[dimension*i:(dimension*i)+(dimension)]]            
    return grille

#Enleve les accents d'un mot
def mot_sans_accents(mot):
    nouveau_mot = ''
    for i in range(len(mot)):
        j=mot[i]
        if j=="é" or j=="è" or j=="ê" or j=="ẽ":
            nouveau_mot += "e"
        elif j=="ç":
            nouveau_mot += "c"
        elif j=="à" or j=="â" or j=="ã" :
            nouveau_mot +="a"
        elif j=="ù" or j=="û":
            nouveau_mot +="u"
        elif j=="î" or j=="ï":
            nouveau_mot +="i"
        else:
            nouveau_mot += j

    return nouveau_mot

#Évalue l'adjacence de deux lettres donnés dans la grille
def est_adjacent(grille,lettre1,lettre2):
    cond=False
    i,j=0,0
    liste1=[]
    liste2=[]
    for i in range(dimension):
        for j in range(dimension):
            if grille[i][j]==mot_sans_accents(lettre1).upper():
                liste1.append((i,j))
            elif grille[i][j]==mot_sans_accents(lettre2).upper():
                liste2.append((i,j))
    for k in range(len(liste1)):
        for l in range(len(liste2)):
            i,j=liste1[k]
            m,n=liste2[l]##
            if (((i,j+1)==(m,n)) or ((i+1,j)==(m,n)) or ((i+1,j+1)==(m,n)) 
                or ((i,j)==(m,n+1)) or ((i,j)==(m+1,n)) or ((i,j)==(m+1,n+1))
                or ((i+1,j)==(m,n+1)) or ((i,j+1)==(m+1,n))):
                
                cond=True
                
    return cond

def est_valide(grille,mot):
    l=[]
    for i in mot:
        l.append(i)
    test=True
    for i in range ((len(mot))-1):
        if not est_adjacent(grille,mot_sans_accents(l[i]),mot_sans_accents(l[i+1])):
            test=False
    return test

#assigne les points a un mot
def point_mot(mots):
    if dimension==4:
        if len(mots)==3: p=1
        elif len(mots)==4: p=2
        elif len(mots)==5: p=3
        elif len(mots)==6: p=5
        elif len(mots)==7: p=8
        else : p+=10
    elif dimension==5:
        if len(mots)==3: p=1
        elif len(mots)==4: p=2
        elif len(mots)==5: p=3
        elif len(mots)==6: p=4
        elif len(mots)==7: p=6
        else : p+=10
    elif dimension==6:
        if len(mots)==3: p=1
        elif len(mots)==4: p=2
        elif len(mots)==5: p=3
        elif len(mots)==6: p=5
        elif len(mots)==7: p=7
        elif len(mots)==8: p=10
        else : p=12
    return p

def calcul_points(grille, mots):
    points_total, liste = 0 , []            #Initialise les variables
    for i in range(len(mots)):
        if mots[i][0] == '1':
            mots[i] = mots[i][1:]
            valide = est_valide(grille, mot_sans_accents(mots[i]))
            if valide == 1:
                points = point_mot(mots[i])
                liste += [(mots[i], points)] 
                points_total += points
            else:
                liste += [(mots[i], 'Invalide')]
        else:
            liste += [(mots[i], 'Refusé')]
            
    return points_total, liste

#La partie ou le jeu est joué
def deroulement():
    mots, mot_in = [],[]
    for i in range(nb_de_joueurs):
        mots +=[[]]
        mot_in += [['nonvide']] #On l'initialise pour commencer la boucle
    for i in range(10):    
        for j in range(nb_de_joueurs):
            if mot_in[j] != '':
                mot_in[j]=(input('Joueur {}, un mot (un espace pour arrêter):'
                                   .format(joueurs[j])).strip()).upper()
                if mot_in[j] == '':
                    continue
                while len(mot_in[j]) < 3:
                    mot_in[j] = (input('Mot invalide, entrez un mot:'
                                       ).strip()).upper()
                x=0
                while x==0:
                    accepte = input('Accepter le mot? (oui, non):').strip()
                    if accepte == 'oui':
                        mots[j] += ['1'+mot_in[j]] 
                        x=1
                    elif accepte == 'non':  
                        mots[j] += [mot_in[j]]
                        x=1
                    else:
                        print('Entrez oui ou non.')
        
    return mots

def jouer(): 
    #Determiner le nombre de joueurs.
    if rejouer != 'OUI':
        global nb_de_joueurs #Global pour le transporter d'une partie à l'autre
        nb_de_joueurs = input('Entrez le nombre de joueurs (2+):').strip()
        
        #Vérification de la validité des input.
        if (nb_de_joueurs == '0' or nb_de_joueurs == '1'):
            nb_de_joueurs = 'invalide' #Pour entrer dans la boucle.
        while nb_de_joueurs.isdigit() == False:
            print('Nombre invalide, entrez un nombre supérieur a 1.')
            nb_de_joueurs = input('Entrez le nombre de joueurs (2+):').strip()
            if (nb_de_joueurs == '0' or nb_de_joueurs == '1'):
                nb_de_joueurs = 'invalide' #Pour rester dans la boucle.
        nb_de_joueurs = int(nb_de_joueurs)
        
        global joueurs #Global pour le transporter d'une partie à l'autre
        joueurs = []
        for i in range(nb_de_joueurs):
            joueurs+= [[]]
            joueurs[i] = input('joueur{}, entrez votre nom:'.format(i+1))
            #Vérification de la validité des input.
            while joueurs[i].isalpha() == False or len(joueurs[i]) < 1:
                print('Entrez un nom valide (lettres uniquement, nonvide)')
                joueurs[i] = input('joueur{}, entrez votre nom:'.format(i+1))    
        
        
    global dimension        #Utilisé fréquement, les dimensions de la grille.
    dimension_in=input('Entrez les dimensions de la grille (4x4, 5x5, 6x6):'
                       ).strip()
    
    #Vérification de la validité des input.
    if len(dimension_in)!=0:
        dimension = dimension_in[0] 
    if len(dimension_in)==0 or dimension.isdigit(): #pour que int() retourne pas une erreur
        if len(dimension_in)==0 or int(dimension) < 4 or int(dimension) > 6:
            print('Dimensions non supportés.')
            dimension = 'invalide' #Pour entrer dans la boucle
    while len(dimension_in)==0 or dimension.isdigit() == False:
        print('Entrez un nombre (4, 5, 6) ou des dimensions (4x4, 5x5, 6x6).')
        dimension_in=input(
            'Entrez les dimensions de la grille (4x4, 5x5, 6x6):').strip()
        if len(dimension_in)!=0:
            dimension = dimension_in[0]
        if len(dimension_in)==0 or dimension.isdigit():
            if len(dimension_in)==0 or int(dimension) < 4 or int(dimension) > 6:
                print('Dimensions non supportés.')
                dimension = 'invalide' #Pour rester dans la boucle
        
    dimension = int(dimension_in[0])
    taille = (dimension**2)
    grille = generer_grille(taille)
    afficher_grille(grille)
    
    mots = deroulement()
    points, liste = [], []
    for i in range(nb_de_joueurs):
        points += [[]]  #Garder le compte des points totals de chaque joueurs.
        liste += [[]]   #Garder en mémoire les mots entrés par les joueurs.
        points[i], liste[i] = calcul_points(grille, mots[i])
    
   
    afficher_fin(points, liste, nb_de_joueurs)
    return 

def afficher_fin(points, liste, nb_de_joueurs):
    global rejouer
    #Initialise la mémoire lors de la première partie
    if rejouer != 'OUI':
        global points_memoire
        points_memoire = []
        for j in range(nb_de_joueurs):
           points_memoire += [0]
           
           #Enregistre les points de la partie en cours dans la mémoire.
    for i in range(nb_de_joueurs):        
        points_memoire[i] += points[i]
    
    #Compte et affiche les listes et le pointage cumulatif.
    for j in range(nb_de_joueurs):
        print('Joueur {}:'.format(j+1),'\n','Mots:     Valeur', sep = '')
        for i in range(len(liste[j])):     
            print('{: <10}{}'.format(liste[j][i][0],liste[j][i][1]))
        print('\n','Total des points:', points_memoire[j])
            
    #Lèoption de rejouer une partie.
    rejouer = (input('Voulez-vous rejouer (oui, non):').strip()).upper()
    if rejouer == 'OUI':
        recreer_dices()
        for i in range(nb_de_joueurs):
            points_memoire[i] += points[i]
    else:
        print('Partie terminée')
        global partie
        partie = 'finie'

        
def recreer_dices():
    global dices
    dices = [['E', 'T', 'U', 'K', 'N', 'O'], ['E', 'V', 'G', 'T', 'I', 'N'], 
             ['D', 'E', 'C', 'A', 'M', 'P'], ['I', 'E', 'L', 'R', 'U', 'W'], 
             ['E', 'H', 'I', 'F', 'S', 'E'], ['R', 'E', 'C', 'A', 'L', 'S'],
             ['E', 'N', 'T', 'D', 'O', 'S'], ['O', 'F', 'X', 'R', 'I', 'A'],
             ['N', 'A', 'V', 'E', 'D', 'Z'], ['E', 'I', 'O', 'A', 'T', 'A'],
             ['G', 'L', 'E', 'N', 'Y', 'U'], ['B', 'M', 'A', 'Q', 'J', 'O'],
             ['T', 'L', 'I', 'B', 'R', 'A'], ['S', 'P', 'U', 'L', 'T', 'E'],
             ['A', 'I', 'M', 'S', 'O', 'R'], ['E', 'N', 'H', 'R', 'I', 'S'],
             ['A', 'T', 'S', 'I', 'O', 'U'], ['W', 'I', 'R', 'E', 'B', 'C'],
             ['Q', 'D', 'A', 'H', 'A', 'U'], ['A', 'C', 'F', 'L', 'N', 'E'],
             ['P', 'R', 'S', 'T', 'U', 'G'], ['J', 'P', 'R', 'X', 'E', 'Z'],
             ['E', 'K', 'V', 'Y', 'B', 'E'], ['A', 'L', 'C', 'H', 'E', 'M'],
             ['E', 'D', 'U', 'F', 'H', 'K'], ['E', 'T', 'U', 'K', 'N', 'O'], 
             ['E', 'V', 'G', 'T', 'I', 'N'], ['D', 'E', 'C', 'A', 'M', 'P'], 
             ['I', 'E', 'L', 'R', 'U', 'W'], ['E', 'H', 'I', 'F', 'S', 'E'], 
             ['R', 'E', 'C', 'A', 'L', 'S'], ['E', 'N', 'T', 'D', 'O', 'S'], 
             ['O', 'F', 'X', 'R', 'I', 'A'], ['N', 'A', 'V', 'E', 'D', 'Z'],
             ['E', 'I', 'O', 'A', 'T', 'A'], ['G', 'L', 'E', 'N', 'Y', 'U']]
    
    
##############################################################################

#Début du code

#'''
while partie == 'active':
    jouer()

#'''
  
##############################################################################
#Section des tests unitaires

#Cette focntion permet de comparer de grille,utilisé dans les tests
def eq_matrice(m1,m2):
    if len(m1) != len(m2):
        return False
    for i in range(len(m1)):
        if len(m1[i]) != len(m2[i]):
            return False
        for j in range(len(m1[i])):
            if m1[i][j] != m2[i][j]:
                return False
    return True

#Cette fonction permet de faire les tests unitaires
def test():
    
    #Tests de genere_grille
    test_array = [4, 5, 6]
    #Les valeurs autres ne se rendent pas a la fonction genere_grille()
    
    for i in range(len(test_array)):
        recreer_dices() #pour que les test de a=5 et a=6 aient des dés.
        test=True
        a = test_array[i]
        global dimension    #utilisé un peu partout, et puisque le test passe
        dimension = a       # pas par jouer() il faut le définir ici.
    
        g=generer_grille(a**2)
        for i in range(a-1):
            if g[i]==g[i+1] or g[0]==g[-1] :
                test=False
            for j in range(a):
                if g[i][j].isalpha==False:
                    test=False
        assert test==True ,"la fonction ne retourne pas un tableau à 2 dimensions où chaque sous-tableau est de même longueur et est composé de valeurs valides"   
        recreer_dices()
        g1=generer_grille(a**2)
        assert eq_matrice(g1,g)==False ,"La fonction a génèré la même grille 2 fois, ce qui est statistiquement impossible" 
        #note: les chances de générer la même grille aléatoirement 2 fois de suite sont 'impossiblement' petite.
        if a == 4:
            #Vérifie que les 16 premiers dés sont utilisé
            intended_dices = [['A', 'T', 'S', 'I', 'O', 'U'], 
                              ['W', 'I', 'R', 'E', 'B', 'C'],
            ['Q', 'D', 'A', 'H', 'A', 'U'], ['A', 'C', 'F', 'L', 'N', 'E'],
            ['P', 'R', 'S', 'T', 'U', 'G'], ['J', 'P', 'R', 'X', 'E', 'Z'],
            ['E', 'K', 'V', 'Y', 'B', 'E'], ['A', 'L', 'C', 'H', 'E', 'M'],
            ['E', 'D', 'U', 'F', 'H', 'K'], ['E', 'T', 'U', 'K', 'N', 'O'], 
            ['E', 'V', 'G', 'T', 'I', 'N'], ['D', 'E', 'C', 'A', 'M', 'P'], 
            ['I', 'E', 'L', 'R', 'U', 'W'], ['E', 'H', 'I', 'F', 'S', 'E'], 
            ['R', 'E', 'C', 'A', 'L', 'S'], ['E', 'N', 'T', 'D', 'O', 'S'], 
            ['O', 'F', 'X', 'R', 'I', 'A'], ['N', 'A', 'V', 'E', 'D', 'Z'],
            ['E', 'I', 'O', 'A', 'T', 'A'], ['G', 'L', 'E', 'N', 'Y', 'U']]
            
            assert dices == intended_dices
            
        if a == 5:
            #Vérifie que les 25 premiers dés sont utilisés
            intended_dices = [['E', 'T', 'U', 'K', 'N', 'O'], 
            ['E', 'V', 'G', 'T', 'I', 'N'], ['D', 'E', 'C', 'A', 'M', 'P'], 
            ['I', 'E', 'L', 'R', 'U', 'W'], ['E', 'H', 'I', 'F', 'S', 'E'], 
            ['R', 'E', 'C', 'A', 'L', 'S'], ['E', 'N', 'T', 'D', 'O', 'S'], 
            ['O', 'F', 'X', 'R', 'I', 'A'], ['N', 'A', 'V', 'E', 'D', 'Z'],
            ['E', 'I', 'O', 'A', 'T', 'A'], ['G', 'L', 'E', 'N', 'Y', 'U']]
            
            assert dices == intended_dices
            
        if a == 6:
            #Vérfifie que les 36 dés (donc tous les dés) sont utilisés
            assert dices == []
    
    #######################################################################
    #test de est_valide()
    g=[["T","I","M","E"],["W","O","R","D"],["F","A","C","T"] ,["G","A","M","E"]]
    dimension = 4
    assert est_valide(g,"time")==True
    assert est_valide(g,"twfg")==True
    assert est_valide(g,"woim")==True
    assert est_valide(g,"tofe")==False
    assert est_valide(g,"torcma1")==False
    ######################################################################
    #test de calcul_points()
    #Les mots approuvés durant la partie reçoivent un indice 1 en préfixe.
    total_points,liste_points=calcul_points(g,["1time"])
    assert total_points==2
    total_points,liste_points=calcul_points(g,["1tofe"])
    assert total_points==0
    total_points,liste_points=calcul_points(g,["woim"])
    assert total_points==0
    total_points,liste_points=calcul_points(g,["1twfga"])
    assert total_points==3
    total_points,liste_points=calcul_points(g,["1gametd"])
    assert total_points==5


# test()