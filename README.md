# Task Manager

I found myself doing too many stupid errors writing code. And the main reason is that I usually do not want to spend time checking long code. I know, this is called laziness. To help me tackle this problem, I wrote this small tool to manage the flow of a program.

Task Manager is an easy library that helps you chunk your code in small pieces and debug things and see how things are interconnected.

The basic unit is a Task. The idea is that a Task does just only one thing and one thing only. You're allowed to make a Task do as many operations as you want, but really, make it do only one main thing.

To create a Task, define your function

```python

import taskmanager as tm

def Identity(a) -> float:
    return a

def Add(a, b, text = None) -> float:
    if text is not None:
        print(text)
    return a+b


T1 = tm.Task('T1', label = 'Input 1', function = Identity, args = {'a': 2})

```

Then you define a Manager. A Manager basically takes your Tasks and execute them in a predefined order dictaded by a graph.

```python

T2 = tm.Task('T2', label = 'Input 2', function = Identity, args = {'a': 53})

T3 = tm. Task('T3', label = 'Adding), function = Add)

M = tm.Manager(name = 'MakeAdd')

M += T1
M += T2
M += T3

graph = {'T3': {'a': 'T1', 'b': 'T2'},   #for the graph you have to define the inputs. Here we have to edges.
          'T2': {},
          'T3': {}}

end = 'T3' #the end of the graph, as this is a graph with a flow

#Terminal visualisation of the order
#result is the analysed graph
#lista is the analysed graph with labels
result, lista = M.analyse_graph(graph, end)

#You can even plot your graph
M.plot_graph(graph)

#Executes
M.execute()

#Results are store in
print(M.T3.result)
```