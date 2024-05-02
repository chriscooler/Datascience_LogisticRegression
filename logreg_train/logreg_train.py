import os
import sys
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from extract_datas_csv import extract_Datas_from_csv

class Logreg_Train():
	def __init__(self, dataSet) -> None:

		self.weights_csv_file_path = '../results/weights.csv'
		self.learning_rate = 0.002
		self.epochs = 10000
		self.stochastic_lr = 0.002
		self.stochastic_epochs = 10
		self.miniBatch_lr = 0.005
		self.miniBatch_epochs = 5
		self.batch_size = 5
		self.n_batches = len(dataSet) // self.batch_size

		self.dataSet = dataSet
		self.dataTrain = 0
		self.n_lines = len(self.dataSet)
		self.houses = 0
		self.weights = []
		self.cost_history = []

		self.defineAndGetTrainSet()


	def standadizeDatas(self) :
		try :
			# moyenne par ecart type de chaque colonne
			means = np.mean(self.dataTrain, axis = 0)
			stds = np.std(self.dataTrain, axis = 0)
			self.dataTrain = (self.dataTrain - means) / stds
		except Exception as e :
			print('[ error ]  ->  Standardization : ', e)
			

	def defineAndGetTrainSet(self) :
		self.dataTrain = self.dataSet
		# Commented lines are used for Model Training, except for 'Hogwarts House' 
		columns_to_drop = [
			'Index',
			'First Name',
			'Last Name',
			'Birthday',
			'Best Hand',
			'Arithmancy',
			'Herbology',
			'Muggle Studies',
			'Potions',
			'Care of Magical Creatures',
			]
		self.dataTrain = self.dataTrain.drop(columns=columns_to_drop)
		self.dataTrain = self.dataTrain.drop(columns='Hogwarts House')
		self.standadizeDatas()

		# Ajoute une colonne pour qui sera remplis de 1 et 0 pour les calculs
		self.dataTrain['One vs All'] = np.float64(0)

		# Ajoute une colonne de biais remplis de 1
		self.dataTrain['Biais'] = np.float64(1)
		self.dataTrain.info()
		
		# Recupere le nom des differentes maisons
		self.houses = self.dataSet['Hogwarts House'].unique()
		print(f'Unique Hogwarts House: {self.houses}')

		# Creation du fichier weights.csv qui sera parse par le prog de prediction
		features = [column for column in self.dataSet.columns if column not in columns_to_drop]
		# print(f'Columns To CSV -> {features}')
		
		# Init des Weights pour les calcules:
		weights_value = 1 / (len(features) - 1)
		# +2 pour 'Biais' et 'One vs All' et -1 car [0] :)
		self.weights = [weights_value] * (len(features) + 2 - 1)	

		# Verif si file deja existant for delete
		if os.path.exists(self.weights_csv_file_path) :
			os.remove(self.weights_csv_file_path)
			print(f"File '{self.weights_csv_file_path}' removed !")
		# Creation du file.csv et del la premiere ligne de features utilises
		with open(self.weights_csv_file_path, 'w') as file_csv:
			file_csv.write(','.join(features) + '\n')



	def Standard_Logistic_Regression(self) :

		for house in self.houses:
			print(f' Train House -> [{house}]')
			# Remplace la house par 1 et le reste par 0
			self.dataTrain['One vs All'] = (self.dataSet['Hogwarts House'] == house).astype(float)

			self.Gradient_Descent()

			# Display les cost du model par maison
			self.plot_cost_function(house, self.epochs)
			self.cost_history =[]

			# re-convert from numpy to list pour csv.writter + -2 pour exclure 'Biais' et 'One vs All'
			weights_list = self.weights[:-2].tolist()
			# Ajout de la ligne avec les poids de la house dans le fichier Csv
			with open(self.weights_csv_file_path, 'a', newline='') as file_csv :
				writer = csv.writer(file_csv)
				writer.writerow( [house] + weights_list )

	def Gradient(self, z, y_true) :
		y_pred = self.sigmoid_function(z)
		gradient = np.dot(z.T, (y_pred - y_true) / len(y_true))
		return gradient 

	def Gradient_Descent(self) :
		try :
			y_true = self.dataTrain['One vs All'].to_numpy()
			z = self.dataTrain.to_numpy() 
			for n in range(self.epochs) :
				self.weights = self.weights - self.learning_rate * self.Gradient( z, y_true)
				predictions = self.sigmoid_function( z )
				cost_loss = -np.mean(y_true * np.log(predictions) + (1 - y_true) * np.log(1 - predictions))
				self.cost_history.append(cost_loss)
		except Exception as e:
			print('[ error ]  ->  Gradient_Descent : ', e)



	def sigmoid_function(self, z) :
		try :
			sig = 1 / (1 +  np.exp( -z @ self.weights))
			return sig
		except Exception as e :
			print('[ error ]  ->  Sigmoid Function : ', e)	



	def Stoch_Gradient(self, z_i, yTrue_i) :
		y_pred = self.sigmoid_function( z_i )
		gradient = np.dot(z_i.T, (y_pred - yTrue_i))
		return gradient 
	
	def Stochastic_Gradiant_Descent(self) :
		try:
			for house in self.houses:
				print(f' Train House -> [{house}]')	
				self.dataTrain['One vs All'] = (self.dataSet['Hogwarts House'] == house).astype(float)
				y_true = self.dataTrain['One vs All'].to_numpy()
				z = self.dataTrain.to_numpy()

				for n in range(self.stochastic_epochs) :
					for i in range(self.n_lines) :
						y_i = y_true[i]
						z_i = z[i]
						self.weights = self.weights - self.stochastic_lr * self.Stoch_Gradient( z_i, y_i)

					predictions = self.sigmoid_function(z_i)
					cost_loss = -np.mean(y_i * np.log(predictions) + (1 - y_i) * np.log(1 - predictions))
					self.cost_history.append(cost_loss)
				
				self.plot_cost_function(house, self.stochastic_epochs)
				self.cost_history =[]			
				weights_list = self.weights[:-2].tolist()
				# Ajout de la ligne avec les poids de la house dans le fichier Csv
				with open(self.weights_csv_file_path, 'a', newline='') as file_csv :
					writer = csv.writer(file_csv)
					writer.writerow( [house] + weights_list )

		except Exception as e :
			print('[ error ]  ->  Stochastic_Gradient_Descent : ', e)


	def Mini_Batch_Gradiant_Descent(self) :
		try:
			for house in self.houses:
				print(f' Train House -> [{house}]')

				self.dataTrain['One vs All'] = (self.dataSet['Hogwarts House'] == house).astype(float)
				y_true = self.dataTrain['One vs All']
				z = self.dataTrain

				for n in range(self.miniBatch_epochs) :
					for i in range(self.n_batches) :
						# Creations des Mini Samples en calculant index debut et fin pour chaque sample
						start_i = i * self.batch_size
						end_i = (i + 1) * self.batch_size
						y_batch = y_true[ start_i : end_i ].to_numpy()
						z_batch = z[ start_i : end_i ].to_numpy()
						self.weights = self.weights - self.miniBatch_lr * self.Gradient( z_batch, y_batch)

					predictions = self.sigmoid_function(z_batch)
					cost_loss = -np.mean(y_batch * np.log(predictions) + (1 - y_batch) * np.log(1 - predictions))
					self.cost_history.append(cost_loss)
				
				self.plot_cost_function(house, self.miniBatch_epochs)
				self.cost_history =[]			
				weights_list = self.weights[:-2].tolist()
				# Ajout de la ligne avec les poids de la house dans le fichier Csv
				with open(self.weights_csv_file_path, 'a', newline='') as file_csv :
					writer = csv.writer(file_csv)
					writer.writerow( [house] + weights_list )

		except Exception as e :
			print('[ error ]  ->  Mini_Batch_Gradient_Descent : ', e)



	# La fonction Sigmoid permet d'obtenir les probabilites log entre [0 et 1]
	# Cest une composante indispensable de la fonction de cout car ce sont les predictions de proba
	# que l'on va comparer au donnees labelisees et ainsi calculer le cout ou ecart a la verite
	# afin de continuer a y appliquer un nouveau tour de descente de gradiant avec un pas (learning rate) supplementaire
	# ( p < 0.5 donc false n'appartient pas a la classe quon test)
	# ( p > 0.5 donc true appartient a la classe quon test)
		
	# Voir pour Mettre demarcation ou element supp dans une colne avec le score et dans
	# une colonne categories 'a'[< 0.2 et > 0.8], 'b'[ >0.2 && < 0.35  || > 0.65 && < 0.8],
	# et categorie 'c'[le reste], les seulement proba 65 % max :), les "indecis"  

	def	plot_cost_function(self, house, epochs) :
		plt.title(f' [ {house} ] Cost Evolution for [ {epochs} ] iterations ')
		plt.xlabel("epochs")
		plt.ylabel('cost')
		plt.plot(range(epochs), self.cost_history)
		plt.show()


	def train(self) :
		choice = 0
		while choice != 4 :
			try :
				choice = int(input('\nWich Method would you like to use to train the Model ? \
					   \n\n\t-> [ 1 ]  Standard Gradiant Descent (Batch Gradient Descent) \
					   \n\t-> [ 2 ]  Stochastic Gradiant Descent (SGD) \
					   \n\t-> [ 3 ]  Mini Batch Gradiant Descent \
					   \n\t-> [ 4 ]  Exit \
					   \n\n\t->   '))
			except ValueError :
				print(' >< Error >< usage: 1, 2, 3 or 4 !')
				choice = 0
			if choice == 1 :
				print('  #  #  #  #  # [ Standard Logistic Regression ] #  #  #  #  #')
				self.Standard_Logistic_Regression()
				return
			if choice == 2 :
				print('  #  #  #  #  # [ Stochastic Logistic Regression ] #  #  #  #  #')
				self.Stochastic_Gradiant_Descent()
				return
			if choice == 3 :
				print('  #  #  #  #  # [ Mini - Batch Logistic Regression ] #  #  #  #  #')
				self.Mini_Batch_Gradiant_Descent()
				return



