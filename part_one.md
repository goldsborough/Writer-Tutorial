# Developing a PyQt text editor

I have always enjoyed building beautiful Graphical User Interfaces (GUIs) to the back-end computations, number-crunching and algorithms of my programs. For Python, my GUI library of choice is the Python binding for Qt, __PyQt__. This tutorial will show you how you can use PyQt to build a simple but useful rich-text editor. The first part of the tutorial will focus on the core features and skeleton of the editor. In the second part of the tutorial we'll take care of text-formatting and in the third part we'll add some useful extensions like a find-and-replace dialog, support for tables and more.

Before we get started, two things:

+ You can find and download the finished source code on GitHub: https://github.com/goldsborough/Writer

+ If you don`t already have PyQt installed, you can go grab it from the official website: http://www.riverbankcomputing.co.uk/software/pyqt/intro


Once you`re set up and ready to go, we can embark on our journey to create a totally awesome text editor.

##An empty canvas

We start out with an empty canvas, a bare-minimum PyQt application:

```Python

import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

class Main(QtGui.QMainWindow):

    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self,parent)

        self.initUI()

    def initUI(self):

        # x and y coordinates on the screen, width, height
        self.setGeometry(100,100,1030,800)

        self.setWindowTitle("Writer")

def main():

    app = QtGui.QApplication(sys.argv)

    main = Main()
    main.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

```

The first thing we need to do is import the sys module, which PyQt needs to start our application, as well as all the necessary modules from the PyQt4 package (PyQt5 if you have the newer version). We'll call our class `Main` and let it inherit from PyQt's QMainWindow class. In the `__init__` method, we initialize the parent class as well as all the UI settings for our application. The latter we just pack into the `initUI()` method. At the moment, the only settings we need are those concerning position on the screen, the size of the window and the window's title. We can set the first two using the `setGeometry()` method, which lets us set the x and y coordinates of the window on the screen, the width and lastly its height. We also set our application's window title using the `setWindowTitle()` method. For simplicity, we'll just call our text editor _Writer_.

Lastly, we need a `main` function that takes care of instantiating and displaying our window. We do so by creating a new `Main`
object and calling its `show()` method.

## And there was text

Now that we have a basic PyQt application up and running, we can start making it look more like a text editor:

```Python
def initToolbar(self):

  self.toolbar = self.addToolBar("Options")

  # Makes the next toolbar appear underneath this one
  self.addToolBarBreak()

def initFormatbar(self):

  self.formatbar = self.addToolBar("Format")

def initMenubar(self):

  menubar = self.menuBar()

  file = menubar.addMenu("File")
  edit = menubar.addMenu("Edit")
  view = menubar.addMenu("View")

def initUI(self):

    self.text = QtGui.QTextEdit(self)
    self.setCentralWidget(self.text)

    self.initToolbar()
    self.initFormatbar()
    self.initMenubar()

    # Initialize a statusbar for the window
    self.statusbar = self.statusBar()

    # x and y coordinates on the screen, width, height

    self.setGeometry(100,100,1030,800)

    self.setWindowTitle("Writer")
```

I left out everything that stayed unchanged from the previous code. As you can see in the `initUI()` function, we first create a QTextEdit object and set it to our window's "central widget". This makes the QTextEdit object take up the window's entire space. Next up, we need to create three more methods: `initToolbar()`, `initFormatbar()` and `initMenubar()`. The first two methods create toolbars that will appear at the top of our window and contain our text editor's features, such as those concerning file management (opening a file, saving a file etc.) or text-formatting. The last method, `initMenubar()` creates a set of drop-down menus at the top of the screen.

As of now, the methods contain only the code necessary to make them appear. For the `initToolbar()` and `initFormatbar()` methods, this means creating a new toolbar object by calling our window's `addToolBar()` method and passing it the name of the toolbar we're creating. Note that in the `initToolbar()` method, we need to also call the `addToolBarBreak()` method. This makes the next toolbar, the format bar, appear underneath this toolbar. In case of the menu bar, we call the window's `menuBar()` method and add three menus to it, "File", "Edit" and "View". We'll populate all of these toolbars and menus in a bit.

