# Vython
Vython は、[Programming with Versions (PWV) プロジェクト](https://prg.is.titech.ac.jp/ja/projects/context-oriented-programming/version-programming/)の予備実験として実装された最小限のPythonサブセットです。
Vythonは以下の機能を特徴としています。
- <b>複数バージョンの利用</b>: 開発者は単一クラスの複数のバージョンを柔軟に利用できます。値(オブジェクト)は計算に使用したクラスのバージョンを記録し、そのバージョンの仕様に従って属性参照を行います。
- <b>動的バージョン検査</b>: 互換性・一貫性のあるバージョンに由来する式・値(オブジェクト)の組み合わせで計算が行われていることを動的に検査します。

これらの言語機能を用いて、煩雑な更新プロセスを分割・半自動化することを目標としています。

<b>免責事項</b>
1. この言語は未完成です。また、研究用途のみを目的とした実験言語です。
2. [`src/syntax/lark-vython.lark`](https://github.com/prg-titech/vython/blob/master/src/syntax/lark-vython.lark) は、[larkのPython 3文法](https://github.com/lark-parser/lark/blob/master/lark/grammars/python.lark)に独自の構文拡張を加えたものです。

<b>※作業を始める前に [Compiler Structure and TODO](https://github.com/prg-titech/vython?tab=readme-ov-file#compiler-structure-and-todo) の節を読んで実装の全体像を把握すること。</b>

## How to install / run / test
### Requirement
Vython は 表面言語の構文解析に [lark](https://github.com/lark-parser/lark) を使用しています。
```sh
sudo apt install python3
pip install lark
pip install pytest # ユニットテストでのみ使用
```

### Install / Uninstall
`vython` をインストール / アンインストールするには、プロジェクトルートで以下を実行してください。
```sh
pip install .        # Install
pip uninstall vython # Uninstall
```

### Run
`vython` 言語処理系はインタプリタとトランスパイラを提供しています。
2つ目のコマンドライン引数で `vython` プログラムをどちらを使用して評価するかを指定できます。
例えば、インタプリタを使用して `test/test_interpreter/sample/basic/classandmethod.py` をコンパイル・実行するには、以下を実行してください。
```sh
vython -i test/test_interpreter/sample/basic/classandmethod.py
```
トランスパイラを使用して `test/test_transpiler/sample/basic/classandmethod.py` をコンパイル・実行するには、以下を実行してください。
```sh
vython -t test/test_transpiler/sample/basic/classandmethod.py
```
#### `vython`言語処理系を使用する際のオプション
- `-d` `--debug` は実行時の詳細な情報を出力します。(インタプリタ & トランスパイラ)
```sh
vython -i --debug test/test_interpreter/sample/basic/classandmethod.py | tee tmp.log # tmp.logと標準出力にログを出力
vython -t -d test/test_transpiler/sample/basic/classandmethod.py | tee tmp.log
```
- `--ast` はトランスパイル後のPython ASTを出力します。(トランスパイラ)
```sh
vython -t --ast test/test_transpiler/sample/basic/classandmethod.py
```
- `--wo` を使用するとバージョンの互換性検査機構を含まないPython ASTにトランスパイルされます。(トランスパイラ)
```sh
vython -t --wo test/test_transpiler/sample/basic/classandmethod.py
```


### Test
`test/` 以下のユニットテストを実行するには、以下を実行してください。
```sh
pytest test/
```
`test/sample` にサンプルのpythonファイルが入っています。
新しいサンプルやテストケースを積極的に追加してください。

## Structure
```
project-name/
├── README.md
├── src/                               # ソースコードが含まれるディレクトリ
│     ├── __init__.py                  # 初期化ファイル
│     ├── main.py                      # Runner
│     │
│     ├── interpreter/                 # インタプリタ実装ソースコードが含まれるディレクトリ
│     │    ├── __init__.py             # 初期化ファイル
│     │    ├── run.py                  # インタプリタのRunner
│     │    ├── compiler.py             # コンパイラパイプラインの統括
│     │    ├── parser.py               # [Phase 1] パーサー
│     │    ├── preprocess.py           # [Phase 2] 前処理
│     │    ├── larkToIR.py             # [Phase 3] Lark構文解析結果から中間表現へのトランスパイラ
│     │    ├── interpreter.py          # [Phase 4] インタープリタ
│     │    ├── compatibilitychecker.py # バージョンテーブルを使った互換性検査器
│     │    └── syntax/                 # Vython IRの構文に関するモジュールが含まれるディレクトリ
│     │        ├── __init__.py         # 初期化ファイル
│     │        ├── language.py         # Vython IRの構文定義
│     │        ├── semantics.py        # Vython IR Interpreterの意味論的なオブジェクト（値、環境、ヒープなど）の定義
│     │        └── lark-vython.lark    # Lark-vython 構文のEBNF定義
│     │
│     ├── transpiler/                  # トランスパイラ実装ソースコードが含まれるディレクトリ
│     │    ├──
│     ...
│
└── test/                       # テストコードが含まれるディレクトリ
    ├── __init__.py             # 初期化ファイル
    ├── test_interpreter/       # インタプリタ用のテストコード & サンプルプログラムが含まれるディレクトリ
    │   ├──     
    │   ...
    ├── test_transpiler/       # トランスパイラ用のテストコード & サンプルプログラムが含まれるディレクトリ
    │   ├── 
...
```

## Compiler Structure and TODO
[src/compiler.py](https://github.com/prg-titech/vython/blob/master/src/compiler.py) に定義されています。
```
+----------+
| Raw Code |
+----------+
  |
  ├ [Phase 1]: Parse to lark-vython AST
  v
+-----------------+
| lark-vython AST |
+-----------------+
  |
  ├ [Phase 2]: Preprocess (if applicable)
  v
+-----------------+
| lark-vython AST |
+-----------------+
  |
  ├ [Phase 3]: Compile from lark-vython AST to Vython-IR AST
  v
+---------------+
| Vython-IR AST |
+---------------+
  |
  ├ [Phase 4]: Evaluate Vython-IR AST on Interpreter
  v
+-------------------+
| Evaluation Result |
+-------------------+
```

- Raw Code: バージョンに関連する構文拡張が行われたPython 3のプログラム
- lark-vython AST: [`src/syntax/lark-vython.lark`](https://github.com/prg-titech/vython/blob/master/src/syntax/lark-vython.lark)のEBNFで定義された言語のAST
- Vython-IR AST: [`src/syntax/language.py`](https://github.com/prg-titech/vython/blob/master/src/syntax/language.py)で定義されたコア言語のAST

### TODO
- [Phase 2] は無視してよい。算術プリミティブ値・演算のIntオブジェクト・メソッドへのコンパイルを定義しているが、未検証故に未使用。
- バグ修正は出来るだけ後回しにすること。1日で実装したためバグが取り切れていないが、少なくとも `test/samples/*` 以下の初期サンプルはすべて正常に評価できる。

#### Step 1: ASTのバージョン対応
- [x] 済。

#### Step 2: バージョンテーブル対応
- [ ] `VersionTable` を定義 @ [`src/syntax/semantics.py`](https://github.com/prg-titech/vython/blob/master/src/syntax/semantics.py)
  - 内部メソッドとしてバージョンテーブル操作用のヘルパー関数を定義
    - 必要なヘルパー関数で原子的なものを特定して実装。`union`? `modify`?
  - `VObject` クラスにバージョンテーブル用の属性を追加
- [ ] `VersionTable` 整合性検査を定義 @ [`src/compatibilitychecker.py`](https://github.com/prg-titech/vython/blob/master/src/compatibilitychecker.py)
  - オブジェクトへの参照(変数)のリストを受け取り、それらのバージョンテーブルを用い、整合性・互換性・一貫性チェックを行う。

#### Step 3: Interpreterのバージョン対応
- [x] （済）変数管理を名前とバージョンの組で行うように変更
- [ ] バージョンテーブルの処理をインタプリタに追加 @ [`src/interpreter.py`](https://github.com/prg-titech/vython/blob/master/src/interpreter.py)
  - `VersionTable` 整合性検査の処理
    - Vython-IR に整合性検査を行うための特別なASTノードを追加(メソッド形式？関数形式？)
    - 対応するASTノードの評価をインタプリタに実装
    - `incompatible` はメソッドとして既にAST・評価規則が追加されている。同じような追加実装をすればよい。
  - `VObject` の `VersionTable` を計算する処理
    - `VObject` を生成する式の評価に、返り値の `VersionTable` を計算する処理を追加
- [ ] `incompatible` メソッドの処理
  - （済）Vython IRに `incompatible` に対応するASTノード `CallIncompatible` を追加 @ [`src/syntax/language.py`](https://github.com/prg-titech/vython/blob/master/src/syntax/language.py)
  - Vython AST `CallIncompatible(value=obj)`のinterpret規則にバージョンテーブル処理を追加 @ [`src/interpreter.py`](https://github.com/prg-titech/vython/blob/master/src/interpreter.py)

## Syntax
### Vython Program
```
<prog> ::=                     # トップレベル式の列
    <class_def> <prog>         # クラス定義
  | <function_def> <prog>      # トップレベル関数定義
  | <stmt> <prog>              # 文
  | ε

<class_def> ::=                # クラス定義
    "class" <vname> "{" <function_def> "}"
  # | "class" <vname> "(" <bases> ")" "{" <function_def> "}"

# <bases> ::=                    # ベースクラスの列(未実装)
#     <name> "," <bases>
#   | ε

<function_def> ::=             # 関数定義
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
  | <get_attr> "=" <expr>      # オブジェクトの属性に対する割当

<expr> ::=                     # 式
    <name>                     # 変数参照
  | <vname> "(" <args> ")"     # バージョン付きインスタンス生成
  | <call>                     # 関数呼び出し
  | <expr> "." <call>          # メソッド呼び出し
  | <get_attr>                 # 属性参照
  | "None"                     # None値

<call> ::=                     # 関数呼び出し
  | <name> "(" <args> ")"

<get_attr> ::=
    <expr> "." <name>          # 属性参照

<args> ::=                     # 引数の列
    <expr> "," <args>
  | ε

<vname> ::= <name> "!" <version>
<name> ::= (任意の変数名またはクラス名)

<version> ::= (任意の非負整数)
```


### Semantic Objects
#### Result and Value
```
<result> ::=                 # 結果
    <value>                  # 値
  # | <failure>                # 失敗(未実装)

<value> ::=                  # 値
    <object>                 # オブジェクト
  | <number>                 # 数値
  | <string>                 # 文字列
  | <heap_index>             # ヒープインデックス(参照)
  # | literal                  # リテラル(未実装)

<object> ::=                 # オブジェクト
    "VObject" "(" <type_tag> "," "{" <attributes> "}" "," <versiontable> ")"

<type_tag> ::=
    <name>                   # 普通のインスタンスを示すtype-tag。クラス名が入る
  | "function"               # 関数オブジェクトを示す特別なtype-tag
  | "class"                  # クラス定義文によって生成されるオブジェクトを示す特別なtype-tag
  | "number"                 # 数値を表す特別なtype-tag
  | "string"                 # 文字列を表す特別なtype-tag
  | "None"                   # Noneオブジェクトを示す特別なtype-tag

<attributes> ::=             # オブジェクトの持つ属性の列
    <attribute> "," <attributes>
  | ε

<attribute> ::=              # オブジェクトの持つ属性
    <name> ":" <value>

<heap_index> ::=             # ヒープインデックス(参照)
    (任意の非負整数)

# <failure> ::=                # 失敗(未実装)
#     "fail" <message>
# <message> ::=                # エラーメッセージ(未実装, checkCompatibilityで使うかも)
#      (任意のエラーメッセージ文字列)

<versiontable> ::=           # バージョンテーブル
    "[" <dependencies> "]"

<dependencies> ::=           # クラス依存性(の列)
    <dependency> "," <dependencies>
  | ε

<dependency> ::=             # 単体のクラスへの依存性
    <name> ":" <version>
```

#### Environment
```
<environment> ::=    # 実行時環境
    "(" "{" <bindings> "}" "," <parent> ")"

<bindings> ::=       # 実行時環境の束縛の列
    <binding> "," <bindings>
  | ε

<binding> ::=        # 実行時環境の束縛
    <name> ":" <heap_index>

<parent> ::=         # 親環境
    <environment>
  | "None"           # 親環境なし(ローカル環境 = グローバル環境のとき)
```

#### Heap Memory
```
<heap> ::=             # ヒープ
    "[" <indexed_objects> "]"

<indexed_objects> ::=  # 格納された値(オブジェクト)の列
    <indexed_object> "," <indexed_objects>
  | ε

<indexed_object> ::=   # 格納された値(オブジェクト)
    <heap_index> ":" <object>
```
