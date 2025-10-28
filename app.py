from flask import Flask, render_template, request, jsonify
import sqlite3, os

app = Flask(__name__)

# ----------------- DATABASE SETUP -----------------
def init_db():
    if not os.path.exists("chatbot.db"):
        conn = sqlite3.connect("chatbot.db")
        cur = conn.cursor()
        cur.execute('''CREATE TABLE messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_message TEXT,
                        bot_reply TEXT
                      )''')
        conn.commit()
        conn.close()

init_db()


# ----------------- CHATBOT LOGIC -----------------
def chatbot_response(user_text):
    user_text = user_text.lower()
    if "hello" in user_text or "hi" in user_text:
        return "Hello! How can I help you today?"
    elif "name" in user_text:
        return "I'm a simple Flask chatbot!"
    elif "bye" in user_text:
        return "Goodbye! Have a nice day!"
    else:
        return "Sorry, I didn’t understand that."


# ----------------- ROUTES -----------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get", methods=["POST"])
def get_response():
    user_msg = request.form["msg"]
    bot_msg = chatbot_response(user_msg)

    # Store both user and bot messages in SQLite
    conn = sqlite3.connect("chatbot.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (user_message, bot_reply) VALUES (?, ?)", (user_msg, bot_msg))
    conn.commit()
    conn.close()

    return jsonify(bot_msg)


@app.route("/history")
def history():
    conn = sqlite3.connect("chatbot.db")
    cur = conn.cursor()
    cur.execute("SELECT user_message, bot_reply FROM messages")
    data = cur.fetchall()
    conn.close()
    return render_template("history.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
