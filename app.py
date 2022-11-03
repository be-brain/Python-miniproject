from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.qy1gvvo.mongodb.net/cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/ha", methods=["POST"])
def ha_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']

    comment_list = list(db.ha.find({}, {'_id': False}))
    count = len(comment_list) + 1

    doc = {
        'num':count,
        'name':name_receive,
        'comment':comment_receive,
        'done':0
    }
    db.ha.insert_one(doc)
    return jsonify({'msg':'저장 완료!'})

@app.route("/ha/done", methods=["POST"])
def delete_comment():
    num_receive = request.form['num_give']
    db.ha.update_one({'num':int(num_receive)},{'$set':{'done':1}})
    return jsonify({'msg': '삭제완료'})

@app.route("/ha", methods=["GET"])
def ha_get():
    comment_list = list(db.ha.find({}, {'_id':False}))
    return jsonify({'comments':comment_list})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)