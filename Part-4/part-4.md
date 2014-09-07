Welcome back to my series on __*Building a text editor with PyQt*__. In the last part, we started to add some great extensions to our text editor, such as a find-and-replace dialog and a way of inserting an image into our text. This part will deal with two more extensions, namely one for inserting the current date and time into our text and another for inserting and managing tables. Also, we'll add a way of prompting the user about saving unsaved changes before closing *Writer*.

## Inserting time and date

The time and date dialog isn't very complicated. Create a new file in `ext` and call it `datetime.py`.

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

In `self.insert()`, we first grab our `QTextEdit`'s cursor and then get the appropriate format string using the `QComboBox`'s `currentIndex()` method and our list of formats, which we then turn into a date-time string using `strftime()`. You might think that we could just use the `QComboBox`'s `currentText()` method to retrieve the actual string and thus avoid a second call to `strftime()`, however the user might decide to make a sandwich *just* when he or she was about to press "insert" and thus the date-time string would not be up-to-date anymore when the user returns - tragic. Once we have the new string, we insert it using our cursor's `insertText()` method. Also, we want to close the dialog once the user has finished, so we call `self.close()` at the end.

The other two snippets of code should be self-explanatory if you've read the previous parts of this series. We add this module to our `ext` package and create an appropriate `QAction` for it in our main window.

## Tables

Next up, I'll show you how to create and manipulate tables. The steps to accomplish this are fairly straightforward:

1. Go to your nearest forest and start choppin' up some wood. I recommend a fine oak or fir tree for our purposes.
2. Saw your wood into appropriately shaped pieces.
3. Dry the wood for approximately 8 months. Check back to this tutorial then.
4. Hammer the table's leg to the base.
5. Profit.

Huh? What do you mean "different kind of table"? Oh right, tables for data! Disregarding whether or not you just found this funny, create a new file in our `ext` package called `table.py`:

`ext/table.py`:

    from PyQt4 import QtGui, QtCore
    from PyQt4.QtCore import Qt

    class Table(QtGui.QDialog):
        def __init__(self,parent = None):
            QtGui.QDialog.__init__(self, parent)

            self.parent = parent

            self.initUI()

        def initUI(self):

            # Rows
            rowsLabel = QtGui.QLabel("Rows: ",self)

            self.rows = QtGui.QSpinBox(self)

            # Columns
            colsLabel = QtGui.QLabel("Columns",self)

            self.cols = QtGui.QSpinBox(self)

            # Cell spacing (distance between cells)
            spaceLabel = QtGui.QLabel("Cell spacing",self)

            self.space = QtGui.QSpinBox(self)

            # Cell padding (distance between cell and inner text)
            padLabel = QtGui.QLabel("Cell padding",self)

            self.pad = QtGui.QSpinBox(self)

            self.pad.setValue(10)

            # Button
            insertButton = QtGui.QPushButton("Insert",self)
            insertButton.clicked.connect(self.insert)

            # Layout
            layout = QtGui.QGridLayout()

            layout.addWidget(rowsLabel,0,0)
            layout.addWidget(self.rows,0,1)

            layout.addWidget(colsLabel,1,0)
            layout.addWidget(self.cols,1,1)

            layout.addWidget(padLabel,2,0)
            layout.addWidget(self.pad,2,1)

            layout.addWidget(spaceLabel,3,0)
            layout.addWidget(self.space,3,1)

            layout.addWidget(insertButton,4,0,1,2)

            self.setWindowTitle("Insert Table")
            self.setGeometry(300,300,200,100)
            self.setLayout(layout)

        def insert(self):

            cursor = self.parent.text.textCursor()

            # Get the configurations
            rows = self.rows.value()

            cols = self.cols.value()

            if not rows or not cols:

                popup = QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                                          "Parameter error",
                                          "Row and column numbers may not be zero!",
                                          QtGui.QMessageBox.Ok,
                                          self)
                popup.show()

            else:

                padding = self.pad.value()

                space = self.space.value()

                # Set the padding and spacing
                fmt = QtGui.QTextTableFormat()

                fmt.setCellPadding(padding)

                fmt.setCellSpacing(space)

                # Inser the new table
                cursor.insertTable(rows,cols,fmt)

                self.close()

`ext/__init__.py`:

    __all__ = ["find","datetime","wordcount","table"]

__Back to `writer.py`. In `initToolbar()`__:

    tableAction = QtGui.QAction(QtGui.QIcon("icons/table.png"),"Insert table",self)
    tableAction.setStatusTip("Insert table")
    tableAction.setShortcut("Ctrl+T")
    tableAction.triggered.connect(table.Table(self).show)

    self.toolbar.addAction(tableAction)

