from collections import deque

import matplotlib.pyplot as plt




def analyse_graph(dictionary, end):
    '''
    Analyse a graph. This function recursively go over the elements of a graph to define the order of run.

    Parameters
    ----------
    dictionary: dict
        The graph.
    end: str
        The end of the graph, or the last node to be explored.

    Returns
    -------
        A list with the order of flow of the graph.

    '''
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
    '''
    A Task is the basic unit that defines the execution of a specific step.
    '''
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
    '''
    A Manager takes Tasks and execute them in the order defined by a graph.
    '''
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
