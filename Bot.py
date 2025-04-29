import os
import Database as db
import matplotlib
import git
from flask import Flask,Response,render_template,request
from io import BytesIO
exit=["bye","Bye","Cu","exit","Quit","q","quit","Exit","See you later"]

def work(a):
    query=a
    send=''
    if query in exit:
            send="\nBye\n"
            return send
    else:
        send=str(db.respond(query))
    return send

app = Flask(__name__)
app.static_folder = 'static'

@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo("")
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400


@app.route("/")
def home():
    return render_template("index.html")
@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return work(userText)
if __name__ == "__main__":
    app.run(host='0.0.0.0')
