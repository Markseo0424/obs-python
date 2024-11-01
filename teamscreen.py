import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, \
    QPushButton, QFormLayout, QGridLayout
from PyQt5.QtCore import Qt
import pandas as pd
import numpy as np

mapping = {
    "stadium": (0, 0),
    "round": (0, 1),
    "teamname_a": (2, 1),
    "formation_a": (3, 1),
    "a_00_num": (3, 2),
    "a_00_name": (3, 3),
    "a_00_major": (3, 4),
    "a_10_num": (3, 5),
    "a_10_name": (3, 6),
    "a_10_major": (3, 7),
    "a_20_num": (3, 8),
    "a_20_name": (3, 9),
    "a_20_major": (3, 10),
    "a_30_num": (3, 11),
    "a_30_name": (3, 12),
    "a_30_major": (3, 13),
    "a_40_num": (3, 14),
    "a_40_name": (3, 15),
    "a_40_major": (3, 16),
    "a_11_num": (4, 5),
    "a_11_name": (4, 6),
    "a_11_major": (4, 7),
    "a_21_num": (4, 8),
    "a_21_name": (4, 9),
    "a_21_major": (4, 10),
    "a_31_num": (4, 11),
    "a_31_name": (4, 12),
    "a_31_major": (4, 13),
    "a_41_num": (4, 14),
    "a_41_name": (4, 15),
    "a_41_major": (4, 16),
    "a_12_num": (5, 5),
    "a_12_name": (5, 6),
    "a_12_major": (5, 7),
    "a_22_num": (5, 8),
    "a_22_name": (5, 9),
    "a_22_major": (5, 10),
    "a_32_num": (5, 11),
    "a_32_name": (5, 12),
    "a_32_major": (5, 13),
    "a_42_num": (5, 14),
    "a_42_name": (5, 15),
    "a_42_major": (5, 16),
    "a_13_num": (6, 5),
    "a_13_name": (6, 6),
    "a_13_major": (6, 7),
    "a_23_num": (6, 8),
    "a_23_name": (6, 9),
    "a_23_major": (6, 10),
    "a_33_num": (6, 11),
    "a_33_name": (6, 12),
    "a_33_major": (6, 13),
    "a_43_num": (6, 14),
    "a_43_name": (6, 15),
    "a_43_major": (6, 16),
    "a_14_num": (7, 5),
    "a_14_name": (7, 6),
    "a_14_major": (7, 7),
    "a_24_num": (7, 8),
    "a_24_name": (7, 9),
    "a_24_major": (7, 10),
    "a_34_num": (7, 11),
    "a_34_name": (7, 12),
    "a_34_major": (7, 13),
    "a_44_num": (7, 14),
    "a_44_name": (7, 15),
    "a_44_major": (7, 16),
    "a_sub": (8, 2),
    "a_all": (9, 2),
    "teamname_b": (11, 1),
    "formation_b": (12, 1),
    "b_00_num": (11, 2),
    "b_00_name": (11, 3),
    "b_00_major": (11, 4),
    "b_10_num": (11, 5),
    "b_10_name": (11, 6),
    "b_10_major": (11, 7),
    "b_20_num": (11, 8),
    "b_20_name": (11, 9),
    "b_20_major": (11, 10),
    "b_30_num": (11, 11),
    "b_30_name": (11, 12),
    "b_30_major": (11, 13),
    "b_40_num": (11, 14),
    "b_40_name": (11, 15),
    "b_40_major": (11, 16),
    "b_11_num": (12, 5),
    "b_11_name": (12, 6),
    "b_11_major": (12, 7),
    "b_21_num": (12, 8),
    "b_21_name": (12, 9),
    "b_21_major": (12, 10),
    "b_31_num": (12, 11),
    "b_31_name": (12, 12),
    "b_31_major": (12, 13),
    "b_41_num": (12, 14),
    "b_41_name": (12, 15),
    "b_41_major": (12, 16),
    "b_12_num": (13, 5),
    "b_12_name": (13, 6),
    "b_12_major": (13, 7),
    "b_22_num": (13, 8),
    "b_22_name": (13, 9),
    "b_22_major": (13, 10),
    "b_32_num": (13, 11),
    "b_32_name": (13, 12),
    "b_32_major": (13, 13),
    "b_42_num": (13, 14),
    "b_42_name": (13, 15),
    "b_42_major": (13, 16),
    "b_13_num": (14, 5),
    "b_13_name": (14, 6),
    "b_13_major": (14, 7),
    "b_23_num": (14, 8),
    "b_23_name": (14, 9),
    "b_23_major": (14, 10),
    "b_33_num": (14, 11),
    "b_33_name": (14, 12),
    "b_33_major": (14, 13),
    "b_43_num": (14, 14),
    "b_43_name": (14, 15),
    "b_43_major": (14, 16),
    "b_14_num": (15, 5),
    "b_14_name": (15, 6),
    "b_14_major": (15, 7),
    "b_24_num": (15, 8),
    "b_24_name": (15, 9),
    "b_24_major": (15, 10),
    "b_34_num": (15, 11),
    "b_34_name": (15, 12),
    "b_34_major": (15, 13),
    "b_44_num": (15, 14),
    "b_44_name": (15, 15),
    "b_44_major": (15, 16),
    "b_sub": (16, 2),
    "b_all": (17, 2)
}


