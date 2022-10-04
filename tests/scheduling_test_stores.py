# packages needed
import simpy
import random

# function/generator that models the process
def elevator_request(env, trial, machine, line):
    # Request and checkout Resource
    with line.request() as request:
        yield request
    
        # Checkout Store and access stored parameters
        m = yield machine.get()
        print(f"Trial {trial:<3} Time {env.now:<5} {m['name']} Starts")
        
        # Logic for the Resource and associated Store
        yield env.timeout(random.randint(1,15))
        print(f"Trial {trial:<3} Time {env.now:<5} {m['name']} Finished")
        
        # Checkin Store
        yield machine.put(m)
        
# create entities to be introduced to the process        
def setup():
    # create 10 elevator requests separated by 3 time units
    for i in range(10):
        env.process(elevator_request(env, i, machine, production_line))
        yield env.timeout(3)

# create environment
env = simpy.Environment()

# assign number of resources and parameters
production_line = simpy.Resource(env, 3)
machine = simpy.FilterStore(env, 3)
machine.put({'id': 0, 'name': 'Elevator 1'})
machine.put({'id': 1, 'name': 'Elevator 2'})
machine.put({'id': 2, 'name': 'Elevator 3'})

# add initial function to env and chained to other functions
env.process(setup())

# run environment and therefore setup() function
env.run(until=50)