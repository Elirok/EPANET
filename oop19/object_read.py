import object
from  epanettools.epanettools import EPANetSimulation
net = object.Network("Trykknett.inp")
file = os.path.join(os.path.dirname(simple.__file__),'Net1.inp') # open an example

skeleton = EPANetSimulation(file)

def node_strip(net, precission=0):
    def collapse(node, node_r):
        net.nodes[node].linked[]




    detected = []
    for node in net.nodes:
        if len(net.nodes[node].neighbours) == 0:
            print(node, 'no connections')

        for i in net.nodes:
            if node is not i and node not in detected:
                if round(net.nodes[node].x, precission) == round(net.nodes[i].x, precission):
                    if round(net.nodes[node].y, precission) == round(net.nodes[i].y, precission):

                        detected.append(i)
                        print(node, net.nodes[node].neighbours)
                        print(i, net.nodes[i].neighbours)
                        print('\n')


node_strip(net)