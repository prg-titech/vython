class Car!10:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        self.speed = 0

    def accelerate(self, increase):
        self.speed = self.speed + increase
        return self.speed

    def brake(self, decrease):
        self.speed = self.speed - decrease
        if self.speed < 0:
            self.speed = 0
        return self.speed

car = Car!10("Toyota", "Corolla", 2020)
print(car.make)       # Toyota
print(car.model)      # Corolla
print(car.year)       # 2020