__In `initUI()`__:

    # We need our own context menu for tables
    self.text.setContextMenuPolicy(Qt.CustomContextMenu)
    self.text.customContextMenuRequested.connect(self.context)

__Below `initUI()`__:

    def context(self,pos):

            # Grab the cursor
            cursor = self.text.textCursor()

            # Grab the current table, if there is one
            table = cursor.currentTable()

            # Above will return 0 if there is no current table, in which case
            # we call the normal context menu. If there is a table, we create
            # our own context menu specific to table interaction
            if table:

                menu = QtGui.QMenu(self)

                appendRowAction = QtGui.QAction("Append row",self)
                appendRowAction.triggered.connect(lambda: table.appendRows(1))

                appendColAction = QtGui.QAction("Append column",self)
                appendColAction.triggered.connect(lambda: table.appendColumns(1))


                removeRowAction = QtGui.QAction("Remove row",self)
                removeRowAction.triggered.connect(self.removeRow)

                removeColAction = QtGui.QAction("Remove column",self)
                removeColAction.triggered.connect(self.removeCol)


                insertRowAction = QtGui.QAction("Insert row",self)
                insertRowAction.triggered.connect(self.insertRow)

                insertColAction = QtGui.QAction("Insert column",self)
                insertColAction.triggered.connect(self.insertCol)


                mergeAction = QtGui.QAction("Merge cells",self)
                mergeAction.triggered.connect(lambda: table.mergeCells(cursor))

                # Only allow merging if there is a selection
                if not cursor.hasSelection():
                    mergeAction.setEnabled(False)


                splitAction = QtGui.QAction("Split cells",self)

                cell = table.cellAt(cursor)

                # Only allow splitting if the current cell is larger
                # than a normal cell
                if cell.rowSpan() > 1 or cell.columnSpan() > 1:

                    splitAction.triggered.connect(lambda: table.splitCell(cell.row(),cell.column(),1,1))

                else:
                    splitAction.setEnabled(False)


                menu.addAction(appendRowAction)
                menu.addAction(appendColAction)

                menu.addSeparator()

                menu.addAction(removeRowAction)
                menu.addAction(removeColAction)

                menu.addSeparator()

                menu.addAction(insertRowAction)
                menu.addAction(insertColAction)

                menu.addSeparator()

                menu.addAction(mergeAction)
                menu.addAction(splitAction)

                # Convert the widget coordinates into global coordinates
                pos = self.mapToGlobal(pos)

                # Add pixels for the tool and formatbars, which are not included
                # in mapToGlobal(), but only if the two are currently visible and
                # not toggled by the user

                if self.toolbar.isVisible():
                  pos.setY(pos.y() + 45)

                if self.formatbar.isVisible():
                    pos.setY(pos.y() + 45)

                # Move the menu to the new position
                menu.move(pos)

                menu.show()

            else:

                event = QtGui.QContextMenuEvent(QtGui.QContextMenuEvent.Mouse,QtCore.QPoint())

                self.text.contextMenuEvent(event)

        def removeRow(self):

            # Grab the cursor
            cursor = self.text.textCursor()

            # Grab the current table (we assume there is one, since
            # this is checked before calling)
            table = cursor.currentTable()

            # Get the current cell
            cell = table.cellAt(cursor)

            # Delete the cell's row
            table.removeRows(cell.row(),1)

        def removeCol(self):

            # Grab the cursor
            cursor = self.text.textCursor()

            # Grab the current table (we assume there is one, since
            # this is checked before calling)
            table = cursor.currentTable()

            # Get the current cell
            cell = table.cellAt(cursor)

            # Delete the cell's column
            table.removeColumns(cell.column(),1)

        def insertRow(self):

            # Grab the cursor
            cursor = self.text.textCursor()

            # Grab the current table (we assume there is one, since
            # this is checked before calling)
            table = cursor.currentTable()

            # Get the current cell
            cell = table.cellAt(cursor)

            # Insert a new row at the cell's position
            table.insertRows(cell.row(),1)

        def insertCol(self):

            # Grab the cursor
            cursor = self.text.textCursor()

            # Grab the current table (we assume there is one, since
            # this is checked before calling)
            table = cursor.currentTable()

            # Get the current cell
            cell = table.cellAt(cursor)

            # Insert a new row at the cell's position
            table.insertColumns(cell.column(),1)


