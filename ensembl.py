#!/opt/local/bin/python
# -*- coding: utf8 -*-

# Auteur : Louis OLLIVIER 
# Mail : louis.ollivier@etu.univ-rouen.fr 

#-------------------------------------------------------------------------------------------#	

import requests, sys

#-------------------------------------------------------------------------------------------#	

# Pour trouver le gene ID, on réutilise la requête lookup symbol 
# qui est donnée dans la documentation

def Ensembl_Gene_ID(species,geneSymbol):
	
	server = "https://rest.ensembl.org"
	ext = "/lookup/symbol/"+species+"/"+geneSymbol+"?"
 
	r = requests.get(server+ext, headers={"Content-Type" : "application/json"})
						  
	if not r.ok:    # On renvoit un message d'erreur si jamais ce gene n'existe pas ici					   
		return("Data not found")
						  
	decoded = r.json()
	return(decoded['id'])

#-------------------------------------------------------------------------------------------#	

# Pour trouver le Transcript ID, on utilise une requête Lookup avec le gene ID
# puis on va chercher les transcrits dans le dico renvoyé. Etant donné qu'il 
# y en a plusieurs, il faut créer une liste à laquelle on y ajoute chaque 
# nouveau transcript ID trouvé.

def Ensembl_Transcript_ID(id):
	
	server = "https://rest.ensembl.org"
	ext = '/lookup/id/'+id+'?expand=1'
	liste=[]
 
	r = requests.get(server+ext, headers={"Content-Type" : "application/json"})
 
	if not r.ok:
		return('Data not found')

	decoded = r.json()
	
	for i in decoded['Transcript']:
		liste.append(i['id'])
	return(liste)

#-------------------------------------------------------------------------------------------#	

# Pour trouver le Prot ID, on utilise une requête Lookup avec le gene ID
# puis on va chercher les transcrits dans le dico renvoyé. Comme pour la fonction
# Transcrpit ID sauf que l'on doit descendre un niveau plus loin dans le dico 
# (dico imbriqués). Etant donné qu'il y en a plusieurs, il faut créer une 
# liste à laquelle on y ajoute chaque nouveau transcript ID trouvé. 

def Ensembl_Prot_ID(id):
	
	server = "https://rest.ensembl.org"
	ext = '/lookup/id/'+id+'?expand=1'
	liste2=[]
 
	r = requests.get(server+ext, headers={"Content-Type" : "application/json"})
 
	if not r.ok:
		return('Data not found')

	decoded = r.json()
	
	for i in decoded['Transcript']:
		if 'Translation' in i:
			liste2.append(i['Translation']['id'])
	return(liste2)

#-------------------------------------------------------------------------------------------#	

# Ici on va chercher la taxonomie de l'espèce avec la requête associée. Grace 
# à cette taxonomie, on va pouvoir remonter à la banque Ensembl qui lui 
# correspond. Pour chaque banque, l'URL commence différement, il est donc important
# de déterminer cette partie avant de générer des liens. 
# En cherchant de manière spécifique dans la taxonomie de l'espèce voulue, 
# on remonte à la banque Ensembl associée. 

def Ensembl_Classif(species):
	
	server = "https://rest.ensembl.org"
	ext = "/taxonomy/classification/"+species+"?"
	r = requests.get(server+ext, headers={"Content-Type" : "application/json"})
	l=[]
	
	if not r.ok:
		return('Data not found')
		
	decoded = r.json()

	for i in decoded:
		l.append(i['name']) # liste stockant tous les termes de la taxonomie 
							# dans l'ordre
		
	# On fait un arbre de décision qui a été déterminé en fonction du type de 
	# taxonomie que renvoyait la requête, afin d'associé l'espèce à sa banque. 
	
	if 'Eukaryota' in l:
		if 'Metazoa' in l:
			if 'Vertebrata' in l:
				return('https://')
			else:
				return('https://metazoa.')
		else:
			if 'Fungi' in l:
				return('https://fungi.')
			else:
				if 'Viridiplantae' in l or 'Rhodophyta' in l:
					return('https://plants.')
				else:
					return('https://protists.')
	else:
		return('https://bacteria.')

#-------------------------------------------------------------------------------------------#	

# Cette fonction va simplement associer plusieurs éléments déterminés grace aux
# fonctions précédentes afin de former le lien menant au GB pour l'espece et
# et le gene voulu, dans la banque qui lui correspond. 

def Ensembl_GBrowser(id,species,banque,geneSymbol):
	
	# On vérifie si le gene ID existe avant de créer le lien, s'il n'existe pas 
	# on ne le créée pas et on renvoit "Data not found".
	
	if not(id=='Data not found'):
		lien=banque+'ensembl.org/'+species+'/Location/View?db=core;g='+id
		return(lien)
		
	else :	
		return("Data not found")

#-------------------------------------------------------------------------------------------#	
		
# Cette fonction va simplement associer plusieurs éléments déterminé grace aux
# fonctions précédentes afin de former le lien menant à la liste des orthologies 
# pour l'espece et le gene voulu. 

def Ensembl_Ortho_List(id,species,banque):
	
	# On vérifie si le gene ID existe avant de créer le lien, s'il n'existe pas 
	# on ne le créée pas et on renvoit "Data not found".
	
	if not(id=='Data not found'):
		lien=banque+'ensembl.org/'+species+'/Gene/Compara_Ortholog?db=core;g='+id
		return(lien)
	else :	
		return("Data not found")
	
#-------------------------------------------------------------------------------------------#	

