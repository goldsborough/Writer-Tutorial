In the last part of my tutorial series on *__Building a text editor with PyQt__*, we built the text editor's basic skeleton and already added some handy features for file management, printing, inserting lists and more. This part will focus on the format bar, which we will populate with actions to change font family, background color, alignment and other features.

## Font

We will start with actions related to font, meaning the user will be able to:

+ Change font family
+ Adjust font size
+ Set font color
+ Choose background color

Now to the code. Just like last time, I will only show the functions that change relative to the previous code:

__`initFormatbar()`__:

	fontBox = QtGui.QFontComboBox(self)
	fontBox.currentFontChanged.connect(self.fontFamily)

	fontSize = QtGui.QComboBox(self)
	fontSize.setEditable(True)

	# Minimum number of chars displayed
	fontSize.setMinimumContentsLength(3)

	fontSize.activated.connect(self.fontSize)

	# Typical font sizes
	fontSizes = ['6','7','8','9','10','11','12','13','14',
	             '15','16','18','20','22','24','26','28',
	             '32','36','40','44','48','54','60','66',
	             '72','80','88','96']

	for i in fontSizes:
	    fontSize.addItem(i)

	fontColor = QtGui.QAction(QtGui.QIcon("icons/font-color.png"),"Change font color",self)
	fontColor.triggered.connect(self.fontColor)

	backColor = QtGui.QAction(QtGui.QIcon("icons/highlight.png"),"Change background color",self)
	backColor.triggered.connect(self.highlight)

	self.formatbar = self.addToolBar("Format")

	self.formatbar.addWidget(fontBox)
	self.formatbar.addWidget(fontSize)

	self.formatbar.addSeparator()

	self.formatbar.addAction(fontColor)
	self.formatbar.addAction(backColor)

	self.formatbar.addSeparator()

__Below `initUI()`__:

	def fontFamily(self,font):
	  self.text.setCurrentFont(font)

	def fontSize(self, fontsize):
	    self.text.setFontPointSize(int(fontsize))

	def fontColor(self):

	    # Get a color from the text dialog
	    color = QtGui.QColorDialog.getColor()

	    # Set it as the new text color
	    self.text.setTextColor(color)

	def highlight(self):

	    color = QtGui.QColorDialog.getColor()

	    self.text.setTextBackgroundColor(color)



Note that the actions we just created don't follow the code pattern for actions I described last time, we don't make these actions class members because we only need to create and use them within the scope of `initFormatbar()`. We also don't give them tooltips or shortcuts anymore (unless you want to, of course).

We start out by creating a `QFontComboBox`, which is a very convenient combo box that automatically includes all the fonts available to the system. We instantiate it and connect its `currentFontChanged` signal to a slot function, `self.fontFamily()`, which we later created underneath the `initUI()` method. As you can see, we also give this slot function a second parameter `font`, so PyQt will pass the user-selected `QFont` object to our function, reducing our work to setting this font to the text's current font.

Next up, we need a combo box for font sizes. PyQt itself doesn't have such a thing, so we need to create one ourself. This is easily done by instantiating a normal combo box, here called `fontSize`, which we set *editable*, meaning the user can enter any number he or she wants for the font. After connecting the `activated` signal to a slot function, we populate the combo box with some common font sizes. For the slot function, we again set a second parameter, `font size`, which PyQt passes to us when the user selects a font size from the combo box or, alternatively, enters a custom size. We set the user's selection as the text's current *font point size*.

The last two actions are very similar. In both cases, we create two actions that open a `QColorDialog` when activated. In case of `fontColor`, we set the color selection as the font color. For `backColor`, we set the color as the current text's background color.

## Bold moves

Next, we'll add actions to make text:

+ bold
+ italic
+ underlined
+ strikeout
+ superscript
+ subscript

The code for this is relatively simple:

__`initFormatbar()`__:

	boldAction = QtGui.QAction(QtGui.QIcon("icons/bold.png"),"Bold",self)
	boldAction.triggered.connect(self.bold)

	italicAction = QtGui.QAction(QtGui.QIcon("icons/italic.png"),"Italic",self)
	italicAction.triggered.connect(self.italic)

	underlAction = QtGui.QAction(QtGui.QIcon("icons/underline.png"),"Underline",self)
	underlAction.triggered.connect(self.underline)

	strikeAction = QtGui.QAction(QtGui.QIcon("icons/strike.png"),"Strike-out",self)
	strikeAction.triggered.connect(self.strike)

	superAction = QtGui.QAction(QtGui.QIcon("icons/superscript.png"),"Superscript",self)
	superAction.triggered.connect(self.superScript)

	subAction = QtGui.QAction(QtGui.QIcon("icons/subscript.png"),"Subscript",self)
	subAction.triggered.connect(self.subScript)


