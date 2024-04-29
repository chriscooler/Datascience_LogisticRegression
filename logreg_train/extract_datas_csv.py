import pandas as pd


def extract_Datas_from_csv(csv_file) :
	try :
		data = pd.read_csv(csv_file)
		data.replace('', pd.NA, inplace=True)
		# print(f"[Best Hand]: {data['Best Hand'].unique()}")
		# print(' -> We Will replace in [\'Best Hand\'] \'Left\' by 1 and \'Right\' by 2')
		# print(' -  and type the column as int64 in order to be displayed and potentially be used to train the Model')
		# data['Best Hand'] = data['Best Hand'].replace({'Left': 1, 'Right': 2})
		# data['Best Hand'] = data['Best Hand'].astype('int64')
		print(f'data.shape : {data.shape}')

		# data = data.apply(lambda col: col.fillna(col.mean()) if pd.api.types.is_numeric_dtype(col) and col.hasnans else col, axis=0)
		# ou :
		for x in range(data.shape[1]):
			for y in range(data.shape[0]):
				if pd.isna(data.iloc[y, x]):
					data.iloc[y, x] = data.iloc[:, x].mean()

	except :
		print(f'error: cannot read csv file: \'{csv_file}\'')
		raise ValueError

	# print(f'\n -[  data.info  ]-\n{data.info}')
	# print(f'\n -[  data.info()  ]-\n{data.info()}')
	# print(f'\n -[  data.describe()  ]-\n{data.describe()}')
	# print('\n -[  Data  ]-\n', data)

	return data