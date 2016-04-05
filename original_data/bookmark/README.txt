--- データセット概要 ---
ソーシャルブックマークサービスDelicious(https://delicious.com/)のユーザログデータ．
ユーザがいつ，どのWebページ(item)にブックマークを付けたかが記録されている．
データのソースはこちら
http://www.dai-labor.de/en/competence_centers/irml/datasets/
データセットが使用された元論文はこちら
http://www.dai-labor.de/fileadmin/files/publications/wetzker_delicious_ecai2008_final.pdf

--- ファイル概要 ---
*.twd: タグごとに以下の12のデータセットがテキストデータとして保存されている．
	ajax.twd
	css.twd
	design.twd
	java.twd
	javascript.twd
	linux.twd
	movielens.twd
	news.twd
	opensource.twd
	photography.twd
	science.twd
	webdesign.twd
ただしmovielens.twdは他とフォーマットが異なるため，残る11データセットを現在使用中．

/tex
stats.pdf: 統計情報(item数，ユーザ数，イベント数)を出力

/histogram
*.png: 林さん作成．前述の11データセットごとにブックマーク数上位１０URLを選び，横軸を時間（日数）にしてヒストグラムをプロット．

--- *.twdファイルの詳細 —1
ユーザ: データセットごとにIDが割り振られている(1〜ユーザ数)．
時間: 日付単位(2003年9月-2007年12月)．
イベント: 1イベント = あるユーザがあるページをブックマークした．
スペース区切りで列を表す．

1行目はitem数とユーザ数を表す．
例えばscience.twdの1行目は，
"89925 36363"
であり1列目がitem数(89925)，2列目がユーザ数(36363)を表す．

2行目以降は各行が1つのitemに対応する．
1列目はそのitemのイベント数を表す．
2列目以降は「ユーザid:日付」のフォーマットが続きイベントの詳細を表す．
例えばscience.twdの4行目は，
"3 706:985 5910:1183 10072:1258"
であり「この行に対応するitemのイベント数は3回で，
985日目にユーザ706，1183日目にユーザ5910，1258日目にユーザ10072が
それぞれブックマークした」ことを意味している．
各行でイベントは古い順にソートされている(はず)．