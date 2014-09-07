In part one of this tutorial series on __*Building a text editor with PyQt*__, we built a basic text editor skeleton and already added features for file management, list insertion, undo/redo and more. In part two, we turned our text editor into a rich-text editor by adding actions for text-formatting. In the third and subsequently the fourth part of this series, we'll be adding some extremely cool extensions to our text editor for:

+ Finding and replacing text
+ Inserting an image
+ Word and symbol count
+ Creating and managing tables
+ Inserting time and date

This part will deal with the first three extensions and in the fourth and final part I'll discuss the remaining two.

## Directory structure

For most of the above actions, we'll be creating dialog classes in separate files, meaning we need a new folder for all of these new files. Create a folder in your working directory called "ext" (for extensions) and in it create an empty file called `__init__.py`. This will turn our folder into a Python package.


Your working directory should look somewhat like this now:

    writer.py
    icons/
      lots of icons
    ext/
      __init__.py


## Find-and-replace

First up, we'll handle our find-and-replace dialog. PyQt unfortunately has no methods of its own for finding and replacing text in a QTextEdit, therefore we'll be doing a lot ourselves for this one.

__In your `ext` folder, create a new file called `find.py`__:

    from PyQt4 import QtGui, QtCore
    from PyQt4.QtCore import Qt

    import re

    class Find(QtGui.QDialog):
        def __init__(self, parent = None):

            QtGui.QDialog.__init__(self, parent)

            self.parent = parent

            self.lastMatch = None

            self.initUI()

        def initUI(self):

            # Button to search the document for something
            findButton = QtGui.QPushButton("Find",self)
            findButton.clicked.connect(self.find)

            # Button to replace the last finding
            replaceButton = QtGui.QPushButton("Replace",self)
            replaceButton.clicked.connect(self.replace)

            # Button to remove all findings
            allButton = QtGui.QPushButton("Replace all",self)
            allButton.clicked.connect(self.replaceAll)

            # Normal mode - radio button
            self.normalRadio = QtGui.QRadioButton("Normal",self)
            self.normalRadio.toggled.connect(self.normalMode)

            # Regular Expression Mode - radio button
            self.regexRadio = QtGui.QRadioButton("RegEx",self)
            self.regexRadio.toggled.connect(self.regexMode)

            # The field into which to type the query
            self.findField = QtGui.QTextEdit(self)
            self.findField.resize(250,50)

            # The field into which to type the text to replace the
            # queried text
            self.replaceField = QtGui.QTextEdit(self)
            self.replaceField.resize(250,50)

            optionsLabel = QtGui.QLabel("Options: ",self)

            # Case Sensitivity option
            self.caseSens = QtGui.QCheckBox("Case sensitive",self)

            # Whole Words option
            self.wholeWords = QtGui.QCheckBox("Whole words",self)

            # Layout the objects on the screen
            layout = QtGui.QGridLayout()

            layout.addWidget(self.findField,1,0,1,4)
            layout.addWidget(self.normalRadio,2,2)
            layout.addWidget(self.regexRadio,2,3)
            layout.addWidget(findButton,2,0,1,2)

            layout.addWidget(self.replaceField,3,0,1,4)
            layout.addWidget(replaceButton,4,0,1,2)
            layout.addWidget(allButton,4,2,1,2)

            # Add some spacing
            spacer = QtGui.QWidget(self)

            spacer.setFixedSize(0,10)

            layout.addWidget(spacer,5,0)

            layout.addWidget(optionsLabel,6,0)
            layout.addWidget(self.caseSens,6,1)
            layout.addWidget(self.wholeWords,6,2)

            self.setGeometry(300,300,360,250)
            self.setWindowTitle("Find and Replace")
            self.setLayout(layout)

            # By default the normal mode is activated
            self.normalRadio.setChecked(True)

        def find(self):

            # Grab the parent's text
            text = self.parent.text.toPlainText()

            # And the text to find
            query = self.findField.toPlainText()

            # If the 'Whole Words' checkbox is checked, we need to append
            # and prepend a non-alphanumeric character
            if self.wholeWords.isChecked():
                query = r'\W' + query + r'\W'

            # By default regexes are case sensitive but usually a search isn't
            # case sensitive by default, so we need to switch this around here
            flags = 0 if self.caseSens.isChecked() else re.I

            # Compile the pattern
            pattern = re.compile(query,flags)

            # If the last match was successful, start at position after the last
            # match's start, else at 0
            start = self.lastMatch.start() + 1 if self.lastMatch else 0

            # The actual search
            self.lastMatch = pattern.search(text,start)

            if self.lastMatch:

                start = self.lastMatch.start()
                end = self.lastMatch.end()

                # If 'Whole words' is checked, the selection would include the two
                # non-alphanumeric characters we included in the search, which need
                # to be removed before marking them.
                if self.wholeWords.isChecked():
                    start += 1
                    end -= 1

                self.moveCursor(start,end)

            else:

                # We set the cursor to the end if the search was unsuccessful
                self.parent.text.moveCursor(QtGui.QTextCursor.End)

        def replace(self):

            # Grab the text cursor
            cursor = self.parent.text.textCursor()

            # Security
            if self.lastMatch and cursor.hasSelection():

                # We insert the new text, which will override the selected
                # text
                cursor.insertText(self.replaceField.toPlainText())

                # And set the new cursor
                self.parent.text.setTextCursor(cursor)

        def replaceAll(self):

            # Set lastMatch to None so that the search
            # starts from the beginning of the document
            self.lastMatch = None

            # Initial find() call so that lastMatch is
            # potentially not None anymore
            self.find()

            # Replace and find until find is None again
            while self.lastMatch:
                self.replace()
                self.find()

        def regexMode(self):

            # First uncheck the checkboxes
            self.caseSens.setChecked(False)
            self.wholeWords.setChecked(False)

            # Then disable them (gray them out)
            self.caseSens.setEnabled(False)
            self.wholeWords.setEnabled(False)

        def normalMode(self):

            # Enable checkboxes (un-gray them)
            self.caseSens.setEnabled(True)
            self.wholeWords.setEnabled(True)

        def moveCursor(self,start,end):

            # We retrieve the QTextCursor object from the parent's QTextEdit
            cursor = self.parent.text.textCursor()

            # Then we set the position to the beginning of the last match
            cursor.setPosition(start)

            # Next we move the Cursor by over the match and pass the KeepAnchor parameter
            # which will make the cursor select the the match's text
            cursor.movePosition(QtGui.QTextCursor.Right,QtGui.QTextCursor.KeepAnchor,end - start)

            # And finally we set this new cursor as the parent's
            self.parent.text.setTextCursor(cursor)

