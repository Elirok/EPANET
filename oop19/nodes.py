information = {'TAGS': None, 'DEMAND': None, 'STATUS': None,
                    'PATTERNS': None, 'CURVES': None, 'CONTROLS': None,
                    'RULES': None, 'EMITTERS': None, 'QUALITY': None,
                    'SOURCES': None, 'REACTIONS': None, 'MIXING': None,
                    'TIMES': None, 'REPORT': None, 'OPTIONS': None,
                    'LABELS': None, 'BACKDROP': None}

class Node:

    def __init__(self, elev, comment):
        self.elev = float(elev)
        self.comment = comment
        self.neighbours = []
        self.linked = []

    def coordinates(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def load_neighours(self, node):
        self.neighbours.append(node)

    def linked_to(self, link):
        self.linked.append(link)


class Junction(Node):

    def __init__(self, elev, demand, pattern=None, comment=None):
        Node.__init__(self, elev, comment)
        self.demand = float(demand)
        self.pattern = pattern


class Reservoirs(Node):

    def __init__(self, elev, pattern=None, comment=None):
        Node.__init__(self, elev, comment)
        self.pattern = pattern


class Tanks(Node):

    def __init__(self, elev, initlevel, minlevel, maxlevel, diameter, minvol, volcurve=None, comment=None):
        Node.__init__(self, elev, comment)
        self.initlevel = float(initlevel)
        self.minlevel = float(minlevel)
        self.maxlevel = float(maxlevel)
        self.diameter = float(diameter)
        self.minvol = float(minvol)
        self.volcurve = volcurve


