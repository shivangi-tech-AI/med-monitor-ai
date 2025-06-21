import sqlite3
import time
from datetime import datetime
from voice_assistant import listen_and_process  # ✅ Correct function name

def check_reminders():
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    now = datetime.now().strftime("%H:%M")

    c.execute("SELECT id, med_name, time, email FROM reminders WHERE time = ? AND status = 'Pending'", (now,))
    rows = c.fetchall()

    for row in rows:
        reminder_id, med_name, reminder_time, email = row
        print(f"⏰ Reminder: Time to take medicine '{med_name}' at {reminder_time}")

        # 🧠 Start voice assistant to confirm medicine intake
        listen_and_process()

        # ✅ Mark as sent to avoid repeat notification
        c.execute("UPDATE reminders SET status = 'Sent' WHERE id = ?", (reminder_id,))
        conn.commit()

    conn.close()

if __name__ == "__main__":
    print("✅ Reminder Scheduler Started...")
    while True:
        check_reminders()
        time.sleep(60)  # Check every 60 seconds
