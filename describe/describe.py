import sys
import matplotlib.pyplot as plt
from extract_datas_csv import extract_Datas_from_csv
from metrics import moyenne
from metrics import ecart_type
from metrics import minimum
from metrics import maximum
from metrics import quartiles
from metrics import deciles


class Describe() :
	def __init__(self, dataSet) -> None:
		self.dataSet = dataSet
		self.houses = 0
		self.byHousesDataSets = {}
		self.RavenclawBookMark = 0
		self.SlytherinBookMark = 0
		self.GryffindorBookMark = 0
		self.HufflepuffBookMark = 0
		self.nonNumericFeatures = []

	def describe(self) -> None :
		column = 0
		describeTab = []
		try :
			for column_name in self.dataSet.columns :
				if self.dataSet[column_name].dtype in ['int64', 'float64'] :
					column = self.dataSet[column_name].dropna() # elimine les nan set dans lextraction
					n = len(column)
					mean = moyenne(column)
					std = ecart_type(column, mean)
					min = minimum(column)
					max = maximum(column)
					q1 = quartiles(column, 0.25)
					q2 = quartiles(column, 0.5)
					q3 = quartiles(column, 0.75)
					# [ Bonus ]
					ecart_Inter_Quartiles = q3 -q1
					d1 = deciles(column, 0.1)
					d2 = deciles(column, 0.2)
					d3 = deciles(column, 0.3)
					d7 = deciles(column, 0.7)
					d8 = deciles(column, 0.8)
					d9 = deciles(column, 0.9)
					# print(f'[ {column_name} ] \t -> \tcount: {n:.6f} \tmean: {mean:.6f} \tstd: {std:.6f}\n\t\t\tmin: {min:.6f} \tmax: {max:.6f}')
					# print(f'\t\t\t25%: {q1:.6} \tmediane: {q2:.6f} \t75%: {q3:.6f}')
					# print('')

					width_max = 12
					feature = {
						'feature': column_name,
						'count': n,
						'mean': mean,
						'std': std,
						'min': min,
						'q1': q1,
						'median': q2,
						'q3': q3,
						'max': max,
						'ecIntrQ': ecart_Inter_Quartiles,
						'd1': d1,
						'd2': d2,
						'd3': d3,
						'd7': d7,
						'd8': d8,
						'd9': d9,
					}
					describeTab.append(feature)
				else :
					self.nonNumericFeatures.append(f'{column_name}')

			print('\n  #  #  #  #  #  #  [  Describe  ]  #  #  #  #  #  #')
			keys = ['feature', 'count', 'mean', 'std', 'min', 'q1', 'median', 'q3', 'max', 'Bonus', 'ecIntrQ', 'd1', 'd2', 'd3', 'd7', 'd8', 'd9',]
			width_max = 12
			for key in keys :
				if key == 'Bonus' :
					print(' o=\======>  [ Bonus ]  <======/=o')
				else :	
					if key == 'feature':
						print('\t', end='')
					else :
						print(f'{key}', sep='', end='\t') 
					for set in describeTab :
						if key == 'feature':
							name = str(set[key])
							if len(name) > 12 :
								print(f'*{name[:11]}', end=' ')
							else :
								ws = width_max - len(name) # white spaces
								print(ws*' ', set[key], sep='', end=' ')
						else :
							value = float(set[key])
							len_int = len(str(int(value)))
							ws = width_max - len_int - 5
							if - 1 < value < 0 :
								ws -= 1
							if ws < 0 :
								print(f' ** Pb Ws** ws: {ws}, value: {value}')
							print(f"{ws*' '}{value:.4f}", end=' ')

						
					print('')
			print(f'[{len(keys) - 2} rows x {len(describeTab)} columns]')
			print(f'Non numeric features:\t{self.nonNumericFeatures}')
		except :
			print(' [ error ] -> Describe.describe()')

