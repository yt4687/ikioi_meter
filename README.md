# ikioi_meter

旧ニコニコ実況にあった勢いのデータを取得できるAPIです  
データは json形式で返ります  

使うためのURL [https://api.hiromi-tech.net/ikioi?jkch=all](URL https://api.hiromi-tech.net/ikioi?jkch=all)  
```
各タグの説明(カッコ内はデータタイプ)

status(str)：放送の状況、on_air(放送中) empty(放送中の番組がない)
live_id(str)：放送中の番組のID(取得時に使ったものを記録してるだけなのでコミュニティはタイミングで切れてるかも)
total_watch(int)：総視聴者数
total_comment(int)：総コメント数
ikioi_count(int)：update_intervalの間に書き込まれたコメント数
ikioi_status(str)：実況の盛り上がり具合　普通　多　激多　祭
update_interval(int)：取得周期、分単位(負荷に合わせてもしかしたら変えるかもっていう予防的措置で送る情報)。
　　　　　　　　　　　　コメント/(update_interval)分みたいな表示で使ってもらう想定
```

```
jsonの形式(抜粋)、実際にはすべての実況チャンネルのデータが返ります
放送がある場合
{
    "meta":{
        "status":200
        },
    "data":{
        "jk5":{
            "status":"on_air",
            "live_id":"lv12345",
            "total_watch":2900,
            "total_comment":6250,
            "ikioi_count":441,
            "ikioi_status":"激多",
            "update_interval":1
            }
}

放送がない場合
{
    "meta":{
        "status":200
        },
    "data":{
        "jk333":{
            "status":"empty"
            }
}

失敗時
現状500が返るようになってます
```
