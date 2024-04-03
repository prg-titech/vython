class Student!1:
    def __init__(self):
        self.score = None


Alice = Student!1()
Bob= Alice  # student2はstudent1と同じオブジェクトを指す

Alice.score = 100  # box1経由でcontentを変更
Bob.score  # box2経由でも変更されたcontentが参照される 
