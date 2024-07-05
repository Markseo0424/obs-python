import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Queue Example")
        self.setGeometry(100, 100, 400, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)

        # Queue list widget
        self.queue_list = QListWidget()
        self.main_layout.addWidget(self.queue_list)

        # Add button to add items to the queue
        self.add_button = QPushButton("Add Item")
        self.add_button.clicked.connect(self.add_item)
        self.main_layout.addWidget(self.add_button)

        # Render button
        self.render_button = QPushButton("Render")
        self.render_button.clicked.connect(self.render_queue)
        self.main_layout.addWidget(self.render_button)

        # Remove button to remove selected items from the queue
        self.remove_button = QPushButton("Remove Selected Item")
        self.remove_button.clicked.connect(self.remove_selected_item)
        self.main_layout.addWidget(self.remove_button)

    def add_item(self):
        item_text = f"Item {self.queue_list.count() + 1}"
        list_item = QListWidgetItem(item_text)
        self.queue_list.addItem(list_item)

    def remove_selected_item(self):
        for item in self.queue_list.selectedItems():
            self.queue_list.takeItem(self.queue_list.row(item))

    def render_queue(self):
        queue_items = [self.queue_list.item(i).text() for i in range(self.queue_list.count())]
        print("Rendering queue:", queue_items)

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