__Further below__:

	self.formatbar.addAction(boldAction)
	self.formatbar.addAction(italicAction)
	self.formatbar.addAction(underlAction)
	self.formatbar.addAction(strikeAction)
	self.formatbar.addAction(superAction)
	self.formatbar.addAction(subAction)

	self.formatbar.addSeparator()

__Below `initUI()`__:

	def bold(self):

        if self.text.fontWeight() == QtGui.QFont.Bold:

            self.text.setFontWeight(QtGui.QFont.Normal)

        else:

            self.text.setFontWeight(QtGui.QFont.Bold)

    def italic(self):

        state = self.text.fontItalic()

        self.text.setFontItalic(not state)

    def underline(self):

        state = self.text.fontUnderline()

        self.text.setFontUnderline(not state)

    def strike(self):

        # Grab the text's format
        fmt = self.text.currentCharFormat()

        # Set the fontStrikeOut property to its opposite
        fmt.setFontStrikeOut(not fmt.fontStrikeOut())

        # And set the next char format
        self.text.setCurrentCharFormat(fmt)

    def superScript(self):

        # Grab the current format
        fmt = self.text.currentCharFormat()

        # And get the vertical alignment property
        align = fmt.verticalAlignment()

        # Toggle the state
        if align == QtGui.QTextCharFormat.AlignNormal:

            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignSuperScript)

        else:

            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignNormal)

        # Set the new format
        self.text.setCurrentCharFormat(fmt)

    def subScript(self):

        # Grab the current format
        fmt = self.text.currentCharFormat()

        # And get the vertical alignment property
        align = fmt.verticalAlignment()

        # Toggle the state
        if align == QtGui.QTextCharFormat.AlignNormal:

            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignSubScript)

        else:

            fmt.setVerticalAlignment(QtGui.QTextCharFormat.AlignNormal)

        # Set the new format
        self.text.setCurrentCharFormat(fmt)

The changes in `initFormatbar()` should be relatively understandable by now. We create actions and connect the `triggered` signals to slot functions, after which we add the actions to the format bar.

In `bold()`, we invert the font weight of the current text. If the text is bold, we set the font weight to "normal". If the font weight is normal, we set it to bold.

For `italic()` and `underline()`, our `QTextEdit` object has functions for setting and getting the state of the text. Therefore, we just grab the current state of the text and invert it.

The `strike()` function is a bit different. We retrieve our text's `currentCharFormat`, invert the state of the `fontStrikeOut` property and finally set our new char format to the text's "current" char format.

Lastly, in `superScript()` and `subScript()`, we again fetch the current char format, toggle the `verticalAlignment` property like we did in `bold()` and reset the new char format to make our changes visible.

## Alignment

Alignment is very simple, as PyQt provides us with the necessary methods:

__`initFormatbar()`__:

	alignLeft = QtGui.QAction(QtGui.QIcon("icons/align-left.png"),"Align left",self)
	alignLeft.triggered.connect(self.alignLeft)

	alignCenter = QtGui.QAction(QtGui.QIcon("icons/align-center.png"),"Align center",self)
	alignCenter.triggered.connect(self.alignCenter)

	alignRight = QtGui.QAction(QtGui.QIcon("icons/align-right.png"),"Align right",self)
	alignRight.triggered.connect(self.alignRight)

	alignJustify = QtGui.QAction(QtGui.QIcon("icons/align-justify.png"),"Align justify",self)
	alignJustify.triggered.connect(self.alignJustify)

__Further below__:

	self.formatbar.addAction(alignLeft)
	self.formatbar.addAction(alignCenter)
	self.formatbar.addAction(alignRight)
	self.formatbar.addAction(alignJustify)

	self.formatbar.addSeparator()

__Below the `initUI()` method__:

    def alignLeft(self):
        self.text.setAlignment(Qt.AlignLeft)

    def alignRight(self):
        self.text.setAlignment(Qt.AlignRight)

    def alignCenter(self):
        self.text.setAlignment(Qt.AlignCenter)

    def alignJustify(self):
        self.text.setAlignment(Qt.AlignJustify)


Changes in the `initFormatbar()` method follow the previous pattern and the slot functions are also very simple. We change the text's alignment using our `QTextEdit`'s `setAlignment` method, passing it the respective member of the Qt namespace, e.g. `Qt.AlignCenter`.

## Indent - dedent

Indenting and dedenting is a little more complex, as PyQt provides us with no methods to efficiently adjust the tabbing of a selected area, meaning we need to come up with our own method of doing so:

__`initFormatbar()`__:

	indentAction = QtGui.QAction(QtGui.QIcon("icons/indent.png"),"Indent Area",self)
	indentAction.setShortcut("Ctrl+Tab")
	indentAction.triggered.connect(self.indent)

	dedentAction = QtGui.QAction(QtGui.QIcon("icons/dedent.png"),"Dedent Area",self)
	dedentAction.setShortcut("Shift+Tab")
	dedentAction.triggered.connect(self.dedent)

