import object
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

def compare_networks(net1, net2):
    links_analysis = {'Matches': [], 'Id Matches': [],
                      'Net1': [], 'Net2': []}
    for link in net2.pipes:
        if link in net1.pipes:
            if net1.pipes[link].connection == net2.pipes[link].connection:
                links_analysis['Matches'].append(link)
            else:
                links_analysis['Id Matches'].append(link)
                print(link, net1.pipes[link].connection, net2.pipes[link].connection)
        else:
            links_analysis['Net2'].append(link)

    print(len(links_analysis['Matches']))
    print(links_analysis['Id Matches'])

    junction = {'Matches': [], 'Id Matches': [], 'Net1': [], 'Net2': []}
    for node in net2.junction:
        if node in net1.junction:
            if net1.junction[node].x == net2.junction[node].x and net1.junction[node].y == net2.junction[node].y:
                junction['Matches'].append(node)
            else:
                junction['Id Matches'].append(node)
        else:
            junction['Net2'].append(node)

    for node in net1.junction:
        if node not in junction['Matches'] or node not in junction['Id Matches']:
            junction['Net2'].append(node)


def coord_check(net1, net2, senestivity=0.02):
    id_match = []
    match = []
    for n1 in net1.junction:
        interval_x = [net1.junction[n1].x - senestivity / 2, net1.junction[n1].x + senestivity / 2]
        interval_y = [net1.junction[n1].y - senestivity / 2, net1.junction[n1].y + senestivity / 2]
        for n2 in net2.junction:
            if interval_x[0] <= net2.junction[n2].x <= interval_x[1]:
                if interval_y[0] <= net1.junction[n1].y <= interval_y[1]:
                    if n1 == n2:
                        id_match.append(n1)
                    else:
                        match.append([n1, n2])

    print(len(match))
    print(len(id_match))
    print(len(id_match)+len(match))
    print(len(net1.junction))

def node_type(net, id):
    if id in net.junction:
        return 0
    elif id in net.tanks:
        return 1
    elif id in net.reservoirs:
        return 2

def senetivity(x, y, sens):
    return [x - sens / 2, x + sens / 2], [y - sens / 2, y + sens / 2]

def distance(n1, n2):
    x_sqrdiff = (n1[0] - n2[0]) ** 2
    y_sqrdiff = (n1[1] - n2[1]) ** 2
    return np.sqrt(x_sqrdiff + y_sqrdiff)

def node_accumulation(net, sensitivity=0.01):
    acc = []
    for check in net.nodes:
        for compare in net.nodes:
            if check != compare:


                r = distance([net.nodes[check].x,net.nodes[check].y],
                             [net.nodes[compare].x, net.nodes[compare].y])

                if r < sensitivity and (compare, check) not in acc:
                    acc.append((check, compare))

    print(acc)


net = object.Network('Trykknett.inp')