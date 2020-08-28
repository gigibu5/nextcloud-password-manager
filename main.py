#!/usr/bin/python3

import json
import webbrowser
import PyQt5.QtWidgets as qtw
from PyQt5.QtCore import Qt
from PyQt5.Qt import QApplication, QClipboard

# Select language: EN - English, SI - Slovene
language = "EN"
f = open("lang_pack.json")

lang = json.loads(f.read())[language]
f.close()

class Password(qtw.QWidget):
	def __init__(self, passwordd):
		super(Password, self).__init__()

		self.name = passwordd["label"]
		self.username = passwordd["username"]
		self.password = passwordd["password"]
		self.url = passwordd["url"]

		self.lbl = qtw.QLabel(self.name)
		self.lbl.setToolTip(passwordd["notes"])

		# Button and label layout
		self.hbox = qtw.QHBoxLayout()
		self.hbox.addWidget(self.lbl)
		
		# Generating buttons
		buttons = ["url","username","password"]
		object_buttons = []

		for i in buttons:
			btn = qtw.QPushButton(lang[i][:1])
			btn.setMaximumWidth(35)
			btn.setMaximumWidth(35)
			self.hbox.addWidget(btn)
			tooltip = lang[i]
			if(i == "url"):
				if(self.url == ""):
					btn.setDisabled(True)
				else:
					tooltip += ": " + self.url
			btn.setToolTip(tooltip)
			object_buttons.append(btn)

		object_buttons[0].clicked.connect(lambda: webbrowser.open(self.url))
		object_buttons[1].clicked.connect(lambda: QApplication.clipboard().setText(self.username))
		object_buttons[2].clicked.connect(lambda: QApplication.clipboard().setText(self.password))

		self.setLayout(self.hbox)
		
	
class Window(qtw.QWidget):
	def __init__(self):
		qtw.QWidget.__init__(self)

		self.setWindowTitle(lang["title"])
		#self.setWindowIcon(QIcon('web.png'))

		layout = qtw.QGridLayout()

		# SEARCH ------------------------------
		self.searchbar = qtw.QLineEdit()
		self.searchbar.textChanged.connect(self.search)
		self.searchbar.setPlaceholderText(lang["search"])

		layout.addWidget(self.searchbar)
		# SEARCH ------------------------------

		# CLEAR CLIPBOARD BUTTON --------------
		self.clearClip = qtw.QPushButton(lang["clipboard"])
		self.clearClip.clicked.connect(lambda: QApplication.clipboard().setText(""))

		layout.addWidget(self.clearClip)
		# CLEAR CLIPBOARD BUTTON --------------

		self.passwords = qtw.QWidget()
		self.passwordsLayout = qtw.QVBoxLayout()

		# A list of passwords used for search functionality
		self.widgets = []

		f = open("passwords.json")
		raw = f.read()
		f.close()

		converted = json.loads(raw)

		converted = self.sortiraj(converted)

		for i in converted["passwords"]:
			label = Password(i)
			self.passwordsLayout.addWidget(label)
			self.widgets.append(label)

		# adding a spacer so eerything is aligned
		spacer = qtw.QSpacerItem(1, 1, qtw.QSizePolicy.Minimum,
			qtw.QSizePolicy.Expanding)
		self.passwordsLayout.addItem(spacer)
		self.passwords.setLayout(self.passwordsLayout)

		# scroll box
		self.scroll = qtw.QScrollArea()
		self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.scroll.setWidgetResizable(True)
		self.scroll.setWidget(self.passwords)

		layout.addWidget(self.scroll)

		self.setLayout(layout)
	
	def search(self, lbl):
		for i in self.widgets:
			if(lbl.lower() in i.name.lower()):
				i.show()
			else:
				i.hide()

	def sortiraj(self, converted_json):
		p = converted_json["passwords"]
		for i in range(len(p)):
			for j in range(len(p)-i-1):
				if(p[j]["label"] > p[j+1]["label"]):
					temp = p[j]
					p[j] = p[j+1]
					p[j + 1] = temp
		converted_json["passwords"] = p
		return converted_json


program = qtw.QApplication([])
okn = Window()
okn.show()
okn.setMinimumWidth(okn.width())
program.exec_()