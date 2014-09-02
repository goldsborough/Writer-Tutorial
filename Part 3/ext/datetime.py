from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

from time import strftime

class DateTime(QtGui.QDialog):
    def __init__(self,parent = None):
        QtGui.QDialog.__init__(self, parent)

        self.parent = parent
         
        self.initUI()
 
    def initUI(self):
 
        self.form = QtGui.QComboBox(self)

        # Display the different time self.formats 
        self.form.addItem(strftime("%A, %d. %B %Y %H:%M"))
        self.form.addItem(strftime("%A, %d. %B %Y"))
        self.form.addItem(strftime("%d. %B %Y %H:%M"))
        self.form.addItem(strftime("%d.%m.%Y %H:%M"))
        self.form.addItem(strftime("%d. %B %Y"))
        self.form.addItem(strftime("%d %m %Y"))
        self.form.addItem(strftime("%d.%m.%Y"))
        self.form.addItem(strftime("%x"))
        self.form.addItem(strftime("%X"))
        self.form.addItem(strftime("%H:%M"))

        insert = QtGui.QPushButton("Insert",self)
        insert.clicked.connect(self.insert)
 
        cancel = QtGui.QPushButton("Cancel",self)
        cancel.clicked.connect(self.close)
 
        layout = QtGui.QGridLayout()

        layout.addWidget(self.form,0,0,1,2)
        layout.addWidget(insert,1,0)
        layout.addWidget(cancel,1,1)
        
        self.setGeometry(300,300,400,80)
        self.setWindowTitle("Date and Time")
        self.setLayout(layout)

    def insert(self):

        # Grab cursor
        cursor = self.parent.text.textCursor()

        # Insert the comboBox's current text
        cursor.insertText(self.form.currentText())

        # Close the window
        self.close()
