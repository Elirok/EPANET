import pandas as pd

def reader(path):
    network = {'JUNCTIONS': ['ID', 'Elev', 'Demand', 'Pattern', 'Comment'],
               'RESERVOIRS': ['ID', 'Head', 'Pattern', 'Comment'],
               'TANKS': ['ID', 'Elevation', 'InitLevel', 'MinLevel', 'MaxLevel', 'Diameter', 'MinVol', 'VolCurve', 'Comment'],
               'PIPES': ['ID', 'Node1', 'Node2', 'Length', 'Diameter', 'Roughness', 'MinorLoss', 'Status', 'Comments'],
               'PUMPS': ['ID', 'Node1', 'Node2', 'Parameters', 'Comments'],
               'VALVES': ['ID', 'Node1', 'Node2', 'Diameter', 'Type', 'Setting', 'MinorLoss', 'Comments']}

    def matrix(content, n, columns):
        if len(content[n]) <= 1:
            return None

        data = []
        while len(content[n]) > 1:
            list = content[n].strip('\n')
            list = list.split('\t')
            temp = []
            for element in list:
                if element == ';':
                    temp.append(None)
                elif element == ' '*16:
                    temp.append(None)
                else:
                    temp.append(element.strip())

            data.append(temp)
            n += 1

        data = pd.DataFrame(data, columns=columns)
        data = data.set_index('ID')
        return data

    with open(path, "r") as f:  # EPA
        content = f.readlines()
        for frame in network.copy():
            try:
                n = content.index('[{}]\n'.format(frame)) + 2
                network[frame] = matrix(content, n, network[frame])
            except:
                print('Error: reading {} in {}'.format(frame, path))

    return network

network = reader('Net1.inp')

for n in network:
    print(n)
    print(network[n])
    print('')

