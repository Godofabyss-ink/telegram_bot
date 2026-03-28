class Car:

   def __init__(self, color, consumption, tank_volume, mileage = 0):
       self.color = color
       self.consumption = consumption
       self.tank_volume = tank_volume
       self.reserve = tank_volume
       self.mileage = mileage
       self.engine_on = False

   def __str__(self):
       return f'Color - {self.color}\n' \
               f'Consumption - {self.consumption}\n' \
               f'Reserve - {self.reserve}\n' \
               f'Mileage - {self.mileage}'

   def start_engine(self): # включение двигателя
       if self.engine_on:
           return f'Engine is already on'
       elif self.reserve == 0:
           return f'Tank is empty'
       else:
           self.engine_on = True
           return f'Engine is on'

   def stop_engine(self): # выключение двигателя
       if self.engine_on or self.reserve == 0:
           return f'Engine is off'
       else:
           return f'Engine is already off'

   def drive(self, distance): # запуск машины
       if not self.engine_on:
           return f'Engine is off'
       elif self.reserve / self.consumption * 100 < distance:
           return f'Low on fuel'
       elif self.reserve == 0:
           self.stop_engine()
       else:
           self.mileage += distance
           self.reserve -= distance / 100 * self.consumption
           return f'Full way - {self.mileage} km\nFuel reserve - {self.reserve} l, {self.reserve / self.tank_volume * 100:.1f} %'

car_1 = Car(color = 'cherry', consumption = 10, tank_volume = 60)
print(car_1)
print(car_1.start_engine())
print(car_1.drive(80))
print(car_1.drive(160))
print(car_1.drive(60))
print(car_1.drive(300))
print(car_1.drive(20))
