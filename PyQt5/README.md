PyQt5
======

The changes between PyQt4 and Pyqt5 are rather manageable

####QtGui
PyQt4’s QtGui module has been split into PyQt5’s QtGui, QtPrintSupport and QtWidgets modules
The Writer is using:

+ **QtGui:** QIcon, QImage, QMenu, QContextMenuEvent, QFont, QTextCharFormat, QTextListFormat, QTextCursor, QTextTableFormat
+ **QtWidgets:** QMainWindow, QApplication, QAction, QFontComboBox, QSpinBox, QTextEdit, QMessageBox, QFileDialog, QColorDialog, QDialog, QPushButton, QGridLayout, QComboBox, QRadioButton, QLabel, QWidget
+ **QtPrintSupport:** QPrintPreviewDialog, QPrintDialog


####QFileDialog

**getOpenFileName()** and **getSaveFileName()** return a tuple (filename, filter) in PyQt5 instead of the filename as a string in PyQt4



####More Infos
The PyQT 5 Reference Guide has a list of all changes:
http://pyqt.sourceforge.net/Docs/PyQt5/pyqt4_differences.html