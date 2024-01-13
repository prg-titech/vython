# Vython
Vython は、[Programming with Versions (PWV) プロジェクト](https://prg.is.titech.ac.jp/ja/projects/context-oriented-programming/version-programming/)の予備実験として実装された最小限のPythonサブセットです。
Vythonは以下の機能を特徴としています。
- <b>複数バージョンの利用</b>: 開発者は単一クラスの複数のバージョンを柔軟に利用できます。値(オブジェクト)は計算に使用したクラスのバージョンを記録し、そのバージョンの仕様に従って属性参照を行います。
- <b>動的バージョン検査</b>: 互換性・一貫性のあるバージョンに由来する式・値(オブジェクト)の組み合わせで計算が行われていることを動的に検査します。

<b>免責事項</b>
1. この言語は未完成で、実験的な研究用途のみを目的としています。
2. `src/vython.lark` は、[lark-parserにより提供されるpython3文法](https://github.com/lark-parser/lark/blob/master/lark/grammars/python.lark)に独自の構文拡張を加えたものです。

## TODO
作業を始める前に [Compilation](https://github.com/prg-titech/vython?tab=readme-ov-file#compilation) の節を読んで全体のコンパイルフローを把握すること。
- [Phase 2]は無視してよい。算術プリミティブ値・演算のIntオブジェクト・メソッドへのコンパイルを定義しているが、未検証故に未使用。
- バグ修正は出来るだけ後回しにすること。少なくとも `test/samples/*` 以下の初期サンプルはすべて正常に評価できる。しかし、1日で実装したためバグが取り切れていない。後で適当な時期に修正すること。

#### Step 1: ASTのバージョン対応
- 最終目標はvyhton-IRにバージョンの情報が含まれるようにすること。
- [ ] ちゃんとやるなら
  - lark-pythonのAST定義 `src/vython.lark` を変更 
  - vython-IRの定義 `src/syntax/language.py` を変更
  - lark-pythonからvython-IRへのトランスパイラ定義 `src/larkToIR.py` を変更
- [ ] その場しのぎ的にやるなら
  - vython-IRの定義 `src/syntax/language.py` を変更
  - lark-pythonからvython-IRへのトランスパイラ定義 `src/larkToIR.py` に 前処理を追加
    - `Classname__1`は`Classname`クラスのバージョン`1`と解釈

#### Step 2: バージョンテーブル対応
- [ ] 2-1 バージョンテーブルクラスを定義 @ `src/syntax/semantic_object.py`
  - 内部メソッドとしてバージョンテーブル操作用のヘルパー関数を定義
    - `union`? `modify`? 必要かつ原子的なヘルパー関数を特定。もしかしたら`union`は`modify`を使って定義するのかも？
  - VObjectクラスにバージョンテーブルを追加 or VObjectとバージョンテーブルを持つラッパークラスを新しく定義
- [ ] 2-2 バージョンテーブル整合性検査を定義 @ `src/syntax/semantic_object.py` か新しいファイル？
  - オブジェクトへの参照(変数)のリストを受け取り、それらのバージョンテーブルを用い、整合性・互換性・一貫性チェックを行う。

#### Step 3: Interpreterのバージョン対応 @ `src/interpreter.py`
- [ ] バージョンテーブルの処理をインタプリタに追加
  - バージョンテーブル整合性検査の文の評価を追加
    - 名前は `check` だと普通の関数と区別がつかないので、`checkVersionCompatibility` など長い名前にしてもいい。
    - 拡張の方向性は２つある。どちらでもOK。
      - lark-pythonとvython-IRに整合性検査を行うための特別なASTノードを追加して、その評価をインタプリタに実装
      - lark-pythonとvython-IRは拡張<u>せず</u>、関数呼び出し(vython ASTレベルでは`Call`)のcalleeのfunctionオブジェクトが特別な名前(`check`や`checkVersionCompatibility`)を持つ場合に限って、interpreterで特別な評価を追加
  - 他のVObjectを使う/生成する式の評価に、返り値のバージョンテーブルを計算する処理を追加

## Requirement
Vython は Parser として [lark](https://github.com/lark-parser/lark) を使用しています。
```sh
sudo apt install python3
pip install lark
pip install pytest # ユニットテストでのみ使用
```

## How to install / run / test
### Install / Uninstall
`vython` をインストール / アンインストールするには、プロジェクトルートで以下を実行してください。
```sh
pip install .        # Install
pip uninstall vython # Uninstall
```

### Run
`vython` はコマンドライン引数としてコンパイル対象へのプロジェクトルートからの相対パスを取ります。
`test/sample/basic.py` をコンパイル・実行するには、以下を実行してください。
```sh
vython test/sample/basic.py
```
`vython` コンパイラのデバッグモードはより詳細な各コンパイルフェーズの情報を出力します。
デバッグモードで `test/sample/basic.py` をコンパイル・実行し、標準出力と `tmp.log` へとログを書きだすには、以下を実行してください。
```sh
vython --debug test/sample/basic.py | tee tmp.log
vython -d test/sample/basic.py | tee tmp.log
```

### Test
pytestを用いて `test/` 以下の全てのユニットテストを実行するには、以下を実行してください。
```sh
pytest test/
```
`test/sample` にサンプルのpythonファイルが入っているので積極的に追加してください。

### Structure
```
project-name/
├── README.md
├── src/                       # ソースコードが含まれるディレクトリ
│   ├── __init__.py            # 初期化ファイル
│   ├── run.py                 # Runner
│   ├── compiler.py            # コンパイラパイプラインの統括
│   ├── parser.py              # [Phase 1] パーサー
│   ├── preprocess.py          # [Phase 2] 前処理
│   ├── larkToIR.py            # [Phase 3] Lark構文解析結果から中間表現へのトランスパイラ
│   ├── interpreter.py         # [Phase 4] インタープリタ
│   ├── syntax/                # Vython IRの構文に関するモジュールが含まれるディレクトリ
│   │   ├── __init__.py        # 初期化ファイル
│   │   ├── language.py        # Vython IRの構文定義
│   │   └── semantic_object.py # Vython IR Interpreterの意味論的なオブジェクト（値、環境、ヒープなど）の定義
│   └── vython.lark            # Lark-python 構文のEBNF定義
│
└── test/                      # テストコードが含まれるディレクトリ
    ├── __init__.py            # 初期化ファイル
    ├── sample/                # サンプルプログラムが含まれるディレクトリ
    │   │
...
```

## Compilation
[src/compiler.py](https://github.com/prg-titech/vython/blob/master/src/compiler.py) に定義されている。
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
+-----------------+
| lark-python AST |
+-----------------+
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
  # | <function_def>             # トップレベル関数定義(未実装)
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
  # | <name> "(" <args> ")"      # 関数呼び出し(未実装)

<attribute> ::=
    <expr> "." <name>          # 属性参照

<args> ::=                     # 引数の列
    <expr> "," <args>
  | ε

<name> ::= (任意の変数名またはクラス名)
```


### Semantic VObjects
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
    "VObject" "(" <type_tag> "," "{" <attributes> "}" ")"

<type_tag> ::=
    <name>                   # 普通のインスタンスを示すtype-tag。クラス名が入る
  | "function"               # 関数オブジェクトを示す特別なtype-tag
  | "class"                  # クラス定義文によって生成されるオブジェクトを示す特別なtype-tag
  | "None"                   # Noneオブジェクトを示す特別なtype-tag

<attributes> ::=             # オブジェクトの持つ属性の列
    <attribute> "," <attributes>
  | ε

<attribute> ::=              # オブジェクトの持つ属性
    <name> ":" <value>

<heap_index> ::=             # ヒープインデックス(参照)
    (任意の非負整数)

# <failure> ::=                # 失敗(未実装)
#     "Failure" "(" <message> ")"  
# <message> ::=                # エラーメッセージ(未実装, version_checkで使うかも)
#      (任意のエラーメッセージ文字列)
```

#### 実行時環境
```
<environment> ::=    # 実行時環境
    "Environment "(" "{" <bindings> "}" "," <parent> ")"

<bindings> ::=       # 実行時環境の束縛の列
    <binding> "," <bindings>
  | ε

<binding> ::=        # 実行時環境の束縛
    <name> ":" <heap_index>

<parent> ::=         # 親環境
    <environment>
  | "None"           # 親環境なし(ローカル環境 = グローバル環境のとき)
```

#### ヒープ(メモリ領域)
```
<heap> ::=             # ヒープ
    "Heap" "(" "[" <indexed_objects> "]" ")"

<indexed_objects> ::=  # 格納された値(オブジェクト)の列
    <indexed_object> "," <indexed_objects>
  | ε

<indexed_object> ::=   # 格納された値(オブジェクト)
    <heap_index> ":" <object>
```