__And insert this line in `__init__.py`__:

  	__all__ = ["find"]

__Back to `writer.py`. At the top of the file__:

	  from ext import *

__In `initToolbar()`__:

    self.findAction = QtGui.QAction(QtGui.QIcon("icons/find.png"),"Find and replace",self)
    self.findAction.setStatusTip("Find and replace words in your document")
    self.findAction.setShortcut("Ctrl+F")
    self.findAction.triggered.connect(find.Find(self).show)

__Further below__:

    self.toolbar.addSeparator()

    self.toolbar.addAction(self.findAction)

__In `initMenubar()`__:

    edit.addAction(self.findAction)

Woah! That was a lot! No worries, I'll explain everything.

First, the easy stuff. In `ext/__init__.py`, we inserted the only line this file will ever contain: `__all__ = ["find"]`. This enables us to import from our `ext` package using the asterix symbol (`*`), which imports all modules that are inside `__all__`. Therefore, at the top of `writer.py`, we can now write `from ext import *`, which is currently equivalent to `from ext import find`, but will be a lot more efficient once we have more modules in our package.

Further down in `writer.py`, more precisely in our toolbar initialization method, `initToolbar()`, we, as we've done many times for our text editor, create a `QAction`, set up a status tip as well as a shortcut and also connect the `triggered` signal to a slot function. In this case, all we need to do is create an instance of the `Find` class (which I'll get to in a bit) and call its `show()` method. Fortunately, this all fits into one line and doesn't require us to create a separate method. In `initMenubar()`, we add this action to the `edit` menu.

