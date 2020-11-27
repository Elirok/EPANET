import csv
import sys
import os

inputfile = "Net3/Net3.inp"

def none(line, n):
    return line, n

def junction(line, n):
    if 'ID' in line or 'JUNCTION' in line:
        return line, n

    temp = line.split()
    node = 'J{}'.format(n)
    if len(temp[0]) > len(node):
        node = '{}\t'.format(node)

    line = line.replace(temp[0], node, 1)
    nodes[temp[0]] = node
    return line, n + 1

def tank(line, n):
    if 'ID' in line or 'TANK' in line:
        return line, n

    temp = line.split()
    node = 'T{}'.format(n)
    if len(temp[0]) > len(node):
        node = '{}\t'.format(node)

    line = line.replace(temp[0], node, 1)
    nodes[temp[0]] = node

    return line, n + 1

def reservoir(line, n):
    if 'ID' in line or 'RESERVOIR' in line:
        return line, n

    temp = line.split()
    node = 'R{}\t '.format(n)
    if len(temp[0]) > len(node):
        node = '{}\t'.format(node)

    line = line.replace(temp[0], node, 1)
    nodes[temp[0]] = node

    return line, n + 1

def pipe(line, n):
    if 'ID' in line or 'PIPES' in line:
        return line, n

    temp = line.split()
    link = 'P{}'.format(n)
    line = line.replace(temp[0], link, 1)
    line = line.replace(temp[1], nodes[temp[1]], 1)
    line = line.replace(temp[2], nodes[temp[2]], 1)

    links[temp[0]] = link
    return line, n + 1

def valve(line, n):
    if 'ID' in line or 'VALVES' in line:
        return line, n

    temp = line.split()
    link = 'V{}'.format(n)
    line = line.replace(temp[0], link, 1)
    line = line.replace(temp[1], nodes[temp[1]], 1)
    line = line.replace(temp[2], nodes[temp[2]], 1)

    links[temp[0]] = link
    return line, n + 1

def pump(line, n):
    if 'ID' in line or 'PUMPS' in line:
        return line, n

    temp = line.split()
    link = 'PU{}'.format(n)
    line = line.replace(temp[0], link, 1)
    line = line.replace(temp[1], nodes[temp[1]], 1)
    line = line.replace(temp[2], nodes[temp[2]], 1)

    links[temp[0]] = link
    return line, n + 1

def control(line, n):
    if 'CONTROL' in line:
        return line, n


    temp = line.split()
    if 'Link' in temp:
        index = temp.index('Link') + 1
        line = line.replace('Link {}'.format(temp[index]), 'Link {}'.format(links[temp[index]]), 1)

    if 'Node' in temp:
        index = temp.index('Node') + 1
        line = line.replace('Node {}'.format(temp[index]), 'Node {}'.format(nodes[temp[index]]), 1)

    return line, n

def coordinates(line, n):
    if 'Node' in line or 'COORDINATES' in line:
        return line, n

    temp = line.split()
    line = line.replace(temp[0], nodes[temp[0]], 1)
    return line, n

def status(line, n):
    if 'ID' in line or 'STATUS' in line:
        return line, n

    temp = line.split()
    line = line.replace(temp[0], links[temp[0]], 1)
    return line, n

def options(line, n):
    if 'Quality' in line:
        temp = line.split()
        line = line.replace(temp[-1], nodes[temp[-1]], 1)
    return line, n


with open(inputfile) as inp:
    content = inp.readlines()

nodes, links = {}, {}
formating, n = none, None
with open("base.inp", "w") as out:
    for line in content:
        if 'JUNCTION' in line: formating, n = junction, 1
        if 'TANK' in line: formating, n = tank, 1
        if 'RESERVOIR' in line: formating, n = reservoir, 1
        if 'PIPE' in line: formating, n = pipe, 1
        if 'VALVES' in line: formating, n = valve, 1
        if 'PUMPS' in line: formating, n = pump, 1
        if 'STATUS' in line: formating = status
        if 'OPTIONS' in line: formating = options
        if 'CONTROL' in line: formating = control
        if 'COORDINATES' in line: formating = coordinates
        if len(line.split()) < 1: formating = none

        output, n = formating(line, n)
        out.write(output)


with open('node_report.csv', 'w') as f:
    for key in nodes.keys():
        f.write("%s,%s\n"%(key,nodes[key]))

with open('link_report.csv', 'w') as f:
    for key in links.keys():
        f.write("%s,%s\n"%(key,links[key]))