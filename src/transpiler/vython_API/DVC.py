


def checkCompatibility():
    # 仮の実装
    print("[LOG]: checkCompatibility() is called")
    return



'''
デコレーターの定義
'''
def check_decorator(func):
    def wrapper(*args, **kwargs):
        checkCompatibility()
        result = func(*args, **kwargs)
        return result
    return wrapper


'''
テスト

@check_decorator
def add(v1,v2):
    return v1 + v2
print(add(1,2))
'''



