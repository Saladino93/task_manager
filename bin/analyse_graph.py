from collections import deque, OrderedDict

import matplotlib.pyplot as plt

import numpy as np


def analyse_graph(dictionary, end):
    lista = deque()
    def explore(lista, item):
        small_dict = dictionary[item]
        for key, element in small_dict.items():
            temp = dictionary[element]
            if len(temp)>0:
                temp = {element: temp}
            else:
                temp = element
            lista.appendleft(temp)
            explore(lista, element)
            #lista += [{item: small_dict}]
    explore(lista, end)
    lista += [{end: dictionary[end]}]
    return lista

class Task():
    def __init__(self, name = None, label = None, function = None, args = None, extra_args = None):
        self.id = name
        if label is None:
            self.label = name
        else:
            self.label = label
        self.function = function
        self.args = args
        self.extra_args = extra_args
        self.result = None

    def run(self):
        if self.result is not None:
            return self.result
        if self.extra_args is not None:
            self.result = self.function(**self.args, **self.extra_args)
        else:
            self.result = self.function(**self.args)
        return self.result

    def compare(self, test): #testing function with known result
        return 0


class Manager():
    def __init__(self, name):
        self.id = name
        self.tasks = []
        self.results = {}

    ## or maybe I can add Managers? but then I have to check intersection, etc...
    ## Maybe I can create a merge operator for Managers
    def __add__(self, other):
        id_task = other.id
        self.tasks += [id_task]
        self.tasks = list(set(self.tasks))
        setattr(self, id_task, other)
        return self

    def analyse_graph(self, graph, end, labels = True):
        self.graph = graph
        self.end = end
        result = analyse_graph(graph, end)
        self.graph_analysed = result

        lista = []

        if labels:
            for element in result:
                print(element)
                try:
                    lista += [getattr(self, element).label]
                except:
                    k = list(element.keys())[0]
                    v = list(element.values())[0]
                    temp = {}
                    for variable, names in v.items():
                        print(variable)
                        temp[variable] = getattr(self, names).label
                    lista += [{getattr(self, k).label: temp}]

        return result, lista

    def plot_graph(self, graph):

        total_number = len(graph)

        x0, y0 = 1, 1
        i = 0
        deltax = 20
        deltay = 10

        positions = {}

        fig, ax = plt.subplots()

        for key, value in graph.items():


            if not key in positions.keys():

                positions[key] = {'x': x0+i*deltax, 'y': y0+i*deltay}
                i += 1

                x, y = positions[key]['x'], positions[key]['y']


                ax.scatter(x, y)
                txt = key
                ax.annotate(txt, (x, y))

                try:
                    for k, v in value.items():
                        if not v in positions.keys():
                            positions[v] = {'x': x0+i*deltax*np.random.random(), 'y': y0+i*deltay}
                            x1, y1 = positions[v]['x'], positions[v]['y']
                            txt = k
                            ax.annotate(txt, (x1, y1))
                            deltax = x1-x
                            deltay = y1-y
                            plt.arrow(x, y, deltax, deltay, width = 0.5, head_width = 1.5)
                        i += 1
                except:
                    i += 1


                

        plt.axis('scaled')
        plt.axis('off')
        plt.show()

            
            

    def execute(self, verbose = True):

        execution_order = self.graph_analysed
        
        if verbose:
            print('Execution order:', execution_order)

        for order in execution_order:
            if type(order) is dict:
                input = {}
                for needy_element, values_dictionary in order.items(): #should be just one key
                    for kk, vv in values_dictionary.items():
                        input[kk] = getattr(self, vv).result
                order = needy_element
            task = getattr(self, order)
            if task.args is None:
                task.args = input
            task.run()


def Add(a, b, text = None) -> float:
    if text is not None:
        print(text)
    return a+b

def Identity(a) -> float:
    return a

def Multiply(a, b) -> float:
    return a*b

def Plot(el, cl, name = None, high_res = False, **extra):
    plt.plot(el, cl, **extra)
    if high_res:
        dpi = 300
    else:
        dpi = None
    plt.savefig(name, dpi = dpi)
    plt.close()


el = np.arange(-10, 10, 0.1)
cl = el**2.+5

