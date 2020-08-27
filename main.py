#!/usr/bin/python3

import json
import PyQt5.QtWidgets as qtw
from PyQt5.QtCore import Qt
from PyQt5.Qt import QApplication, QClipboard

# Select language: EN - English, SI - Slovene
language = "EN"
f = open("lang_pack.json")

lang = json.loads(f.read())[language]
f.close()

class Password(qtw.QWidget):
	def __init__(self, name, username, password):
		super(Password, self).__init__()

		self.name = name
		self.username = username
		self.password = password

		self.lbl = qtw.QLabel(self.name)
		self.btnUsername = qtw.QPushButton(lang["username"])
		self.btnPassword = qtw.QPushButton(lang["password"])

		self.btnUsername.setMinimumWidth(35)
		self.btnUsername.setMaximumWidth(35)
		self.btnPassword.setMaximumWidth(35)
		self.btnPassword.setMaximumWidth(35)

		# Button and label layout
		self.hbox = qtw.QHBoxLayout()
		self.hbox.addWidget(self.lbl)
		self.hbox.addWidget(self.btnUsername)
		self.hbox.addWidget(self.btnPassword)

		self.btnUsername.clicked.connect(self.btnUser)
		self.btnPassword.clicked.connect(self.btnPass)
		
		self.setLayout(self.hbox)
	
	def btnUser(self):
		QApplication.clipboard().setText(self.username)

	def btnPass(self):
		QApplication.clipboard().setText(self.password)

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
		self.clearClip.clicked.connect(self.clearClipboard)

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

		for i in converted["passwords"]:
			label = Password(i["label"], i["username"], i["password"])
			self.passwordsLayout.addWidget(label)
			self.widgets.append(label)

		# tale del je da ne gre vse na sredino in da je lepo poravnan
		spacer = qtw.QSpacerItem(1, 1, qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Expanding)
		self.passwordsLayout.addItem(spacer)
		self.passwords.setLayout(self.passwordsLayout)

		# da lohk gor pa dol skrolas
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
		#print(lbl)
	
	def clearClipboard(self):
		QApplication.clipboard().setText("")

program = qtw.QApplication([])
okn = Window()
okn.show()
okn.setFixedWidth(okn.width())
program.exec_()