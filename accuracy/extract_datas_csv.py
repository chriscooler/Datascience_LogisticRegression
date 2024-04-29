import pandas as pd


def extract_Datas_from_csv(csv_file) :
	try :
		data = pd.read_csv(csv_file)
		data.replace('', pd.NA, inplace=True)
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