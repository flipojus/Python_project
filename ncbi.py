#!/opt/local/bin/python
# -*- coding: utf8 -*-

# Auteur : Louis OLLIVIER 
# Mail : louis.ollivier@etu.univ-rouen.fr 

#-------------------------------------------------------------------------------------------#	

from Bio import Entrez
import os 

#-------------------------------------------------------------------------------------------#	

# Pour trouver le prot ID on va faire une requete esearch avec l'espèce et le 
# gene voulu sur la banque Gene puis on va isoler le gene ID qui est contenu 
# dans le dicto renvoyé par la requête. 

def NCBI_Gene_ID(species,geneSymbol): 

	Entrez.email = 'louis.ollivier@etu.univ-rouen.fr'
	handle = Entrez.esearch(db = "gene", term=str(species)+"[Organism] AND "+
											  str(geneSymbol)+"[Gene Name]",retmax=1)
															# On se limite un 1 gène 
	records = Entrez.read(handle)
	NCBIgeneID = records["IdList"] # C'est la clé "IdList" qui est associée avec le gene ID.
	
	# Si jamais le gene ID n'existe pas dans la banque, IdList sera vide et ainsi, on 
	# renvoit un message d'erreur. Il pourra être interprété par les autres fonctions 
	# pourra savoir si elle doivent chercher ou non (transcrits ou protéines). 
	if not(NCBIgeneID==[]):
		return(NCBIgeneID)
	
	else :
		return("Data not found")

#-------------------------------------------------------------------------------------------#	

# Pour trouver le nom complet du gene on va utiliser une technique un peu moche 
# qui consiste à cherher la position du nom par rapport à certains caractères qui
# l'entourent et qui sont fixes afin de déterminer la position relative du nom complet.

def NCBI_Full_Name(NCBIgeneID): 
	
	# Au lieu de lancer la recherche directement (assez long), on check d'abord si le gene ID 
	# a été trouvé avec la 1ère fonction, si c'est le cas on peut lancer la requête.
	
	if not (NCBIgeneID=="Data not found"):
		# On effectue une requete efetch avec le gene ID pour récuperer une fiche GenBank
		# qui va contenir les annotations (dont le nom complet).
		handle = Entrez.efetch(db="gene", id=NCBIgeneID, retmax="100", rettype="gb", retmode="text")
		annot = handle.read()

		# On verifie que le fichier temporaire contenant les annotations n'existe
		# pas déjà pour éviter des erreurs, puis on le créer avec toutes les 
		# annotations à l'intérieur.
		if os.path.exists('tmp_annot.txt'):
			os.remove('tmp_annot.txt')

		tmp_annot = open("tmp_annot.txt", "w") 
		tmp_annot.write(annot)
		tmp_annot.close()
		
		# On va parcourir le fichier ligne par ligne jusqu'à trouver des "marqueurs" de la 
		# position du nom complet (Name et [) puis on va stocker ces positions afin de 
		# d'extraire le nom complet du gène. 
		with open("tmp_annot.txt") as file:
			for line in file:
				if "Name" in line:
					for i in range(0,len(line)):
						# On s'assure de bien trouver la position de Name, pas seulement le N 
						# car il pourrait être contenu dans le gene ID qui le précède et ainsi 
						# tout décaler 
						if line[i:i+4]=="Name" :
							nameStart = i+6
						if line[i]=="[" :
							nameStop = i-1
					NCBIgeneName = line[nameStart:nameStop]
					return(NCBIgeneName)

			return("Data not found") # Si jamais le gene existe mais n'a pas de nom complet 
									 # officiel comme psbA du pin par exemple
		os.remove('tmp_annot.txt')
		
	else : 
		if os.path.exists('tmp_annot.txt'): # On supprime le fichier déjà existant même si 
			os.remove('tmp_annot.txt') 		# on a pas trouvé de nom complet officiel. Utile 
											# si par exemple le dernier gene n'a pas de nom 
		return("Data not found")			# complet officiel, on supprime quand même le 
											# fichier précédent, pour ne pas avoir de fichier 
											# à la fin.
		
#-------------------------------------------------------------------------------------------#	

# Pour trouver le transcript ID, on va faire une requete esearch avec l'espèce et le 
# gene voulu sur la banque Nucleotide puis on va isoler les transcript ID qui sont contenus 
# dans le dico renvoyé par la requête. (Limite ici à 10 transcrits, à voir par la suite)

def NCBI_Transcript_ID(species,geneSymbol,NCBIgeneID): 
	
	# Au lieu de lancer la recherche directement (assez long), on check d'abord si le gene ID 
	# a été trouvé avec la 1ère fonction, si c'est le cas on peut lancer la requête.
	if not (NCBIgeneID=="Data not found"):
		Entrez.email = 'louis.ollivier@etu.univ-rouen.fr'
		handle = Entrez.esearch(db = "nucleotide", term=str(species)+"[Organism] AND "+
												  str(geneSymbol)+"[Gene Name]",retmax=10)
														  # On se limite un 10 transcripts

		records = Entrez.read(handle)
		NCBItranscriptID = records["IdList"] # C'est la clé "IdList" qui est associée avec les 
											 # transcript ID.
		return(NCBItranscriptID)
	else : 
		return("Data not found") 

#-------------------------------------------------------------------------------------------#	

# Pour trouver le prot ID on va faire une requete esearch avec l'espèce et le 
# gene voulu sur la banque Protein puis on va isoler les prot ID qui sont contenus 
# dans le dico renvoyé par la requête. (Limite ici à 10 protéines, à voir par la suite)

def NCBI_Prot_ID(species,geneSymbol,NCBIgeneID): 
	
	# Au lieu de lancer la recherche directement (assez long), on check d'abord si le gene ID 
	# a été trouvé avec la 1ère fonction, si c'est le cas on peut lancer la requête.
	if not (NCBIgeneID=="Data not found"):
		Entrez.email = 'louis.ollivier@etu.univ-rouen.fr'
		handle = Entrez.esearch(db = "protein", term=str(species)+"[Organism] AND "+
												str(geneSymbol)+"[Gene Name]",retmax=10)
														  # On se limite un 10 protéines
		records = Entrez.read(handle)
		NCBIprotID = records["IdList"] # C'est la clé "IdList" qui est associée avec les 
									   # prot ID.
		return(NCBIprotID)
	
	else :
		return("Data not found")

#-------------------------------------------------------------------------------------------#	