First up, the `Table` class. This `QDialog` will allow the user to set initial configurations for the table he or she is about to insert into the text. This includes the number of rows and columns, as well as cell spacing, the distance between individual cells (similar to `margin` in CSS), and cell padding, the distance between the outer edge of a cell and its inner text (comparable to `padding` in CSS). We visualize these settings with a few labels indicating what the user is configuring (e.g. "Rows:") and a `QSpinBox` each to input actual values for these parameters. Also, we create an "insert" button which the user presses to insert his or her table. We connect this `QPushButton`'s `clicked` signal to a slot function, `self.insert()`:

    # Rows
    rowsLabel = QtGui.QLabel("Rows: ",self)

    self.rows = QtGui.QSpinBox(self)

    # Columns
    colsLabel = QtGui.QLabel("Columns",self)

    self.cols = QtGui.QSpinBox(self)

    # Cell spacing (distance between cells)
    spaceLabel = QtGui.QLabel("Cell spacing",self)

    self.space = QtGui.QSpinBox(self)

    # Cell padding (distance between cell and inner text)
    padLabel = QtGui.QLabel("Cell padding",self)

    self.pad = QtGui.QSpinBox(self)

    self.pad.setValue(10)

    # Button
    insertButton = QtGui.QPushButton("Insert",self)
    insertButton.clicked.connect(self.insert)

We followingly add all of these widgets to a layout and set it as our dialog's layout, as well as configuring all the other necessary window settings already discussed before (window size, title etc.). In `insert()`, we grab our parent's text cursor again and all of the values the user set for the various parameters on our dialog. Our cursor's method for inserting a table is `insertTable()`, which takes the number of rows, the number of columns and optionally a `QTextTableFormat` object. If either the number of rows or the number of columns is zero, `insertTable()` does nothing. To prevent confusion, we check if `rows` or `cols` is zero and, if it is the case, pop up an error dialog. Else, we move on to inserting the table. We can directly use the values we retrieved for row and column numbers, however we must use a `QTextTableFormat` object to make changes to cell padding and cell spacing. Therefore, we create a new `QTextTableFormat` and set the spacing and padding using `setCellPadding()` and `setCellSpacing()`, respectively. Finally, we use `insertTable()` method to insert the table and subsequently close the dialog:


        def insert(self):

            cursor = self.parent.text.textCursor()

            # Get the configurations
            rows = self.rows.value()

            cols = self.cols.value()

            if not rows or not cols:

                popup = QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                                          "Parameter error",
                                          "Row and column numbers may not be zero!",
                                          QtGui.QMessageBox.Ok,
                                          self)
                popup.show()

            else:

                padding = self.pad.value()

                space = self.space.value()

                # Set the padding and spacing
                fmt = QtGui.QTextTableFormat()

                fmt.setCellPadding(padding)

                fmt.setCellSpacing(space)

                # Insert the new table
                cursor.insertTable(rows,cols,fmt)

                self.close()

As you can see, the `Table` class is quite simple. The real fun starts back in `writer.py`. Before we get to that, though, don't forget to add this module to `__all__` in `ext/__init__.py`. Now, in `writer.py`, you'll first need to create a `QAction` for the dialog in `initToolbar()` to make it accessible from the editor's toolbar. I trust that this needs no further explaining by now.

With the code I discussed up to now, the user can insert a table into his or her document. The problem is, however, that PyQt's tables aren't very interactive. You can't stretch or resize them and PyQt provides no way of adding or deleting rows and columns once the table has been initialized, also merging cells is impossible with these static tables. Therefore, we'll create our own way of manipulating tables, which we accomplish by showing a custom context menu when the user right-clicks on a table. If the user right-clicks anywhere else, we'll display the standard context menu again.

Here we go! In `initUI()`, we need to reset our `QTextEdit`'s context menu policy, which we do by passing `Qt.CustomContextMenu` to the `setContextMenuPolicy()` method. By doing so, PyQt will no longer display its standard context menu when you right-click the `QTextEdit` and thus enable us to create our own menu. Next, connect the `customContextMenuRequested()` signal to a slot function, `self.context()`:

    # We need our own context menu for tables
    self.text.setContextMenuPolicy(Qt.CustomContextMenu)
    self.text.customContextMenuRequested.connect(self.context)

In `self.context()`, we first grab our `QTextEdit`'s `QTextCursor` again, which has a method for retrieving the table the cursor is currently over: `currentTable()`. If there is no table underneath the cursor, `currentTable()` returns zero, so we can check which context menu to call, our custom context menu for tables or the normal context menu for everything else. Just to get it out of the way, if there is no table, we call the standard context menu with the following code:

    event = QtGui.QContextMenuEvent(QtGui.QContextMenuEvent.Mouse,QtCore.QPoint())

    self.text.contextMenuEvent(event)

