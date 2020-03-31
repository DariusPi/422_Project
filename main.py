# The input file is in the format:
# Number of cities: A B C D ...(N cities)
# Cost/Reliability matrix: A-B,A-C,A-D...B-C,B-D...C-D....(N(N-1)/2)
import edge_generator
import edge


def bitfield(number):
    return [1 if digit == '1' else 0 for digit in bin(number)[2:]]


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
        for index in range(0, 2 ** (len(arr))):
            ntree = list()
            # build tree
            encoded = bitfield(index)
            while len(encoded) != len(arr):
                encoded.insert(0, 0)
            # print(encoded)
            for tes in range(0, len(arr)):
                if encoded[tes] == 1:
                    ntree.append(arr[tes])
            # print(ntree)
            path = True
            for elem in range(1, len(city_list)):
                vis = list()
                if not findpath(ntree, city_list[0], city_list[elem], vis):
                    path = False
                    break
            if path:
                # multiply reliability of edges in ntree and 1 - reliability of edges not in ntree
                # print("path found")
                product = 1
                for ed in arr:
                    if ed in ntree:
                        product = product * ed.getReliability()
                    else:
                        product = product * (1 - ed.getReliability())
                rel = rel + product
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
    print(sysreliability(tree, 0))
    max_reliability = 0
    max_network = list()
    optimal_reliability = sysreliability(edge_list, 0)
    optimal_cost = syscost(edge_list)
    if reliability_goal > optimal_reliability:
        print("No network possible to meet reliability constraint: ")
    elif cost_constraint > optimal_cost:
        print("Optimal network found: ")
        print(edge_list)
        print("reliability = ")
        print(optimal_reliability)
        print(" cost :")
        print(optimal_cost)
    else:
        first_found = False
        for idx in range((2 ** (len(city_list)) - 1), 2 ** (len(edge_list))):
            #print(idx)
            gh = list()
            encod = bitfield(idx)
            if encod.count(1) >= 6:
                while len(encod) != len(edge_list):
                    encod.insert(0, 0)
                for ts in range(0, len(edge_list)):
                    if encod[ts] == 1:
                        gh.append(edge_list[ts])
                if first_found or syscost(gh) <= cost_constraint:
                    temp_reliability = sysreliability(gh, 0)
                    if not first_found:
                        if temp_reliability >= reliability_goal:
                            print("first network that meets goal found : ")
                            print(gh)
                            first_found = True
                            if syscost(gh) <= cost_constraint:
                                max_reliability = temp_reliability
                                max_network = gh
                    else:
                        if (temp_reliability >= max_reliability) and (syscost(gh) <= cost_constraint):
                            max_reliability = temp_reliability
                            max_network = gh

        if max_reliability == 0:
            print("No suitable network found for cost constraint")
        else:
            print("Optimal network found: ")
            print(max_network)
            print("reliability = ")
            print(max_reliability)
            print(" cost :")
            print(syscost(max_network))
