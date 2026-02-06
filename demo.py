import pymysql
from flask import Flask


app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(
        host=app.config["MYSQL_HOST"],
        user=app.config["MYSQL_USER"],
        password=app.config["MYSQL_PASSWORD"],
        database=app.config["MYSQL_DATABASE"],
        port=app.config["MYSQL_PORT"],
        cursorclass=pymysql.cursors.DictCursor
    )


@app.route("/")
def hello():
    conn = get_db_connection()
    conn.close()
    return "Database Connected Successfully!"


if __name__ == "__main__":
    app.run(debug=True)
