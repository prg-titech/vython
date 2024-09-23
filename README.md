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
- `-t` の**直後**で以下に示すオプションを使用すると、`vython`の提案言語機構のON,OFFを選択したトランスパイルができます。(トランスパイラ) 
  - `vython`  : 全ての提案言語機構がON
  - `python`  : 全ての提案言語機構がOFF
  - `wrap-primitive`: primitiveな値を専用のクラスでラップする
  - `vt-init` : オブジェクトに自身のバージョン情報だけを持たせる
  - `vt-prop` : オブジェクトが自身のバージョン情報を持ち、他のオブジェクトの計算でそれらが合成される
```sh
vython -t python --wo test/test_transpiler/sample/basic/classandmethod.py
```


### Test
`test/` 以下のユニットテストを実行するには、以下を実行してください。
```sh
pytest test/
```
`test/sample_program` にサンプルの`vython`プログラムファイルが入っています。



## Benchmarking / Evaluation
<b>注意</b>
1. グラフ生成など、フルで評価スクリプトを使えるのはトランスパイラの評価のみです。
2. 汎用的ではないので細かい仕様は各々の環境でハードコーディングをする必要があります。

### How to run
0. `benchmark/benchmark_settings.json` を以下にしたがって編集する
1. プロジェクトルートで次のコマンドを打つ
```sh
python3 benchmark/main.py
```
2. 生成された`benchmark/log/result`に結果の`*.csv`とグラフの`*.png`を確認する

#### ベンチマーク設定
- ベンチマークモード共通の設定
  - `"processor"`       : どちらの言語処理系を利用した測定を行うか
    - モード`interpreter`: インタプリタで測定
    - モード`transpiler` : トランスパイラで測定
  - `"benchmark_target"`: 測定するプログラムは何を用いるか
    - モード`sample`  : 事前に用意したプログラムを用いる
    - モード`generate`: ベンチマーク用のプログラムを生成して用いる 
  - `"num_iretations"`  : ベンチマークを何回実行するか
- `"processor": transpiler`時の追加設定項目
  - `"comparison_strategy"`: 使用する言語機構を切り替えた測定が可能
    - モード`all`: 切り替えられる全てのケースで測定 
    - モード`v&p`: 全ての言語機構を使用(vython)と、全て使用しない(python)の二つで測定
- `"benchmark_target": generate`時の追加設定項目
  - `"num_loop"`                 : 何回primitive演算を行うか
  - `"num_base_names"`           : 生成されるvythonファイルにおけるクラス名の種類数
  - `"num_base_versions"`        : 生成されるvythonファイルにおける各クラスのバージョン数
  - `"num_interval_num_versions"`: 実際に使用するバージョン数を決定する引数
    - モード`geometric`: 使用するバージョン数は、1,2,4,...
    - モード`min_max`: 
- `"benchmark_target": sample`時の追加設定項目
  - `"path_benchmarks"`: 測定するプログラムのファイルパス or 測定するプログラムの集合を直下に含むディレクトリパス

### SRCに記載した評価を行う方法
Benchmark Settings used in 3p-abstract of APLAS SRC 2024
```bash
{
  "processor": "transpiler",
  "benchmark_target": "generate",
  "num_iterations": 500,

  "num_loop": 2000,
  "num_base_names": 25,
  "num_base_versions": 2,
  "interval_num_versions": "geometric",

  "comparison_strategy": "all"
}
```
```bash
{
  "processor": "transpiler",
  "benchmark_target": "sample",
  "num_iterations": 500,

  "path_benchmarks": "benchmark/sample_programs",

  "comparison_strategy": "all"
}
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
必要があれば適宜追加

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

