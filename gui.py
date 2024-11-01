import os
import sys
import asyncio
import json
import subprocess
from PyQt5.QtGui import QIcon, QFont, QTextCursor
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QLabel, QTextEdit, QVBoxLayout, QHBoxLayout, \
    QDialog, QMainWindow, QCheckBox, QListWidgetItem, QListWidget, QLineEdit, QScrollArea
from PyQt5.QtCore import QCoreApplication, QRect, Qt, QTimer
from obsfunctions import *
import time
from teamscreen import TeamScreen

after_effects_path = r"C:\Program Files\Adobe\Adobe After Effects 2024\Support Files\AfterFX.exe"

# Path to the ExtendScript file
script_path = r".\render.jsx"

# Path to the After Effects project file
project_path = r"C:\Users\marks\OneDrive\Documents\SNU\동아리\SUB\SUB Sports\SUB SPORTS TEMPLATE\SUBsports_v2.aep"

csv_path = r"C:\Users\marks\OneDrive\Documents\SNU\동아리\SUB\SUB Sports\SUB SPORTS TEMPLATE\team_info_converted.csv"

comp_names = ["start_screen"]

output_paths = [r"C:\Users\marks\OneDrive\Desktop\start_screen.mov"]

script_path = os.path.abspath(script_path)
print(script_path)

# Command to open the After Effects project
open_project_command = [after_effects_path, "-project", project_path]

# Open the project
subprocess.Popen(open_project_command)

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

    def _handle_timeout(self):
        self.callback()

class NumberOnlyTextEdit(QTextEdit):
    permitted = [Qt.Key_Right, Qt.Key_Left, Qt.Key_Backspace]

    def __init__(self, *args, parent=None, max_length=3, **kwargs):
        super().__init__(*args, parent, **kwargs)
        self.max_length = max_length

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Ignore Enter key
            return
        elif event.text().isdigit() or event.key() in self.permitted:
            # Accept only digits and Backspace
            if len(super().toPlainText()) >= self.max_length and event.text().isdigit():
                return

            super().keyPressEvent(event)

        else:
            # Ignore all other keys
            return


