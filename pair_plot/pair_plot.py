import sys
import matplotlib.pyplot as plt
from extract_datas_csv import extract_Datas_from_csv


class Pair_Plot() :
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
			print('[ error ]  ->  pp.getStudentsByHouses()', e)



	def VisualizeRelations(self) :
		try :
			n = len(self.courses)
			fig, axs = plt.subplots(n, n, figsize=(14, 7.5))
			fig.suptitle(f'Pair Plot  -  * Results *\n')

			for y, matiere_y in enumerate(self.courses):
				# print('y: ', y, ' . matiere_y: ', matiere_y)	
				for x, matiere_x in enumerate(self.courses):
					if x == 0 :
						if len(str(matiere_x)) >= 9 :
							axs[y, x].set_ylabel(f'{matiere_y[:8]}.\n', fontsize=5)
						else :
							axs[y, x].set_ylabel(f'{matiere_y}\n', fontsize=5)
						axs[y, x].tick_params(axis='y', labelsize=3)
						if y != n - 1:
							axs[y, x].set_xticks([])
						else:
							axs[y, x].set_xlabel(f'{matiere_x}', fontsize=6.8)
							axs[y, x].tick_params(axis='x', labelsize=3)
					elif y == n - 1:
						axs[y, x].set_xlabel(f'{matiere_x}', fontsize=6.8)
						axs[y, x].tick_params(axis='x', labelsize=3)
						axs[y, x].set_yticks([])
					else:
						axs[y, x].set_yticks([])
						axs[y, x].set_xticks([])
					if matiere_y == matiere_x :
						axs[y, x].hist([self.HufflepuffBookMark[matiere_x], self.GryffindorBookMark[matiere_x], self.RavenclawBookMark[matiere_x], self.SlytherinBookMark[matiere_x]],
						bins=5, density=True, color=['yellow', 'red', 'blue', 'green'], label=['Hufflepuff', 'Gryffindor', 'Ravenclaw', 'Slytherin'], alpha=0.5, edgecolor='black')
					else :
						point = 2
						axs[y, x].scatter(self.GryffindorBookMark[matiere_x], self.GryffindorBookMark[matiere_y], label='Gryffindor', color='red', s=point)
						axs[y, x].scatter(self.HufflepuffBookMark[matiere_x], self.HufflepuffBookMark[matiere_y], label='Hufflepuff', color='yellow', s=point)
						axs[y, x].scatter(self.RavenclawBookMark[matiere_x], self.RavenclawBookMark[matiere_y], label='Ravenclaw', color='blue', s=point)
						axs[y, x].scatter(self.SlytherinBookMark[matiere_x], self.SlytherinBookMark[matiere_y], label='Slytherin', color='green', s=point)

			# plt.tight_layout()  # Ajuste automatiquement la disposition pour éviter les chevauchements
			plt.tight_layout(pad=0, w_pad=0.05, h_pad=0.06)
			plt.show()

		except Exception as e:
			print('[ error ]  ->  pp.VisualizeRelations()\n', e)	



def main() :
	if len(sys.argv) != 2 :
		print('usage:  \'python3 histogram.py [-h] file')
		return
	else :
		csv_file_path = sys.argv[1]
	try :
		print('\n  # # # # # # # # # # # # # # # # # # # # # # # # # # # #')
		print('  #  #  #  #  # [  Pair Plot Visualization  ] #  #  #  #  #')
		print('  # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n')
		
		dataSet = extract_Datas_from_csv(csv_file_path)
		pp = Pair_Plot(dataSet)
		pp.VisualizeRelations()

	except ValueError :
		return

if __name__ == '__main__' :
	main()