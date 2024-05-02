# Et oui ! la regression logistique est une methode de classification et non pas reelement de prediction 
import os
import sys
import csv
import numpy as np
import pandas as pd
from extract_datas_csv import extract_Datas_from_csv


class Logreg_Predict():
	def __init__(self, dataSet) -> None:
		
		self.weights_csv_file_path = '../results/weights.csv'
		self.houses_csv_file_path = '../results/houses.csv'
		self.accuracy_csv_file_path = '../results/accuracy_perso.csv'

		self.dataSet = dataSet
		self.dataTest = 0
		self.features = []
		self.weights_df =[]
		self.houses = 0
		self.n_lines = 0
		self.predict_Df = 0
		

		self.define_AndGet_TestSet()



	def get_features_from_Csv(self) :
		with open(self.weights_csv_file_path, 'r', newline='') as weight_csv :
			the_file = csv.reader(weight_csv)
			# la premiere ligne 
			self.features = next(the_file)
			self.features.remove('Hogwarts House')
			print(f'Features used for classification: {self.features}')


	def standadizeDatas(self) :
		try :
			# moyenne par ecart type de chaque colonne
			means = np.mean(self.dataTest, axis = 0)
			stds = np.std(self.dataTest, axis = 0)
			self.dataTest = (self.dataTest - means) / stds
		except Exception as e :
			print('[ error ]  ->  Standardization : ', e)
			


	def define_AndGet_TestSet(self) :
		try :
			self.get_features_from_Csv()
			# Creer un DataFrame pour recup les poids en fonction des mifs
			self.weights_df = pd.read_csv(self.weights_csv_file_path)
			# Creation du DataSet pour les predictions
			self.dataTest = self.dataSet[self.features]
			self.standadizeDatas()
			print(self.dataTest.head(5))

			# Recupere le nom des differentes maisons
			self.houses = self.weights_df['Hogwarts House'].unique()
			print(f'Unique Hogwarts House (Weights): {self.houses}')
			# Ajoute une colonne 'Probas' au Df des weights pour les futurs calculs
			self.weights_df = self.weights_df.assign(Probas = 0.0)
			print(self.weights_df)

			self.n_lines = len(self.dataSet)
			self.predict_Df = pd.DataFrame({
				'Index': range(self.n_lines),
				'Hogwarts House': [''] * self.n_lines
			})
   
			self.accuracy_Df = pd.DataFrame({
				'Index': range(self.n_lines),
				'Hogwarts House': [''] * self.n_lines,
				'Proba': [0.0] * self.n_lines,
				'Second House': [''] * self.n_lines,
				'Second Proba': [0.0] * self.n_lines
			})			
		except Exception as e :
			print('[ error ]  ->  define_AndGet_TestSet : ', e)
			
	def sigmoid(self, x) :
		return 1 / ( 1 + np.exp( -x ) )

	def Predictions(self) :
		try :
			# Index de la colonne 'Probas' pour l'eliminer des calculs
			i_prob = len(self.weights_df.columns) - 1
			
			for row_index, row in self.dataTest.iterrows() :
				max_prob = 0.0
				second_prob = 0.0
				main_house = ''
				second_house = ''

				for l, line in self.weights_df.iterrows() :

					logit_scores = np.dot(line.values[1:i_prob], row.values)
					proba = self.sigmoid(logit_scores)
					self.weights_df.at[l, 'Probas'] = proba

					if proba > max_prob :
						second_prob = max_prob
						max_prob = proba
						second_house = main_house
						main_house = line['Hogwarts House']
					elif proba > second_prob :
						second_prob = proba
						second_house = line['Hogwarts House']
				
				self.predict_Df.at[row_index, 'Index'] = row_index
				self.predict_Df.at[row_index, 'Hogwarts House'] = main_house
				self.accuracy_Df.at[row_index, 'Index'] = row_index
				self.accuracy_Df.at[row_index, 'Hogwarts House'] = main_house
				self.accuracy_Df.at[row_index, 'Second House'] = second_house
				self.accuracy_Df.at[row_index, 'Proba'] = max_prob
				self.accuracy_Df.at[row_index, 'Second Proba'] = second_prob
				
			print('\n --> self.predict_Df.head(6) <--')		
			print(self.predict_Df.head(7))

			# Verif si file deja existant for delete
			if os.path.exists(self.houses_csv_file_path) :
				os.remove(self.houses_csv_file_path)
				print(f"Former File '{self.houses_csv_file_path}' removed !")
			# Enregistrement des results en CSV
			self.predict_Df.to_csv(self.houses_csv_file_path, index=False)
			print(f"New File '{self.houses_csv_file_path}' succesfully created !")

			# second fichier pour accuracy Perso
			
			if os.path.exists(self.accuracy_csv_file_path) :
				os.remove(self.accuracy_csv_file_path)
				print(f"Former File '{self.accuracy_csv_file_path}' removed !")
			self.accuracy_Df.to_csv(self.accuracy_csv_file_path, index=False)
			print(f"New File '{self.accuracy_csv_file_path}' succesfully created !")

		except Exception as e :
			print('[ error ]  ->  Prediction : ', e)



def main() :
	if len(sys.argv) != 2 :
		print('usage:  \'python3 logreg_classification.py [-h] file')
		return
	else :
		data_csv_file_path = sys.argv[1]

	try :
		print('\n  # # # # # # # # # # # # # # # # # # # # # # # # # # # #')
		print('  #  #  #  #  # [ Logistic Regression Predictions ] #  #  #  #  #')
		print('  # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n')
		
		dataSet = extract_Datas_from_csv(data_csv_file_path)
		predict = Logreg_Predict(dataSet)
		predict.Predictions()	

	except ValueError :
		return

if __name__ == '__main__' :
	main()