class SettingsWindow(QDialog):
    def portChanged(self):
        global port
        port = int(self.port.toPlainText())

    def passwordChanged(self):
        global password
        password = self.password.toPlainText()

    def connect(self):
        global ws, connection

        print("connect")
        try:
            ws = obsws(host, port, password)  # , legacy=True)
            ws.connect()
            connection = True

        except obswebsocket.exceptions.ConnectionFailure:
            ws = None
            connection = False

        self.connectStatus.setText("status - Not connected" if not connection else "status - Connected")

    def renderSettingChanged(self):
        global project_path, after_effects_path, comp_names, output_paths

        after_effects_path = self.aePath.toPlainText()
        project_path = self.aepPath.toPlainText()
        comp_names = self.compName.toPlainText().split("\n")
        output_paths = self.outputPath.toPlainText().split("\n")

    def closeSetting(self):

        # Command to open the After Effects project
        open_project_command = [after_effects_path, "-project", project_path]

        # Open the project
        subprocess.Popen(open_project_command)

        self.saveAll()
        self.close()

    def csvPathChange(self):
        global csv_path
        csv_path = self.csvPath.toPlainText()

    def saveAll(self):
        setting = {}
        setting['port'] = self.port.toPlainText()
        setting['password'] = self.password.toPlainText()
        setting['aePath'] = self.aePath.toPlainText()
        setting['aepPath'] = self.aepPath.toPlainText()
        setting['compName'] = self.compName.toPlainText()
        setting['outputPath'] = self.outputPath.toPlainText()
        setting['csvPath'] = self.csvPath.toPlainText()
        with open("./setting.json", 'w') as f:
            json.dump(setting, f, indent=4)

    def loadAll(self):
        try:
            with open("./setting.json", 'r') as f:
                setting = json.load(f)
                self.port.setPlainText(setting['port'])
                self.password.setPlainText(setting['password'])
                self.aePath.setPlainText(setting['aePath'])
                self.aepPath.setPlainText(setting['aepPath'])
                self.compName.setPlainText(setting['compName'])
                self.outputPath.setPlainText(setting['outputPath'])
                self.csvPath.setPlainText(setting['csvPath'])

        except FileNotFoundError:
            return

    def __init__(self):
        global ws, connection, host, port, password

        super().__init__()
        self.setWindowTitle("Settings")
        self.setGeometry(300, 300, 500, 800)

        portLabel = QLabel("port number (ex:4455)")
        self.port = NumberOnlyTextEdit(str(port), max_length=6)
        passwordLabel = QLabel("connection password")
        self.password = QTextEdit(password)
        self.connectButton = QPushButton("Connect")
        self.connectStatus = QLabel("status - Not connected" if not connection else "status - Connected")

        aePathLabel = QLabel("after effects exe path")
        self.aePath = QTextEdit(after_effects_path)
        aepPathLabel = QLabel("after effects project file path")
        self.aepPath = QTextEdit(project_path)
        compNameLabel = QLabel("comp names")
        self.compName = QTextEdit("\n".join(comp_names))
        outputPathLabel = QLabel("output paths")
        self.outputPath = QTextEdit("\n".join(output_paths))

        self.aePath.textChanged.connect(self.renderSettingChanged)
        self.aepPath.textChanged.connect(self.renderSettingChanged)
        self.compName.textChanged.connect(self.renderSettingChanged)
        self.outputPath.textChanged.connect(self.renderSettingChanged)

        self.exitButton = QPushButton("Close")

        self.port.textChanged.connect(self.portChanged)
        self.password.textChanged.connect(self.passwordChanged)
        self.connectButton.clicked.connect(self.connect)
        self.exitButton.clicked.connect(self.closeSetting)

        self.aePath.setFixedHeight(50)
        self.aepPath.setFixedHeight(50)

        csvPathLabel = QLabel("csv file path")
        self.csvPath = QTextEdit(csv_path)
        self.csvPath.textChanged.connect(self.csvPathChange)

        vbox = QVBoxLayout()
        vbox.setContentsMargins(20, 20, 20, 20)

        vbox.addWidget(portLabel)
        vbox.addWidget(self.port)
        vbox.addWidget(passwordLabel)
        vbox.addWidget(self.password)
        vbox.addWidget(self.connectButton)
        vbox.addWidget(self.connectStatus)
        vbox.addWidget(aePathLabel)
        vbox.addWidget(self.aePath)
        vbox.addWidget(aepPathLabel)
        vbox.addWidget(self.aepPath)
        vbox.addWidget(compNameLabel)
        vbox.addWidget(self.compName)
        vbox.addWidget(outputPathLabel)
        vbox.addWidget(self.outputPath)
        vbox.addWidget(csvPathLabel)
        vbox.addWidget(self.csvPath)
        vbox.addWidget(self.exitButton)

        self.setLayout(vbox)

        self.loadAll()

class TimeTextEdit(NumberOnlyTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, max_length=5, **kwargs)

    def keyPressEvent(self, event):
        onColon = self.toPlainText()[self.textCursor().position() - 1] == ":" if len(self.toPlainText()) else False

        super().keyPressEvent(event)

        if len(super().toPlainText()) == 2:
            if event.key() == Qt.Key_Backspace:
                if onColon:
                    super().keyPressEvent(event)
            else:
                if ":" not in self.toPlainText():
                    self.insertPlainText(":")


class SourceSwitchScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Source Switch")
        self.setGeometry(100, 100, 800, 600)

        self.main_layout = QVBoxLayout(self)

        # Add button
        self.add_button = QPushButton("+")
        self.add_button.clicked.connect(self.add_element)
        self.main_layout.addWidget(self.add_button)

        # Scroll area for the elements
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_widget = QWidget()
        self.scroll_area_layout = QVBoxLayout(self.scroll_area_widget)
        self.scroll_area_layout.setAlignment(Qt.AlignTop)
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.main_layout.addWidget(self.scroll_area)

        # Labels for each column
        labels_layout = QHBoxLayout()
        labels_layout.addWidget(QLabel("Delete", self))
        labels_layout.addWidget(QLabel("Path", self))
        labels_layout.addWidget(QLabel("OBS Source Name", self))
        labels_layout.addWidget(QLabel("Replace Source", self))
        self.main_layout.insertLayout(1, labels_layout)

        self.elements = []
        self.textEdits = []

        self.loadAll()

    def loadAll(self):
        try:
            with open("sourceReplaceList.json", "r") as f:
                lst = json.load(f)
        except FileNotFoundError:
            return

        for elem in lst:
            self.add_element(path=elem['path'], sourceName=elem['source'], save=False)

    def saveAll(self):
        lst = []
        for pathEdit, sourceEdit in self.textEdits:
            lst.append({"path": pathEdit.text(),
                        "source": sourceEdit.text()})

        with open("sourceReplaceList.json", "w") as f:
            json.dump(lst, f, indent=4)

    def add_element(self, checked=False, path=None, sourceName=None, save=True):
        element_layout = QHBoxLayout()

        delete_button = QPushButton("x")
        delete_button.setFixedWidth(30)
        delete_button.clicked.connect(lambda: self.remove_element(element_layout))
        element_layout.addWidget(delete_button)

        if path is not None:
            path_edit = QLineEdit(path)
        else:
            path_edit = QLineEdit()

        path_edit.setPlaceholderText("Path")
        path_edit.textChanged.connect(self.saveAll)
        element_layout.addWidget(path_edit)

        if sourceName is not None:
            source_name_edit = QLineEdit(sourceName)
        else:
            source_name_edit = QLineEdit()

        source_name_edit.setPlaceholderText("OBS Source Name")
        source_name_edit.textChanged.connect(self.saveAll)
        element_layout.addWidget(source_name_edit)

        replace_button = QPushButton("Replace Source")
        replace_button.clicked.connect(lambda: self.replaceSource(path_edit.text(), source_name_edit.text()))
        element_layout.addWidget(replace_button)

        self.scroll_area_layout.addLayout(element_layout)
        self.elements.append(element_layout)

        self.textEdits.append((path_edit, source_name_edit))

        if save:
            self.saveAll()

    def remove_element(self, element_layout, save=True):
        for i in reversed(range(element_layout.count())):
            widget = element_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        self.scroll_area_layout.removeItem(element_layout)
        elem = self.textEdits[self.elements.index(element_layout)]
        self.elements.remove(element_layout)
        self.textEdits.remove(elem)

        if save:
            self.saveAll()

    def replaceSource(self, path, target):
        setInputSettings(target, {'local_file': path}, ws)


