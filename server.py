from flask import Flask
from waitress import serve

app = Flask(__name__)

@app.route("/")
def returnHTML():
    return "Hi, This is Wife-Bot Hosting with render.com service"

if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=80)
    serve(app, host='0.0.0.0', port=80)



    