__Further below__:

	self.formatbar.addAction(indentAction)
	self.formatbar.addAction(dedentAction)

__Below `initUI()`__:

    def indent(self):

        # Grab the cursor
        cursor = self.text.textCursor()

        if cursor.hasSelection():

            # Store the current line/block number
            temp = cursor.blockNumber()

            # Move to the selection's last line
            cursor.setPosition(cursor.selectionEnd())

            # Calculate range of selection
            diff = cursor.blockNumber() - temp

            # Iterate over lines
            for n in range(diff + 1):

                # Move to start of each line
                cursor.movePosition(QtGui.QTextCursor.StartOfLine)

                # Insert tabbing
                cursor.insertText("\t")

                # And move back up
                cursor.movePosition(QtGui.QTextCursor.Up)

        # If there is no selection, just insert a tab
        else:

            cursor.insertText("\t")

    def dedent(self):

        cursor = self.text.textCursor()

        if cursor.hasSelection():

            # Store the current line/block number
            temp = cursor.blockNumber()

            # Move to the selection's last line
            cursor.setPosition(cursor.selectionEnd())

            # Calculate range of selection
            diff = cursor.blockNumber() - temp

            # Iterate over lines
            for n in range(diff + 1):

                self.handleDedent(cursor)

                # Move up
                cursor.movePosition(QtGui.QTextCursor.Up)

        else:
            self.handleDedent(cursor)


    def handleDedent(self,cursor):

        cursor.movePosition(QtGui.QTextCursor.StartOfLine)

        # Grab the current line
        line = cursor.block().text()

        # If the line starts with a tab character, delete it
        if line.startswith("\t"):

            # Delete next character
            cursor.deleteChar()

        # Otherwise, delete all spaces until a non-space character is met
        else:
            for char in line[:8]:

                if char != " ":
                    break

                cursor.deleteChar()


Changes to `initFormatbar()` as previously discussed.

Let's go through the `indent()` function step by step. The first thing we need to do is grab our text's current `QTextCursor` object. We check if the user currently has any text under selection. If not, we just insert a tab. If he or she does have something under selection, however, we need to get a bit more funky. More specifically, we have to find out how many lines the user has under selection and insert a tab before each line. We do so by first getting the current line/block number at the start of the selection, then moving the cursor to the end and subtracting the previously stored block/line number from the new one. This provides us with the range of lines over which we subsequently iterate. For each iteration, we move the cursor to the start of the current line, insert a tab and finally move up one line until we reach the top (remember that before we start iterating, we have the cursor at the end of the selection, where we moved it to find out the selection's last line number)

The `dedent()` method is quite similar, it differs, however, in our need to also handle excess space and not only tabs. That's what `handleDedent()` is for. It is called at each iteration of the loop that moves up the lines of the selection. In it, we again set the cursor to the beginning of each line, after which we grab the current line's text. If the line starts with a tab, we can just delete it and our job is done. If it doesn't, we also check wether there is any excess space (up to 8 spaces, which equals a tab) and delete it if so. This ensures two things:

+ People who prefer 8 spaces over a tab character ('/t') also get their money's worth
+ Excess space that could block from you from completely dedenting a block of text is deleted

## Final customization options

Now that our tool bar, our format bar and our status bar are populated, we can add some final customization options to toggle the visibility of these three bars:

__`initMenubar()`__:

	# Toggling actions for the various bars
	toolbarAction = QtGui.QAction("Toggle Toolbar",self)
	toolbarAction.triggered.connect(self.toggleToolbar)

	formatbarAction = QtGui.QAction("Toggle Formatbar",self)
	formatbarAction.triggered.connect(self.toggleFormatbar)

	statusbarAction = QtGui.QAction("Toggle Statusbar",self)
	statusbarAction.triggered.connect(self.toggleStatusbar)

	view.addAction(toolbarAction)
	view.addAction(formatbarAction)
	view.addAction(statusbarAction)

__Below `initUI()`__:

	def toggleToolbar(self):

      state = self.toolbar.isVisible()

      # Set the visibility to its inverse
      self.toolbar.setVisible(not state)

    def toggleFormatbar(self):

        state = self.formatbar.isVisible()

        # Set the visibility to its inverse
        self.formatbar.setVisible(not state)

    def toggleStatusbar(self):

        state = self.statusbar.isVisible()

        # Set the visibility to its inverse
        self.statusbar.setVisible(not state)


We create three actions in our `initMenubar()` method,

+ toolbarAction
+ formatbarAction
+ statusbarAction

and connect them to slot functions. Note that we don't add these actions to any of the toolbars, but only to the drop-down menus at the top of our screen.

In the slot functions, we do what we did for some of the formatting functions, we retrieve the visibility states of the various bars and set the them to their opposite.

That'll be it for this post. Be sure to check back for the upcoming parts of this series on __*Building a text editor with PyQt*__, in which we'll add some very cool actions for find-and-replace, inserting and manipulating tables and more.
