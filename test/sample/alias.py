class Apple:
    pass


class Box:
    def __init__(self):
        self.content = None


box1 = Box()
box2 = box1  # box2はbox1と同じオブジェクトを指す

box1.content = Apple()  # box1経由でcontentを変更
box2.content  # box2経由でも変更されたcontentが参照される
