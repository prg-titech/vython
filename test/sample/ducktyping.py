class Fly:
    pass

class Swim:
    pass

class Bird:
    def move(self):
        return Fly()

class Fish:
    def move(self):
        return Swim()

class Animal:
    def make_it_move(animal):
        return animal.move()

bird = Bird()
fish = Fish()

# move()メソッドは引数の値によって動的に振る舞いが変わる
Animal().make_it_move(bird)  # Fly()
Animal().make_it_move(fish)  # Swim()
