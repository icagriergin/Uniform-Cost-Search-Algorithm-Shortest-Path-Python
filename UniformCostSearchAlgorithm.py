import csv
import numpy as np
import pandas as pd
from queue import PriorityQueue as hq


class CityNotFoundError(Exception):
    def __init__(self, city):
        print("%s does not exist in Route csv file." % city)


def build_graph(dataSet):
    lines = {}
    df = pd.DataFrame(dataSet)
    groupedListForward = df.groupby(["city1"], as_index=False)[['city2', 'distance']].agg(lambda x: list(x))
    groupedListBackward = df.groupby(["city2"], as_index=False)[['city1', 'distance']].agg(lambda x: list(x))
    groupedListBackward.columns = ['city1', 'city2', 'distance']

    groupedList = groupedListForward.append(groupedListBackward)
    df = pd.DataFrame(groupedList)
    groupedList = df.groupby(["city1"], as_index=False)[['city2', 'distance']].agg(lambda x: list(x))
    for i in range(len(groupedList.values)):
        newCityList = []
        newDistanceList = []
        for j in range(len(groupedList.values[i][1])):
            newCityList += groupedList.values[i][1][j]
            newDistanceList += groupedList.values[i][2][j]
        groupedList.values[i][1] = newCityList
        groupedList.values[i][2] = newDistanceList
    for i in range(len(groupedList.values)):
        lines[groupedList.values[i][0]] = {}
        for j in range(len(groupedList.values[i][1])):
            lines[groupedList.values[i][0]][groupedList.values[i][1][j]] = groupedList.values[i][2][j]
    return lines


def uniform_cost_search(graph, start, end):

    heapQueue = hq()
    heapQueue.put((0, [start]))
    while not heapQueue.empty():
        current = heapQueue.get()
        currentCity = current[1][len(current[1]) - 1]
        if end in current[1]:
            print("Shortest Path: " + str(current[1]) + ", and It's Cost = " + str(current[0]))
            break
        cost = current[0]
        for neighbor in graph[currentCity]:
            list = current[1][:]
            list.append(neighbor)
            heapQueue.put((cost + graph[currentCity][neighbor], list))


if __name__ == "__main__":
    print("Enter City Road Map File Path: ")
    filePath = input()
    try:
        dataSet = pd.read_csv(filePath)
        print("Start City: ")
        startCity = input()
        print("Target City: ")
        targetCity = input()
        cityPath = build_graph(dataSet);
        if startCity not in cityPath:
            CityNotFoundError(startCity)
        elif  targetCity not in cityPath:
            CityNotFoundError(targetCity)
        else:
            uniform_cost_search(cityPath, startCity, targetCity)
    except OSError:
        print("File cannot found on : " + filePath)

