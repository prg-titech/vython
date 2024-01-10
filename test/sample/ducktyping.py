class Animal:
    def move(self, movement):
        return movement


class Walk:
    pass


class Swim:
    pass


animal = Animal()
walk_movement = Walk()
swim_movement = Swim()
walking_animal = animal.move(walk_movement)
swimming_animal = animal.move(swim_movement)
walking_animal
