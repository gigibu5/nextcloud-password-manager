#!/usr/bin/python3

import json
import PyQt5.QtWidgets as qtw
from PyQt5.QtCore import Qt
from PyQt5.Qt import QApplication, QClipboard

# Select language: EN - English, SI - Slovene
language = "SI"
f = open("lang_pack.json")

lang = json.loads(f.read())[language]
f.close()

class Geslo(qtw.QWidget):
	def __init__(self, name, username, password):
		super(Geslo, self).__init__()

		self.name = name
		self.username = username
		self.password = password

		self.napis = qtw.QLabel(self.name)
		self.gumbUsername = qtw.QPushButton(lang["username"])
		self.gumbPassword = qtw.QPushButton(lang["password"])

		self.gumbUsername.setMinimumWidth(35)
		self.gumbUsername.setMaximumWidth(35)
		self.gumbPassword.setMaximumWidth(35)
		self.gumbPassword.setMaximumWidth(35)

		# razporeditev
		self.hbox = qtw.QHBoxLayout()
		self.hbox.addWidget(self.napis)
		self.hbox.addWidget(self.gumbUsername)
		self.hbox.addWidget(self.gumbPassword)

		self.gumbUsername.clicked.connect(self.gumbUsr)
		self.gumbPassword.clicked.connect(self.gumbPass)
		
		self.setLayout(self.hbox)
	
	def gumbUsr(self):
		QApplication.clipboard().setText(self.username)

	def gumbPass(self):
		QApplication.clipboard().setText(self.password)

class Okno(qtw.QWidget):
	def __init__(self):
		qtw.QWidget.__init__(self)

		self.setWindowTitle(lang["title"])
		#self.setWindowIcon(QIcon('web.png'))

		layout = qtw.QGridLayout()

		# SEARCH ------------------------------
		self.searchbar = qtw.QLineEdit()
		self.searchbar.textChanged.connect(self.iskanje)
		self.searchbar.setPlaceholderText(lang["search"])

		layout.addWidget(self.searchbar)
		# SEARCH ------------------------------

		# gumb izbris clipboarda --------------
		self.clearClip = qtw.QPushButton(lang["clipboard"])
		self.clearClip.clicked.connect(self.pocistiOdlozisce)

		layout.addWidget(self.clearClip)
		# gumb izbris clipboarda --------------

		self.gesla = qtw.QWidget()
		self.geslaRazporeditev = qtw.QVBoxLayout()

		# Uporablja se da veš kje je kej, ker je tole zelo čudn
		self.widgets = []

		f = open("passwords.json")
		raw = f.read()
		f.close()

		pretvorjeno = json.loads(raw)

		for i in pretvorjeno["passwords"]:
			#label = qtw.QLabel(i)
			label = Geslo(i["label"], i["username"], i["password"])
			self.geslaRazporeditev.addWidget(label)
			self.widgets.append(label)

		self.gesla.setLayout(self.geslaRazporeditev)

		# tale del je da ne gre vse na sredino in da je lepo poravnan
		spacer = qtw.QSpacerItem(1, 1, qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Expanding)
		self.geslaRazporeditev.addItem(spacer)
		self.gesla.setLayout(self.geslaRazporeditev)

		# da lohk gor pa dol skrolas
		self.scroll = qtw.QScrollArea()
		self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.scroll.setWidgetResizable(True)
		self.scroll.setWidget(self.gesla)

		layout.addWidget(self.scroll)

		self.setLayout(layout)
	
	def iskanje(self, napis):
		for i in self.widgets:
			if(napis.lower() in i.name.lower()):
				i.show()
			else:
				i.hide()
		#print(napis)
	
	def pocistiOdlozisce(self):
		QApplication.clipboard().setText("")

program = qtw.QApplication([])
okn = Okno()
okn.show()
okn.setFixedWidth(okn.width())
program.exec_()