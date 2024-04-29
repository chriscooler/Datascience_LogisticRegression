import matplotlib.pyplot as plt

def display_scatter_2_colums(column_x, column_y, name_x, name_y) :
	if len(column_x) == len(column_y) == 2 :
		plt.xlabel(name_x)
		plt.ylabel(name_y)
		plt.title(f'Visualization ({name_x}) by ({name_y})')
		plt.scatter(column_x, column_y)
		plt.show()
	else :
		print(' [ Error ]: display_scatter_2_colums(): csv file must only have 2 Columns')
		raise ValueError