def replace(df, row, col, val):
    cols = df.columns
    df.loc[row, cols[col]] = val


def read(df, row, col):
    cols = df.columns
    try:
        return df[cols[col]][row]
    except:
        return np.nan


def interpret(df):
    interpreted = mapping.copy()

    for key in interpreted.keys():
        if "sub" in key or "all" in key:
            pos = mapping[key]
            val = read(df, *pos)
            while True:
                pos = (pos[0], pos[1] + 1)
                newVal = read(df, *pos)
                if newVal is np.nan:
                    break
                val += "," + str(newVal)
        elif "num" in key:
            val = read(df, *mapping[key])
            try:
                val = int(val)
            except ValueError:
                pass
        else:
            val = read(df, *mapping[key])
        interpreted[key] = val

    return interpreted


def changeDf(df, it):
    data = it.copy()
    df2 = df.copy()
    for key in data.keys():
        # print(key)
        pos = mapping[key]
        if "sub" in key or "all" in key:
            data_list = data[key].split(",")
            # replace(df2, *pos, "\t".join(data_list))
            count = 0
            for dat in data_list:
                dat = dat.strip()
                count += 1
                # print(count)
                try:
                    replace(df2, *pos, dat)
                except:
                    df2[f"add_{count}"] = ""
                    replace(df2, *pos, dat)

                pos = (pos[0], pos[1] + 1)

            while True:
                try:
                    replace(df2, *pos, np.nan)
                    pos = (pos[0], pos[1] + 1)
                except:
                    break
        else:
            replace(df2, *pos, data[key])
    return df2

