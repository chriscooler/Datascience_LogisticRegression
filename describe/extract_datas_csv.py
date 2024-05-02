import pandas as pd


def extract_Datas_from_csv(csv_file) :
	try :
		data = pd.read_csv(csv_file)
		data.replace('', pd.NA, inplace=True)
		print(f"[Best Hand]: {data['Best Hand'].unique()}")
		print(' -> We Will replace in [\'Best Hand\'] \'Left\' by 1 and \'Right\' by 2')
		print(' -  and type the column as int64 in order to be displayed and potentially be used to train the Model')
		data['Best Hand'] = data['Best Hand'].replace({'Left': 1, 'Right': 2})
		data['Best Hand'] = data['Best Hand'].astype('int64')

	except :
		print(f'error: cannot read csv file: \'{csv_file}\'')
		raise ValueError

	return data