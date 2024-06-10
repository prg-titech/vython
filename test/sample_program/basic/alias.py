class Apple!1:
    pass


class Box!1:
    def __init__(self):
        self.content = None


box1 = Box!1()
box2 = box1  # box2はbox1と同じオブジェクトを指す

box1.content = Apple!1()  # box1経由でcontentを変更
box2.content  # box2経由でも変更されたcontentが参照される