def main() :
	if len(sys.argv) != 2 :
		print('usage:  \'python3 logreg_train.py [-h] file')
		return
	else :
		csv_file_path = sys.argv[1]

	try :
		print('\n  # # # # # # # # # # # # # # # # # # # # # # # # # # # #')
		print('  #  #  #  #  # [ Logistic Regression Train ] #  #  #  #  #')
		print('  # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n')
		
		dataSet = extract_Datas_from_csv(csv_file_path)
		model = Logreg_Train(dataSet)
		model.train()

	except ValueError :
		return

if __name__ == '__main__' :
	main()













	# def getStudentsByHouses(self) :
	# 	try :
	# 		self.houses = self.dataSet['Hogwarts House'].unique()
	# 		print(f'Hogwarts Houses: \t{self.houses}')
	# 		for maison in self.houses :
	# 			self.byHousesDataSets[maison] = self.dataSet[self.dataSet['Hogwarts House'] == maison]
	# 		# [ Debug ]
	# 		# for maison, sous_dataset in self.byHousesDataSets.items():
	# 		# 	print(f"Élèves de la maison {maison} :\n{sous_dataset}\n")
	# 		self.GryffindorBookMark = self.byHousesDataSets['Gryffindor'].iloc[:, 5:]
	# 		self.SlytherinBookMark = self.byHousesDataSets['Slytherin'].iloc[:, 5:]
	# 		self.HufflepuffBookMark = self.byHousesDataSets['Hufflepuff'].iloc[:, 5:]
	# 		self.RavenclawBookMark = self.byHousesDataSets['Ravenclaw'].iloc[:, 5:]
	# 		self.courses = self.GryffindorBookMark.columns
	# 	except Exception as e:
	# 		print('[ error ]  ->  logReg_train.getStudentsByHouses()', e)