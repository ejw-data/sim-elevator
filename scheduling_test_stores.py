import simpy
import random

def user(env, trial, machine, line):
  
    with line.request() as request:
        yield request
    
        m = yield machine.get()
        print(f"Trial {trial:<3} Time {env.now:<5} {m['name']} Starts")
        yield env.timeout(random.randint(1,15))
        print(f"Trial {trial:<3} Time {env.now:<5} {m['name']} Finished")
        yield machine.put(m)
        
        
def setup():
    for i in range(10):
        env.process(user(env, i, machine, production_line))
        yield env.timeout(3)
    # yield line.request()
    # m = yield machine.get()
    # print(env.now, " >> ", m)
    # yield machine.put(m)
    # env.timeout(1)

    # yield line.request()
    # m = yield machine.get()
    # print(env.now, " >> ", m)
    # yield machine.put(m)
    # env.timeout(1)

    # yield line.request()
    # m = yield machine.get()
    # print(env.now, " >> ", m)
    # yield machine.put(m)
    # env.timeout(1)


env = simpy.Environment()
production_line = simpy.Resource(env, 3)
machine = simpy.FilterStore(env, 3)
machine.put({'id': 0, 'name': 'Elevator 1'})
machine.put({'id': 1, 'name': 'Elevator 2'})
machine.put({'id': 2, 'name': 'Elevator 3'})

env.process(setup())
env.run(until=50)