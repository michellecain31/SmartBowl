import sys
import sqlite3
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox
)
from PyQt5.QtGui import QFont, QPalette, QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class FeedingStatsGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📊 Feeding Statistics")
        self.resize(800, 600)
        self.set_light_palette()

        self.graph_windows = []  # ⬅️ כדי לשמור רפרנסים לגרפים הפתוחים

        layout = QVBoxLayout()

        self.show_graphs_btn = QPushButton("📈 Show Stats")
        self.show_graphs_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.show_graphs_btn.clicked.connect(self.display_graphs)

        layout.addWidget(self.show_graphs_btn)

        self.setLayout(layout)

    def set_light_palette(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#f1f8e9"))
        self.setPalette(palette)

    def display_graphs(self):
        try:
            conn = sqlite3.connect("pet_feeder.db")
            query = "SELECT timestamp, bowl_level FROM feed_log"
            df = pd.read_sql_query(query, conn)
            conn.close()

            if df.empty:
                QMessageBox.information(self, "No Data", "No feeding data found.")
                return

            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['date'] = df['timestamp'].dt.date

            daily_stats = df.groupby('date').agg({
                'bowl_level': ['count', 'sum']
            }).reset_index()
            daily_stats.columns = ['Date', 'Feedings', 'Total_Bowl_Fill']

            # Clear previous figures
            plt.close('all')

            # Graph 1: Number of feedings per day
            fig1, ax1 = plt.subplots()
            ax1.bar(daily_stats['Date'], daily_stats['Feedings'], color='cornflowerblue')
            ax1.set_title("Number of Feedings per Day")
            ax1.set_xlabel("Date")
            ax1.set_ylabel("Feedings")
            fig1.autofmt_xdate()
            self.show_plot(fig1)

            # Graph 2: Total Bowl Fill per day
            fig2, ax2 = plt.subplots()
            ax2.bar(daily_stats['Date'], daily_stats['Total_Bowl_Fill'], color='mediumseagreen')
            ax2.set_title("Total Bowl Fill per Day (%)")
            ax2.set_xlabel("Date")
            ax2.set_ylabel("Total Bowl Fill (%)")
            fig2.autofmt_xdate()
            self.show_plot(fig2)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred:\n{e}")

    def show_plot(self, fig):
        canvas = FigureCanvas(fig)
        plot_window = QWidget()
        self.graph_windows.append(plot_window)  # ⬅️ שמירת רפרנס כדי שהחלון לא ייסגר

        plot_window.setWindowTitle("📊 Graph")
        layout = QVBoxLayout()
        layout.addWidget(canvas)
        plot_window.setLayout(layout)
        plot_window.resize(640, 480)
        plot_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = FeedingStatsGUI()
    win.show()
    sys.exit(app.exec_())