Now, for our table-manipulation menu, we need to create a `QMenu` and populate just like we did for our tool- and menubars. This means creating a `QAction` and connecting its `triggered` signal to a slot function. We want actions for:

+ Appending rows and columns
+ Removing rows and columns
+ Inserting rows and columns
+ Merging multiple cells into a single cell
+ Splitting previously merged cells back into individual cells

For the first set of actions, responsible for appending rows or columns to the table, we don't need to create separate slot methods. We just use one-line lambda expressions in which we call the table's `appendRows()` or `appendColumns()` methods and pass it the number 1, to insert a single row or column, respectively:

    appendRowAction = QtGui.QAction("Append row",self)
    appendRowAction.triggered.connect(lambda: table.appendRows(1))

    appendColAction = QtGui.QAction("Append column",self)
    appendColAction.triggered.connect(lambda: table.appendColumns(1))

The actions concerning removing and inserting rows and columns need a bit more code than a single line, so connect them to external slot functions:


    removeRowAction = QtGui.QAction("Remove row",self)
    removeRowAction.triggered.connect(self.removeRow)

    removeColAction = QtGui.QAction("Remove column",self)
    removeColAction.triggered.connect(self.removeCol)


    insertRowAction = QtGui.QAction("Insert row",self)
    insertRowAction.triggered.connect(self.insertRow)

    insertColAction = QtGui.QAction("Insert column",self)
    insertColAction.triggered.connect(self.insertCol)

Merging and splitting actions are a little special, as we'll only want to make these actions accessible when they actually are of use.

First up, merging. After creating a `QAction` for it, we connect its signal to a lambda expression again, in which we call our table's overloaded `mergeCells()` method, which requires us to pass it our cursor object and then takes care of merging selected cells, if there are any. We disable the action if the user's cursor has no selection:

    mergeAction = QtGui.QAction("Merge cells",self)
    mergeAction.triggered.connect(lambda: table.mergeCells(cursor))

    # Only allow merging if there is a selection
    if not cursor.hasSelection():
        mergeAction.setEnabled(False)

For our action taking care of splitting merged cells, we need to, after creating a `QAction` for it, retrieve the cell of the table that has been right-clicked by the user. We do so by calling the table's `cellAt()` method and passing it our cursor object. Then, we check if the row and column span of this cell is more than one, in which case it would have been previously merged with other cells. If so, we connect the `triggered` signal of our splitting action to a lambda expression again, in which we call our table's `splitCell()` method. We pass this method the merged cell's row and column indices as well as the row and column spans of the to-be-split cells. By making the last two parameters 1, we split the merged cells into individual cells again. I think this is the behaviour most people would expect. You could, of course, pop up a question box where the user inserts the new span values, but I believe this will do fine for now. If the cell beneath the cursor has a row or column span of one, it hasn't been merged so we disable the split action:


    splitAction = QtGui.QAction("Split cells",self)

    cell = table.cellAt(cursor)

    # Only allow splitting if the current cell is larger
    # than a normal cell
    if cell.rowSpan() > 1 or cell.columnSpan() > 1:

        splitAction.triggered.connect(lambda: table.splitCell(cell.row(),cell.column(),1,1))

    else:
        splitAction.setEnabled(False)


We then add all of these actions to our `QMenu` object and add separators between logically connected actions, such as between those handling appending rows/columns and those for removing:


    menu.addAction(appendRowAction)
    menu.addAction(appendColAction)

    menu.addSeparator()

    menu.addAction(removeRowAction)
    menu.addAction(removeColAction)

    menu.addSeparator()

    menu.addAction(insertRowAction)
    menu.addAction(insertColAction)

    menu.addSeparator()

    menu.addAction(mergeAction)
    menu.addAction(splitAction)

One tricky issue with creating custom context menus is positioning it. As you may have noticed, our `self.context()` method has a second parameter, `pos`. PyQt passes us a `QPoint` object which holds the coordinates of where the user right-clicked in our `QTextEdit`. However, there is one big problem: this `QPoint` PyQt hands us doesn't take our tool and format bars into account! The table cell may be positioned at (0,0) within the `QTextEdit` but in terms of window coordinates, its real coordinates are in fact (0,90), as our toolbars, if not customized, are 45 pixels long. To solve this problems, we need to check whether the toolbars are visible, as the user may have toggled their visibility, and add 45 pixels per visible toolbar to our `QPoint` object's y coordinate. Also, we need to convert the coordinates from `QTextEdit` coordinates to global ones, which we achieve via our window's `mapToGlobal()` method. We then re-position our menu with its `move()` method and finally display it by calling `show()`:

    # Convert the widget coordinates into global coordinates
    pos = self.mapToGlobal(pos)

    # Add pixels for the tool and format bars, which are not included
    # in mapToGlobal(), but only if the two are currently visible and
    # not toggled by the user

    if self.toolbar.isVisible():
        pos.setY(pos.y() + 45)

    if self.formatbar.isVisible():
        pos.setY(pos.y() + 45)


    # Move the menu to the new position
    menu.move(pos)

    menu.show()

