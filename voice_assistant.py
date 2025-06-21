import speech_recognition as sr
import sqlite3
from datetime import datetime

def mark_as_taken():
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    now = datetime.now().strftime("%H:%M")
    c.execute("UPDATE reminders SET status = 'Taken' WHERE time = ? AND status = 'Pending'", (now,))
    conn.commit()
    conn.close()

def listen_and_process():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎤 Please say: 'I took my medicine'")
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")

            if "took" in text.lower() and "medicine" in text.lower():
                print("✅ Medicine intake confirmed!")
                mark_as_taken()
            else:
                print("⚠️ Could not confirm medicine intake.")

        except sr.UnknownValueError:
            print("❌ Could not understand audio.")
        except sr.RequestError:
            print("⚠️ Could not request results. Check your internet.")

if __name__ == "__main__":
    listen_and_process()
