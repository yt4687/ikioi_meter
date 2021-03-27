from flask import Flask, jsonify
from flask_restful import Api, Resource, abort, reqparse
from MySQLdb.cursors import DictCursor
import MySQLdb
import json

import ikioi_data

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False # 文字をASCII変換しない
app.config['JSON_SORT_KEYS'] = False # JSONをソートしない
api = Api(app)

# SQLへの接続情報
connection = MySQLdb.connect(host = '127.0.0.1', user = 'username', passwd = 'password', db = 'database', charset = 'utf8mb4')
cursor = connection.cursor(DictCursor)

class Hello(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("jkch", required=True, help="jkch cannot be blank!")
        #parser.add_argument("age", type=int, help="Age cannot be converted")
        args = parser.parse_args()

        # 処理分岐(現状はまったく意味がない)
        # もともと複数の処理を同時に実装するつもりだったころの名残、もったいないので残してある
        if not args["jkch"] in ikioi_data.jikkyo_id_table:
            abort(401, message={"jkch": "jkch cannot be blank!"})

        if args["jkch"] == 'all':
            # GroupCDの呼び出し
            cursor.execute('SELECT * FROM ikioi order by No desc;')
            sqldata = cursor.fetchone()
            # 呼び出したGroupCDをもとに同一グループのデータを取り出す
            cursor.execute('SELECT * FROM ikioi WHERE GroupCD="'+ str(sqldata["GroupCD"]) +'";')
            sqldata = cursor.fetchall()
            #print(sqldata)
        
            # 配列をセット
            jsonr = {}

            for elem in sqldata:
                # 勢いの文字をセット
                if elem['comment_ikioi'] >999:
                    ikioi = '祭'
                elif elem['comment_ikioi'] >199:
                    ikioi = '激多'
                elif elem['comment_ikioi'] >99:
                    ikioi = '多'
                else:
                    ikioi = '普通'

                # 返すjsonを生成
                # 放送がないとき(emptyのとき)は status = empty だけを返す
                # 放送があるときは取得してあるデータを返す
                if elem["LiveStatus"] == 'empty':
                    jsondata = { "status": elem["LiveStatus"]}
                else:
                    jsondata = { "status": elem["LiveStatus"],"live_id": elem["LiveID"], "total_watch": elem["Watchcount"], "total_comment": elem["Commentcount"], "ikioi_count": elem["comment_ikioi"], "ikioi_status": ikioi, "update_interval": elem["interbal"]}
                temp = {elem["JKChannel"]:jsondata}
                # 生成したjsonデータを蓄える
                jsonr.update(temp)
        
        # 最終的なjsonデータを生成
        jsonbody = {'meta':{'status':200},'data': jsonr}
         
        return jsonify(jsonbody)
        
api.add_resource(Hello, "/")

if __name__ == "__main__":
    app.run(debug=False)