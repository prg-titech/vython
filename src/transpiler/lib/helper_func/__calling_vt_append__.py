# wrapされるメソッド名に変わる
def tmp_method():
    result = self.tmpInvoke()# wrapされるメソッドの呼び出し: wrapされるメソッド名は少し変える
    if result is not None:
        append(result,self)
        return result
    return
