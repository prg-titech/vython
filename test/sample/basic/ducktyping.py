class Fly!1:
    pass

class Swim!1:
    pass

class Bird!1:
    def move(self):
        return Fly!1()

class Fish!1:
    def move(self):
        return Swim!1()

class Animal!1:
    def make_it_move(animal):
        return animal.move()

bird = Bird!1()
fish = Fish!1()

# move()メソッドは引数の値によって動的に振る舞いが変わる
Animal!1().make_it_move(bird)  # Fly()
Animal!1().make_it_move(fish)  # Swim()