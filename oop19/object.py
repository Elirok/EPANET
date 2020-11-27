import pandas as pd
import nodes
import numpy as np
from time import gmtime, strftime

def system_bounderies(content):
    blacklist = [' ', ' '*6]
    content = content.strip('\n')
    content = content.split()

    data = []
    for element in content:
        if element.strip() in blacklist:
            data.append(None)
        else:
            data.append(element.strip())

    return data

def get_title(name, time):
    name = name.strip('\n')
    name = name.split()
    time = time.strip('\n')
    time = time.split()

    if len(name) < 1 or len(time)<1:
        return None, None

    if name[0] == 'Name:':
        name_str = ''
        for n in name[1:]:
            name_str += '{} '.format(n)
    else:
        name_str = None

    if time[0] == 'Modified:':
        time_str = ''
        for n in time[1:]:
            time_str += '{} '.format(n)
    else:
        time_str = None

    return name_str, time_str

def time():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())

class Network:

    def __init__(self, inputfile=None):
        self.inputfile = inputfile

        self.nodes = {}
        self.junctions = []
        self.reservoirs = []
        self.tanks = []
        self.links = {}

        self.pattern = {}
        self.curves = {}
        self.energy = {}
        self.reactions = {}
        self.times = {}
        self.report = {}
        self.options = {}
        self.backdrop = {}
        self.labels = []
        self.controls = []

        with open(inputfile, "r") as f:  # EPA
            content = f.readlines()

            n = content.index('[TITLE]\n')
            self.name, self.generated = get_title(content[n+1], content[n+2])

            n = content.index('[JUNCTIONS]\n') + 2
            while len(content[n]) > 1:
                data = system_bounderies(content[n])
                if len(data) < 5:
                    self.nodes[data[0]] = Junctions(data[1], 0)
                    self.junctions.append(data[0])
                else:
                    self.nodes[data[0]] = Junctions(data[1], data[2], data[3], data[4])
                    self.junctions.append(data[0])
                n += 1

            if '[RESERVOIRS]\n' in content:
                n = content.index('[RESERVOIRS]\n') + 2
                while len(content[n]) > 1:
                    data = system_bounderies(content[n])
                    if len(data) < 4:
                        self.nodes[data[0]] = Reservoirs(data[1])
                        self.reservoirs.append(data[0])
                    else:
                        self.nodes[data[0]] = Reservoirs(data[1], data[2], data[3])
                        self.reservoirs.append(data[0])
                    n += 1

            if '[TANKS]\n' in content:
                n = content.index('[TANKS]\n') + 2
                while len(content[n]) > 1:
                    data = system_bounderies(content[n])
                    if len(data) < 9:
                        self.nodes[data[0]] = Tanks(data[1], data[2], data[3], data[4], data[5], data[6], comment=data[7])
                        self.tanks.append(data[0])
                    else:
                        self.tanks.append(data[0])
                        self.nodes[data[0]] = Tanks(data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8])
                    n += 1

            n = content.index('[COORDINATES]\n') + 2
            while len(content[n]) > 1:
                data = system_bounderies(content[n])
                self.nodes[data[0]].coordinates(data[1], data[2])
                n += 1

            n = content.index('[PIPES]\n') + 2
            while len(content[n]) > 1:
                data = system_bounderies(content[n])
                self.links[data[0]] = Pipes(data[1], data[2], data[3], data[4], data[5], data[6], data[7])
                self.neigbouring(data)
                n += 1

            self.valves = {}
            if '[VALVES]\n' in content:
                n = content.index('[VALVES]\n') + 2
                while len(content[n]) > 1:
                    data = system_bounderies(content[n])
                    self.links[data[0]] = Valves(data[1], data[2], data[3], data[4], data[5], data[6], data[7])
                    self.neigbouring(data)
                    n += 1

            if '[PUMPS]\n' in content:
                n = content.index('[PUMPS]\n') + 2
                while len(content[n]) > 1:
                    data = system_bounderies(content[n])
                    self.links[data[0]] = Pumps(data[1], data[2], data[3], data[4])
                    self.neigbouring(data)
                    n += 1

            n = content.index('[VERTICES]\n') + 2
            while len(content[n]) > 1 and n >= len(content):
                data = system_bounderies(content[n])

                self.links[data[0]].vertices(data[1], data[2])
                n += 1

            if '[QUALITY]\n' in content:
                n = content.index('[QUALITY]\n') + 2
                while len(content[n]) > 1:
                    data = system_bounderies(content[n])

                    if data[0] in self.nodes.keys():
                        self.nodes[data[0]].set_quality(data[1])
                    n +=1

            if '[TAGS]\n' in content:
                n = content.index('[TAGS]\n') + 1
                while len(content[n]) > 1:
                    data = system_bounderies(content[n])
                    if data[0] == 'LINK':
                        self.links[data[1]].set_tag(data[2:])

                    elif data[0] == 'NODE':
                        self.nodes[data[1]].set_tag(data[2:])

                    n += 1

            if '[PATTERNS]\n' in content:
                n = content.index('[PATTERNS]\n') + 2
                while len(content[n]) > 1:
                    data = system_bounderies(content[n])
                    if data[0][0] == ';':
                        name = data[0][1:]
                        self.pattern[name] = []
                    else:
                        for value in data:
                            self.pattern[name].append(float(value))
                    n += 1

            if '[CURVES]\n' in content:
                n = content.index('[CURVES]\n') + 2
                while len(content[n]) > 1:
                    data = system_bounderies(content[n])
                    if data[0][0] == ';':
                        name = data[0][1:]
                        self.curves[name] = []
                    else:
                        self.curves[name].append(data)

                    n += 1

            if '[CONTROLS]\n' in content:
                n = content.index('[CONTROLS]\n') + 1
                while len(content[n]) > 1:
                    data = content[n].strip('\n')
                    self.controls.append(data)
                    n += 1

            if '[ENERGY]\n' in content:
                n = content.index('[ENERGY]\n') + 1
                while len(content[n]) > 1:
                    data = system_bounderies(content[n])
                    self.energy[data[0]] = data[1]

                    n += 1

            if '[REACTIONS]\n' in content:
                n = 0
                reaction_index = []
                for element in content:
                    if element == '[REACTIONS]\n':
                        reaction_index.append(n)
                        if len(reaction_index) == 2:
                            break
                    n += 1
                if len(reaction_index) > 1:
                    n += 1
                    while len(content[n]) > 1:
                        data = system_bounderies(content[n])
                        self.reactions[data[0]] = data[1]

                        n += 1

            if '[TIMES]\n' in content:
                n = content.index('[TIMES]\n') + 1
                while len(content[n]) > 1:
                    data = system_bounderies(content[n])
                    self.times[data[0]] = data[1]

                    n += 1

            if '[REPORT]\n' in content:
                n = content.index('[REPORT]\n') + 1
                while len(content[n]) > 1:
                    data = system_bounderies(content[n])
                    self.report[data[0]] = data[1]

                    n += 1

            if '[OPTIONS]\n' in content:
                n = content.index('[OPTIONS]\n') + 1
                while len(content[n]) > 1:
                    data = system_bounderies(content[n])
                    self.options[data[0]] = data[1]

                    n += 1

            if '[LABELS]\n' in content:
                n = content.index('[LABELS]\n') + 2
                while len(content[n]) > 1:
                    data = content[n].strip('\n')
                    data = data.split()
                    self.labels.append(data)

                    n += 1

            if '[BACKDROP]\n' in content:
                n = content.index('[BACKDROP]\n') + 1
                while len(content[n]) > 1:
                    data = system_bounderies(content[n])
                    self.backdrop[data[0]] = data[1:]

                    n += 1

    def neigbouring(self, data):
        self.nodes[data[1]].load_neighours(data[2])
        self.nodes[data[1]].linked_to(data[0])

        self.nodes[data[2]].linked_to(data[0])
        self.nodes[data[2]].load_neighours(data[1])

    def frame_data(self):
        """ Frame nodes """
        self.Nodedata = []
        for id in self.nodes.keys():
            product = self.nodes[id]
            self.Nodedata.append([id, product.type, product.elev, product.x, product.y, product.demand, product.comment])

        self.Nodedata = pd.DataFrame(self.Nodedata, columns=['id', 'type', 'elev', 'x', 'y', 'demand', 'comment'])
        self.Nodedata = self.Nodedata.set_index('id')

    def write_file(self, outputfile = 'Generated_net.inp'):
        dictionary = {}
        spacing = "%-16s"

        with open(outputfile, "w") as f:
            tags = []
            quality = []

            f.write('[TITLE]\n')
            f.write('{}\n'.format(self.name))
            f.write('Modified:\t{}\n'.format(time()))
            f.write('From:\t\t{}\n\n'.format((self.inputfile)))

            f.write('[JUNCTIONS]\n')
            boundery = [[";ID", "Elev", "Demand", "Pattern", ""]]
            for i in self.junction.keys():
                product = self.junction[i]
                boundery.append([' {}'.format(i), product.elev, product.demand, product.pattern, product.comment])

                if product.tag != None:
                    tag = ''
                    for name in product.tag:
                        tag += '{} '.format(name)
                    tags.append([' NODE', i, tag])

                if product.initqual != None:
                    quality.append([' {}'.format(i), product.initqual])

            np.savetxt(f, np.array(boundery), fmt=spacing)
            f.write('\n')

            f.write('[RESERVOIRS]\n')
            boundery = [[";ID", "Head", "Pattern", ""]]
            for i in self.reservoirs.keys():
                product = self.reservoirs[i]
                boundery.append([' {}'.format(i), product.elev, product.pattern, product.comment])
                if product.tag != None:
                    tag = ''
                    for name in product.tag:
                        tag += '{} '.format(name)
                    tags.append([' NODE', i, tag])

                if product.initqual != None:
                    quality.append([' {}'.format(i), product.initqual])

            np.savetxt(f, np.array(boundery), fmt=spacing)
            f.write('\n')

            f.write('[TANKS]\n')
            boundery = [[";ID", "Elev", "Initlevel", "MinLevel", "MaxLevel", 'Diameter', 'MinVol', 'VolCurve', '']]
            for i in self.tanks.keys():
                product = self.tanks[i]
                boundery.append([' {}'.format(i), product.elev, product.initlevel, product.minlevel, product.maxlevel, product.diameter, product.minvol, product.volcurve, product.comment])
                if product.tag != None:
                    tag = ''
                    for name in product.tag:
                        tag += '{} '.format(name)
                    tags.append([' NODE', i, tag])

                if product.initqual != None:
                    quality.append([' {}'.format(i), product.initqual])

            np.savetxt(f, np.array(boundery), fmt=spacing)
            f.write('\n')

            f.write('[PIPES]\n')
            boundery = [[";ID", "Node1", "Node2", "Length", "Diameter", 'Roughness', 'MinorLoss', '']]
            for i in self.pipes.keys():
                product = self.pipes[i]
                boundery.append([' {}'.format(i), product.connection[0], product.connection[1], product.length, product.diameter, product.roughness, product.minorloss, product.comment])
                if product.tag != None:
                    tag = ''
                    for name in product.tag:
                        tag += '{} '.format(name)
                    tags.append([' LINK', i, tag])

            np.savetxt(f, np.array(boundery), fmt=spacing)
            f.write('\n')

            f.write('[PUMPS]\n')
            boundery = [[";ID", "Node1", "Node2", 'Parameter', '']]
            for i in self.pumps.keys():
                product = self.pumps[i]
                boundery.append([' {}'.format(i), product.connection[0], product.connection[1], product.parameter, product.comment])
                if product.tag != None:
                    tag = ''
                    for name in product.tag:
                        tag += '{} '.format(name)
                    tags.append([' LINK', i, tag])
            np.savetxt(f, np.array(boundery), fmt=spacing)
            f.write('\n')

            f.write('[VALVES]\n')
            boundery = [[";ID", "Node1", "Node2", "Diameter", 'Type', 'Setting', 'MinorLoss', '']]
            for i in self.valves.keys():
                product = self.valves[i]
                boundery.append([' {}'.format(i), product.connection[0], product.connection[1], product.diameter, product.type, product.setting, product.minorloss, product.comment])
            if product.tag != None:
                tag = ''
                for name in product.tag:
                    tag += '{} '.format(name)
                tags.append([' LINK', i, tag])
            np.savetxt(f, np.array(boundery), fmt=spacing)
            f.write('\n')

            f.write('[TAGS]\n')
            np.savetxt(f, np.array(tags), fmt=spacing)
            f.write('\n')

            f.write('[DEMANDS]\n')
            np.savetxt(f, np.array([[';Junction', 'Demand', 'Pattern', 'Category']]), fmt="%-16s")
            f.write('\n')

            f.write('[PATTERNS]\n')
            boundery = [[';ID', 'Multipliers', '', '', '', '']]
            for key in self.pattern:
                boundery.append([';{}'.format(key), '', '', '', '', ''])
                temp = []
                for value in self.pattern[key]:
                    if len(temp) == 0:
                        temp.append(' {}'.format(value))
                    else:
                        temp.append(value)

                    if len(temp) == 6:
                        boundery.append(temp)
                        temp = []
            np.savetxt(f, np.array(boundery), fmt=spacing)
            f.write('\n')

            f.write('[CURVES]\n')
            boundery = [[';ID', 'X-Value', 'Y-Value']]
            for key in self.curves:
                boundery.append([';{}'.format(key), '', ''])
                for values in self.curves[key]:
                    values[0] = ' {}'.format(values[0])
                    boundery.append(values)
            np.savetxt(f, np.array(boundery), fmt=spacing)
            f.write('\n')

            f.write('[CONTROLS]\n')
            for control in self.controls:
                f.write('{}\n'.format(control))
            f.write('\n')

            f.write('[RULES]\n')
            # TODO: write rules
            f.write('\n')

            f.write('[ENERGY]\n')
            boundery = []
            for marked in self.energy:
                boundery.append([' {}'.format(marked), self.energy[marked]])
            np.savetxt(f, np.array(boundery), fmt="%-33s")
            f.write('\n')

            f.write('[EMITTERS]\n')
            boundery = [[';Junction', 'Coefficient']]
            # TODO: write emitters
            np.savetxt(f, np.array(boundery), fmt=spacing)
            f.write('\n')

            f.write('[QUALITY]\n')
            boundery = [[';Node', 'InitQual']]
            for values in quality:
                boundery.append([values[0], values[1]])
            np.savetxt(f, np.array(boundery), fmt=spacing)
            f.write('\n')

            f.write('[SOURCES]\n')
            boundery = [[';Node', 'Type', 'Quality', 'Pattern']]
            # TODO: research/write sources
            np.savetxt(f, np.array(boundery), fmt=spacing)
            f.write('\n')

            f.write('[REACTIONS]\n')
            boundery = [[';Type', 'Pipe/Tank', 'Coefficient']]
            # TODO: research/write reactions
            np.savetxt(f, np.array(boundery), fmt=spacing)
            f.write('\n')

            f.write('[REACTIONS]\n')
            boundery = []
            for marked in self.reactions:
                boundery.append([' {}'.format(marked), self.reactions[marked]])
            np.savetxt(f, np.array(boundery), fmt="%-33s")
            f.write('\n')

            f.write('[MIXING]\n')
            boundery = [[';Tank', 'Model']]
            # TODO: mixing theory
            np.savetxt(f, np.array(boundery), fmt=spacing)
            f.write('\n')

            f.write('[TIMES]\n')
            boundery = []
            for marked in self.times:
                boundery.append([' {}'.format(marked), self.times[marked]])
            np.savetxt(f, np.array(boundery), fmt="%-33s")
            f.write('\n')

            f.write('[REPORT]\n')
            boundery = []
            for marked in self.report:
                boundery.append([' {}'.format(marked), self.report[marked]])
            np.savetxt(f, np.array(boundery), fmt="%-33s")
            f.write('\n')

            f.write('[OPTIONS]\n')
            boundery = []
            for marked in self.options:
                boundery.append([' {}'.format(marked), self.options[marked]])
            np.savetxt(f, np.array(boundery), fmt="%-33s")
            f.write('\n')

            f.write('[COORDINATES]\n')
            boundery = [[";Node", "X-Coord", 'Y-Coord']]
            for i in self.junction.keys():
                product = self.junction[i]
                boundery.append([' {}'.format(i), product.x, product.y])
            for i in self.reservoirs.keys():
                product = self.reservoirs[i]
                boundery.append([' {}'.format(i), product.x, product.y])
            for i in self.tanks.keys():
                product = self.tanks[i]
                boundery.append([' {}'.format(i), product.x, product.y])
            np.savetxt(f, np.array(boundery), fmt=spacing)
            f.write('\n')

            f.write('[VERTICES]\n')
            boundery = [[";Link", "X-Coord", 'Y-Coord']]
            for i in self.pipes.keys():
                product = self.pipes[i]
                for pair in product.vertice:
                    boundery.append([' {}'.format(i), pair[0], pair[1]])
            for i in self.pumps.keys():
                product = self.pumps[i]
                for pair in product.vertice:
                    boundery.append([' {}'.format(i), pair[0], pair[1]])
            for i in self.valves.keys():
                product = self.valves[i]
                for pair in product.vertice:
                    boundery.append([' {}'.format(i), pair[0], pair[1]])
            np.savetxt(f, np.array(boundery), fmt=spacing)
            f.write('\n')

            f.write('[LABELS]\n')
            boundery = [[";X-Coord", 'Y-Coord', 'Label & Anchor Node']]
            for element in self.labels:
                boundery.append([' {}'.format(element[0]), element[1], element[2]])
            np.savetxt(f, np.array(boundery), fmt=spacing)
            f.write('\n')

            f.write('[BACKDROP]\n')
            for element in self.backdrop:
                temp = [' {}'.format(element)]
                for value in self.backdrop[element]:
                    temp.append(value)
                np.savetxt(f, np.array([temp]), fmt=spacing)
            f.write('\n')

            f.write('[END]')


