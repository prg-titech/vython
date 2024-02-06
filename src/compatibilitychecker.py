from src.syntax.semantics import VersionTable

# バージョンの整合性検査
# アルゴリズムと仕様もコメントで書くこと
def checkCompatibility(vt1, vt2):
    x = vt1.compat(vt2)
    if vt1.compat(vt2) == True:
        pass
    else:
        raise TypeError(f"Inconsistent Version Usage:\nComparing {x[0]}!{x[1]} and {x[0]}!{x[2]} values")
        