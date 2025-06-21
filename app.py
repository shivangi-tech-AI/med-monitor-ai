from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
import subprocess
from datetime import datetime
from image_detection import detect_pill

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reminders (
                  id INTEGER PRIMARY KEY,
                  med_name TEXT,
                  time TEXT,
                  mode TEXT,
                  email EMAIL,
                  status TEXT DEFAULT "Pending")''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set', methods=['POST'])
def set_medicine():
    time = request.form['time']
    med_name = request.form['med_name']
    mode = request.form['confirmation_mode']
    email = request.form['email']
    
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("INSERT INTO reminders (med_name, time, mode, email) VALUES (?, ?, ?, ?)", (med_name, time, mode, email))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/logs')
def logs():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("SELECT * FROM reminders")
    data = c.fetchall()
    conn.close()
    return render_template('logs.html', data=data)

@app.route('/pending')
def pending_check():
    now = datetime.now().strftime("%H:%M")
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute("SELECT * FROM reminders WHERE time = ? AND status = 'Pending'", (now,))
    result = c.fetchall()
    conn.close()

    if result:
        return jsonify({"status": "trigger", "data": result})
    return jsonify({"status": "wait"})

@app.route("/verify")
def verify():
    return render_template("verify.html")

@app.route("/verify_image", methods=["POST"])
def verify_image():
    file = request.files['image']
    file.save("temp/captured_image.jpg")

    result = detect_pill("temp/captured_image.jpg")  # Modify detect_pill() to accept path

    if result == "Pill Detected":
        return jsonify({"message": "✅ Medicine Verified!"})
    elif result == "No Pill":
        return jsonify({"message": "❌ No medicine detected. Please try again."})
    else:
        return jsonify({"message": "❌ Camera error occurred."}), 500

@app.route("/verify_voice")
def verify_voice():
    try:
        subprocess.run(["python", "voice_assistant.py"])
        return jsonify({"message": "🎤 Voice verification complete!"})
    except Exception as e:
        return jsonify({"message": f"❌ Voice error: {str(e)}"}), 500

@app.route("/delete/<int:id>", methods=["POST"])
def delete_reminder(id):
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute("DELETE FROM reminders WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/history")


@app.route('/history')
def history():
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute("SELECT * FROM reminders ORDER BY id DESC ")
    data = c.fetchall()
    conn.close()
    return render_template("history.html", data=data)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
