import sys
import matplotlib.pyplot as plt
from extract_datas_csv import extract_Datas_from_csv


class Scatter_Plot() :
	def __init__(self, dataSet) -> None:
		self.dataSet = dataSet
		self.houses = 0
		self.byHousesDataSets = {}
		self.RavenclawBookMark = 0
		self.SlytherinBookMark = 0
		self.GryffindorBookMark = 0
		self.HufflepuffBookMark = 0
		self.nonNumericFeatures = []
		self.courses = 0
		self.getStudentsByHouses()

	def getStudentsByHouses(self) :
		try :
			self.houses = self.dataSet['Hogwarts House'].unique()
			print(f'Hogwarts Houses: \t{self.houses}')
			for maison in self.houses :
				self.byHousesDataSets[maison] = self.dataSet[self.dataSet['Hogwarts House'] == maison]
			# [ Debug ]
			# for maison, sous_dataset in self.byHousesDataSets.items():
			# 	print(f"Élèves de la maison {maison} :\n{sous_dataset}\n")
			self.GryffindorBookMark = self.byHousesDataSets['Gryffindor'].iloc[:, 5:]
			self.SlytherinBookMark = self.byHousesDataSets['Slytherin'].iloc[:, 5:]
			self.HufflepuffBookMark = self.byHousesDataSets['Hufflepuff'].iloc[:, 5:]
			self.RavenclawBookMark = self.byHousesDataSets['Ravenclaw'].iloc[:, 5:]
			self.courses = self.GryffindorBookMark.columns
		except Exception as e:
			print('[ error ]  ->  scp.getStudentsByHouses()', e)



	def VisualizeRelations(self) :
		try :
			# nombre_lignes = len(self.courses)
			# nombre_colonnes = len(self.courses)
			nombre_lignes = (len(self.courses)) // 3 + ((len(self.courses)) % 3 > 0)
			nombre_colonnes = 4
			# Créer un seul graphique avec plusieurs sous-graphiques
			taille_graphique = (3.5, 2)

			# Parcourir chaque matière et créer un nuage de points par rapport à toutes les autres matières
			for i, matiere_x in enumerate(self.courses):
				fig, axs = plt.subplots(nombre_lignes, nombre_colonnes, figsize=(nombre_colonnes * taille_graphique[0], nombre_lignes * taille_graphique[1]))
				fig.suptitle(f'*red: [ Gryffindor ]      *yellow: [ Hufflepuff ]      *blue: [ Ravenclaw ]      *green: [ Slytherin ]')
				for j, matiere_y in enumerate(self.courses):
					ligne = j // nombre_colonnes
					colonne = j % nombre_colonnes
					point = 2

					if i == j :
						axs[ligne, colonne].set_title(f'* - SELF - *\n{matiere_x}')
					else :
						axs[ligne, colonne].set_title(f'')
						# axs[ligne, colonne].set_title(f"* {matiere_x}\nvs {matiere_y} *")
					axs[ligne, colonne].scatter(self.GryffindorBookMark[matiere_x], self.GryffindorBookMark[matiere_y], label='Gryffindor', color='red', s=point)
					axs[ligne, colonne].scatter(self.HufflepuffBookMark[matiere_x], self.HufflepuffBookMark[matiere_y], label='Hufflepuff', color='yellow', s=point)
					axs[ligne, colonne].scatter(self.RavenclawBookMark[matiere_x], self.RavenclawBookMark[matiere_y], label='Ravenclaw', color='blue', s=point)
					axs[ligne, colonne].scatter(self.SlytherinBookMark[matiere_x], self.SlytherinBookMark[matiere_y], label='Slytherin', color='green', s=point)
					axs[ligne, colonne].set_xlabel(f'{matiere_x}')
					axs[ligne, colonne].set_ylabel(f'{matiere_y}')
				# Supprimer les sous-graphiques inutilisés, le cas échéant
				for i in range(len(self.courses), nombre_lignes * nombre_colonnes):
					fig.delaxes(axs.flatten()[i])
				plt.tight_layout()  # Ajuste automatiquement la disposition pour éviter les chevauchements
				plt.show()

		except Exception as e:
			print('[ error ]  ->  scp.VisualizeRelations()\n', e)	


	def VisualizeResults(self) :
		try:
			matiere_x = 'Astronomy'
			matiere_y = 'Defense Against the Dark Arts'

			taille_graphique = (14, 7)
			plt.figure(figsize=taille_graphique)
			plt.suptitle(f'\nResults Showing correlation between:\n * {matiere_x} *\nVS\n* {matiere_y} *\n')

			for i, matiere in enumerate([matiere_x, matiere_y]):
				plt.subplot(1, 2, i+1)  # Utilisez i+1 pour incrémenter correctement le numéro du sous-graphique
				point = 200
				plt.scatter(self.GryffindorBookMark[matiere], self.GryffindorBookMark[matiere_y], label='Gryffindor', color='red', s=point, alpha=0.5)
				plt.scatter(self.RavenclawBookMark[matiere], self.RavenclawBookMark[matiere_y], label='Ravenclaw', color='blue', s=point, alpha=0.5)
				plt.scatter(self.HufflepuffBookMark[matiere], self.HufflepuffBookMark[matiere_y], label='Hufflepuff', color='yellow', s=point, alpha=0.5)
				plt.scatter(self.SlytherinBookMark[matiere], self.SlytherinBookMark[matiere_y], label='Slytherin', color='green', s=point, alpha=0.5)
				if matiere == matiere_x :
					x = matiere_x
					y = matiere_y
				else :
					y = matiere_x
					x = matiere_y

				plt.xlabel(f'{x}')
				plt.ylabel(f'{y}')
				plt.legend()

			plt.tight_layout()  # Ajuste automatiquement la disposition pour éviter les chevauchements
			plt.show()

		except Exception as e:
			print('[ error ]  ->  scp.VisualizeResult()\n', e)	





def main() :
	if len(sys.argv) != 2 :
		print('usage:  \'python3 histogram.py [-h] file')
		return
	else :
		csv_file_path = sys.argv[1]

	try :
		print('\n  # # # # # # # # # # # # # # # # # # # # # # # # # # # #')
		print('  #  #  #  #  # [ ScatterPlot Visualization ] #  #  #  #  #')
		print('  # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n')
		
		dataSet = extract_Datas_from_csv(csv_file_path)
		scp = Scatter_Plot(dataSet)
		scp.VisualizeRelations()
		scp.VisualizeResults()

	except ValueError :
		return

if __name__ == '__main__' :
	main()