import sys
import pandas as pd
from extract_datas_csv import extract_Datas_from_csv
from sklearn.metrics import accuracy_score

class Accurary() :
	def __init__(self, dataSet_df, predictions_df) :

		self.dataSet = dataSet_df
		self.predictions_df = predictions_df

		# Calcul de l'accuracy avec sklearn
		accurancy = ( accuracy_score(self.dataSet['Hogwarts House'], self.predictions_df['Hogwarts House']) ) * 100
		print(f"Accurary ( sklearn )-> [ { accurancy } % ]\n")

		# Extrait les differences
		differences_df = self.dataSet[self.dataSet['Hogwarts House'] != self.predictions_df['Hogwarts House']]
		
		# Rearange l'affichage des Diffs
		results_dif_df = differences_df[['Index', 'Hogwarts House']].copy()
		results_dif_df = results_dif_df.rename(columns={'Hogwarts House' : 'True'})
		results_dif_df['False'] = self.predictions_df['Hogwarts House']
		results_dif_df['Proba'] = self.predictions_df['Proba']
		results_dif_df['Second Choice'] = self.predictions_df['Second House']
		results_dif_df['Second Proba'] = self.predictions_df['Second Proba']
		results_dif_df['Last Name'] = self.dataSet['Last Name']
		results_dif_df['First Name'] = self.dataSet['First Name']
		print(f'Differences : \n{results_dif_df}')

		# Accuracy si on avait selectionne le second choix 
		accurancy_second_choice = ( accuracy_score(results_dif_df['True'], results_dif_df['Second Choice']) ) * 100
		print(f"Accurary Second House Choice-> [ { accurancy_second_choice } % ]")
		falses_score = 100 - accurancy
		accu_corected = accurancy + (falses_score * accurancy_second_choice / 100 )
		print(f"Accurary Corrected -> [ { accu_corected } % ]")
		print('Ca ne fait malheuresement Aucun Sens Bro 😅 😘')

	

def main() :

	data_csv_file_path = '../dataset_train.csv'
	accuracy_perso_houses_cvs_file_path = '../results/accuracy_perso.csv'


	if len(sys.argv) !=  1:
		print('usage:  \'python3 accuracy.py\n  -> We already know where are the files Bro\n  --> Just run Me and Chill out Bro ! 😘')
		return

	try :
		print('\n  # # # # # # # # # # # # # # # # # # # # # # # # # # # #')
		print('  #  #  #  #  #  #  [ Model  Accuracy ]  #  #  #  #  #  #')
		print('  # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n')
		
		dataSet_df = extract_Datas_from_csv(data_csv_file_path)
		predictions_df = extract_Datas_from_csv(accuracy_perso_houses_cvs_file_path)
		Accurary(dataSet_df, predictions_df)

	except Exception as e :
		print(f'Usage [ Error ] -> : {e}')
		return

if __name__ == '__main__' :
	main()