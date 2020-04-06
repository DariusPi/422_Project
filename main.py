# The input file is in the format:
# Number of cities: A B C D ...(N cities)
# Cost/Reliability matrix: A-B,A-C,A-D...B-C,B-D...C-D....(N(N-1)/2)
import edge_generator
import edge


# Method that converts an integer to a binary array
def bitfield(number):
    return [1 if digit == '1' else 0 for digit in bin(number)[2:]]


# Boolean method that determines if a better version of the network was already found
def worsenetwork(current, goods):
    for elem in goods:
        match = True
        for bit in range(0, len(current)):
            if current[bit] == 1 and elem[bit] == 0:
                match = False
                break
        if match:
            return True
    return False


# Boolean method that determines if there is a path to all nodes
def isvalidnetwork(arr, cities):
    for elem in range(1, len(cities)):
        vis = list()
        if not findpath(arr, cities[0], cities[elem], vis):
            return False
    return True


# Boolean recursive method that determines if there is a path from one node to another in a network
def findpath(arr, current, target, visited):
    visited.append(current)
    for elem in arr:
        if elem.vertice_1 == current:
            if elem.vertice_2 == target:
                return True
            elif elem.vertice_2 not in visited:
                suc = findpath(arr, elem.vertice_2, target, visited)
                if suc:
                    return True
                else:
                    visited.remove(elem.vertice_2)
        elif elem.vertice_2 == current:
            if elem.vertice_1 == target:
                return True
            elif elem.vertice_1 not in visited:
                suc = findpath(arr, elem.vertice_1, target, visited)
                if suc:
                    return True
                else:
                    visited.remove(elem.vertice_1)
    return False


# Quicksort helper method to find partition point based on reliability of edges
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


# Recursive sorting algorithm
def quicksort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quicksort(arr, low, pi - 1)
        quicksort(arr, pi + 1, high)


# Method to find the most reliable spanning tree of a network
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


# Method to find the reliability of a network by enumeration
def sysreliability(arr):
    rel = 0
    for index in range(0, 2 ** (len(arr))):
        ntree = list()
        # build tree
        encoded = bitfield(index)
        while len(encoded) != len(arr):
            encoded.insert(0, 0)

        for tes in range(0, len(arr)):
            if encoded[tes] == 1:
                ntree.append(arr[tes])
        path = isvalidnetwork(ntree, city_list)
        if path:
            # multiply reliability of edges in ntree and 1 - reliability of edges not in ntree
            product = 1
            for ed in arr:
                if ed in ntree:
                    product = product * ed.getReliability()
                else:
                    product = product * (1 - ed.getReliability())
            rel = rel + product
    return rel


# Method to find the cost of a network
def syscost(arr):
    cost = 0
    for elem in arr:
        cost = cost + elem.getCost()
    return cost


# Main program begins here
# Take input and output error if incorrect format
try:
    file_path = input("Please set input file path: ")
    reliability_goal = float(input("Please enter reliability goal: "))
    cost_constraint = int(input("Please enter cost constraint: "))
except Exception as e:
    print(e)
    exit()

if reliability_goal < 0.0 or reliability_goal >= 1.0:
    print("reliability goal must be positive and under 1")
elif cost_constraint < 0.0:
    print("cost constraint must be positive")
else:
    city_list, edge_list = edge_generator.generate(file_path)
    print("city list: ", end='')
    print(city_list)
    print("edge list: ", end='')
    print(edge_list)

    # sort edges by reliability
    n = len(edge_list)
    k = len(city_list)
    quicksort(edge_list, 0, n - 1)
    max_reliability = 0
    max_network = list()
    max_network_index = 0

    # Determine max possible reliability of network and max cost
    optimal_reliability = sysreliability(edge_list)
    optimal_cost = syscost(edge_list)
    found_list = list()
    if reliability_goal > optimal_reliability:
        print("No network possible to meet reliability constraint: ")
    elif cost_constraint > optimal_cost:
        print("\na) and b) Optimal network found: ")
        print(edge_list)
        print("reliability = ")
        print(optimal_reliability)
        print("cost :")
        print(optimal_cost)
    else:
        # Network with all edges meets reliability target
        print("\na) Network that meets reliability goal: ")
        print(edge_list)
        print("reliability = ")
        print(optimal_reliability)
        print("cost :")
        print(optimal_cost)
        print("\nb) Finding Best Network for Cost Constraint: This process can take a while...")
        for idx in range(2 ** (len(edge_list)), (2 ** (len(city_list)) - 1), -1):
            gh = list()
            encod = bitfield(idx)
            if encod.count(1) >= 6:
                while len(encod) != len(edge_list):
                    encod.insert(0, 0)
                for ts in range(0, len(edge_list)):
                    if encod[ts] == 1:
                        gh.append(edge_list[ts])
                if (syscost(gh) <= cost_constraint) and not (worsenetwork(encod, found_list)):
                    found_list.append(encod)
                    if isvalidnetwork(gh, city_list):
                        temp_reliability = sysreliability(gh)
                        if temp_reliability > max_reliability:
                            max_reliability = temp_reliability
                            max_network_index = idx

        if max_reliability == 0:
            print("No network found for cost constraint and reliability target")
        else:
            print("Optimal network found: ")
            encode = bitfield(max_network_index)
            while len(encode) != len(edge_list):
                encode.insert(0, 0)
            for ts in range(0, len(edge_list)):
                if encode[ts] == 1:
                    max_network.append(edge_list[ts])
            print(max_network)
            print("reliability = ")
            print(max_reliability)
            print("cost :")
            print(syscost(max_network))
