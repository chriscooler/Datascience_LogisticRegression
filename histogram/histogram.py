import sys
import matplotlib.pyplot as plt
from extract_datas_csv import extract_Datas_from_csv


class Histogram() :
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
			self.GryffindorBookMark = self.byHousesDataSets['Gryffindor'].iloc[:, 5:]
			self.SlytherinBookMark = self.byHousesDataSets['Slytherin'].iloc[:, 5:]
			self.HufflepuffBookMark = self.byHousesDataSets['Hufflepuff'].iloc[:, 5:]
			self.RavenclawBookMark = self.byHousesDataSets['Ravenclaw'].iloc[:, 5:]
			self.courses = self.GryffindorBookMark.columns
		except Exception as e:
			print('[ error ]  ->  his.getStudentsByHouses()', e)



	def vizualiseHistograms1b1(self) :
		choix = '?'
		for course in self.courses:
			plt.figure(figsize=(10, 6))
			plt.hist([self.HufflepuffBookMark[course], self.GryffindorBookMark[course], self.RavenclawBookMark[course], self.SlytherinBookMark[course]],
			bins=20, density=True, color=['yellow', 'red', 'blue', 'green'], label=['Hufflepuff', 'Gryffindor', 'Ravenclaw', 'Slytherin'], alpha=0.7, edgecolor='black')
			plt.title(f'Histogram pour la matière {course}')
			plt.xlabel('Notes')
			plt.ylabel('Fréquence')
			plt.legend()
			plt.show()

		try :
			while choix == '?' :
				choix = str(input('\n 0=/===[ Bonux ]==>\nWould you like to Visualize \'Fusion\' Histograms ?\n\t-> [ y ] Yes\n\t-> [ n ] No\n -> '))
				if choix != 'y' and choix != 'n' :
					choix = '?'
					print("[ error ] -> usage: input must be 'y' or 'n'.\n")
			
			if choix == 'n' :
				return
			else :
				for course in self.courses:
					plt.title(f'Histogram pour la matière {course}')
					for house in self.houses:
						coursesPerHouse = self.dataSet[self.dataSet['Hogwarts House'] == house]
						plt.hist(coursesPerHouse[course].dropna(), bins=20, label=house, alpha=0.5)
					plt.xlabel('Notes')
					plt.ylabel('Nbr Eleves')
					plt.legend()
					plt.show()
			
		except Exception as e:
			print('[ error ]  ->  his.vizualiseHistograms1b1()\n', e)	



	def vizualiseSubplotHistograms(self) :
		num_courses = len(self.courses)
		num_cols = 4  # display par column
		num_rows = num_courses // num_cols + num_courses % num_cols  # Calcul du nombre de lignes

		plt.figure(figsize=(15, 10))
		for i, course in enumerate(self.courses, start=1):
			plt.subplot(num_rows, num_cols, i)
			plt.hist([self.HufflepuffBookMark[course], self.GryffindorBookMark[course], self.RavenclawBookMark[course], self.SlytherinBookMark[course]],
			bins=10, color=['yellow', 'red', 'blue', 'green'], label=['Hufflepuff', 'Gryffindor', 'Ravenclaw', 'Slytherin'], edgecolor='black')
			plt.title(f'* {course} *')
			plt.xlabel('Notes')
			plt.ylabel('Fréquence')

		plt.suptitle(f'*red: [ Gryffindor ]      *yellow: [ Hufflepuff ]      *blue: [ Ravenclaw ]      *green: [ Slytherin ]')
		plt.tight_layout() # Ajuste automatiquement la disposition pour éviter les chevauchements
		plt.show()

		try :
			choix = '?'
			while choix == '?' :
				choix = str(input('\n 0=/===[ Bonux ]==>\nWould you like to Visualize Histogram differently ?\n\t-> [ y ] Yes\n\t-> [ n ] No\n -> '))
				if choix != 'y' and choix != 'n' :
					choix = '?'
					print("[ error ] -> usage: input must be 'y' or 'n'.\n")
			
			if choix == 'n' :
				return
			else :
				plt.figure(figsize=(15, 10))
				for i, course in enumerate(self.courses, start=1):
					plt.subplot(num_rows, num_cols, i)
					plt.title(f"* {course} *")
					for house in self.houses:
						coursesPerHouse = self.byHousesDataSets[house]
						plt.hist(coursesPerHouse[course].dropna(), bins=20, label=house, alpha=0.5)
				plt.xlabel('Notes')
				plt.ylabel('Nbr Eleves')
				plt.legend()
				plt.tight_layout()
				plt.show()
			
		except Exception as e:
			print('[ error ]  ->  his.vizualiseSubplotHistograms()\n', e)


	def whatUSerWants(self) :
		try :
			choix = 0
			while choix == 0 :
				try :
					choix = int(input('\nWhat would you like to do ?\n\t-> [1] Visuaze Histograms One By One\n\t-> [2] Visualize Histograms Globally\n\t-> [3] Exit\n -> '))
					if choix != 1 and choix != 2 and choix != 3:
						choix = 0
						raise ValueError
				except :
					print("[ error ] -> usage: input must be '1', '2' or '3'.\n")
			if choix == 1 :
				self.vizualiseHistograms1b1()
			elif choix ==2 :
				self.vizualiseSubplotHistograms()
			elif choix == 3 :
				return
			
		except Exception as e:
			print('[ error ]  ->  his.whatUSerWants():\n', e)	



def main() :
	if len(sys.argv) != 2 :
		print('usage:  \'python3 histogram.py [-h] file')
		return
	else :
		csv_file_path = sys.argv[1]

	try :
		print('\n  # # # # # # # # # # # # # # # # # # # # # # # # # # # #')
		print('  #  #  #  #  #  [ Histogram Visualization ]  #  #  #  #  #')
		print('  # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n')
		
		dataSet = extract_Datas_from_csv(csv_file_path)
		his = Histogram(dataSet)
		his.whatUSerWants()
	except ValueError :
		return

if __name__ == '__main__' :
	main()