class Node:

    def __init__(self, elev, comment=';'):
        self.elev = float(elev)
        self.comment = comment
        self.neighbours = []
        self.linked = []
        self.tag = None
        self.initqual = None

    def coordinates(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def set_quality(self, initQual=1):
        self.initqual = initQual

    def set_tag(self, tag):
        self.tag = tag

    def load_neighours(self, node):
        self.neighbours.append(node)

    def linked_to(self, link):
        self.linked.append(link)


class Junctions(Node):

    def __init__(self, elev, demand, pattern=None, comment=None):
        Node.__init__(self, elev, comment)
        self.type = 'junction'
        self.demand = float(demand)
        self.pattern = pattern


class Reservoirs(Node):

    def __init__(self, elev, pattern=None, comment=None):
        Node.__init__(self, elev, comment)
        self.pattern = pattern
        self.type = 'reservoir'


class Tanks(Node):

    def __init__(self, elev, initlevel, minlevel, maxlevel, diameter, minvol, volcurve=None, comment=None):
        Node.__init__(self, elev, comment)
        self.type = 'tank'
        self.initlevel = float(initlevel)
        self.minlevel = float(minlevel)
        self.maxlevel = float(maxlevel)
        self.diameter = float(diameter)
        self.minvol = float(minvol)
        self.volcurve = volcurve


class Link:

    def __init__(self, node1, node2, comment=';'):
        self.connection = [node1, node2]
        self.comment = comment
        self.vertice = []
        self.tag = None

    def vertices(self, x, y):
        self.vertice.append([float(x), float(y)])

    def set_tag(self, tag):
        self.tag = tag


class Pipes(Link):

    def __init__(self, node1, node2, length, diameter, roughness, minorloss, status, comment=';'):
        Link.__init__(self, node1, node2, comment)
        self.type = 'pipe'
        self.length = length
        self.diameter = diameter
        self.roughness = roughness
        self.minorloss = minorloss
        self.status = status


class Valves(Link):

    def __init__(self, node1, node2, diameter, type, setting, minorloss, comment=';'):
        Link.__init__(self, node1, node2, comment)
        self.type = 'valve'
        self.diameter = diameter
        self.type = type
        self.setting = setting
        self.minorloss = minorloss



class Pumps(Link):

    def __init__(self, node1, node2, parameter, comment):
        Link.__init__(self, node1, node2, comment)
        self.type = 'pump'
        self.parameter = parameter







