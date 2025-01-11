from abc import ABC, abstractmethod
import random

class Strategy(ABC): #pattern for strategy
    def __init__(self):
        self.vehicles =[]
        self.ride_time = 0
        self.fire_time = 0

    @abstractmethod
    def execute(self, iterator):
        pass
    
    def notify_observers(self):
        for vehicle in self.vehicles:
            vehicle.update(self)
    
    def add_observer(self,vehicle):
        self.vehicles.append(vehicle)

class IObserver(ABC): #pattern for observer
    @abstractmethod
    def update(self, strategy):
        pass

class IState(ABC): #pattern for stae
    @abstractmethod
    def next_state(slef):
        pass

class Iterator(ABC): #pattern for iterator
    def __init__(self, collection):
        self.collection = collection
        self.position = -1

    def has_next(self):
        return self.position < len(self.collection) - 1
    
    def next(self):
        if self.has_next():
            self.position +=1
            return self.collection[self.position]
        return None
    
class FreeState(IState): #state pattern implementation 
    def __init__(self, vehicle):
        self.vehicle = vehicle

    def next_state(self):
        return BusyState(self.vehicle)
    
class BusyState(IState):
    def __init__(self,vehicle):
        self.vehicle = vehicle

    def next_state(self):
        return FreeState(self.vehicle)
    
class Vehicle(IObserver):
    def __init__(self):
        self.state = FreeState(self)
        self.action_time = 0
    
    def update(self, strategy):
        self.state = self.state.next_state
        self.action_time = strategy.fire_time + 2* strategy.ride_time
    
    def make_step(self):
        if self.action_time > 0:
            self.action_time -=1
            if self.action_time == 0:
                self.state = self.state.next_state()
    def is_free(self):
        return isinstance(self.state, FreeState)
    
class Fire(Strategy):
    def execute(self, iterator):
        self.ride_time = random.randint(0, 3)
        self.fire_time = random.randint(5, 25)

class Unit:
    def __init__(self, name, coordinates):
        self.name = name
        self.coordinates = coordinates
        self.vehicle = [Vehicle() for _ in range(5)]
    def get_vehicle(self):
        return self.vehicle

    def get_distance(self, coordinates):
        x = self.coordinates[0] - coordinates[0]
        y = self.coordinates[1] - coordinates[1]
        return (x**2 + y**2)**0.5
    


def main(): # main function
    print("main funciton")