That's it for `context()`. Let's move on to the slot functions we connected our context menu actions to. They're fairly similar to each other, so I'll just discuss one. In `removeRow()`, the method that removes the row the user's cursor is over, we grab our `QTextEdit`'s cursor, the cursor's current table and the table's current cell. We then remove the row by calling the table's `removeRows()` method and passing it the cell's `row()` number along with the number 1, thus removing only the current row (passing a higher number removes `n` rows starting at the cell's row index):

    def removeRow(self):

        # Grab the cursor
        cursor = self.text.textCursor()

        # Grab the current table (we assume there is one, since
        # this is checked before calling)
        table = cursor.currentTable()

        # Get the current cell
        cell = table.cellAt(cursor)

        # Delete the cell's row
        table.removeRows(cell.row(),1)

The other slot methods only differ in the functions we call, I'm sure you'll understand them. That's it for tables!

## A final add-on

After finishing part one of this series, I noticed that there was no way of prompting the user about saving a a modified document before closing. Let's change that. In `writer.py`:

__In `__init__()`, add this__:

    self.changesSaved = True

__In `initUI()`, add this__:

    self.text.textChanged.connect(self.changed)

__Below `initUI`__:

    def changed(self):
        self.changesSaved = False

    def closeEvent(self,event):

        if self.changesSaved:

            event.accept()

        else:

            popup = QtGui.QMessageBox(self)

            popup.setIcon(QtGui.QMessageBox.Warning)

            popup.setText("The document has been modified")

            popup.setInformativeText("Do you want to save your changes?")

            popup.setStandardButtons(QtGui.QMessageBox.Save    |
                                      QtGui.QMessageBox.Cancel |
                                      QtGui.QMessageBox.Discard)

            popup.setDefaultButton(QtGui.QMessageBox.Save)

            answer = popup.exec_()

            if answer == QtGui.QMessageBox.Save:
                self.save()

            elif answer == QtGui.QMessageBox.Discard:
                event.accept()

            else:
                event.ignore()

__At the end of `self.save()`, insert this line__:

    self.changesSaved = True

In `__init__()`, we create a new class member, `self.changesSaved`, that'll store a boolean indicating whether or not the current document's changes have been saved or not. Then, in `initUI()`, we connect our `QTextEdit`'s `textChanged` signal to a slot function, `self.changed()`, in which we set our `self.changesSaved` member to `False`, signifying that there are unsaved modifications. We can't use a lambda expression for this slot function, as you can't assign anything in a lambda expression.

Next, we need to re-define our window's `closeEvent()` method which takes a `QCloseEvent` as its only argument. This function will be called when the user attempts to close the window. Normally this method just calls the `QCloseEvent`'s `accept()` method, which then closes the window. In our case, however, we want to check if there are any unsaved modifications to the document. If not, we also call `event.accept()` and just close our application. If there are changes, however, we'll want to inform the user about this, which we do by popping up a message box. Therefore, we create a `QMessageBox` object, give it an icon like we did for the table dialog's message box, set its "headline" text using the `setText()` method and add some further clarification using `setInformativeText()`. We then give this dialog some buttons using the `setStandardButtons()` method, namely one for saving the document, one for canceling the closing of the window and one for discarding the changes and closing the document without saving. After displaying the message box by calling its `exec_()` method, which returns the user's choice, we act accordingly by either saving the document, discarding changes by accepting the event or aborting the closing of the window by calling the event's `ignore()` method.

Lastly, we set the `self.changesSaved` variable to `True` in the `self.save()` method, ensuring that the message box doesn't pop if the user has already saved his or her changes.

# Thank you

That's it for this part and, unfortunately, also for this series on __*Building a text editor with PyQt*__. I hope you learnt a lot and enjoyed building this text editor with me!

__*But hey, who says it should end here? There's so much potential! If you have any ideas or suggestions on how to improve Writer, don't hesitate to fork or clone this project on [GitHub](https://github.com/goldsborough/Writer-Tutorial). Change its layout, add some color, improve features and add a few of your own!*__

Cheers!