Lastly, in the `initUI()` method, we also create a status bar object. This will create a status bar at the bottom of our window.

## An icon is worth a thousand words

Before we start injecting some life into our text editor, we're going to need some icons for its various features. If you had a look at the GitHub repository I linked to at the top of this post, you might have noticed that it contains a folder full of icons. I recommend that you download the repo (if you haven't yet) and copy the icons folder into your working directory. The icons are from [iconmonstr](http://www.iconmonstr.com), completely free and require no attribution.

## File management

Now that we have a basic text editor skeleton in place, we can add some meat to the bone. We'll start with the functions concerning file management.

__`__init__()`__:

```Python
def __init__(self, parent = None):
    QtGui.QMainWindow.__init__(self,parent)

    self.filename = ""

    self.initUI()
```

__`initToolbar()`:__

```Python
def initToolbar(self):

  self.newAction = QtGui.QAction(QtGui.QIcon("icons/new.png"),"New",self)
  self.newAction.setStatusTip("Create a new document from scratch.")
  self.newAction.setShortcut("Ctrl+N")
  self.newAction.triggered.connect(self.new)

  self.openAction = QtGui.QAction(QtGui.QIcon("icons/open.png"),"Open file",self)
  self.openAction.setStatusTip("Open existing document")
  self.openAction.setShortcut("Ctrl+O")
  self.openAction.triggered.connect(self.open)

  self.saveAction = QtGui.QAction(QtGui.QIcon("icons/save.png"),"Save",self)
  self.saveAction.setStatusTip("Save document")
  self.saveAction.setShortcut("Ctrl+S")
  self.saveAction.triggered.connect(self.save)

  self.toolbar = self.addToolBar("Options")

  self.toolbar.addAction(self.newAction)
  self.toolbar.addAction(self.openAction)
  self.toolbar.addAction(self.saveAction)

  self.toolbar.addSeparator()

  # Makes the next toolbar appear underneath this one
  self.addToolBarBreak()
```

__`initMenubar()`__:

```Python
file.addAction(self.newAction)
file.addAction(self.openAction)
file.addAction(self.saveAction)
```

__Below the `initUI()` method:__

```Python
def new(self):

    spawn = Main(self)
    spawn.show()

def open(self):

    # Get filename and show only .writer files
    self.filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File',".","(*.writer)")

    if self.filename:
        with open(self.filename,"rt") as file:
            self.text.setText(file.read())

def save(self):

    # Only open dialog if there is no filename yet
    if not self.filename:
        self.filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File')

    # Append extension if not there yet
    if not self.filename.endswith(".writer"):
        self.filename += ".writer"

    # We just store the contents of the text file along with the
    # format in html, which Qt does in a very nice way for us
    with open(self.filename,"wt") as file:
        file.write(self.text.toHtml())
```

As you might have noticed, all the actions we'll be creating for our text editor follow the same code pattern:

+ Create a QAction and pass it an icon and a name

+ Create a status tip, which will display a message in the status bar (and a tool tip if you hover the action)

+ Create a shortcut

+ Connect the QAction's `triggered` signal to a slot function

Once you've done this for the "new", "open" and "save" actions, you can add them to the toolbar, using the toolbar's `addAction()` method. Make sure you also call the `addSeparator()` method, which inserts a separator line between toolbar actions. Because these three actions are responsible for file management, we want to add a separator here. Also, we want to add these three actions to the "file" menu, so in the `initMenubar()` method, we add the three actions to the appropriate menu.

Next up, we need to create the three slot functions that we connected to our action in the `initToolbar()` method. The `new()` method is very easy, all it does is create a new instance of our window and call its `show()` method to display it. 

Before we create the last two methods, let me mention that we'll use ".writer" as our text files' extensions. Now, for `open()`, we need to open PyQt's `getOpenFileName` dialog. This opens a file dialog which returns the name of the file the user opens. We also pass this method a title for the file dialog, in this case "Open File", the directory to open initially, "." (current directory) and finally a file filter, so that we only show ".writer" files. If the user didn't close or cancel the file dialog, we open the file and set its text to our text editor's current text.

Lastly, the `save()` method. We first check whether the current file already has a file name associated with it, either because it was opened with the `open()` method or already saved before, in case of a new text file. If this isn't the case, we open a `getSaveFileName`  dialog which will again return a filename for us, given the user doesn't cancel or close the file dialog. Once we have a file name, we need to check whether the user already entered our extension when saving the file. If not, we add the extension. Finally, we save our file in HTML format (which stores style as well), using the QTextEdit's `toHTML()` method.


## Printing

Next, we'll create some actions for printing and preview-ing our document.

__`initToolbar()`__:

```Python
self.printAction = QtGui.QAction(QtGui.QIcon("icons/print.png"),"Print document",self)
self.printAction.setStatusTip("Print document")
self.printAction.setShortcut("Ctrl+P")
self.printAction.triggered.connect(self.print)

self.previewAction = QtGui.QAction(QtGui.QIcon("icons/preview.png"),"Page view",self)
self.previewAction.setStatusTip("Preview page before printing")
self.previewAction.setShortcut("Ctrl+Shift+P")
self.previewAction.triggered.connect(self.preview)
```

__Further below__:

```Python
self.toolbar.addAction(self.printAction)
self.toolbar.addAction(self.previewAction)

self.toolbar.addSeparator()
```

__`initMenubar()`__:

```Python
file.addAction(self.printAction)
file.addAction(self.previewAction)
```

__Below the `initUI()` method:__

```Python
def preview(self):

    # Open preview dialog
    preview = QtGui.QPrintPreviewDialog()

    # If a print is requested, open print dialog
    preview.paintRequested.connect(lambda p: self.text.print_(p))

    preview.exec_()

def print(self):

    # Open printing dialog
    dialog = QtGui.QPrintDialog()

    if dialog.exec_() == QtGui.QDialog.Accepted:
        self.text.document().print_(dialog.printer())
```

We create the actions following the same scheme as we did for the file management actions and add them to our toolbar as well as the "file" menu. The `preview()` method opens a `QPrintPreviewDialog` and optionally prints the document, if the user wishes to do so. The `print()` method opens a `QPrintDialog` and prints the document if the user accepts.

## Copy and paste - undo and redo

These actions will let us copy, cut and paste text as well as undo/redo actions:

__`initToolbar()`__:

```Python
self.cutAction = QtGui.QAction(QtGui.QIcon("icons/cut.png"),"Cut to clipboard",self)
self.cutAction.setStatusTip("Delete and copy text to clipboard")
self.cutAction.setShortcut("Ctrl+X")
self.cutAction.triggered.connect(self.text.cut)

self.copyAction = QtGui.QAction(QtGui.QIcon("icons/copy.png"),"Copy to clipboard",self)
self.copyAction.setStatusTip("Copy text to clipboard")
self.copyAction.setShortcut("Ctrl+C")
self.copyAction.triggered.connect(self.text.copy)

self.pasteAction = QtGui.QAction(QtGui.QIcon("icons/paste.png"),"Paste from clipboard",self)
self.pasteAction.setStatusTip("Paste text from clipboard")
self.pasteAction.setShortcut("Ctrl+V")
self.pasteAction.triggered.connect(self.text.paste)

self.undoAction = QtGui.QAction(QtGui.QIcon("icons/undo.png"),"Undo last action",self)
self.undoAction.setStatusTip("Undo last action")
self.undoAction.setShortcut("Ctrl+Z")
self.undoAction.triggered.connect(self.text.undo)

self.redoAction = QtGui.QAction(QtGui.QIcon("icons/redo.png"),"Redo last undone thing",self)
self.redoAction.setStatusTip("Redo last undone thing")
self.redoAction.setShortcut("Ctrl+Y")
self.redoAction.triggered.connect(self.text.redo)
```

__Further below__:

```Python
self.toolbar.addAction(self.cutAction)
self.toolbar.addAction(self.copyAction)
self.toolbar.addAction(self.pasteAction)
self.toolbar.addAction(self.undoAction)
self.toolbar.addAction(self.redoAction)

self.toolbar.addSeparator()
```

__`initMenubar()`__:

```Python
edit.addAction(self.undoAction)
edit.addAction(self.redoAction)
edit.addAction(self.cutAction)
edit.addAction(self.copyAction)
edit.addAction(self.pasteAction)
```


As you can see, we don't need any separate slot functions for these actions, as our QTextEdit object already has very handy methods for all of these actions. Note that in the `initMenubar()` method, we add these actions to the "Edit" menu and not the "File" menu.

## Lists

Finally, we'll add two actions for inserting lists. One for numbered lists and one for bulleted lists:

__`initToolbar()`__:

```Python
bulletAction = QtGui.QAction(QtGui.QIcon("icons/bullet.png"),"Insert bullet List",self)
bulletAction.setStatusTip("Insert bullet list")
bulletAction.setShortcut("Ctrl+Shift+B")
bulletAction.triggered.connect(self.bulletList)

numberedAction = QtGui.QAction(QtGui.QIcon("icons/number.png"),"Insert numbered List",self)
numberedAction.setStatusTip("Insert numbered list")
numberedAction.setShortcut("Ctrl+Shift+L")
numberedAction.triggered.connect(self.numberList)
```

__Further below__:

```Python
self.toolbar.addAction(bulletAction)
self.toolbar.addAction(numberedAction)
```

__Below the `initUI()` method:__

```Python
    def bulletList(self):

        cursor = self.text.textCursor()

        # Insert bulleted list
        cursor.insertList(QtGui.QTextListFormat.ListDisc)

    def numberList(self):

        cursor = self.text.textCursor()

        # Insert list with numbers
        cursor.insertList(QtGui.QTextListFormat.ListDecimal)
```

As you can see, we don't make these actions class members because we don't need to access them anywhere else in our code, we only need to create and use them within the scope of `initToolbar()`.

Concerning the slot functions, we retrieve our `QTextEdit`'s `QTextCursor`, which has a lot of very useful methods, such `insertList()`, which, well, does what it's supposed to do. In case of `bulletList()`, we insert a list with the `QTextListFormat` set to `ListDisc`. For `numberList()`, we insert a list with `ListDecimal` format. 

## Final changes

To finish off this part of _**Developing a PyQt text editor**_,  let's make some final changes in the `initUI()` method:

`self.text.setTabStopWidth(33)`

Because PyQt's tab width is very strange, I recommend you set the `QTextEdit`'s "tab stop width" to 33 pixels, which is around 8 spaces. 

`self.setWindowIcon(QtGui.QIcon("icons/icon.png"))`

Now that we have icons, we can add an icon for our window.

`self.text.cursorPositionChanged.connect(self.cursorPosition`

By connecting our `QTextEdit`'s `cursorPositionChanged` signal to a function, we can display the cursor's current line and column number in the status bar. Here is the corresponding slot function, below `initUI()`:

```Python
def cursorPosition(self):

    cursor = self.text.textCursor()

    # Mortals like 1-indexed things
    line = cursor.blockNumber() + 1
    col = cursor.columnNumber()

    self.statusbar.showMessage("Line: {} | Column: {}".format(line,col))
```

We first retrieve our `QTextEdit`'s `QTextCursor`, then grab the cursor's column and block/line number and finally display these numbers in the status bar. 

That'll be it for this part of the series. See you soon.