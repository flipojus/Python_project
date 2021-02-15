#!/opt/local/bin/python
# -*- coding: utf8 -*-

# Auteur : Louis OLLIVIER 
# Mail : louis.ollivier@etu.univ-rouen.fr 

#-------------------------------------------------------------------------------------------#	

import ensembl,ncbi,fileinput

#-------------------------------------------------------------------------------------------#	
# On fait une boucle qui lit dans le fichier contenant "espece,gene" et qui range l'espèce et
# le gene dans des variables afin de les utiliser en tant qu'arguments des différentes fonctions.

for line in fileinput.input(): 
	x = line[:-1].split(",") # On retire le caractère de saut de ligne à la fin de chaque ligne.
	geneSymbol = str(x[0])
	species = str(x[1])

	print("----------------- ESPECE : "+species+" GENE : "+geneSymbol+" -----------------\n")
	
	#----------------------------------------------------------------------------------------#

	# Partie Ensembl : gene ID, transript ID, protein ID, lien vers le GB, lien liste orthologues

	EnsemblGeneID=ensembl.Ensembl_Gene_ID(species,geneSymbol)
	print("Gene ID Ensembl : "+EnsemblGeneID+"\n")
	#
	EnsemblTranscriptID=ensembl.Ensembl_Transcript_ID(EnsemblGeneID)
	print("Transcript ID Ensembl : "+str(EnsemblTranscriptID)+"\n")
	#
	EnsemblProtID=ensembl.Ensembl_Prot_ID(EnsemblGeneID)
	print("Prot ID Ensembl : "+str(EnsemblProtID)+"\n")
	#
	EnsemblClassif=ensembl.Ensembl_Classif(species) # 
	#
	Ensembl_Gbrowser=ensembl.Ensembl_GBrowser(EnsemblGeneID,species,EnsemblClassif,geneSymbol)
	print("Lien du génome browser : "+Ensembl_Gbrowser+"\n")
	#
	EnsemblOrthoList=ensembl.Ensembl_Ortho_List(EnsemblGeneID,species,EnsemblClassif)
	print("Lien pour la liste des orthologues : "+EnsemblOrthoList+"\n")

	#----------------------------------------------------------------------------------------#
		
	# Partie NCBI : gene ID, official full name, transript ID et protein ID

	NCBIgeneID = ncbi.NCBI_Gene_ID(species,geneSymbol)
	print("Gene ID NCBI : "+str(NCBIgeneID)+"\n") 
	#
	NCBIfullName = ncbi.NCBI_Full_Name(str(NCBIgeneID))
	print("Nom complet officiel : "+str(NCBIfullName)+"\n")
	#
	NCBItranscriptID = ncbi.NCBI_Transcript_ID(species,geneSymbol,NCBIgeneID)
	print("Transcript ID NCBI : "+str(NCBItranscriptID)+"\n") 
	#
	NCBIprotID = ncbi.NCBI_Prot_ID(species,geneSymbol,NCBIgeneID)
	print("Prot ID NCBI : "+str(NCBIprotID)+"\n") 

#-------------------------------------------------------------------------------------------#	
	
	
	
	
	
