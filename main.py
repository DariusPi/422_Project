# The input file is in the format:
# Number of cities: A B C D ...(N cities)
# Cost/Reliability matrix: A-B,A-C,A-D...B-C,B-D...C-D....(N(N-1)/2)
import edge_generator
import edge


def partition(arr, low, high):
	i = (low - 1)  # index of smaller element
	pivot = arr[high].getReliability()  # pivot

	for j in range(low, high):

		if arr[j].getReliability() <= pivot:
			# increment index of smaller element
			i = i + 1
			arr[i], arr[j] = arr[j], arr[i]

	arr[i + 1], arr[high] = arr[high], arr[i + 1]
	return i + 1


def quicksort(arr, low, high):
	if low < high:
		pi = partition(arr, low, high)

		quicksort(arr, low, pi - 1)
		quicksort(arr, pi + 1, high)


def minspan(arr, j):
	q = 0
	edges = list()
	vertices = list()
	while len(edges) < (j - 1):
		if (arr[q].vertice_1 in vertices) and (arr[q].vertice_2 in vertices):
			q = q + 1
		else:
			edges.append(arr[q])
			vertices.append(arr[q].vertice_1)
			vertices.append(arr[q].vertice_2)
			q = q + 1
	return edges


def sysreliability(arr, bol):
	rel = 1
	if bol == 1:
		for elem in arr:
			rel = rel * elem.getReliability()
	else:
		rel = 0
	return rel


def syscost(arr):
	cost = 0
	for elem in arr:
		cost = cost + elem.getCost()
	return cost


try:
	file_path = input("Please set input file path: ")
	reliability_goal = float(input("Please enter reliability goal: "))
	cost_constraint = int(input("Please enter cost constraint: "))
except Exception as e:
	print(e)
	exit()

if reliability_goal < 0.0 or reliability_goal >= 1.0:
	print("reliability goal must be positive and under 1")
else:
	city_list, edge_list = edge_generator.generate(file_path)
	print(city_list)
	print(edge_list)

	n = len(edge_list)
	k = len(city_list)
	quicksort(edge_list, 0, n - 1)
	edge_list.reverse()
	print(edge_list)
	tree = minspan(edge_list, k)
	print(tree)
	print(sysreliability(tree, 1))
	print(syscost(tree))
	if (sysreliability(tree, 1) >= reliability_goal) and (syscost(tree) <= cost_constraint):
		print("network found")
