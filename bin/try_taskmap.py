import taskmap
import asyncio
import time


# simulates io waits with asyncio.sleep
async def io_bound_a(): await asyncio.sleep(1); return 'io_a'
async def io_bound_b(x): await asyncio.sleep(1); return x + ' io_b'

# simulates cpu usage with time.sleep
async def cpu_bound_a(x): time.sleep(1); return x + ' cpu_a'
async def cpu_bound_b(): time.sleep(1); return 'cpu_b'

def test_async_parallel_demo():
    # given
    funcs = {
        'io_bound_a': io_bound_a,
        'io_bound_b': io_bound_b,
        'cpu_bound_a': cpu_bound_a,
        'cpu_bound_b': cpu_bound_b,
    }

    dependencies = {
        'io_bound_a': [],
        'io_bound_b': ['cpu_bound_b'],
        'cpu_bound_a': ['io_bound_a'],
        'cpu_bound_b': [],
    }

    io_bound = ['io_bound_a', 'io_bound_b']
    graph = taskmap.create_graph(funcs, dependencies, io_bound=io_bound)

    # when
    graph = taskmap.run_parallel_async(graph, nprocs=2)

    # then
    assert graph.results['io_bound_a'] == 'io_a'
    assert graph.results['io_bound_b'] == 'cpu_b io_b'
    assert graph.results['cpu_bound_a'] == 'io_a cpu_a'
    assert graph.results['cpu_bound_b'] == 'cpu_b'


test_async_parallel_demo()
