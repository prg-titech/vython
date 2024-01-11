# Vython

## Requirements
-- Python 3 (確認済み v3.10.13)
-- Lark

## How to use
`pipeline.py`が今のmain関数。コンパイル対象のファイルへの(プロジェクトルートからの)相対パスを引数に取る。

### Run
`test/sample/basic.py`をコンパイルして実行。ログは標準出力と`log.txt`へ。
```sh
python -m src.pipeline test/sample/basic.py | tee log.txt
```

### Test
未実装。

## Syntax
### MiniPython Syntax
```
<prog> ::=                     # トップレベル式の列
    <class_def> <prog>         # クラス定義
  # | <function_def>             # トップレベル関数定義
  | <stmt> <prog>              # 文
  | ε

<class_def> ::=                # クラス定義
    "class" <name> "(" <bases> ")" "{" <function_def> "}"

<bases> ::=                    # ベース(スーパー)クラスの列
    <name> "," <bases>
  | ε

<function_def> ::=             # 関数定義(今はメソッド定義と同じ)
    "def" <name> "(" <args> ")" ":" <stmts>

<stmts> ::=                    # 文の列
    <stmt> <stmts>
  | ε

<stmt> ::=                     # 文
    <expr>                     # 式
  | <assign>                   # 属性割当て
  | "return" <expr>            # return文
  | "pass"                     # pass文

<assign> ::=                   # 属性割当
    <name> "=" <expr>          # 変数割当
  | <attribute> "=" <expr>     # オブジェクトの属性に対する割当

<expr> ::=                     # 式
    <name>                     # 変数参照
  | <call>                     # 関数呼び出し(メソッド含む)
  | <attribute>                # 属性参照
  | "None"                     # None値

<call> ::=                     # 関数呼び出し
    <attribute> "(" <args> ")" # メソッド呼び出し
  # | <name> "(" <args> ")"      # 関数呼び出し

<attribute> ::=
    <expr> "." <name>          # 属性参照

<args> ::=                     # 引数の列
    <expr> "," <args>
  | ε

<name> ::= (任意の変数名またはクラス名)
```


### Semantic Objects
#### 結果/値
```
<result> ::=                 # 結果
    <value>                  # 値
  # | <failure>                # 失敗(未実装)

<value> ::=                  # 値
    <object>                 # オブジェクト
  | <heap_index>             # ヒープインデックス(参照)
  # | literal                  # リテラル(未実装)

<object> ::=                 # オブジェクト
    "Object(" <type_tag> ", {" <attributes> "})"

<type_tag> ::=
    <name>                   # 普通のインスタンスを示すtype-tag。クラス名が入る
  | "function"               # 関数オブジェクトを示す特別なtype-tag
  | "class"                  # クラス定義文によって生成されるオブジェクトを示す特別なtype-tag
  | "None"                   # Noneオブジェクトを示す特別なtype-tag

<attributes> ::=             # オブジェクトの持つ属性の列
    <attribute> <attributes>
  | ε

<attribute> ::=              # オブジェクトの持つ属性
    <name> ":" <value>

<heap_index> ::=             # ヒープインデックス(参照)
    (任意の非負整数)

# <failure> ::= "Failure(message=" <message> ")"
# <message> ::= (任意のエラーメッセージ文字列)
```

#### 実行時間環境
```
<environment> ::=    # 実行時環境
    "Environment({" <bindings> "}, " <parent> ")"

<bindings> ::=       # 実行時環境の束縛の列
    <binding> ("," <binding>)*
  | ε

<binding> ::=        # 実行時環境の束縛
    <name> ":" <heap_index>

<parent> ::=         # 親環境
    <environment>    # 親の環境
  | "None"           # 親環境なし(ローカル環境 = グローバル環境のとき)
```

#### ヒープ(メモリ領域)
```
<heap> ::=             # ヒープ
    "Heap([" <indexed_objects> "])"

<indexed_objects> ::=  # 格納された値(オブジェクト)の列
    <indexed_object> <indexed_objects>
  | ε

<indexed_object> ::=   # 格納された値(オブジェクト)
    <heap_index> ":" <object>
```
## Compilation
```
+----------+
| Raw Code |
+----------+
|
├ [Phase 1]: Parse to lark-python AST
v
+-----------------+
| lark-python AST |
+-----------------+
|
├ [Phase 2]: Preprocess (if applicable)
v
+------------------------------+
| Preprocessed lark-python AST |
+------------------------------+
|
├ [Phase 3]: Compile from lark-python AST to vython-IR AST
v
+---------------+
| vython-IR AST |
+---------------+
|
├ [Phase 4]: Evaluate vython-IR AST on Interpreter
v
+-------------------+
| Evaluation Result |
+-------------------+
```