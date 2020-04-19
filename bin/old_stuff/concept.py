from varname import varname

import inspect

#A Task definition is given by the user. The user has to define the blocking operation that need to reach a goal.
#The main idea is that a Task can do only one thing
#For example a Task can only plot
#A Task can only calculate spectra
#A Task performs an integral
#Basically a Task contains a function or procedure that has a definite self contained output
#From input --> output
#A Task can work also without a Manager
class Task():
    def __init__(self, function = None, args = None, extra_args = None):
        self.id = varname()
        self.function = function
        self.args = args
        self.extra_args = extra_args

    def run(self):
        if self.extra_args is not None:
            return self.function(**self.args, **self.extra_args)
        else:
            return self.function(**self.args)

#best practice
#write a module for compatible Tasks

#class Plotter(Task):
#    def main(self, l, cl):

def Add(a, b, text = None) -> float:
    if text is not None:
        print(text)
    return a+b

def Multiply(a, b) -> float:
    return a*b

'''
class Add(Task):
    def __init__(self, a: float = 0., b: float = 0.) -> float:
        super().__init__()
        self.id = varname()
        self.a = a
        self.b = b

    def run(self, **optional):
        for k, v in optional.items():
            setattr(self, k, v)
        somma = self.a+self.b
        return somma

class Multiply(Task):
    def __init__(self, a: float = 0., b: float = 0.) -> float:
        super().__init__()
        self.id = varname()
        self.a = a
        self.b = b

    def run(self, **optional):
        for k, v in optional.items():
            setattr(self, k, v)
        product = self.a*self.b

'''

class Manager():
    def __init__(self):
        self.id = varname()
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

    def analyise_graph(self, graph):
        self.graph = graph
        results = {}

        for k in graph.keys():
            results[k] = {'result': None, 'intermediate': None}

        self.results = results
        return 0

    def execute(self, graph):

        results = self.results

        for key, lista in graph.items():

            intermediate_results = {}
            intermediate = {}

            task = getattr(self, key)
            variable_list = inspect.getfullargspec(task.function)[0]

            i = 0

            for l in lista:
                if results[l]['result'] is None:
                    t = getattr(self, l)
                    ris = t.run()
                else:
                    ris = results[l]['result']
                intermediate_results[variable_list[i]] = ris
                intermediate[l] = intermediate_results[variable_list[i]]
                i += 1

            if lista != []:
                task.args = intermediate_results
                results[key] = {'result': task.run(), 'intermediate': intermediate}

        self.results = results





#each task has its own variables, no shared variables with other tasks

#if you want to share, use Manager

#Manager then run the tasks. You do this:
#[[task1, task2, task3], [task4], [task1], [task10, task11]...]
#Basically all the tasks inside the same list get each other output as input (a apart of first element)
#What if a task requires output of more than one task?
#Have to define a network
#Suppose
'''
1
 ----> 3 ---> 4 ----> 5 ----> 6
2 ----------- ^

'''
#Then maybe I can write an mpi/multiprocess optional feature that allows to do 1 and 2 in parallel

#Basic rule of thumb, everything has to be simple. Network of tasks has to be simple

#How to define the graph/network
'''
graph = {'6': ['5']
         '5': ['4']
         '3': ['1', '2'],
         '4': ['2', '3']}
'''
#Maybe I can define an attribute: was_executed, that tells you if everything finished

#Can I repeat a task?
#Maybe graph can save results for each step

#You define Tasks
#You define Manager
#
###UNIT TEST FEATURE

#save, load from disk


'''

T = Task()

A1 = Task(Add, args = {'a': 4, 'b': 1}, extra_args = {'text': 'Ciao'})
A2 = Task(Add, args = {'a': 1, 'b': 2}, extra_args = {'text': None})

print('Add 1 run', A1.run())
print('Add 2 run', A2.run())
print(A1.id)

M1 = Task(Multiply)
M2 = Task(Multiply)

boss = Manager()
boss += A1
boss += A2
boss += M1
boss += M2

print(boss.tasks)
boss += M2

print(boss.tasks)

graph = {'A1': [],
         'A2': [],
         'M1': ['A1', 'A2'],
         'M2': ['A1', 'M1']}
#         'A1': None,
#         'A2': None}

boss.analyise_graph(graph) #Means M needs A1 and A2 output
boss.execute(graph)
print(boss.results)

'''