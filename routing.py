from flask import Flask,render_template,request
from model import agent

app=Flask(__name__)

@app.route("/")
def home():
    return render_template("/main.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(agent.get_response(userText))



if __name__ == "__main__":

    app.run(
        host="10.18.23.88"

    )