class RenderScreen(QWidget):
    def __init__(self, mainScreen):
        super().__init__()
        self.setWindowTitle("Render Footage")
        self.widgets = []
        self.mainScreen = mainScreen

        self.refreshButton = QPushButton("refresh")
        self.refreshButton.setFixedSize(200, 50)
        self.refreshButton.clicked.connect(self.refresh)
        container = QWidget(self)
        container.setContentsMargins(0, 0, 0, 0)
        container.setFixedSize(220,70)
        container.move(0,0)
        hbox = QHBoxLayout(container)
        hbox.addWidget(self.refreshButton)

        renderButtonLabel = QLabel("to render queue")
        renderButtonLabel.move(70,30)

        obsSourceLabel = QLabel("obs source label")
        obsSourceLabel.move(70,150)

        container = QWidget(self)
        container.setContentsMargins(0, 0, 0, 0)
        container.setFixedSize(800, 50)
        container.move(0, 55)
        hbox = QHBoxLayout(container)
        hbox.addWidget(renderButtonLabel)
        hbox.addWidget(obsSourceLabel)

        self.renderQueue = []

        self.refresh()

    def remove_hbox(self, hbox):
        # Remove all widgets from the hbox
        while hbox.count():
            item = hbox.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                hbox.removeItem(item)

    def renderFootage(self, index, check, target):
        checked = check.isChecked()
        target_text = target.toPlainText()

        item = self.add_item(comp_names[index])
        self.renderQueue.append((index, checked, target_text, item))

    def initUI(self):
        self.setFixedSize(800, 120 * len(comp_names) + 290)

        container = QWidget(self)
        container.setContentsMargins(0, 0, 0, 0)
        container.setFixedSize(800,120 * len(comp_names) + 200)
        container.move(0,70)
        vbox = QVBoxLayout(container)

        for i, comp in enumerate(comp_names):
            container = QWidget(self)
            container.setContentsMargins(0, 0, 0, 0)
            container.setFixedSize(800,100)
            hbox = QHBoxLayout(container)

            btn = QPushButton(comp)
            btn.setFixedSize(200,60)

            check = QCheckBox("replace footage")

            target = QTextEdit("start_screen")
            target.setPlaceholderText("write OBS source name")

            btn.clicked.connect(lambda checked, index=i, c=check, t=target: self.renderFootage(index, c, t))

            hbox.addWidget(btn)
            hbox.addWidget(check)
            hbox.addWidget(target)

            vbox.addWidget(container)


        self.render_queue_label = QLabel("Render Queue")

        # Queue list widget
        self.queue_list = QListWidget()

        # Render button
        self.render_button = QPushButton("Render")
        self.render_button.clicked.connect(self.render_queue)

        # Remove button to remove selected items from the queue
        self.remove_button = QPushButton("Remove Selected Item")
        self.remove_button.clicked.connect(self.remove_selected_item)

        vbox.addWidget(self.render_queue_label)
        vbox.addWidget(self.queue_list)
        vbox.addWidget(self.render_button)
        vbox.addWidget(self.remove_button)

        self.widgets.append(vbox)


    def add_item(self, item_text):
        list_item = QListWidgetItem(item_text)
        self.queue_list.addItem(list_item)
        return list_item

    def remove_selected_item(self):
        for item in self.queue_list.selectedItems():
            for queue in self.renderQueue:
                if queue[3] == item:
                    self.renderQueue.remove(queue)

            self.queue_list.takeItem(self.queue_list.row(item))
        print(self.renderQueue)

    def render_queue(self,  idx=0):
        queue_items = [self.queue_list.item(i).text() for i in range(self.queue_list.count())]

        print("Rendering queue:", queue_items)

        item = self.queue_list.item(idx)
        self.queue_list.setDisabled(True)
        self.render_button.setDisabled(True)
        self.remove_button.setDisabled(True)
        for queue in self.renderQueue:
            if queue[3] == item:
                self.mainScreen.renderAEP(*queue[:3], [self.checkQueue])

    def checkQueue(self):
        print('check queue')
        self.queue_list.item(0).setSelected(True)
        self.remove_selected_item()
        if self.queue_list.count():
            self.render_queue()
        else:
            self.queue_list.setDisabled(False)
            self.render_button.setDisabled(False)
            self.remove_button.setDisabled(False)

    def refresh(self):
        self.close()
        for widget in self.widgets:
            self.remove_hbox(widget)
            widget.deleteLater()
        self.widgets.clear()
        self.initUI()
        self.show()

class ChangeSceneScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Change Scene")
        self.widgets = []

        self.refreshButton = QPushButton("refresh")
        self.refreshButton.setFixedSize(200, 50)
        self.refreshButton.clicked.connect(self.refresh)
        container = QWidget(self)
        container.setContentsMargins(0, 0, 0, 0)
        container.setFixedSize(220,70)
        container.move(0,0)
        hbox = QHBoxLayout(container)
        hbox.addWidget(self.refreshButton)

        # time.sleep(5)
        # self.main_layout = QVBoxLayout()
        self.refresh()

    def remove_hbox(self, hbox):
        # Remove all widgets from the hbox
        while hbox.count():
            item = hbox.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                hbox.removeItem(item)

    def initUI(self):

        sceneList = [scene['sceneName'] for scene in getSceneLists(ws).datain['scenes']]
        buttons = []

        for scene in sceneList:
            buttons.append(QPushButton(scene, self))
            buttons[-1].clicked.connect(lambda checked, s=scene: self.sceneChange(s))
            buttons[-1].setFixedSize(200, 100)

        rowCount = len(sceneList) // 4 + 1

        for i in range(rowCount):
            items = buttons[i * 4: i * 4 + 4]

            container = QWidget(self)
            container.setContentsMargins(0, 0, 0, 0)
            container.setFixedSize(len(items) * 220 if i == 0 else 880, 120)
            container.move(0, 70 + i * 120)

            hbox = QHBoxLayout(container)
            hbox.setAlignment(Qt.AlignLeft)
            for item in items:
                hbox.addWidget(item)

            # self.main_layout.addWidget(hbox)
            self.widgets.append(hbox)

        self.setFixedSize(len(items) * 220 if i == 0 else 880, 100 * rowCount + 90)

    def refresh(self):
        self.close()
        for widget in self.widgets:
            self.remove_hbox(widget)
            widget.deleteLater()
        self.widgets.clear()
        self.initUI()
        self.show()

    def sceneChange(self, sceneName):
        changeScene(sceneName, ws)

