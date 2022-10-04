# sim-elevator
pySim of an elevator system


## Notes:
<hr>

### Phase 1
- Developed procedural model using functions/generators with simpy
- Works with only one elevator correctly
- Model is getting complex due to chaining functions and passing function parameters

### Phase 2
- Converted procedural model to object oriented
- Reduced code complexity
- Works only with one elevator correctly

### Phase 3
- Updating model to work with multiple elevators
- Initial thought was to create dictionary holding elevator information and floors but does not look promising
- Looking at other options.

### Phase 4  
- Found several options from documentation and stackoverflow.  
- Initially tried using simpy.Store but having issues integrating into existing code and determining effect.
- Creating simple model to test functionality and then will integrate into existing OOP version.
- New file called `scheduling_test_store.py`.  
- After several tries, using `simpy.FilteredStore` method works but only when combined with `simpy.Resources`.  My method uses the Resources method to allocate resources upon request and upon making a request the FilteredStore method allocates a name and other properties to the model.  The big picture idea is that I am doing two checkout steps - checking out an elevator resource and at the same time checking out an available elevator data store.  Before the request is checked in, I checkin the store so the two checkout systems are synchronized.  I can use this method to pass specific parameters related to that elevator or update those parameters and I can customize which elevator is selected at the store level (in many scenarios); thus, allowing custom logic for elevator activity.  

### Phase 5 (current)

- Integrated `scheduling_test_store.py` verified method into main script - `elevator_oop.py`.  
- Need to validate results
- Need to clean printout results
- Need to store trip results as dataframe or csv
