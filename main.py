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
    
    def make_step(self, index):
        if self.action_time > 0:
            print(f"{index} is occupied. Time remaining: {self.action_time}")
            self.action_time -=1
            if self.action_time == 0:
                print("Vehicle is free")
                self.state = self.state.next_state()

    def is_free(self):
        return isinstance(self.state, FreeState)
    
class Fire(Strategy):
    def execute(self, iterator):
        self.ride_time = random.randint(0, 3)
        while len(self.vehicles) < 3:
            unit = iterator.next()
            if unit is None:  
                break
            for i, vehicle in enumerate(unit.get_vehicles()):
                if vehicle.is_free():
                    print(f"Dispatching vehicle {i} from {unit.get_name()} for fire")
                    self.add_observer(vehicle)
                if len(self.vehicles) >= 3:
                    break

        if random.random() > 0.16:
            self.fire_time = random.randint(5, 25)
            print(f"\nArrival time: {self.ride_time} fire duration: {self.fire_time}\n")
        else:
            self.fire_time = 0
            print(f"\nFalse alarm arrival time: {self.ride_time}\n")

        self.notify_observers()

class Danger(Strategy):
    def execute(self, iterator):
        self.ride_time = random.randint(0,3)
        while len(self.vehicles) < 2:
            unit = iterator.next()
            for i, vehicle in enumerate(unit.get_vehicles()):
                if vehicle.is_free():
                    print(f"Dispatching vehicle {i} from {unit.get_name()} for danger")
                    self.add_observer(vehicle)
                if len(self.vehicles) >= 2:
                    break
        if random.random() > 0.07:
            self.fire_time = random.randint(5,25)
            print(f"\nArrival time: {self.ride_time} danger duration: {self.fire_time}\n")
        else:
            self.fire_time = 0
            print(f"\nFalse alarm arrival time: {self.ride_time}\n")

class Unit:
    def __init__(self, name, coordinates):
        self.name = name
        self.coordinates = coordinates
        self.vehicles = [Vehicle() for _ in range(5)]

    def get_name(self):
        return self.name
    
    def get_vehicles(self):
        return self.vehicles

    def step(self):
        print(f"Vehicles in use {self.name}:")
        for i, vehicle in enumerate(self.vehicles):
            vehicle.make_step(i)

    def get_vehicle(self):
        return self.vehicle

    def get_distance(self, coordinates):
        x = self.coordinates[0] - coordinates[0]
        y = self.coordinates[1] - coordinates[1]
        return (x**2 + y**2)**0.5
    
class Collection():
    def __init__(self):
        self.units = []

    def add(self, unit):
        self.units.append(unit)
    
    def create_iterator(self):
        return Iterator(self.units)
    
    def sort(self, coordinates):
        self.units.sort(key=lambda unit: unit.get_distance(coordinates))
    
class AllUnits:
    def __init__(self):
        self.units = Collection()
        self.strategy = None
        self.init_units()

    def init_units(self):
        self.units.add(Unit("JRG-1", [50.12345678901234, 19.85432167890123]))
        self.units.add(Unit("JRG-2", [50.04512345678901, 19.90456789012345]))
        self.units.add(Unit("JRG-3", [50.07654321098765, 19.81234567890123]))
        self.units.add(Unit("JRG-4", [50.09876543210987, 19.97543210987654]))
        self.units.add(Unit("JRG-5", [50.08123456789012, 19.73567890123456]))
        self.units.add(Unit("JRG-6", [50.03123456789012, 19.99345678901234]))
        self.units.add(Unit("JRG-7", [50.08765432109876, 19.95678901234567]))
        self.units.add(Unit("JRG Szkoly Aspirantow PSP", [50.07098765432109, 20.00876543210987]))
        self.units.add(Unit("JRG Skawina", [49.97234567890123, 19.77234567890123]))
        self.units.add(Unit("LSP Lotnisko w Balicach", [50.06345678901234, 19.79456789012345]))

    def step(self):
        for unit in self.units.units:
            unit.step()

    def set_strategy(self, strategy):
        self.strategy = strategy

    def start(self, coordinates):
        self.units.sort(coordinates)
        self.strategy.execute(self.units.create_iterator())

def main(): # main function
    units = AllUnits()

    x_max, x_min = 50.154564013341734, 49.95855025648944
    y_max, y_min = 20.02470275868903, 19.688292482742394