graph = {'T5': {'a':'T2', 'b': 'T3'},
         'T2': {},
         'T3': {}, 
         'T4': {'a': 'T3', 'b': 'T5'},
         'T1': {'a': 'T2' ,'b': 'T4'}}

order = []

end = 'T1'

M = Manager('M')

T5 = Task('T5', function = Add)
T4 = Task('T4', function = Add)
T3 = Task('T3', function = Identity, args = {'a': 2})
T2 = Task('T2', function = Identity, args = {'a': 1})
T1 = Task('T1', function = Multiply)

M += T5
M += T3
M += T2
M += T4
M += T1

result, lista = M.analyse_graph(graph, end)
print(result, lista)

M.plot_graph(graph)

M.execute()


T1 = Task('T1', function = Plot, extra_args = {'name': 'ciap.png', 'high_res': True, 'marker': 'x'})
T2 = Task('T2', function = Identity, args = {'a': el})
T3 = Task('T3', function = Identity, args = {'a': cl})

graph = {'T1': {'el': 'T2', 'cl': 'T3'},
        'T2': {},
        'T3': {}}

end = 'T1'

M = Manager('M')
M += T1
M += T2
M += T3
M.analyse_graph(graph, end = end)
M.execute()



from pixell import enmap

# Tools for working with enmaps, i/o, catalogs and statistics
from orphics import maps as omaps,io,catalogs as cats,stats,cosmology as cosmo


def create_map(width_deg = 20., px_res_arcmin = 0.5, Ngals = 10000000):
    shape,wcs = omaps.rect_geometry(width_deg = width_deg, px_res_arcmin = px_res_arcmin)
    bounds = enmap.box(shape,wcs)*180./np.pi
    Ngals = Ngals
    ras = np.random.uniform(bounds[0,1], bounds[1,1], Ngals) 
    decs = np.random.uniform(bounds[0,0], bounds[1,0], Ngals)
    cmapper = cats.CatMapper(ras, decs, shape, wcs)
    delta = cmapper.counts/cmapper.counts.mean()-1.
    modlmap = cmapper.counts.modlmap()
    
    #result = {'shape': shape, 'wcs': wcs, 'delta': delta} #PIPE
    result = OrderedDict([('shape', shape), ('wcs', wcs), ('delta', delta), ('modlmap', modlmap)])

    return result

def fts(result, lmin, lmax, deltal):
    shape,wcs, delta, modlmap = list(result.values())
    fc = omaps.FourierCalc(shape,wcs)
    p2d,kgal,_ = fc.power2d(delta)
    bin_edges = np.arange(lmin, lmax, deltal)
    binner = stats.bin2D(modlmap,bin_edges)
    cents, p1d = binner.bin(p2d)
    result = OrderedDict([('cents', cents), ('p1d', p1d)])
    return result

def Plot_spectrum(result, name = None, high_res = False, **extra):
    el, cl = list(result.values())
    plt.plot(el, cl, **extra)
    if high_res:
        dpi = 300
    else:
        dpi = None
    plt.savefig(name, dpi = dpi)
    plt.close()
    return result

def Save_spectrum(result, name = None):
    el, cl = list(result.values())
    np.savetxt(name, np.c_[el, cl])

    
T1 = Task('T1', label = 'Plot', function = Plot_spectrum, extra_args = {'name': 'spectrum.png', 'high_res': True, 'marker': 'x'})
T2 = Task('T2', label = 'Create Map', function = create_map, args = {'width_deg': 20., 'px_res_arcmin': 0.5, 'Ngals': 10000000})
T3 = Task('T3', label = 'Get spectrum', function = fts, extra_args = {'lmin': 100, 'lmax': 3000, 'deltal': 100})
T4 = Task('T4', label = 'Save spectrum', function = Save_spectrum, extra_args = {'name': 'spectrum.txt'})

graph = {'T1': {'result': 'T3'},
        'T2': {},
        'T3': {'result': 'T2'}, 
        'T4': {'result': 'T1'}}

end = 'T4'

M = Manager('M')
M += T1
M += T2
M += T3
M += T4

graph, labeled_graph = M.analyse_graph(graph, end = end)

print(labeled_graph)

M.execute()