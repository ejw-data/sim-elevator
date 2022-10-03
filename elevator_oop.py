# Converstion of simpy model to Object Oriented
# - aids in structuring the code

import random
import simpy

class ModelConstants:
    random_seed = 42
    number_elevators = 1
    normal_speed_elevator = 3
    stop_speed_elevator = 5
    sim_duration = 120

# current_floor tracking doesn't work for multi-elevator system
# Global Variables
current_floor = 1
total_trips = 0

class User:
    def __init__(self, user_id, initial_floor, destination):
        self.id = user_id
        self.name = f'Button Press {user_id}'
        self.initial_floor = initial_floor
        self.destination = destination

class ElevatorBank:

    def __init__(self):
        self.env = simpy.Environment()
        self.elevator = simpy.Resource(self.env, ModelConstants.number_elevators)
        # self.elevator_info = simpy.FilterStore(self.env, ModelConstants.number_elevators)
        self.user_counter = 0
        self.registered_elevators = 0
        self.elevator_name = []
        self.elevator_location = {}
        # self.current_floor = 1 # need to change


    def add_elevator(self):
        self.registered_elevators += 1
        elevator_name = f"Elevator_{self.registered_elevators}"
        self.elevator_name.append(elevator_name)
        self.elevator_location[elevator_name] = 1
        # self.elevator_info.put({'id':elevator_name, 'floor':1})

    def remove_elevator(self):
        pass
        # future code for taking existing elevator out of service

    def generate_user(self):
        initial_floor = 1
        destination = random.randint(2,19)

        # while True:
        self.user_counter += 1
        new_user = User(self.user_counter, initial_floor, destination)
        yield self.env.process(self.user_request(new_user))

    def user_request(self, user):
        print(f'{user.name} occurs at {self.env.now:.2f}.')
        with self.elevator.request() as request:
            yield request 

            print(f'{user.name}:  Elevator begins to move from Floor {user.initial_floor} to Floor {user.destination} at {self.env.now:.2f}.')
            yield self.env.process(self.call(user.name, user.destination))

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
                yield self.env.timeout(ModelConstants.normal_speed_elevator)
                print(f"{name}:  Located at Floor {elevator_floor+direction} at {self.env.now:.2f}")
                current_floor = elevator_floor + direction
            else:
                yield self.env.timeout(ModelConstants.stop_speed_elevator)
                print(f"{name}:  Doors open on Floor {floor} at {self.env.now:.2f}")
                current_floor = elevator_floor + direction
                

        yield self.env.timeout(2)
        print(f'{name}: Doors close at {self.env.now:.2f}')

        #  select new floor destination
        #  initially make it go to floor one
        first_floor = 1
        for elevator_floor in range(current_floor-1, 0,-1):
            if elevator_floor != first_floor:
                yield self.env.timeout(ModelConstants.normal_speed_elevator)
                print(f"{name}:  Located at Floor {elevator_floor} at {self.env.now:.2f}")
                current_floor = elevator_floor -1 
            else:
                yield self.env.timeout(ModelConstants.stop_speed_elevator)
                print(f"{name}:  Doors open on Floor 1 at {self.env.now:.2f}")
                total_trips += 1

        yield self.env.timeout(2)
        print(f'{name}: Doors close at {self.env.now:.2f}')

    def setup(self):
        # create elevator lists
        for _ in range(ModelConstants.number_elevators):
            self.add_elevator()

        # Create 4 initial calls
        for _ in range(4):
            yield self.env.timeout(1)
            self.env.process(self.generate_user())
            
        # Create more button presses while the simulation is running
        while True:
            yield self.env.timeout(random.randint(2,12))
            self.env.process(self.generate_user())

    def run(self):
        print("Starting Model")
        random.seed(ModelConstants.random_seed)  
        self.env.process(self.setup())
        self.env.run(until=ModelConstants.sim_duration)
        print(f"Elevator is on Floor {current_floor}")
        print(f"Total Completed Trips:  {total_trips}")

# Run model
my_model = ElevatorBank()
my_model.run()

print(my_model.elevator_location)