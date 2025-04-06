# md2pxv

md2pxvは、Markdownで執筆された文書をpixiv小説の記法に変換するためのトランスパイラです。

## 機能

- Markdownの見出しをpixiv小説の章記法に変換
- 水平線を改ページに変換
- ルビ記法の変換
- リンク記法の変換
- 文書の検証（linting）
- HTMLコメントの除去（オプション）

## インストール

```bash
git clone https://github.com/TachibanaIone/md2pxv.git
```

または、GitHub上から"Download ZIP"を選択してZIPファイルをダウンロードし、解凍してください。

## 使用方法

Python 3が必要です。

基本的な使用方法：

```bash
python md2pxv.py input.md
```

オプション：

```plain
usage: mpc.py [-h] [-o OUTPUT] [-q] [-s] [-ic] input

Process a markdown file.

positional arguments:
  input                 Input markdown file

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file name
  -q, --quiet           Suppress output messages
  -s, --strict          Compile Check the input file
  -ic, --ignore-comment
                        Ignore HTML style comments (<!---->) in the input file. Note: This option overrides the strict mode.
```

## 入出力の例
### 入力:

```md
# Title: レベル1の見出しは無視されます

## Chapter 1 - The "Lipsum"

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

## Chapter 2 - ルビ

｜仮名《かな》

## Chapter 3 - 改ページ

`***`や`---`、`===`は改ページに変換されます。

***

## Chapter 4 - コメント

<!-- `ignore-comment` フラグをオンにすると、コメントは無視されます。 -->

文章中に挿入された<!-- コメント -->も無視されます。
```

### 出力:

```plain
[chapter:Chapter 1 - The "Lipsum"]

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

[chapter:Chapter 2 - ルビ]

[[rb:仮名 > かな]]

[chapter:Chapter 3 - 改ページ]

`***`や`---`、`===`は改ページに変換されます。

[newpage]

[chapter:Chapter 4 - コメント]

文章中に挿入されたも無視されます。
```

## コンパイルチェック

`-s` または `--strict` オプションを使用すると、入力ファイルに対して以下の検証を行います：

- レベル1の見出しは文書の最初に配置し、複数存在してはならない
- HTMLコメントが含まれていないこと（`--ignore-comment` オプションで無視可能）

## 今後の開発計画

- [ ] 挿絵のサポート
- [ ] ページリンク・外部リンクのサポート
- [ ] 複数ファイルの結合機能
- [ ] より詳細なコンパイルチェック機能

## ライセンス

MIT License
