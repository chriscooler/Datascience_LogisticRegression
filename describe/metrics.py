import numpy as np


def moyenne(column) -> float :
	mean = np.sum(column)  / len(column)
	return float(mean)


def ecart_type(column, mean) -> float :
	stdev = np.sqrt(np.sum((column - mean) ** 2) / (len(column) - 1))
	return float(stdev)


def minimum(column) -> float :
	sorted_column = np.sort(column)
	return float(sorted_column[0])


def maximum(column) -> float :
	sorted_column = np.sort(column)
	return float(sorted_column[len(sorted_column) - 1])


# Pour obtenir q1, q doit etre egale a 0.25, median q = 0.5, q3 q = 0.75 !	
def quartiles(column, q) -> float :
	sorted_column = np.sort(column)
	n = len (sorted_column)

	try :
		if q == 0.5 :
			if n % 2 != 0 : # dataset nbr values impaire
				index_mediane = int((n + 1) / 2) - 1
				return float(sorted_column[index_mediane])
			else :
				index_mediane = int(n / 2) - 1
				mediane = (sorted_column[index_mediane] + sorted_column[index_mediane + 1]) / 2
				return float(mediane)
		else :
			index = int( (n / (1 / q)) - 1 )
			value = (sorted_column[index] + sorted_column[index + 1]) / 2
			# print(f'Q( {q} % ) index[ {index} ]  -> Value: {value}')
			return float(value)
		
	except ValueError:
		print(f' ><* Error *><   - -->   quartiles\n[ Value Error ] -> {ValueError}',)


def deciles(column, d) -> float :
	sorted_column = np.sort(column)
	index = d * len(column) - 1
	if index % 1 != 0 : # Si la position n'est pas egale a un index, prend moyenne sup et inf
		i = int(index)
		return float((sorted_column[i] + sorted_column[i + 1]) / 2)
	else :
		return float(sorted_column[ int(index)])



	
	