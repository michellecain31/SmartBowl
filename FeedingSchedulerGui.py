import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QTimeEdit, QMessageBox, QSlider, QHBoxLayout
)
from PyQt5.QtCore import QTime, QTimer, Qt
from PyQt5.QtGui import QFont, QPalette, QColor

class FeedingSchedulerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🕒 Feeding Scheduler")
        self.resize(350, 420)
        self.set_light_palette()

        font = QFont("Arial", 11)
        layout = QVBoxLayout()

        title = QLabel("Set feeding times and amounts:")
        title.setFont(QFont("Arial", 13, QFont.Bold))
        layout.addWidget(title)

        # שדות לבוקר
        label_morning = QLabel("🌞 Morning:")
        label_morning.setFont(font)
        self.time_morning = QTimeEdit()
        self.slider_morning = self.create_slider()
        layout.addWidget(label_morning)
        layout.addWidget(self.time_morning)
        layout.addLayout(self.wrap_slider(self.slider_morning))

        # שדות לצהריים
        label_noon = QLabel("🌤️ Noon:")
        label_noon.setFont(font)
        self.time_noon = QTimeEdit()
        self.slider_noon = self.create_slider()
        layout.addWidget(label_noon)
        layout.addWidget(self.time_noon)
        layout.addLayout(self.wrap_slider(self.slider_noon))

        # שדות לערב
        label_evening = QLabel("🌙 Evening:")
        label_evening.setFont(font)
        self.time_evening = QTimeEdit()
        self.slider_evening = self.create_slider()
        layout.addWidget(label_evening)
        layout.addWidget(self.time_evening)
        layout.addLayout(self.wrap_slider(self.slider_evening))

        # כפתור התחלה
        self.start_button = QPushButton("✅ Start Scheduling")
        self.start_button.setFont(font)
        self.start_button.setStyleSheet("background-color: #a5d6a7; font-weight: bold;")
        self.start_button.clicked.connect(self.start_scheduling)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

        # טיימר לבדיקה
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_times)
        self.timer.start(60000)

        # טען נתונים קיימים
        self.load_times_from_db()

    def set_light_palette(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#e0f7fa"))
        self.setPalette(palette)

    def create_slider(self):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(10, 100)
        slider.setTickInterval(10)
        slider.setValue(30)
        slider.setStyleSheet("background-color: #b2dfdb;")
        return slider

    def wrap_slider(self, slider):
        layout = QHBoxLayout()
        label = QLabel("Amount: ")
        percent = QLabel()
        percent.setFixedWidth(40)

        def update_label(val):
            percent.setText(f"{val}%")

        slider.valueChanged.connect(update_label)
        update_label(slider.value())

        layout.addWidget(label)
        layout.addWidget(slider)
        layout.addWidget(percent)
        return layout

    def load_times_from_db(self):
        try:
            conn = sqlite3.connect("pet_feeder.db")
            cursor = conn.cursor()
            cursor.execute("SELECT label, time, amount FROM feeding_schedule")
            rows = cursor.fetchall()
            conn.close()

            for label, time, amount in rows:
                if label == 'morning':
                    self.time_morning.setTime(QTime.fromString(time, "HH:mm"))
                    self.slider_morning.setValue(amount)
                elif label == 'noon':
                    self.time_noon.setTime(QTime.fromString(time, "HH:mm"))
                    self.slider_noon.setValue(amount)
                elif label == 'evening':
                    self.time_evening.setTime(QTime.fromString(time, "HH:mm"))
                    self.slider_evening.setValue(amount)
        except Exception as e:
            print(f"[⚠] Failed to load times: {e}")

    def start_scheduling(self):
        morning = self.time_morning.time().toString("HH:mm")
        noon = self.time_noon.time().toString("HH:mm")
        evening = self.time_evening.time().toString("HH:mm")

        am_morning = self.slider_morning.value()
        am_noon = self.slider_noon.value()
        am_evening = self.slider_evening.value()

        try:
            conn = sqlite3.connect("pet_feeder.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM feeding_schedule")
            cursor.execute("INSERT INTO feeding_schedule (label, time, amount) VALUES (?, ?, ?)", ("morning", morning, am_morning))
            cursor.execute("INSERT INTO feeding_schedule (label, time, amount) VALUES (?, ?, ?)", ("noon", noon, am_noon))
            cursor.execute("INSERT INTO feeding_schedule (label, time, amount) VALUES (?, ?, ?)", ("evening", evening, am_evening))
            conn.commit()
            conn.close()
            print("[✓] Feeding times and amounts saved.")
        except Exception as e:
            print(f"[⚠] DB error: {e}")

        message = (
            "✅ Feeding schedule updated!\n\n"
            f"• Morning: {morning} - {am_morning}%\n"
            f"• Noon: {noon} - {am_noon}%\n"
            f"• Evening: {evening} - {am_evening}%\n\n"
            "Schedule saved successfully."
        )
        QMessageBox.information(self, "Schedule Set", message)

    def check_times(self):
        now = QTime.currentTime().toString("HH:mm")
        schedule = {
            self.time_morning.time().toString("HH:mm"): self.slider_morning.value(),
            self.time_noon.time().toString("HH:mm"): self.slider_noon.value(),
            self.time_evening.time().toString("HH:mm"): self.slider_evening.value(),
        }
        if now in schedule:
            amount = schedule[now]
            print(f"[⏰] Feeding time at {now}: {amount}%")
            # future: publish via MQTT if needed

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = FeedingSchedulerGUI()
    win.show()
    sys.exit(app.exec_())