# Hogwarts House

	def plot_scatter_houses_By_Class(self) -> None:
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
			# print(self.GryffindorBookMark)

			choix = 0
			while choix == 0 :
				try :
					choix = int(input('\nWhat would you like to do ?\n\t-> [1] Visuaze Datas One By One\n\t-> [2] Visualize Datas Globally\n\t-> [3] Exit\n -> '))
					if choix != 1 and choix != 2 and choix != 3:
						choix = 0
						raise ValueError
				except :
					print("[ error ] -> usage: input must be '1', '2' or '3'.\n")

			if choix == 3 :
				return

			matieres = self.GryffindorBookMark.columns

			if choix == 1 : # [ Display  chaque Graph Individuellement ]
				for matiere in matieres:
					point = 5
					plt.figure(figsize=(10, 6))
					plt.scatter(self.HufflepuffBookMark.index, self.HufflepuffBookMark[matiere], label='Hufflepuff', color='yellow', s=point)
					plt.scatter(self.GryffindorBookMark.index, self.GryffindorBookMark[matiere], label='Gryffindor', color='red', s=point)
					plt.scatter(self.RavenclawBookMark.index, self.RavenclawBookMark[matiere], label='Ravenclaw', color='blue', s=point)
					plt.scatter(self.SlytherinBookMark.index, self.SlytherinBookMark[matiere], label='Slytherin', color='green', s=point)
					plt.title(f'Nuage de points pour la matière {matiere}')
					plt.xlabel('Élèves')
					plt.ylabel('Notes')
					plt.legend()
					plt.show()

			else :
				nombre_lignes = len(matieres) // 3 + (len(matieres) % 3 > 0)
				nombre_colonnes = 4

				# Créer un seul graphique avec plusieurs sous-graphiques
				taille_graphique = (3.5, 2)
				fig, axs = plt.subplots(nombre_lignes, nombre_colonnes, figsize=(nombre_colonnes * taille_graphique[0], nombre_lignes * taille_graphique[1]))
				# fig, axs = plt.subplots(nombre_lignes, nombre_colonnes, figsize=(15, nombre_lignes * 5))

				# Parcourir chaque matière et créer un nuage de points pour chaque maison
				for i, matiere in enumerate(matieres):
					ligne = i // nombre_colonnes
					colonne = i % nombre_colonnes
					point = 2

					fig.suptitle(f'*red: [ Gryffindor ]      *yellow: [ Hufflepuff ]      *blue: [ Ravenclaw ]      *green: [ Slytherin ]')
					axs[ligne, colonne].scatter(self.GryffindorBookMark.index, self.GryffindorBookMark[matiere], label='Gryffindor', color='red', s=point)
					axs[ligne, colonne].scatter(self.HufflepuffBookMark.index, self.HufflepuffBookMark[matiere], label='Hufflepuff', color='yellow', s=point)
					axs[ligne, colonne].scatter(self.RavenclawBookMark.index, self.RavenclawBookMark[matiere], label='Ravenclaw', color='blue', s=point)
					axs[ligne, colonne].scatter(self.SlytherinBookMark.index, self.SlytherinBookMark[matiere], label='Slytherin', color='green', s=point)

					axs[ligne, colonne].set_title(f'* {matiere} *')
					axs[ligne, colonne].set_xlabel('Élèves')
					axs[ligne, colonne].set_ylabel('Notes')
					# axs[ligne, colonne].legend()

				# Supprimer les sous-graphiques inutilisés, le cas échéant
				for i in range(len(matieres), nombre_lignes * nombre_colonnes):
					fig.delaxes(axs.flatten()[i])

				plt.tight_layout()  # Ajuste automatiquement la disposition pour éviter les chevauchements
				plt.show()

		except :
			print('[ error ]  ->  Describe.plot_values()')


def main() :
	if len(sys.argv) != 2 :
		print('usage:  \'python3 describe.py [-h] file')
		return
	else :
		csv_file_path = sys.argv[1]
	try :
		print('\n  # # # # # # # # # # # # # # # # # # # # # # # # # # # #')
		print('  #  #  #  #  #  #  [  D . s . L . r  ]  #  #  #  #  #  #')
		print('  #  #  #  [ DataScience X Logistic Regression ]  #  #  #')
		print('  # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n')
		dataSet = extract_Datas_from_csv(csv_file_path)
		des = Describe(dataSet)
		des.describe()
		des.plot_scatter_houses_By_Class()
	except ValueError :
		return

if __name__ == '__main__' :
	main()