class ScoreboardApp(QMainWindow):
    def __init__(self, appName="Demo"):
        super().__init__()
        self.display_size = None
        self.screen_size = None

        self.score_a = 0
        self.score_b = 0

        self.app_name = appName
        self.initUI()

        self.start_time = 0
        self.time_interval = 0
        self.time_amount = 0

        self.renderCheckTimer = None
        self.renderEndCallback = []

        settingScreen = SettingsWindow()
        settingScreen.show()
        settingScreen.closeSetting()

        self.changeSceneScreen = ChangeSceneScreen()
        self.changeSceneScreen.show()

        self.renderScreen = RenderScreen(self)
        self.renderScreen.show()

        self.sourceSwitchScreen = SourceSwitchScreen()
        self.sourceSwitchScreen.show()

        self.teamScreen = None # TeamScreen(csv_path, 0)
        # self.teamScreen.show()


    def keyPressEvent(self, a0):
        if a0.key() == Qt.Key_A:
            self.changeSceneScreen.show()
            self.renderScreen.show()
            self.sourceSwitchScreen.show()

    def timerStart(self):
        # print("timer Start!")
        self.playbutton.setDisabled(True)
        self.pausebutton.setDisabled(False)
        self.stopbutton.setDisabled(False)
        self.start_time = time.time() + self.time_interval
        if not self.time_interval: self.time_amount = self.getTime()
        self.async_timer.start()

    def timerStop(self):
        # print("timer Stop!")
        self.playbutton.setDisabled(False)
        self.pausebutton.setDisabled(True)
        self.stopbutton.setDisabled(True)
        self.async_timer.stop()
        self.time_interval = 0
        self.setTime(self.time_amount)

    def timerPause(self):
        # print("timer Pause!")
        self.playbutton.setDisabled(False)
        self.pausebutton.setDisabled(True)
        self.stopbutton.setDisabled(False)
        self.async_timer.stop()
        self.time_interval = self.start_time - time.time()

    def timerCheck(self):
        self.setTime(self.time_amount - time.time() + self.start_time)
        # print("timer Check!")
        setInputSettings("time", {'text': self.timeText.toPlainText()}, ws)

    def setTime(self, seconds):
        seconds = int(min(max(0, seconds), 99*60 + 99))
        align = self.timeText.alignment()
        minute = seconds // 60
        second = seconds % 60
        self.timeText.setPlainText(f"{str(minute).zfill(2)}:{str(second).zfill(2)}")
        self.timeText.setAlignment(align)

    def getTime(self):
        txt = self.timeText.toPlainText()
        txt = txt.split(":")
        minute = int(txt[0]) if txt[0] else 0
        second = int(txt[1]) if txt[1] else 0
        return minute * 60 + second

    def timerUI(self):
        self.async_timer = AsyncTimer(100, self.timerCheck)

        container = QWidget(self)
        container.setContentsMargins(0, 0, 0, 0)
        container.setFixedSize(500, 50)
        container.move(self.screen_size[0]//2 - 250, 30)

        self.timeText = TimeTextEdit("00:00")

        self.timeText.setAcceptRichText(False)
        self.timeText.setFont(QFont('SansSerif', 10))
        self.timeText.setAlignment(Qt.AlignCenter)
        self.timeText.resize(200, 200)

        self.playbutton = QPushButton('play', self)
        self.pausebutton = QPushButton('pause', self)
        self.stopbutton = QPushButton('stop', self)

        self.playbutton.clicked.connect(self.timerStart)
        self.pausebutton.clicked.connect(self.timerPause)
        self.stopbutton.clicked.connect(self.timerStop)

        self.playbutton.setDisabled(False)
        self.pausebutton.setDisabled(True)
        self.stopbutton.setDisabled(True)

        hbox = QHBoxLayout(container)
        hbox.setContentsMargins(0, 0, 0, 0)

        hbox.addWidget(self.timeText)
        hbox.addWidget(self.playbutton)
        hbox.addWidget(self.pausebutton)
        hbox.addWidget(self.stopbutton)

    def scoreUpA(self):
        if self.score_a < 999: self.score_a += 1
        self.updateScore()

    def scoreDownA(self):
        if self.score_a > 0: self.score_a -= 1
        self.updateScore()

    def scoreUpB(self):
        if self.score_b < 999: self.score_b += 1
        self.updateScore()

    def scoreDownB(self):
        if self.score_b > 0: self.score_b -= 1
        self.updateScore()

    def updateScore(self):
        self.a_score.textChanged.disconnect(self.writeScore)
        self.b_score.textChanged.disconnect(self.writeScore)

        self.a_score.setPlainText(str(self.score_a))
        self.a_score.setAlignment(Qt.AlignCenter)
        self.b_score.setPlainText(str(self.score_b))
        self.b_score.setAlignment(Qt.AlignCenter)

        self.b_score.textChanged.connect(self.writeScore)
        self.a_score.textChanged.connect(self.writeScore)
        self.scoreUpdate()

    def writeScore(self):
        self.score_a = int(self.a_score.toPlainText()) if self.a_score.toPlainText() else 0
        self.score_b = int(self.b_score.toPlainText()) if self.b_score.toPlainText() else 0
        self.scoreUpdate()

    def scoreUpdate(self):
        print(f"score update: {self.score_a} : {self.score_b}")
        setInputSettings('score', {'text': f"{self.score_a} : {self.score_b}"}, ws)

    def scoreUI(self):
        # scores
        container = QWidget(self)
        container.setContentsMargins(0, 0, 0, 0)
        container.setFixedSize(500, 130)
        container.move(self.screen_size[0]//2 - 250, 100)

        self.a_score = NumberOnlyTextEdit("0")
        self.b_score = NumberOnlyTextEdit("0")

        self.a_score.setAcceptRichText(False)
        self.a_score.setFont(QFont('SansSerif', 50))
        self.a_score.setAlignment(Qt.AlignCenter)
        self.a_score.resize(200, 200)
        self.a_score.textChanged.connect(self.writeScore)

        self.b_score.setAcceptRichText(False)
        self.b_score.setFont(QFont('SansSerif', 50))
        self.b_score.setAlignment(Qt.AlignCenter)
        self.b_score.resize(200, 200)
        self.b_score.textChanged.connect(self.writeScore)

        hbox = QHBoxLayout(container)
        hbox.setContentsMargins(0, 0, 0, 0)

        hbox.addWidget(self.a_score)
        hbox.addWidget(self.b_score)

        # up buttons
        container = QWidget(self)
        container.setContentsMargins(0, 0, 0, 0)
        container.setFixedSize(500, 100)
        container.move(self.screen_size[0]//2 - 250, 250)

        self.a_up = QPushButton('Up', self)
        self.b_up = QPushButton('Up', self)

        self.a_up.setFixedHeight(100)
        self.a_up.setFont(QFont('SansSerif', 20))
        self.a_up.clicked.connect(self.scoreUpA)
        self.b_up.setFixedHeight(100)
        self.b_up.setFont(QFont('SansSerif', 20))
        self.b_up.clicked.connect(self.scoreUpB)

        hbox = QHBoxLayout(container)
        hbox.setContentsMargins(0, 0, 0, 0)

        hbox.addWidget(self.a_up)
        hbox.addWidget(self.b_up)

        # down buttons
        container = QWidget(self)
        container.setContentsMargins(0, 0, 0, 0)
        container.setFixedSize(500, 100)
        container.move(self.screen_size[0]//2 - 250, 350)

        self.a_down = QPushButton('Down', self)
        self.b_down = QPushButton('Down', self)

        self.a_down.setFixedHeight(100)
        self.a_down.setFont(QFont('SansSerif', 20))
        self.a_down.clicked.connect(self.scoreDownA)
        self.b_down.setFixedHeight(100)
        self.b_down.setFont(QFont('SansSerif', 20))
        self.b_down.clicked.connect(self.scoreDownB)

        hbox = QHBoxLayout(container)
        hbox.setContentsMargins(0, 0, 0, 0)

        hbox.addWidget(self.a_down)
        hbox.addWidget(self.b_down)

    def checkRenderStatus(self):
        #print("check render")
        try:
            with open("./renderStatus.json", "r") as f:
                jsonFile = json.load(f)
                if jsonFile["status"]:
                    self.breakCallbackFlag = False
                    self.renderCheckTimer.stop()
                    print("render done!")
                    print("conflict check : ", self.conflictCheck)
                    print(self.renderEndCallback)
                    for callback in self.renderEndCallback:
                        if self.breakCallbackFlag:
                            break
                        print('execute ', callback)
                        callback()

        except FileNotFoundError:
            print("renderStatus.json not found")

    def replaceSource(self, target):
        setInputSettings(target, {'local_file': self.conflictCheck[1]}, ws)

    def renderAEP(self, index=0, replace=True, target="start_screen", endCallback=None):
        self.renderEndCallback.clear()

        global output_paths
        # Command to run the script
        run_script_command = [after_effects_path, "-r", script_path]

        # Execute the script
        # prog = subprocess.Popen(run_script_command, stdin=subprocess.PIPE)
        # prog.stdin.write(str.encode('0109'))
        # prog.communicate()

        comp_name = comp_names[index]
        output_path = output_paths[index]
        m_output_path = output_paths[index]

        conflict = True
        increment = 0

        while conflict:
            # Check if the file exists
            if os.path.exists(output_path):
                conflict = True
                print(f"File exists: {output_path}")
                try:
                    os.remove(output_path)
                    print(f"Successfully deleted the file: {output_path}")
                    conflict = False
                    break
                except PermissionError:
                    print(f"Permission denied: Unable to delete the file {output_path}")
                except FileNotFoundError:
                    print(f"File not found: {output_path} (already deleted)")
                except Exception as e:
                    print(f"Error deleting file: {e}")

                increment += 1
                output_path = m_output_path.split(".")[0] + f"_{increment}." + m_output_path.split(".")[1]
            else:
                conflict = False
                print(f"File does not exist: {output_path}")

        with open('./render.json', 'w') as file:
            json.dump({
                "compName": comp_name,
                "filePath": output_path,
                "renderTemplate": "High Quality with Alpha",
                "replaceExist": True
            }, file, indent=4)

        subprocess.run(run_script_command)
        self.renderCheckTimer = AsyncTimer(5000, self.checkRenderStatus)
        self.renderCheckTimer.start()
        self.conflictCheck = (increment > 0, output_path)

        if replace:
            self.renderEndCallback.append(lambda t=target: self.replaceSource(t))

        if endCallback != None:
            self.renderEndCallback += endCallback

        self.renderEndCallback.append(self.renderEndCallback.clear)
        print('start render ', comp_name)
        print(self.renderEndCallback)
        self.breakCallbackFlag = True

    def initUI(self):
        # self.lbl1 = QLabel('Enter your sentence:')
        # self.te = QTextEdit()
        # self.te.setAcceptRichText(False)
        # self.lbl2 = QLabel('The number of words is 0')
        #
        # self.te.textChanged.connect(self.text_changed)
        self.setWindowTitle(self.app_name)
        self.setWindowIcon(QIcon('assets/icon/sub_logo.png'))

        self.display_size = self.screen().geometry().width(), self.screen().geometry().height()
        self.screen_size = 800, int(self.display_size[1] / 2)

        self.move(int((self.display_size[0] - self.screen_size[0]) / 2), int((self.display_size[1] - self.screen_size[1]) / 2))
        self.setFixedSize(*self.screen_size)

        btn = QPushButton('Quit', self)
        btn.move(self.screen_size[0] // 2 - 250, self.screen_size[1] - 80)
        btn.resize(500, 50)
        btn.clicked.connect(QCoreApplication.instance().quit)

        QToolTip.setFont(QFont('SansSerif', 10))

        btn.setToolTip('This is a <b>QPushButton</b> widget')

        # Settings button
        settings_button = QPushButton("Settings", self)
        settings_button.clicked.connect(self.open_settings)
        settings_button.move(self.screen_size[0] // 2 - 250, self.screen_size[1] - 140)
        settings_button.resize(500, 50)

        # Settings button
        settings_button = QPushButton("Sync", self)
        settings_button.clicked.connect(self.sync)
        settings_button.move(self.screen_size[0] // 2 - 250, self.screen_size[1] - 200)
        settings_button.resize(500, 50)

        # Render button
        settings_button = QPushButton("Render", self)
        settings_button.clicked.connect(self.renderAEP)
        settings_button.move(self.screen_size[0] // 2 - 250, self.screen_size[1] - 260)
        settings_button.resize(500, 50)


        # team setting buttons
        container = QWidget(self)
        container.setContentsMargins(0, 0, 0, 0)
        container.setFixedSize(500, 60)
        container.move(self.screen_size[0]//2 - 250, 450)

        self.a_setting = QPushButton('A Team Setting', self)
        self.b_setting = QPushButton('B Team Setting', self)

        self.a_setting.setFixedHeight(60)
        self.a_setting.setFont(QFont('SansSerif', 15))
        self.a_setting.clicked.connect(self.openASetting)
        self.b_setting.setFixedHeight(60)
        self.b_setting.setFont(QFont('SansSerif', 15))
        self.b_setting.clicked.connect(self.openBSetting)

        hbox = QHBoxLayout(container)
        hbox.setContentsMargins(0, 0, 0, 0)

        hbox.addWidget(self.a_setting)
        hbox.addWidget(self.b_setting)

        self.scoreUI()
        self.timerUI()

        self.show()

    def openASetting(self):
        teamscreen_a = TeamScreen(csv_path, 0)
        teamscreen_a.show()

    def openBSetting(self):
        teamscreen_b = TeamScreen(csv_path, 1)
        teamscreen_b.show()

    def sync(self):
        self.scoreUpdate()
        setInputSettings("time", {'text': self.timeText.toPlainText()}, ws)

    def open_settings(self):
        self.settings_window = SettingsWindow()
        self.settings_window.exec_()

    def text_changed(self):
        text = self.te.toPlainText()
        self.lbl2.setText('The number of words is ' + str(len(text.split())))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ScoreboardApp("SUB Sports Scoreboard")

    sys.exit(app.exec_())

