from flask import Flask, request, render_template, redirect, url_for
import os
from wsgiref import simple_server
import pandas as pd
from flask import jsonify

from werkzeug.utils import secure_filename
from db import database
import train as t
import recommend as rec

app = Flask(__name__)


@app.route("/", methods=['GET'])
def home():
    db_session = database.CassandraConnect.conn()
    row = db_session.execute("select * from books.books_details")
    l = rec.Recommend.recommend('Data Smart')
    print(l)
    return render_template('index.html', books=row)


@app.route("/admin", methods=['GET'])
def admin():
    return render_template('admin.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    db_session = database.CassandraConnect.conn()
    if request.method == 'POST':
        f = request.files['bookCsv']
        split_tup = os.path.splitext(f.filename)

        if split_tup[1] == '.csv':
            f.save(secure_filename(f.filename))
            df = pd.read_csv(f.filename)
            df.fillna('', inplace=True)
            delete = db_session.execute("TRUNCATE books.books_details;")
            insert = "INSERT INTO books.books_details (id,Title,Author,Genre,SubGenre, Publisher) VALUES(?,?,?,?,?,?)"
            prepared = db_session.prepare(insert)
            for ind in df.index:
                db_session.execute(prepared, (
                ind, df.at[ind, 'Title'], df.at[ind, 'Author'], df.at[ind, 'Genre'], df.at[ind, 'SubGenre'],
                df.at[ind, 'Publisher']))
            os.remove(f.filename)
            return redirect(url_for("admin", status='true'))
        else:
            return redirect(url_for("admin", status='false'))


@app.route("/train", methods=['POST'])
def train():
    trainModal = t.Train()
    trainModal.train()
    return redirect(url_for('admin', train='true'))

@app.route("/recommend", methods=['POST'])
def recommend():
    recm = rec.Recommend()
    return jsonify(recm.recommend(request.form['book_title']))

port = int(os.getenv("PORT", 5000))
if __name__ == "__main__":
    host = '0.0.0.0'
    # port = 5000
    httpd = simple_server.make_server(host, port, app)
    # print("Serving on %s %d" % (host, port))
    httpd.serve_forever()