class TeamScreen(QMainWindow):
    def changeData(self, key, value):
        val = value.text()

        if 'num' in key:
            try:
                val = int(val)
            except:
                val = np.nan

        self.it[key] = val

        self.update_allplayer()
        print(self.it)

    def update_allplayer(self):
        t = ""

        num_input, name_input, belong_input = self.player_inputs[0]
        if name_input.text():
            t += num_input.text() + " " + name_input.text()

        for i, (num_input, name_input, belong_input) in enumerate(self.player_inputs[1:]):
            if name_input.text():
                t += ", " + num_input.text() + " " + name_input.text()

        if self.it[f"{self.team}_sub"]:
            t += ", " + self.it[f"{self.team}_sub"]

        self.it[f"{self.team}_all"] = t

    def wrapper(self, value):
        if isinstance(value, int):
            return str(value)
        elif value is np.nan:
            return ""
        elif isinstance(value, float):
            return str(value)
        else:
            return value


    def __init__(self, csvPath, team_idx=0):
        self.csvPath = csvPath
        try:
            self.df = pd.read_csv(csvPath)
            self.it = interpret(self.df)
        except FileNotFoundError:
            return

        self.team = ["a", "b"][team_idx]

        super().__init__()
        self.setWindowTitle("Soccer Team Formation")
        self.setGeometry(100, 100, 600, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)

        # Team name input
        stadium_layout = QHBoxLayout()
        self.stadium_label = QLabel("Stadium:")
        self.stadium_input = QLineEdit(self.wrapper(self.it[f"stadium"]))
        self.stadium_input.textChanged.connect(lambda: self.changeData(f"stadium", self.stadium_input))
        stadium_layout.addWidget(self.stadium_label)
        stadium_layout.addWidget(self.stadium_input)
        self.main_layout.addLayout(stadium_layout)

        # Team name input
        round_layout = QHBoxLayout()
        self.round_label = QLabel("Round:")
        self.round_input = QLineEdit(self.wrapper(self.it[f"round"]))
        self.round_input.textChanged.connect(lambda: self.changeData(f"round", self.round_input))
        round_layout.addWidget(self.round_label)
        round_layout.addWidget(self.round_input)
        self.main_layout.addLayout(round_layout)

        # Team name input
        team_name_layout = QHBoxLayout()
        self.team_name_label = QLabel("Team Name:")
        self.team_name_input = QLineEdit(self.wrapper(self.it[f"teamname_{self.team}"]))
        self.team_name_input.textChanged.connect(lambda: self.changeData(f"teamname_{self.team}", self.team_name_input))
        team_name_layout.addWidget(self.team_name_label)
        team_name_layout.addWidget(self.team_name_input)
        self.main_layout.addLayout(team_name_layout)

        # Formation label
        formation_layout = QHBoxLayout()
        self.formation_label = QLabel("Formation:")
        self.formation_input = QLineEdit(self.wrapper(self.it[f"formation_{self.team}"]))
        self.formation_input.textChanged.connect(lambda: self.changeData(f"formation_{self.team}", self.formation_input))
        self.formation_input.setReadOnly(True)
        formation_layout.addWidget(self.formation_label)
        formation_layout.addWidget(self.formation_input)
        self.main_layout.addLayout(formation_layout)

        # Formation constraint label
        self.formation_constraint_label = QLabel("Formation must sum up to 10.")
        self.main_layout.addWidget(self.formation_constraint_label)

        # Player slots grid
        self.player_grid_layout = QGridLayout()
        self.main_layout.addLayout(self.player_grid_layout)

        self.player_inputs = []

        # First row for goalkeeper
        goalkeeper_layout = QVBoxLayout()
        goalkeeper_number_input = QLineEdit(self.wrapper(self.it[f"{self.team}_00_num"]))
        goalkeeper_number_input.setPlaceholderText("Number")
        goalkeeper_number_input.textChanged.connect(lambda: self.changeData(f"{self.team}_00_num", goalkeeper_number_input))
        goalkeeper_layout.addWidget(goalkeeper_number_input)

        goalkeeper_name_input = QLineEdit(self.wrapper(self.it[f"{self.team}_00_name"]))
        goalkeeper_name_input.setPlaceholderText("Name")
        goalkeeper_name_input.textChanged.connect(lambda: self.changeData(f"{self.team}_00_name", goalkeeper_name_input))
        goalkeeper_layout.addWidget(goalkeeper_name_input)

        goalkeeper_belong_input = QLineEdit(self.wrapper(self.it[f"{self.team}_00_major"]))
        goalkeeper_belong_input.setPlaceholderText("Major")
        goalkeeper_belong_input.textChanged.connect(lambda: self.changeData(f"{self.team}_00_major", goalkeeper_belong_input))
        goalkeeper_layout.addWidget(goalkeeper_belong_input)

        container = QWidget()
        container.setLayout(goalkeeper_layout)
        self.player_grid_layout.addWidget(container, 0, 2, 1, 1)
        self.player_inputs.append((goalkeeper_number_input, goalkeeper_name_input, goalkeeper_belong_input))

        # Other rows for field players
        for i in range(1, 5):  # 1 goalkeeper + 4*4 = 17 slots
            for j in range(5):
                playernum = str(i) + str(j)
                player_layout = QVBoxLayout()

                player_number_input = QLineEdit(self.wrapper(self.it[f"{self.team}_{playernum}_num"]))
                player_number_input.setPlaceholderText("Number")
                player_number_input.textChanged.connect(lambda checked, p=player_number_input, n=playernum: self.changeData(f"{self.team}_{n}_num", p))
                player_layout.addWidget(player_number_input)

                player_name_input = QLineEdit(self.wrapper(self.it[f"{self.team}_{playernum}_name"]))
                player_name_input.setPlaceholderText("Name")
                player_name_input.textChanged.connect(lambda checked, p=player_name_input, n=playernum: self.changeData(f"{self.team}_{n}_name", p))
                player_layout.addWidget(player_name_input)

                player_belong_input = QLineEdit(self.wrapper(self.it[f"{self.team}_{playernum}_major"]))
                player_belong_input.setPlaceholderText("Major")
                player_belong_input.textChanged.connect(lambda checked, p=player_belong_input, n=playernum: self.changeData(f"{self.team}_{n}_major", p))
                player_layout.addWidget(player_belong_input)

                container = QWidget()
                container.setLayout(player_layout)
                self.player_grid_layout.addWidget(container, i, j)
                self.player_inputs.append((player_number_input, player_name_input, player_belong_input))

        # Substitute input
        substitute_layout = QHBoxLayout()
        self.substitute_label = QLabel("Substitutes:")
        self.substitute_input = QLineEdit(self.wrapper(self.it[f"{self.team}_sub"]))
        self.substitute_input.textChanged.connect(lambda: self.changeData(f"{self.team}_sub", self.substitute_input))
        substitute_layout.addWidget(self.substitute_label)
        substitute_layout.addWidget(self.substitute_input)
        self.main_layout.addLayout(substitute_layout)

        # Save and Cancel buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save)
        button_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)
        button_layout.addWidget(self.cancel_button)

        self.main_layout.addLayout(button_layout)

        # Connect text change to update formation
        for inputs in self.player_inputs:
            inputs[1].textChanged.connect(self.update_formation)

        self.update_formation()

    def update_formation(self):
        # Calculate formation based on filled player slots
        formation_counts = [0, 0, 0, 0, 0]
        for i, (num_input, name_input, belong_input) in enumerate(self.player_inputs[1:]):
            if name_input.text().strip():
                row = i // 5
                formation_counts[row] += 1

        formation = '-'.join(str(count) for count in formation_counts if count > 0)
        self.formation_input.setText(formation)

        # Check if formation sum is 10
        formation_sum = sum(formation_counts)
        if formation_sum == 10:
            self.formation_constraint_label.setText("Formation is valid.")
            self.save_button.setEnabled(True)
        else:
            self.formation_constraint_label.setText("Formation must sum up to 10.")
            self.save_button.setEnabled(False)

    def save(self):
        # Implement save functionality here
        print("Saving team data...")
        df = changeDf(self.df, self.it)
        print("changed df")
        # df.style()
        df.to_csv(self.csvPath, encoding="utf-8", index=False)
        self.close()


def main():
    app = QApplication(sys.argv)
    main_window = TeamScreen(
        r"C:\Users\marks\OneDrive\Documents\SNU\동아리\SUB\SUB Sports\2024-07 SHA-CUP\assets\team_info_converted.csv", 0)
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
