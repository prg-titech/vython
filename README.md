# Vython
Vython は、[Programming with Versions (PWV) プロジェクト](https://prg.is.titech.ac.jp/ja/projects/context-oriented-programming/version-programming/)の予備実験として実装された最小限のPythonサブセットです。Vython では、開発者は単一クラスの複数のバージョンを柔軟に利用できると同時に、プログラム中の計算が期待される仕様のデータフローで行われているかを動的に検査します。

<b>免責事項</b>:
1. 研究言語なので小さい
2. 1日で実装したのでバグがある(多分)

## TODO
やることリスト
#### Step 1: ASTのバージョン対応
- ちゃんとやるなら
  - `src/vython.lark` を変更 
  - `src/syntax/language.py` を変更
  - `src/larkToIR.py` を変更
- その場しのぎ的にやるなら
  - `src/syntax/language.py` を変更
  - `src/larkToIR.py` に 前処理を追加：`Classname__1`は`Classname`クラスのバージョン`1`と解釈

#### Step 2: バージョンテーブル対応
- バージョンテーブルクラスを新しく追加する @ `src/syntax/semantic_object.py`
  - 内部メソッドとしてバージョンテーブル操作用のヘルパー関数を持つ
  - Objectクラスにバージョンテーブルをもたせる or Objectとバージョンテーブルを持つラッパークラスを新しく定義する
- バージョンテーブル整合性検査 @ `src/syntax/semantic_object.py` か新しいファイル？
  - オブジェクトを(1つ? or 2つ?)受け取り、バージョンテーブルを用いて整合性・互換性・一貫性チェックを行う特別な`version_check`関数を追加する。
  - IR ASTに特別な関数を追加する必要はないかも。関数としてパースさせinterpreterで特別な評価を行ってもよい。

#### Step 3: Interpreterのバージョン対応 @ `src/interpreter.py`
- Objectを使う/生成する式の評価に、バージョンテーブルの処理を追加する


## Installation
```
sudo apt install python3
pip install lark
```

## How to use
`pipeline.py`がすべてのコンパイルパスを含む関数。引数としてコンパイル対象へのプロジェクトルートからの相対パスを取る。

### Run
`test/sample/basic.py`をコンパイルして実行。ログは標準出力と`log.txt`へ。
```sh
python -m src.pipeline test/sample/basic.py | tee log.txt
```

### Test
未実装。`test/sample`にサンプルのpythonファイルが入っているのでどんどん追加しましょう。
いいテストフレームワークがあったら導入したほうがいい。

### Structure
```
project-name/
├── README.md
├── src/                      # ソースコードが含まれるディレクトリ
│   ├── __init__.py           # Pythonパッケージとしての初期化ファイル
│   ├── pipeline.py           # コンパイルプロセス全体を統括するパイプラインの実装
│   ├── parser.py             # [Phase 1] パーサー
│   ├── preprocess.py         # [Phase 2] 前処理
│   ├── larkToIR.py           # [Phase 3] Lark構文解析結果を中間表現に変換するモジュール
│   ├── interpreter.py        # [Phase 4] インタープリタ
│   ├── syntax/               # 言語の構文や意味論に関するモジュールが含まれるディレクトリ
│   │   ├── language.py       # 言語の文法定義やASTノードのクラスを定義
│   │   └── semantic_object.py# 意味論的なオブジェクト（値、環境、ヒープなど）の定義
│   └── vython.lark           # Larkで使用する構文定義ファイル
│
└── test/                     # テストコードが含まれるディレクトリ
    ├── __init__.py           # テストパッケージの初期化ファイル
    ├── sample/               # サンプルプログラムやテストケースが含まれるディレクトリ
    │   │
...
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
| Vython-IR AST |
+---------------+
  |
  ├ [Phase 4]: Evaluate vython-IR AST on Interpreter
  v
+-------------------+
| Evaluation Result |
+-------------------+
```

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
#### 結果と値
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

#### 実行時環境
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
