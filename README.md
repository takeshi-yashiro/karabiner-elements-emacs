# Karabiner Elements 用 Emacs キーバインド

## 概要

Karabiner Elements を用いて任意のアプリ上での Emacs キーバインドを実現する
設定ファイルのジェネレータです。

個人的な嗜好にあわせて以下の通り設定されていますが、ジェネレータを修正すれば
カスタマイズが可能です

- JISキーボード用
- マーク周り(C-Space, C-w, M-w, C-y)も一通り実装
- Emacsキーバインド以外も含む (C-t, C-z, etc.)
- Visual Studio Code はリマップの対象外 (Awesome Emacs 拡張を利用する前提)

## 使い方

利用方法は以下のとおりです。

1. Karabiner Elements をインストール
2. Simple modifications で right_command を right_option にマップ (Metaキー用)
3. 好きなように emacskeys.py をカスタマイズ
4. python3 emacskeys.py > ~/.config/karabiner/assets/complex_modifications/myemacs.json
5. Karabiner Elements の Complex modifications に追加された "Emacs key bindings (yashiro)" を Enable する

## もとにしたもの

公式の complex modifications <https://ke-complex-modifications.pqrs.org/> で公開されている、
以下のルールを再利用しています。

- toggle eisuu with shift + space
- Emacs key bindings (rev 12)

マーク周りのロジックについては emacs.ahk <https://github.com/usi3/emacs.ahk> を参考に、
ほぼ同様のロジックで作成しています。
