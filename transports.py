class Vehicle:
    def __init__(self, id, current_location):
        self.id = id
        self.current_location = current_location 

    def move_to(self,new_location):
        plan = self.plan_route(self.current_location, new_location)
        if plan:
            self.current_location = new_location

    def plan_route(self, current_location, new_location):
        return NotImplementedError()
    
    def __str__(self):
        return f'{self.id} at {self.current_location}' 


class WaterVehicle(Vehicle):
    def plan_route(self, new_location):
        return []

class GroundVehicle(Vehicle):
     def plan_route(self, new_location):
         return[self.current_location, 'gas station', new_location]

class AirVehicle(Vehicle):
     def plan_route(self, new_location):
         return[self.current_location, new_location]





vehicles = [
    WaterVehicle(id='Titanic', current_location='Liverpool'),
    GroundVehicle(id='Humvee', current_location='Baghdad'),
    AirVehicle(id='Air Force One', current_location='Washington')
    ]
 
for vehicle in vehicles:
    vehicle.move_to('Prague')
    print(vehicle)