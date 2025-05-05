import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QTimeEdit, QMessageBox
)
from PyQt5.QtCore import QTime, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor

class FeedingSchedulerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🕒 Feeding Scheduler")
        self.resize(320, 280)
        self.set_light_palette()

        font = QFont("Arial", 11)
        layout = QVBoxLayout()

        title = QLabel("Set feeding times:")
        title.setFont(QFont("Arial", 13, QFont.Bold))
        layout.addWidget(title)

        self.time_morning = QTimeEdit()
        self.time_noon = QTimeEdit()
        self.time_evening = QTimeEdit()

        # טען מה-DB אם יש זמני האכלה
        self.load_times_from_db()

        label_morning = QLabel("🌞 Morning:")
        label_morning.setFont(font)
        layout.addWidget(label_morning)
        layout.addWidget(self.time_morning)

        label_noon = QLabel("🌤️ Noon:")
        label_noon.setFont(font)
        layout.addWidget(label_noon)
        layout.addWidget(self.time_noon)

        label_evening = QLabel("🌙 Evening:")
        label_evening.setFont(font)
        layout.addWidget(label_evening)
        layout.addWidget(self.time_evening)

        self.start_button = QPushButton("✅ Start Scheduling")
        self.start_button.setFont(font)
        self.start_button.setStyleSheet("background-color: #a5d6a7; font-weight: bold;")
        self.start_button.clicked.connect(self.start_scheduling)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.check_times)
        self.timer.start(60000)  # every 60 seconds

    def set_light_palette(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#e0f7fa"))
        palette.setColor(QPalette.WindowText, QColor("#000000"))
        self.setPalette(palette)

    def load_times_from_db(self):
        try:
            conn = sqlite3.connect("pet_feeder.db")
            cursor = conn.cursor()
            cursor.execute("SELECT label, time FROM feeding_schedule")
            rows = cursor.fetchall()
            conn.close()

            times = {label: time for label, time in rows}
            if 'morning' in times:
                self.time_morning.setTime(QTime.fromString(times['morning'], "HH:mm"))
            if 'noon' in times:
                self.time_noon.setTime(QTime.fromString(times['noon'], "HH:mm"))
            if 'evening' in times:
                self.time_evening.setTime(QTime.fromString(times['evening'], "HH:mm"))
        except Exception as e:
            print(f"[⚠] Failed to load times: {e}")

    def start_scheduling(self):
        morning = self.time_morning.time().toString("HH:mm")
        noon = self.time_noon.time().toString("HH:mm")
        evening = self.time_evening.time().toString("HH:mm")

        # שמירה ל־DB
        try:
            conn = sqlite3.connect("pet_feeder.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM feeding_schedule")
            cursor.execute("INSERT INTO feeding_schedule (label, time) VALUES (?, ?)", ("morning", morning))
            cursor.execute("INSERT INTO feeding_schedule (label, time) VALUES (?, ?)", ("noon", noon))
            cursor.execute("INSERT INTO feeding_schedule (label, time) VALUES (?, ?)", ("evening", evening))
            conn.commit()
            conn.close()
            print("[✓] Feeding times saved to DB.")
        except Exception as e:
            print(f"[⚠] DB error: {e}")

        message = (
            "✅ Feeding times updated!\n\n"
            f"• Morning: {morning}\n"
            f"• Noon: {noon}\n"
            f"• Evening: {evening}\n\n"
            "The bowl will automatically fill at the selected times."
        )
        QMessageBox.information(self, "Schedule Set", message)

    def check_times(self):
        now = QTime.currentTime().toString("HH:mm")
        for time_edit in [self.time_morning, self.time_noon, self.time_evening]:
            if time_edit.time().toString("HH:mm") == now:
                print(f"[⏰] Feeding time triggered at {now}")
                # future: self.client.publish(...) אם תרצה לשלוח MQTT

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = FeedingSchedulerGUI()
    win.show()
    sys.exit(app.exec_())
