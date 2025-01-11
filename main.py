from abc import ABC, abstractmethod

class Strategy(ABC): #pattern for strategy
    @abstractmethod
    def execute(self, iterator):
        pass

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
    
def main(): # main function
    print("main funciton")