from src.syntax.semantics import VersionTable

# バージョンの整合性検査
# アルゴリズムと仕様もコメントで書くこと
def checkCompatibility(vt1, vt2):
    x = vt1.compat(vt2)
    if vt1.compat(vt2) == True:
        pass
    else:
        raise TypeError(f"互換性のない値を混ぜて使っている: クラス{x[0]}のバージョン{x[1]},{x[2]}の値")
        