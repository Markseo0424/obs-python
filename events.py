import sys
import asyncio
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer

class AsyncTimer:
    def __init__(self, interval, callback):
        self.interval = interval
        self.callback = callback
        self.timer = QTimer()
        self.timer.setInterval(interval)
        self.timer.timeout.connect(self._handle_timeout)

    def start(self):
        self.timer.start()

    def stop(self):
        self.timer.stop()

    async def _handle_timeout(self):
        await self.callback()

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.async_timer = AsyncTimer(1000, self.update_label)

    def initUI(self):
        self.layout = QVBoxLayout()
        self.label = QLabel("Starting...", self)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.setWindowTitle('Async Timer Example')
        self.show()

    async def update_label(self):
        current_text = self.label.text()
        new_text = str(int(current_text.split()[-1]) + 1)
        self.label.setText(f"Updated: {new_text}")

    def start_timer(self):
        self.async_timer.start()

    def stop_timer(self):
        self.async_timer.stop()

def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.start_timer()

if __name__ == '__main__':
    main()