### Initializing the UI

Now to our `Find` class in `find.py`. We start out like we did for our main window. First, we import the necessary modules from PyQt as well as the `re` module, which we'll use for text search. Next, we create a class and let it inherit from one of PyQt's GUI windows. In this case, we're going to inherit from `QDialog` instead of from `QMainWindow`, because, well, it's a dialog and not our main window. In the constructor, `__init__()`, we make the parent object a member (we pass `Find`'s constructor `self` in `Main.initToolbar()`). Moreover, we need another class member, `self.lastMatch`, which will store the last found match (more about it soon).

In `initUI()`, we take care of the graphical part of our find-and-replace dialog. We'll create three push-buttons, one for finding text, one for replacing a single occurence and a last one for replacing all occurences. We create non-member instances of our buttons and connect their `clicked` signals to slot functions that we'll discuss in a bit:

    # Button to search the document for something
    findButton = QtGui.QPushButton("Find",self)
    findButton.clicked.connect(self.find)

    # Button to replace the last finding
    replaceButton = QtGui.QPushButton("Replace",self)
    replaceButton.clicked.connect(self.replace)

    # Button to remove all findings
    allButton = QtGui.QPushButton("Replace all",self)
    allButton.clicked.connect(self.replaceAll)

Next, we create two radio buttons that'll enable the user to switch between regular expression finding mode and normal, plain-text, finding mode. We make them class members, because we need to access their states later on, and connect their `toggled` signals to slot functions, as for the buttons above:

    # Normal mode - radio button
    self.normalRadio = QtGui.QRadioButton("Normal",self)
    self.normalRadio.toggled.connect(self.normalMode)

    # Regular Expression Mode - radio button
    self.regexRadio = QtGui.QRadioButton("RegEx",self)
    self.regexRadio.toggled.connect(self.regexMode)

Then, we create two text fields. One where the user inputs text that he or she would like to find and another for the text the user'd like to replace occurences with. We resize both text fields to 250x50 pixels:

    # The field into which to type the query
    self.findField = QtGui.QTextEdit(self)
    self.findField.resize(250,50)

    # The field into which to type the text to replace the
    # queried text
    self.replaceField = QtGui.QTextEdit(self)
    self.replaceField.resize(250,50)

Almost done. We want to also provide the user with some search options, namely case-sensitivy control and a "Whole word" flag, which only highlights occurences that have non-alphanumeric characters to their left and right. For example, "I like cat soup" would pass the "Whole word" check for the word "cat" because the word "cat" is not part of another word. In "I greatly enjoy concatenating strings", the string "cat" would be highlighted if the "whole words" flag is unchecked, but would be ignored if the user only wants "whole words". The code for this is very simple, the only important things is that these `QCheckBox`es are class members so we can check their states later on. Also, we create a `QLabel` that will hold the string "Options:", just for visual clarity:

    optionsLabel = QtGui.QLabel("Options: ",self)

    # Case Sensitivity option
    self.caseSens = QtGui.QCheckBox("Case sensitive",self)

    # Whole Words option
    self.wholeWords = QtGui.QCheckBox("Whole words",self)

Now we need to order all of these widgets on our dialog. We do so by creating a `QGridLayout` and adding the widgets we just created using the `QGridLayout`'s `addWidget()` method, which takes the widget to add, the row, column, row-span and column-span in the layout as its arguments. Note that I create a "spacer" widget which is just a plain `QWidget` with a fixed size of 0 by 10 pixels. We insert this spacer to add some distance between the replace buttons and our options:

    # Layout the objects on the screen
    layout = QtGui.QGridLayout()

    layout.addWidget(self.findField,1,0,1,4)
    layout.addWidget(self.normalRadio,2,2)
    layout.addWidget(self.regexRadio,2,3)
    layout.addWidget(findButton,2,0,1,2)

    layout.addWidget(self.replaceField,3,0,1,4)
    layout.addWidget(replaceButton,4,0,1,2)
    layout.addWidget(allButton,4,2,1,2)

    # Add some spacing
    spacer = QtGui.QWidget(self)

    spacer.setFixedSize(0,10)

    layout.addWidget(spacer,5,0)

    layout.addWidget(optionsLabel,6,0)
    layout.addWidget(self.caseSens,6,1)
    layout.addWidget(self.wholeWords,6,2)

Lastly, some window settings. We set our dialog's geometry settings, give it a window title and set our newly created layout as the dialog's layout. Also, we want to activate our `normalRadio` checkbox initially:

    self.setGeometry(300,300,360,250)
    self.setWindowTitle("Find and Replace")
    self.setLayout(layout)

    # By default the normal mode is activated
    self.normalRadio.setChecked(True)

### Raiders of the lost text

Now that we have an interface, we can make our dialog ... do something. As a start, I'll discuss `find()` line by line. The first thing this method needs to do is get the text in which we'll look for queries, our main window's `QTextEdit`, and find out what text the user wants to find, which we get from our `findField`:

    # Grab the parent's text
    text = self.parent.text.toPlainText()

    # And the text to find
    query = self.findField.toPlainText()

Then, we need to check whether the user has ticked any options. Note that we will use Python's regular expression engine to do our searching. If the user wants only whole words, we append and prepend a `'\W'` character, which matches any non-alphanumeric character such as a space or any form of punctuation. After checking for the case-sensitivy flag, we compile our regular expression. To find out where we need to start our search in the text, we check if the `self.lastMatch` object is not `None`. If it isn't, we can use the last match's starting position and increment it by one for our new search. If `self.lastMatch` is `None`, however, we re-start from index 0. Note that Python's regex functions return `None` if no match was found for a regular expression, meaning that this way of resetting the search index to 0 will work in such a way that if the user searches the text to its end, the search starts all over again, which is great. Lastly, we do the actual search:

    # If the 'Whole Words' checkbox is checked, we need to append
    # and prepend a non-alphanumeric character
    if self.wholeWords.isChecked():
        query = r'\W' + query + r'\W'

    # By default regexes are case sensitive but usually a search isn't
    # case sensitive by default, so we need to switch this around here
    flags = 0 if self.caseSens.isChecked() else re.I

    # Compile the pattern
    pattern = re.compile(query,flags)

    # If the last match was successful, start at position after the last
    # match's start, else at 0
    start = self.lastMatch.start() + 1 if self.lastMatch else 0

    # The actual search
    self.lastMatch = pattern.search(text,start)

If the search was succesful, we need to highlight the match. We have to do this manually using our main window's `QTextEdit`'s `QTextCursor` again, but more about that in a bit. If the user had the "whole word" flag checked, this means that the match also includes the two non-alphanumeric characters that we included in the search. Would we leave the indices like this, replacing the matched text would mean also replacing the spaces or punctuation around the actual matched text, which would make our users frustrated and make them hate us, which in turn would make us very sad. To keep everyone happy and loving, we increment the starting position and decrement the ending index of our match. If the search was unsuccessful, we set the cursor to the end of the text:

    if self.lastMatch:

        start = self.lastMatch.start()
        end = self.lastMatch.end()

        # If 'Whole words' is checked, the selection would include the two
        # non-alphanumeric characters we included in the search, which need
        # to be removed before marking them.
        if self.wholeWords.isChecked():
            start += 1
            end -= 1

        self.moveCursor(start,end)

    else:

        # We set the cursor to the end if the search was unsuccessful
        self.parent.text.moveCursor(QtGui.QTextCursor.End)

### Highlights

Because we just used the `self.moveCursor()` method in `find()`, I'll talk about that next. As commented, *We retrieve the QTextCursor object from the parent's QTextEdit* and *Then we set the position to the beginning of the last match*. *Next we move the Cursor over the match and pass the KeepAnchor parameter which will make the cursor select the match's text*. *And finally we set this new cursor as the parent's*:

    def moveCursor(self,start,end):

      # We retrieve the QTextCursor object from the parent's QTextEdit
      cursor = self.parent.text.textCursor()

      # Then we set the position to the beginning of the last match
      cursor.setPosition(start)

      # Next we move the Cursor over the match and pass the KeepAnchor parameter
      # which will make the cursor select the match's text
      cursor.movePosition(QtGui.QTextCursor.Right,QtGui.QTextCursor.KeepAnchor,end - start)

      # And finally we set this new cursor as the parent's
      self.parent.text.setTextCursor(cursor)

### Replacing

Now that we managed to find text and highlight it, we'll want to also handle our slot functions that take care of replacing the matched text. In `replace()`, we again grab our parent's `QTextCursor` object. Then, we ensure

1. That the last match was succesful and `self.lastMatch` is not `None`
2. The cursor currently has a selection

If those two conditions are met, we can use the cursor's `insertText()` method and retrieve the text we want to replace our match with from the replace field. Because the cursor has a selection, it will replace the selected text with the new text. Finally, we reset our cursor:

        def replace(self):

            # Grab the text cursor
            cursor = self.parent.text.textCursor()

            # Security
            if self.lastMatch and cursor.hasSelection():

                # We insert the new text, which will override the selected
                # text
                cursor.insertText(self.replaceField.toPlainText())

                # And set the new cursor
                self.parent.text.setTextCursor(cursor)

### Replace all the occurences!

To replace all the occurences of a query in the text, we need to first reset our `self.lastMatch` member to None and call `find()`, so that the search will begin from the start of the text. Then, if the first match was successful, we enter a loop that will replace and find occurences as long as `self.lastMatch` is not `None`, so as long as the search doesn't hit the end of the text.

        def replaceAll(self):

            # Set lastMatch to None so that the search
            # starts from the beginning of the document
            self.lastMatch = None

            # Initial find() call so that lastMatch is
            # potentially not None anymore
            self.find()

            # Replace and find until find is None again
            while self.lastMatch:
                self.replace()
                self.find()

### Some last slots

The last two functions we need for our `Find` class are the handlers for the search mode (normal or regex):

        def regexMode(self):

            # First uncheck the checkboxes
            self.caseSens.setChecked(False)
            self.wholeWords.setChecked(False)

            # Then disable them (gray them out)
            self.caseSens.setEnabled(False)
            self.wholeWords.setEnabled(False)

        def normalMode(self):

            # Enable checkboxes (un-gray them)
            self.caseSens.setEnabled(True)
            self.wholeWords.setEnabled(True)

Regex mode means that the search flags are unnecessary, since the user will want to input flags using regular expressions him- or herself. Therefore, we uncheck the check boxes and also disable them, which will "gray" them out.

For `normalMode()`, we simply re-enable the check boxes.

So much for our find-and-replace dialog! Next up:

## Image insertion

Image insertion does not require a class of its own, so we'll stick around `writer.py` for this one. In fact, all we need is a `QAction` in `initToolbar()`:

    imageAction = QtGui.QAction(QtGui.QIcon("icons/image.png"),"Insert image",self)
    imageAction.setStatusTip("Insert image")
    imageAction.setShortcut("Ctrl+Shift+I")
    imageAction.triggered.connect(self.insertImage)

    self.toolbar.addAction(imageAction)

And a slot function, `self.insertImage()`. In it, we open a `getOpenFileName` dialog like we did for opening a `.writer` file in the very beginning, from which we retrieve a file name. For the file dialog's filter, we include common image formats. If we got a file name, we create a `QImage` and, if it was loadable (`isNull` == False), we insert it using our `QTextCursor`'s `insertImage()` method. If it wasn't loadable, we pop up a `QMessageBox`. The constructor of this `QMessageBox` requires an icon from the QMessageBox namespace (either a question, information, warning or "critical" icon), a window title, the message to display, a set of buttons to show and lastly a parent object:

    def insertImage(self):

        # Get image file name
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Insert image',".","Images (*.png *.xpm *.jpg *.bmp *.gif)")

        # Create image object
        image = QtGui.QImage(filename)

        # Error if unloadable
        if image.isNull():

            popup = QtGui.QMessageBox(QtGui.QMessageBox.Critical,
                                      "Image load error",
                                      "Could not load image file!",
                                      QtGui.QMessageBox.Ok,
                                      self)
            popup.show()

        else:

            cursor = self.text.textCursor()

            cursor.insertImage(image,filename)

## Counting words

For the next extension, a word-count dialog that'll display the number of words and symbols in the document's selected and total text, we'll create a new class in a separate file again. So, in

__`ext/wordcount.py`__:

    from PyQt4 import QtGui, QtCore
    from PyQt4.QtCore import Qt

    class WordCount(QtGui.QDialog):
        def __init__(self,parent = None):
            QtGui.QDialog.__init__(self, parent)

            self.parent = parent

            self.initUI()

        def initUI(self):

            # Word count in selection
            currentLabel = QtGui.QLabel("Current selection",self)
            currentLabel.setStyleSheet("font-weight:bold; font-size: 15px;")

            currentWordsLabel = QtGui.QLabel("Words: ", self)
            currentSymbolsLabel = QtGui.QLabel("Symbols: ",self)

            self.currentWords = QtGui.QLabel(self)
            self.currentSymbols = QtGui.QLabel(self)

            # Total word/symbol count
            totalLabel = QtGui.QLabel("Total",self)
            totalLabel.setStyleSheet("font-weight:bold; font-size: 15px;")

            totalWordsLabel = QtGui.QLabel("Words: ", self)
            totalSymbolsLabel = QtGui.QLabel("Symbols: ",self)

            self.totalWords = QtGui.QLabel(self)
            self.totalSymbols = QtGui.QLabel(self)

            # Layout

            layout = QtGui.QGridLayout(self)

            layout.addWidget(currentLabel,0,0)

            layout.addWidget(currentWordsLabel,1,0)
            layout.addWidget(self.currentWords,1,1)

            layout.addWidget(currentSymbolsLabel,2,0)
            layout.addWidget(self.currentSymbols,2,1)

            spacer = QtGui.QWidget()
            spacer.setFixedSize(0,5)

            layout.addWidget(spacer,3,0)

            layout.addWidget(totalLabel,4,0)

            layout.addWidget(totalWordsLabel,5,0)
            layout.addWidget(self.totalWords,5,1)

            layout.addWidget(totalSymbolsLabel,6,0)
            layout.addWidget(self.totalSymbols,6,1)

            self.setWindowTitle("Word count")
            self.setGeometry(300,300,200,200)
            self.setLayout(layout)

        def getText(self):

            # Get the text currently in selection
            text = self.parent.text.textCursor().selectedText()

            # Split the text to get the word count
            words = str(len(text.split()))

            # And just get the length of the text for the symbols
            # count
            symbols = str(len(text))

            self.currentWords.setText(words)
            self.currentSymbols.setText(symbols)

            # For the total count, same thing as above but for the
            # total text

            text = self.parent.text.toPlainText()

            words = str(len(text.split()))
            symbols = str(len(text))

            self.totalWords.setText(words)
            self.totalSymbols.setText(symbols)

__And in `__init__.py`__:

    __all__ = ["find","wordcount"]


__Back to `writer.py`. In `initToolbar()`__:

    wordCountAction = QtGui.QAction(QtGui.QIcon("icons/count.png"),"See word/symbol count",self)
    wordCountAction.setStatusTip("See word/symbol count")
    wordCountAction.setShortcut("Ctrl+W")
    wordCountAction.triggered.connect(self.wordCount)

    self.toolbar.addAction(wordCountAction)

__Below `initUI()`__:

    def wordCount(self):

        wc = wordcount.WordCount(self)

        wc.getText()

        wc.show()

As mentioned, this dialog will show the user the number of words and symbols currently under selection (if there is a selection) and also the number of words and symbols in the entire document. The UI is fairly simple. We create labels that indicate whether the numbers shown are for the current selection or the whole text, `currentLabel` and `totalLabel`, as well as two labels each that hold the strings "Words:" and "Symbols:", plus two labels each in which we'll show the actual numbers (these must be class members):

        # Word count in selection
        currentLabel = QtGui.QLabel("Current selection",self)
        currentLabel.setStyleSheet("font-weight:bold; font-size: 15px;")

        currentWordsLabel = QtGui.QLabel("Words: ", self)
        currentSymbolsLabel = QtGui.QLabel("Symbols: ",self)

        self.currentWords = QtGui.QLabel(self)
        self.currentSymbols = QtGui.QLabel(self)

        # Total word/symbol count
        totalLabel = QtGui.QLabel("Total",self)
        totalLabel.setStyleSheet("font-weight:bold; font-size: 15px;")

        totalWordsLabel = QtGui.QLabel("Words: ", self)
        totalSymbolsLabel = QtGui.QLabel("Symbols: ",self)

        self.totalWords = QtGui.QLabel(self)
        self.totalSymbols = QtGui.QLabel(self)

We put them into a layout and set the dialog's geometry and window title:

        # Layout

        layout = QtGui.QGridLayout(self)

        layout.addWidget(currentLabel,0,0)

        layout.addWidget(currentWordsLabel,1,0)
        layout.addWidget(self.currentWords,1,1)

        layout.addWidget(currentSymbolsLabel,2,0)
        layout.addWidget(self.currentSymbols,2,1)

        spacer = QtGui.QWidget()
        spacer.setFixedSize(0,5)

        layout.addWidget(spacer,3,0)

        layout.addWidget(totalLabel,4,0)

        layout.addWidget(totalWordsLabel,5,0)
        layout.addWidget(self.totalWords,5,1)

        layout.addWidget(totalSymbolsLabel,6,0)
        layout.addWidget(self.totalSymbols,6,1)

        self.setWindowTitle("Word count")
        self.setGeometry(300,300,200,200)
        self.setLayout(layout)

The function that will count all of these words and symbols is `getText()`. First, we want to count the words and symbols of the selected text, which we get by grabbing our `QTextEdit`'s `QTextCursor` and calling its `selectedText()` method. We use the retrieved string's `split()` method to split the string into a list of individual words, of which we then get the length. The number of symbols is simply the length of the entire string. We then visualize the two numbers we just got using the respective labels' `setText()` method. We repeat this process for the whole text and again set the counts we retrieved to the respective labels' text:

        def getText(self):

            # Get the text currently in selection
            text = self.parent.text.textCursor().selectedText()

            # Split the text to get the word count
            words = str(len(text.split()))

            # And just get the length of the text for the symbols
            # count
            symbols = str(len(text))

            self.currentWords.setText(words)
            self.currentSymbols.setText(symbols)

            # For the total count, same thing as above but for the
            # total text

            text = self.parent.text.toPlainText()

            words = str(len(text.split()))
            symbols = str(len(text))

            self.totalWords.setText(words)
            self.totalSymbols.setText(symbols)

In `writer.py`, we again create a `QAction` for our word count dialog and add it to the toolbar. In the slot function, `self.wordCount()`, we create an instance of our `WordCount` class, call its `getText()` method and finally show the dialog.

That'll be it for this part of the series. In the next part, we'll be adding some more awesome extensions for inserting the current time and date into the text as well as a more sophisticated dialog for inserting tables. Moreover, I'll show you how to enable custom context menus that will enable us to manipulate the tables we insert into the text (adding/deleting/merging rows and columns).

In the meantime, don't hesitate to leave me a comment below this post. See you next week!
