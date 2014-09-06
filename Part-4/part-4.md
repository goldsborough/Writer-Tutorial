Welcome back to my series on

## Inserting time and date

The time and date dialog will be very simple. Create a new file in `ext` and call it `datetime.py`.

__In `ext/datetime.py`__:

    from PyQt4 import QtGui, QtCore
    from PyQt4.QtCore import Qt

    from time import strftime

    class DateTime(QtGui.QDialog):
        def __init__(self,parent = None):
            QtGui.QDialog.__init__(self, parent)

            self.parent = parent

            self.formats = ["%A, %d. %B %Y %H:%M",
                            "%A, %d. %B %Y",
                            "%d. %B %Y %H:%M",
                            "%d.%m.%Y %H:%M",
                            "%d. %B %Y",
                            "%d %m %Y",
                            "%d.%m.%Y",
                            "%x",
                            "%X",
                            "%H:%M"]

            self.initUI()

        def initUI(self):

            self.box = QtGui.QComboBox(self)

            for i in self.formats:
                self.box.addItem(strftime(i))

            insert = QtGui.QPushButton("Insert",self)
            insert.clicked.connect(self.insert)

            cancel = QtGui.QPushButton("Cancel",self)
            cancel.clicked.connect(self.close)

            layout = QtGui.QGridLayout()

            layout.addWidget(self.box,0,0,1,2)
            layout.addWidget(insert,1,0)
            layout.addWidget(cancel,1,1)

            self.setGeometry(300,300,400,80)
            self.setWindowTitle("Date and Time")
            self.setLayout(layout)

        def insert(self):

            # Grab cursor
            cursor = self.parent.text.textCursor()

            datetime = strftime(self.formats[self.box.currentIndex()])

            # Insert the comboBox's current text
            cursor.insertText(datetime)

            # Close the window
            self.close()

__In `ext/__init__.py`__:

    __all__ = ["find","wordcount","datetime"]

__Back to `writer.py`. In `initToolbar()`__:

        dateTimeAction = QtGui.QAction(QtGui.QIcon("icons/calender.png"),"Insert current date/time",self)
        dateTimeAction.setStatusTip("Insert current date/time")
        dateTimeAction.setShortcut("Ctrl+D")
        dateTimeAction.triggered.connect(datetime.DateTime(self).show)

        self.toolbar.addAction(dateTimeAction)


Very little code! In the constructor, `__init__()`, we again make our parent object a class member and also create a list of different time formats, which we'll make use of in a bit. If you're unfamiliar with these time and date parameters used by Python (originally C) you can find a description and list of them [here](https://docs.python.org/3/library/time.html#time.strftime).

Next up, `initUI()`. We create a `QComboBox`, `self.box`, and fill it with all of our time formats, which we turn into actual date and time strings using Python's `time.strftime()` function. We also initialize a `QPushButton` for inserting the date and time string into the text and another button for canceling the operation. We connect the former to a slot function, `self.insert()`, and the latter very simply to the dialog's `close()` method, which initiates your computer's self-destruct sequence and blows it up after 60 seconds. Oh, wait, that's `self.detonate()`; `self.close()` just closes the window. In any case, we put all of these widgets into a layout again and configure some of the dialog's basic settings such as size and window title.

In `self.insert()`, we first grab our `QTextEdit`'s cursor and then get the appropriate format string using the `QComboBox`'s `currentIndex()` and our list of formats, which we then turn into a date-time string using `strftime()`. You might think that we could just use the `QComboBox`'s `currentText()` method to retrieve the actual string and thus avoid a second call to `strftime()`, however the user might decide to make a sandwich *just* when he or she was about to press "insert" and thus the date-time string would not be up-to-date anymore once the user returns from gloriously feasting - tragic. Once we have the new string, we insert it using our cursor's `insertText()` method. Also, we want to close the dialog once the user has finished, so we call `self.close()` at the end.

The other two snippets of code should be self-explanatory by now. We add this module to our `ext` package and create an appropriate `QAction` for it in our main window.
