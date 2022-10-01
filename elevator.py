import random
import simpy


RANDOM_SEED = 42
NUMBER_ELEVATORS = 1
NORMAL_SPEED_ELEVATOR = 3
STOP_SPEED_ELEVATOR = 5

# WASHTIME = 5      # Minutes it takes to clean a car
REQUEST_INTERVAL = 7       # Create a car every ~7 minutes
SIM_TIME = 120     # Simulation time in minutes

# current_floor tracking doesn't work for multi-elevator system
current_floor = 1
total_trips = 0

class Elevator(object):

    def __init__(self, env, num_elevators, normal_speed, stop_speed, current_elevator_floor):
        self.env = env
        self.elevator = simpy.Resource(env, num_elevators)
        self.normal_speed = normal_speed
        self.stop_speed = stop_speed
        self.current_floor = current_elevator_floor

    def call(self, name, floor):
        global current_floor 
        global total_trips

        if current_floor > floor:
            elevator_path = range(current_floor, floor, -1)
            slow_floor = floor + 1
            direction = -1
        else:
            elevator_path = range(current_floor, floor)
            slow_floor = floor - 1
            direction = 1

        for elevator_floor in elevator_path:
            if elevator_floor != slow_floor:
                yield self.env.timeout(self.normal_speed)
                print(f"{name}:  Located at Floor {elevator_floor+direction} at {env.now:.2f}")
                current_floor = elevator_floor + direction
            else:
                yield self.env.timeout(self.stop_speed)
                print(f"{name}:  Doors open on Floor {floor} at {env.now:.2f}")
                current_floor = elevator_floor + direction
                

        yield self.env.timeout(2)
        print(f'{name}: Doors close at {env.now:.2f}')

        #  select new floor destination
        #  initially make it go to floor one
        first_floor = 1
        for elevator_floor in range(current_floor-1, 0,-1):
            if elevator_floor != first_floor:
                yield self.env.timeout(self.normal_speed)
                print(f"{name}:  Located at Floor {elevator_floor} at {env.now:.2f}")
                current_floor = elevator_floor -1 
            else:
                yield self.env.timeout(self.stop_speed)
                print(f"{name}:  Doors open on Floor 1 at {env.now:.2f}")
                total_trips += 1

def user(env, name, elevator_instance, call_floor):
    print(f'{name} occurs at {env.now:.2f}.')
    with elevator_instance.elevator.request() as request:
        yield request   
        print(f'{name}:  Elevator begins to move from Floor {current_floor} to Floor {call_floor} at {env.now:.2f}.')
        yield env.process(elevator_instance.call(name, call_floor))


def setup(env, num_elevators, normal_speed, stop_speed, current_elevator_floor):

    building_elevator = Elevator(env, num_elevators, normal_speed, stop_speed, current_elevator_floor)

    # # Create test cases
    # env.process(user(env, 'Button Press 1', building_elevator, 12))
    # yield env.timeout(20)
    # env.process(user(env, 'Button Press 2', building_elevator, 6))
    
    # Create 4 initial calls
    for i in range(4):
        env.process(user(env, f'Button Press {i+1}', building_elevator, random.randint(2,19)))
        yield env.timeout(1)


    # Create more button presses while the simulation is running
    while True:
        yield env.timeout(random.randint(2,12))
        i += 1
        env.process(user(env, f'Button Press {i}', building_elevator, random.randint(1,19)))


# Setup and start the simulation
print('Elevator')

random.seed(RANDOM_SEED)  # This helps reproducing the results

# Create an environment and start the setup process
env = simpy.Environment()
env.process(setup(env, NUMBER_ELEVATORS, NORMAL_SPEED_ELEVATOR, STOP_SPEED_ELEVATOR, current_floor))

# Execute!
env.run(until=SIM_TIME)
print(f"Elevator is on Floor {current_floor}")
print(f"Total Completed Trips:  {total_trips}")