from PyQt5.QtWidgets import QTextEdit, QApplication
from PyQt5.QtGui import QTextCursor,QTextCharFormat,QFont
from PyQt5 import QtCore, QtGui
import sys
import re
import urllib.request
import textwrap
from copy import deepcopy

#self.format.setFontWeight(QFont.Bold)
#self.format.setFontItalic(True)

#The void elements in HTML 4.01/XHTML 1.0 Strict are are;
#base, br, col, hr, img, input, link, meta, and param.
#HTML5 currently adds command, keygen, and source to that list.

#HTML head> tag does not print things, but puts in elements for the rest
# of the document. tags that can be ONLY in head are:
#title>,style>,base>,link>,meta>,script>,noscript>

class Renderer:
    def __init__(self, initWidget,mode):
        self.testMode=mode
        self.imageWidth = 0
        self.imageHeight = 0
        self.imageSrc = ""
        self.imageSrcLocation = 0
        self.pageSrc = ""

        self.ACTIVE_TAGS = []
        self.LAST_WAS_TWO_RETURN = 1
        self.LAST_WAS_ONE_RETURN = 1
        self.DEFAULT_FONT_SIZE = 12
        self.CURRENT_FONT_SIZE = self.DEFAULT_FONT_SIZE
        self.B_STILL_ACTIVE = 0
        self.H_STILL_ACTIVE = 0
        self.Title = "New Tab"
        if mode:
            self.textOutput=""
            return

        self.widget = initWidget
        self.textCursor = QTextCursor(initWidget.textCursor())
        self.format = QTextCharFormat()
        self.format.setFontPointSize(self.DEFAULT_FONT_SIZE)
        self.widget.setOpenLinks(False)
        self.widget.setStyleSheet("")

        
    def printString(self, text):
        if self.testMode:
            self.textOutput += text
            return
        text = text.replace("&lt;", "<")
        text = text.replace("&gt;", ">")
        text = text.replace("&amp;", "&")
        text = text.replace("\\n", "\n")
        if "TITLE" in self.ACTIVE_TAGS:
            self.Title=text
        if ("HEAD" not in self.ACTIVE_TAGS) and ("SCRIPT" not in self.ACTIVE_TAGS):
            if(self.LAST_WAS_TWO_RETURN == 0) and (self.LAST_WAS_ONE_RETURN == 0):
                self.textCursor.insertText(" ", self.format)
            self.LAST_WAS_TWO_RETURN = 0
            self.LAST_WAS_ONE_RETURN = 0
            self.textCursor.insertText(str(text), self.format)


    def foundTag(self, tag):
        if self.testMode:
            self.textOutput+=tag
            return
#========================================================
#      START TAG         START TAG       START TAG
#========================================================
        if not re.match("/", tag): #do open tags first
            
##            if tag not in self.ACTIVE_TAGS:
##               self.ACTIVE_TAGS.append(tag)
            # some tags need to stack, others need to be closed and reopened

            self.ACTIVE_TAGS.append(tag)
            if(tag == "COMMENT_START"):
                return
            elif(tag == "A"):
                self.format.setAnchor(True)
                self.format.setFontUnderline(True)
                return
            elif(tag == "ABBR"):
                return
            elif(tag == "ACRONYM"):
                #NOT SUPPORTED IN HTML5
                return
            elif(tag == "ADDRESS"):
                return
            elif(tag == "APPLET"):
                #NOT SUPPORTED IN HTML5
                return
            elif(tag == "AREA"):
                return
            elif(tag == "ARTICLE"):
                return
            elif(tag == "ASIDE"):
                return
            elif(tag == "AUDIO"):
                return
            elif(tag == "B"):
                self.B_STILL_ACTIVE=1
                self.format.setFontWeight(QFont.Bold)
                return
            elif(tag == "BASE"):
                self.ACTIVE_TAGS.remove(tag)
                return
            elif(tag == "BASEFONT"):
                #NOT SUPPORTED IN HTML5
                return
            elif(tag == "BDI"):
                return
            elif(tag == "BDO"):
                return
            elif(tag == "BIG"):
                #NOT SUPPORTED IN HTML5
                self.CURRENT_FONT_SIZE += 3
                self.format.setFontPointSize(self.CURRENT_FONT_SIZE)
                return
            elif(tag == "BLOCKQUOTE"):
                return
            elif(tag == "BODY"):
                return
            elif(tag == "BR"):
                self.ACTIVE_TAGS.remove(tag)
                self.textCursor.insertText("\n")
                self.LAST_WAS_ONE_RETURN = 1
                return
            elif(tag == "BUTTON"):
                return
            elif(tag == "CANVAS"):
                return
            elif(tag == "CAPTION"):
                return
            elif(tag == "CENTER"):
                #NOT SUPPORTED IN HTML5
                if(self.LAST_WAS_ONE_RETURN == 0) and (self.LAST_WAS_TWO_RETURN == 0):
                    self.textCursor.insertText("\n")
                    self.LAST_WAS_ONE_RETURN = 1
                self.widget.setAlignment(QtCore.Qt.AlignCenter);
                return
            elif(tag == "CITE"):
                return
            elif(tag == "CODE"):
                return
            elif(tag == "COL"):
                self.ACTIVE_TAGS.remove(tag)
                return
            elif(tag == "COLGROUP"):
                return
            elif(tag == "DATALIST"):
                return
            elif(tag == "DD"):
                return
            elif(tag == "DEL"):
                self.format.setFontStrikeOut(True)
                return
            elif(tag == "DETAILS"):
                return
            elif(tag == "DFN"):
                return
            elif(tag == "DIALOG"):
                return
            elif(tag == "DIR"):
                #NOT SUPPORTED IN HTML5
                return
            elif(tag == "DIV"):
                return
            elif(tag == "DL"):
                return
            elif(tag == "DT"):
                return
            elif(tag == "EM"):
                self.format.setFontItalic(True)
                return
            elif(tag == "FIELDSET"):
                return
            elif(tag == "FIGCAPTION"):
                return
            elif(tag == "FIGURE"):
                return
            elif(tag == "FONT"):
                #NOT SUPPORTED IN HTML5
                return
            elif(tag == "FOOTER"):
                return
            elif(tag == "FORM"):
                return
            elif(tag == "FRAME"):
                #NOT SUPPORTED IN HTML5
                return
            elif(tag == "FRAMESET"):
                #NOT SUPPORTED IN HTML5
                return
            elif(tag == "H1"):

                if(self.LAST_WAS_TWO_RETURN == 0) and (self.LAST_WAS_ONE_RETURN == 0):
                    self.LAST_WAS_TWO_RETURN = 1
                    self.LAST_WAS_ONE_RETURN = 1
                    self.textCursor.insertText("\n\n")
                elif(self.LAST_WAS_TWO_RETURN == 0) and (self.LAST_WAS_ONE_RETURN == 1):
                    self.LAST_WAS_TWO_RETURN = 1
                    self.textCursor.insertText("\n")
                self.CURRENT_FONT_SIZE += 12
                self.format.setFontPointSize(self.CURRENT_FONT_SIZE)
                self.format.setFontWeight(QFont.Bold)
                self.H_STILL_ACTIVE = 1
                return
            elif(tag == "H2"):
                if(self.LAST_WAS_TWO_RETURN == 0) and (self.LAST_WAS_ONE_RETURN == 0):
                    self.LAST_WAS_TWO_RETURN = 1
                    self.LAST_WAS_ONE_RETURN = 1
                    self.textCursor.insertText("\n\n")
                elif(self.LAST_WAS_TWO_RETURN == 0) and (self.LAST_WAS_ONE_RETURN == 1):
                    self.LAST_WAS_TWO_RETURN = 1
                    self.textCursor.insertText("\n")
                self.CURRENT_FONT_SIZE += 9
                self.format.setFontPointSize(self.CURRENT_FONT_SIZE)
                self.format.setFontWeight(QFont.Bold)
                self.H_STILL_ACTIVE = 1
                return
            elif(tag == "H3"):
                if(self.LAST_WAS_TWO_RETURN == 0) and (self.LAST_WAS_ONE_RETURN == 0):
                    self.LAST_WAS_TWO_RETURN = 1
                    self.LAST_WAS_ONE_RETURN = 1
                    self.textCursor.insertText("\n\n")
                elif(self.LAST_WAS_TWO_RETURN == 0) and (self.LAST_WAS_ONE_RETURN == 1):
                    self.LAST_WAS_TWO_RETURN = 1
                    self.textCursor.insertText("\n")
                self.CURRENT_FONT_SIZE += 6
                self.format.setFontPointSize(self.CURRENT_FONT_SIZE)
                self.format.setFontWeight(QFont.Bold)
                self.H_STILL_ACTIVE = 1
                return
            elif(tag == "H4"):
                if(self.LAST_WAS_TWO_RETURN == 0) and (self.LAST_WAS_ONE_RETURN == 0):
                    self.LAST_WAS_TWO_RETURN = 1
                    self.LAST_WAS_ONE_RETURN = 1
                    self.textCursor.insertText("\n\n")
                elif(self.LAST_WAS_TWO_RETURN == 0) and (self.LAST_WAS_ONE_RETURN == 1):
                    self.LAST_WAS_TWO_RETURN = 1
                    self.textCursor.insertText("\n")
                #self.CURRENT_FONT_SIZE += 0
                #self.format.setFontPointSize(self.CURRENT_FONT_SIZE)
                self.format.setFontWeight(QFont.Bold)
                self.H_STILL_ACTIVE = 1
                return
            elif(tag == "H5"):
                if(self.LAST_WAS_TWO_RETURN == 0) and (self.LAST_WAS_ONE_RETURN == 0):
                    self.LAST_WAS_TWO_RETURN = 1
                    self.LAST_WAS_ONE_RETURN = 1
                    self.textCursor.insertText("\n\n")
                elif(self.LAST_WAS_TWO_RETURN == 0) and (self.LAST_WAS_ONE_RETURN == 1):
                    self.LAST_WAS_TWO_RETURN = 1
                    self.textCursor.insertText("\n")
                self.CURRENT_FONT_SIZE -= 2
                self.format.setFontPointSize(self.CURRENT_FONT_SIZE)
                self.format.setFontWeight(QFont.Bold)
                self.H_STILL_ACTIVE = 1
                return
            elif(tag == "H6"):
                if(self.LAST_WAS_TWO_RETURN == 0) and (self.LAST_WAS_ONE_RETURN == 0):
                    self.LAST_WAS_TWO_RETURN = 1
                    self.LAST_WAS_ONE_RETURN = 1
                    self.textCursor.insertText("\n\n")
                elif(self.LAST_WAS_TWO_RETURN == 0) and (self.LAST_WAS_ONE_RETURN == 1):
                    self.LAST_WAS_TWO_RETURN = 1
                    self.textCursor.insertText("\n")
                self.CURRENT_FONT_SIZE -= 4
                self.format.setFontPointSize(self.CURRENT_FONT_SIZE)
                self.format.setFontWeight(QFont.Bold)
                self.H_STILL_ACTIVE = 1
                return
            elif(tag == "HEAD"):
                return
            elif(tag == "HEADER"):
                return
            elif(tag == "HR"):
                self.ACTIVE_TAGS.remove(tag)
                if(self.LAST_WAS_TWO_RETURN == 0) and (self.LAST_WAS_ONE_RETURN == 0):
                    self.textCursor.insertText("\n")
                self.textCursor.insertText("———————————————————————————")
                self.textCursor.insertText("\n")
                self.LAST_WAS_ONE_RETURN = 1
                return
            elif(tag == "HTML"):
                return
            elif(tag == "I"):
                self.format.setFontItalic(True)
                return
            elif(tag == "IFRAME"):
                return
            elif(tag == "IMG"):
                self.ACTIVE_TAGS.remove(tag)
                self.LAST_WAS_TWO_RETURN = 0
                self.LAST_WAS_ONE_RETURN = 0
                print("found img")
                if(self.imageSrcLocation == 1):
                    try:
                        data = urllib.request.urlopen(str(self.imageSrc)).read()
                        image = QtGui.QImage()
                        image.loadFromData(data)
                        if(int(self.imageWidth) > 0) and (int(self.imageHeight) > 0):
                            image = image.scaled(int(self.imageWidth), int(self.imageHeight))
                        self.textCursor.insertImage(image)
                    except Exception:
                        self.textCursor.insertText("[IMG from site not found]" + str(self.imageSrc), self.format)
                elif(self.imageSrcLocation == 2):
##                    print("in loc 2")
##                    print(self.imageSrc)
##                    try:
##                        icon = QtGui.QPixmap(str(self.imageSrc))
##                        if(int(self.imageWidth) > 0) and (int(self.imageHeight) > 0):
##                            icon = icon.scaled(int(self.imageWidth), int(self.imageHeight))
##                        image = icon.toImage()
##                        self.textCursor.insertImage(image)
##                    except Exception:
##                        self.textCursor.insertText("[IMG from file not found]", self.format)
                    try:
                        i = self.pageSrc.find("//")
                        i = i+2 if i != -1 else -1
                        if i != -1:
                            i2 = self.pageSrc.find("/", i)
                            i2 = i2 if i2 != -1 else len(self.pageSrc)

                            if self.imageSrc[1] != "/":
                                self.imageSrc = "/" + self.imageSrc
                            
                            self.imageSrc = self.pageSrc[:i2] + self.imageSrc
##                        print(self.imageSrc)
                        data = urllib.request.urlopen(str(self.imageSrc)).read()
                        image = QtGui.QImage()
                        image.loadFromData(data)
                        if(int(self.imageWidth) > 0) and (int(self.imageHeight) > 0):
                            image = image.scaled(int(self.imageWidth), int(self.imageHeight))
                        self.textCursor.insertImage(image)
                    except Exception:
                        self.textCursor.insertText("[IMG from site not found]" + str(self.imageSrc), self.format)
                elif(self.imageSrcLocation == 0):
                    self.textCursor.insertText("[IMG WITH BAD SRC]", self.format)
                    
                return
            elif(tag == "INPUT"):
                self.ACTIVE_TAGS.remove(tag)
                return
            elif(tag == "INS"):
                self.format.setFontUnderline(True)
                return
            elif(tag == "KBD"):
                return
            elif(tag == "KEYGEN"):
                return
            elif(tag == "LABEL"):
                return
            elif(tag == "LEGEND"):
                return
            elif(tag == "LI"):
                return
            elif(tag == "LINK"):
                self.ACTIVE_TAGS.remove(tag)
                return
            elif(tag == "MAIN"):
                return
            elif(tag == "MAP"):
                return
            elif(tag == "MARK"):
                return
            elif(tag == "MENU"):
                return
            elif(tag == "MENUITEM"):
                return
            elif(tag == "META"):
                self.ACTIVE_TAGS.remove(tag)
                return
            elif(tag == "METER"):
                return
            elif(tag == "NAV"):
                return
            elif(tag == "NOFRAMES"):
                #NOT SUPPORTED IN HTML5
                return
            elif(tag == "NOSCRIPT"):
                return
            elif(tag == "OBJECT"):
                return
            elif(tag == "OL"):
                return
            elif(tag == "OPTGROUP"):
                return
            elif(tag == "OPTION"):
                return
            elif(tag == "OUTPUT"):
                return
            elif(tag == "P"):
                if(self.LAST_WAS_TWO_RETURN == 0) and (self.LAST_WAS_ONE_RETURN == 0): 
                    self.LAST_WAS_ONE_RETURN = 1
                    self.LAST_WAS_TWO_RETURN = 1
                    self.textCursor.insertText("\n\n")
                elif(self.LAST_WAS_TWO_RETURN == 0) and (self.LAST_WAS_ONE_RETURN == 1): 
                    self.LAST_WAS_TWO_RETURN = 1
                    self.textCursor.insertText("\n")
                #Yes, then do nothing since /p> already did it
                return
            elif(tag == "PARAM"):
                self.ACTIVE_TAGS.remove(tag)
                return
            elif(tag == "PICTURE"):
                return
            elif(tag == "PRE"):
                return
            elif(tag == "PROGRESS"):
                return
            elif(tag == "Q"):
                return
            elif(tag == "RP"):
                return
            elif(tag == "RT"):
                return
            elif(tag == "RUBY"):
                return
            elif(tag == "S"):
                self.format.setFontStrikeOut(True)
                return
            elif(tag == "SAMP"):
                return
            elif(tag == "SCRIPT"):
                return
            elif(tag == "SECTION"):
                return
            elif(tag == "SELECT"):
                return
            elif(tag == "SMALL"):
                self.CURRENT_FONT_SIZE -= 3
                self.format.setFontPointSize(self.CURRENT_FONT_SIZE)
                return
            elif(tag == "SOURCE"):
                return
            elif(tag == "SPAN"):
                return
            elif(tag == "STRIKE"):
                #NOT SUPPORTED IN HTML5
                return
            elif(tag == "STRONG"):
                self.format.setFontWeight(QFont.Black)
                return
            elif(tag == "STYLE"):
                return
            elif(tag == "SUB"):
                self.format.setVerticalAlignment(QTextCharFormat.AlignSubScript)
                return
            elif(tag == "SUMMARY"):
                return
            elif(tag == "SUP"):
                self.format.setVerticalAlignment(QTextCharFormat.AlignSuperScript)
                return
            elif(tag == "TABLE"):
                return
            elif(tag == "TBODY"):
                return
            elif(tag == "TD"):
                return
            elif(tag == "TEXTAREA"):
                return
            elif(tag == "TFOOT"):
                return
            elif(tag == "TH"):
                return
            elif(tag == "THEAD"):
                return
            elif(tag == "TIME"):
                return
            elif(tag == "TITLE"):
                return
            elif(tag == "TR"):
                return
            elif(tag == "TRACK"):
                return
            elif(tag == "TT"):
                #NOT SUPPORTED IN HTML5
                return
            elif(tag == "U"):
                self.format.setFontUnderline(True)
                return
            elif(tag == "UL"):
                return
            elif(tag == "VAR"):
                return
            elif(tag == "VIDEO"):
                self.LAST_WAS_TWO_RETURN = 0
                self.LAST_WAS_ONE_RETURN = 0
                self.textCursor.insertText("[[[[[VID]]]]]", self.format)
                return
            elif(tag == "WBR"):
                return
    



#========================================================
#      CLOSE TAG         CLOSE TAG       CLOSE TAG
#======================================================== 
        else:
            #if the tag without the first char '/' is in...
            if tag[1:] in self.ACTIVE_TAGS: #remove, then deal with special cases
                self.ACTIVE_TAGS.remove(tag[1:])
                
                if(tag == "/A"):
                    #self.textCursor.insertText("[LINK]", self.format)
                    self.format.setAnchor(False)
                    self.format.setFontUnderline(False)
                    self.format.setAnchorHref(None)
                    return
                elif(tag == "/ABBR"):
                    return
                elif(tag == "/ACRONYM"):
                    #NOT SUPPORTED IN HTML5
                    return
                elif(tag == "/ADDRESS"):
                    return
                elif(tag == "/APPLET"):
                    #NOT SUPPORTED IN HTML5
                    return
                elif(tag == "/AREA"):
                    return
                elif(tag == "/ARTICLE"):
                    return
                elif(tag == "/ASIDE"):
                    return
                elif(tag == "/AUDIO"):
                    return
                elif(tag == "/B"):
                    self.B_STILL_ACTIVE = 0
                    if not (self.H_STILL_ACTIVE):
                        self.format.setFontWeight(QFont.Normal)
                    return
                elif(tag == "/BASEFONT"):
                    #NOT SUPPORTED IN HTML5
                    return
                elif(tag == "/BDI"):
                    return
                elif(tag == "/BDO"):
                    return
                elif(tag == "/BIG"):
                    #NOT SUPPORTED IN HTML5
                    self.CURRENT_FONT_SIZE -= 3
                    self.format.setFontPointSize(self.CURRENT_FONT_SIZE)
                    return
                elif(tag == "/BLOCKQUOTE"):
                    return
                elif(tag == "/BODY"):
                    return
                elif(tag == "/BUTTON"):
                    return
                elif(tag == "/CANVAS"):
                    return
                elif(tag == "/CAPTION"):
                    return
                elif(tag == "/CENTER"):
                    #NOT SUPPORTED IN HTML5
                    if(self.LAST_WAS_ONE_RETURN == 0) and (self.LAST_WAS_TWO_RETURN == 0):
                        self.textCursor.insertText("\n")
                        self.LAST_WAS_ONE_RETURN = 1
                    self.widget.setAlignment(QtCore.Qt.AlignLeft);
                    return
                elif(tag == "/CITE"):
                    return
                elif(tag == "/CODE"):
                    return
                elif(tag == "/COLGROUP"):
                    return
                elif(tag == "/DATALIST"):
                    return
                elif(tag == "/DD"):
                    return
                elif(tag == "/DEL"):
                    self.format.setFontStrikeOut(False)
                    return
                elif(tag == "/DETAILS"):
                    return
                elif(tag == "/DFN"):
                    return
                elif(tag == "/DIALOG"):
                    return
                elif(tag == "/DIR"):
                    #NOT SUPPORTED IN HTML5
                    return
                elif(tag == "/DIV"):
                    return
                elif(tag == "/DL"):
                    return
                elif(tag == "/DT"):
                    return
                elif(tag == "/EM"):
                    self.format.setFontItalic(False)
                    return
                elif(tag == "/FIELDSET"):
                    return
                elif(tag == "/FIGCAPTION"):
                    return
                elif(tag == "/FIGURE"):
                    return
                elif(tag == "/FONT"):
                    #NOT SUPPORTED IN HTML5
                    return
                elif(tag == "/FOOTER"):
                    return
                elif(tag == "/FORM"):
                    return
                elif(tag == "/FRAME"):
                    #NOT SUPPORTED IN HTML5
                    return
                elif(tag == "/FRAMESET"):
                    #NOT SUPPORTED IN HTML5
                    return
                elif(tag == "/H1"):
                    if(self.LAST_WAS_TWO_RETURN == 0) and (self.LAST_WAS_ONE_RETURN == 0):
                        self.LAST_WAS_TWO_RETURN = 1
                        self.LAST_WAS_ONE_RETURN = 1
                        self.textCursor.insertText("\n\n")
                    elif(self.LAST_WAS_TWO_RETURN == 0) and (self.LAST_WAS_ONE_RETURN == 1):
                        self.LAST_WAS_TWO_RETURN = 1
                        self.textCursor.insertText("\n")
                    self.CURRENT_FONT_SIZE -= 12
                    self.format.setFontPointSize(self.CURRENT_FONT_SIZE)
                    if not (self.B_STILL_ACTIVE):
                        self.format.setFontWeight(QFont.Normal)
                    self.H_STILL_ACTIVE=0
                    return
                elif(tag == "/H2"):
                    if(self.LAST_WAS_TWO_RETURN == 0) and (self.LAST_WAS_ONE_RETURN == 0):
                        self.LAST_WAS_TWO_RETURN = 1
                        self.LAST_WAS_ONE_RETURN = 1
                        self.textCursor.insertText("\n\n")
                    elif(self.LAST_WAS_TWO_RETURN == 0) and (self.LAST_WAS_ONE_RETURN == 1):
                        self.LAST_WAS_TWO_RETURN = 1
                        self.textCursor.insertText("\n")
                    self.CURRENT_FONT_SIZE -= 9
                    self.format.setFontPointSize(self.CURRENT_FONT_SIZE)
                    if not (self.B_STILL_ACTIVE):
                        self.format.setFontWeight(QFont.Normal)
                    self.H_STILL_ACTIVE=0
                    return
                elif(tag == "/H3"):
                    if(self.LAST_WAS_TWO_RETURN == 0) and (self.LAST_WAS_ONE_RETURN == 0):
                        self.LAST_WAS_TWO_RETURN = 1
                        self.LAST_WAS_ONE_RETURN = 1
                        self.textCursor.insertText("\n\n")
                    elif(self.LAST_WAS_TWO_RETURN == 0) and (self.LAST_WAS_ONE_RETURN == 1):
                        self.LAST_WAS_TWO_RETURN = 1
                        self.textCursor.insertText("\n")
                    self.CURRENT_FONT_SIZE -= 6
                    self.format.setFontPointSize(self.CURRENT_FONT_SIZE)
                    if not (self.B_STILL_ACTIVE):
                        self.format.setFontWeight(QFont.Normal)
                    self.H_STILL_ACTIVE=0
                    return
                elif(tag == "/H4"):
                    if(self.LAST_WAS_TWO_RETURN == 0) and (self.LAST_WAS_ONE_RETURN == 0):
                        self.LAST_WAS_TWO_RETURN = 1
                        self.LAST_WAS_ONE_RETURN = 1
                        self.textCursor.insertText("\n\n")
                    elif(self.LAST_WAS_TWO_RETURN == 0) and (self.LAST_WAS_ONE_RETURN == 1):
                        self.LAST_WAS_TWO_RETURN = 1
                        self.textCursor.insertText("\n")
                    #self.CURRENT_FONT_SIZE -= 0
                    #self.format.setFontPointSize(self.CURRENT_FONT_SIZE)
                    if not (self.B_STILL_ACTIVE):
                        self.format.setFontWeight(QFont.Normal)
                    self.H_STILL_ACTIVE=0
                    return
                elif(tag == "/H5"):
                    if(self.LAST_WAS_TWO_RETURN == 0) and (self.LAST_WAS_ONE_RETURN == 0):
                        self.LAST_WAS_TWO_RETURN = 1
                        self.LAST_WAS_ONE_RETURN = 1
                        self.textCursor.insertText("\n\n")
                    elif(self.LAST_WAS_TWO_RETURN == 0) and (self.LAST_WAS_ONE_RETURN == 1):
                        self.LAST_WAS_TWO_RETURN = 1
                        self.textCursor.insertText("\n")
                    self.CURRENT_FONT_SIZE += 2
                    self.format.setFontPointSize(self.CURRENT_FONT_SIZE)
                    if not (self.B_STILL_ACTIVE):
                        self.format.setFontWeight(QFont.Normal)
                    self.H_STILL_ACTIVE=0
                    return
                elif(tag == "/H6"):
                    if(self.LAST_WAS_TWO_RETURN == 0) and (self.LAST_WAS_ONE_RETURN == 0):
                        self.LAST_WAS_TWO_RETURN = 1
                        self.LAST_WAS_ONE_RETURN = 1
                        self.textCursor.insertText("\n\n")
                    elif(self.LAST_WAS_TWO_RETURN == 0) and (self.LAST_WAS_ONE_RETURN == 1):
                        self.LAST_WAS_TWO_RETURN = 1
                        self.textCursor.insertText("\n")
                    self.CURRENT_FONT_SIZE += 4
                    self.format.setFontPointSize(self.CURRENT_FONT_SIZE)
                    if not (self.B_STILL_ACTIVE):
                        self.format.setFontWeight(QFont.Normal)
                    self.H_STILL_ACTIVE=0
                    return
                elif(tag == "/HEAD"):
                    return
                elif(tag == "/HEADER"):
                    return
                elif(tag == "/HTML"):
                    return
                elif(tag == "/I"):
                    self.format.setFontItalic(False)
                    return
                elif(tag == "/IFRAME"):
                    return
                elif(tag == "/INS"):
                    self.format.setFontUnderline(False)
                    return
                elif(tag == "/KBD"):
                    return
                elif(tag == "/KEYGEN"):
                    return
                elif(tag == "/LABEL"):
                    return
                elif(tag == "/LEGEND"):
                    return
                elif(tag == "/LI"):
                    return
                elif(tag == "/MAIN"):
                    return
                elif(tag == "/MAP"):
                    return
                elif(tag == "/MARK"):
                    return
                elif(tag == "/MENU"):
                    return
                elif(tag == "/MENUITEM"):
                    return
                elif(tag == "/METER"):
                    return
                elif(tag == "/NAV"):
                    return
                elif(tag == "/NOFRAMES"):
                    #NOT SUPPORTED IN HTML5
                    return
                elif(tag == "/NOSCRIPT"):
                    return
                elif(tag == "/OBJECT"):
                    return
                elif(tag == "/OL"):
                    return
                elif(tag == "/OPTGROUP"):
                    return
                elif(tag == "/OPTION"):
                    return
                elif(tag == "/OUTPUT"):
                    return
                elif(tag == "/P"):
                    if(self.LAST_WAS_TWO_RETURN == 0) and (self.LAST_WAS_ONE_RETURN == 0):
                        self.LAST_WAS_TWO_RETURN = 1
                        self.LAST_WAS_ONE_RETURN = 1
                        self.textCursor.insertText("\n\n")
                    elif(self.LAST_WAS_TWO_RETURN == 0) and (self.LAST_WAS_ONE_RETURN == 1):
                        self.LAST_WAS_TWO_RETURN = 1
                        self.textCursor.insertText("\n")
                    return
                elif(tag == "/PICTURE"):
                    return
                elif(tag == "/PRE"):
                    return
                elif(tag == "/PROGRESS"):
                    return
                elif(tag == "/Q"):
                    return
                elif(tag == "/RP"):
                    return
                elif(tag == "/RT"):
                    return
                elif(tag == "/RUBY"):
                    return
                elif(tag == "/S"):
                    self.format.setFontStrikeOut(False)
                    return
                elif(tag == "/SAMP"):
                    return
                elif(tag == "/SCRIPT"):
                    return
                elif(tag == "/SECTION"):
                    return
                elif(tag == "/SELECT"):
                    return
                elif(tag == "/SMALL"):
                    self.CURRENT_FONT_SIZE += 3
                    self.format.setFontPointSize(self.CURRENT_FONT_SIZE)
                    return
                elif(tag == "/SOURCE"):
                    return
                elif(tag == "/SPAN"):
                    return
                elif(tag == "/STRIKE"):
                    #NOT SUPPORTED IN HTML5
                    return
                elif(tag == "/STRONG"):
                    self.format.setFontWeight(QFont.Normal)
                    return
                elif(tag == "/STYLE"):
                    return
                elif(tag == "/SUB"):
                    self.format.setVerticalAlignment(QTextCharFormat.AlignNormal)
                    return
                elif(tag == "/SUMMARY"):
                    return
                elif(tag == "/SUP"):
                    self.format.setVerticalAlignment(QTextCharFormat.AlignNormal)
                    return
                elif(tag == "/TABLE"):
                    return
                elif(tag == "/TBODY"):
                    return
                elif(tag == "//TD"):
                    return
                elif(tag == "//TEXTAREA"):
                    return
                elif(tag == "/TFOOT"):
                    return
                elif(tag == "/TH"):
                    return
                elif(tag == "/THEAD"):
                    return
                elif(tag == "/TIME"):
                    return
                elif(tag == "/TITLE"):
                    return
                elif(tag == "/TR"):
                    return
                elif(tag == "/TRACK"):
                    return
                elif(tag == "/TT"):
                    #NOT SUPPORTED IN HTML5
                    return
                elif(tag == "/U"):
                    self.format.setFontUnderline(False)
                    return
                elif(tag == "/UL"):
                    return
                elif(tag == "/VAR"):
                    return
                elif(tag == "/VIDEO"):
                    return
                elif(tag == "/WBR"):
                    return    

    def foundLink(self, link):
        if "A" in self.ACTIVE_TAGS:
            self.format.setAnchorHref(link)
        return
    
    def setBackgroundColor(self,hex):
        while len(hex) < 6:
            hex = hex + 'f'
        colors=re.findall("..?",hex)
        self.widget.setAutoFillBackground(True)
        color=QtGui.QColor(int(colors[0],16),int(colors[1],16),int(colors[2],16))
        alpha = 140
        values = "{r}, {g}, {b}, {a}".format(r=color.red(),g=color.green(),b=color.blue(),a=alpha)
        self.widget.setStyleSheet("QTextBrowser { background-color: rgba(" + values + "); }")

    def imageParams(self, w, h, src, srcLoc, pSrc):
        self.imageWidth=w
        self.imageHeight=h
        self.imageSrc=""+src
        self.imageSrcLocation=srcLoc
        self.pageSrc=""+pSrc

##        print(self.imageWidth)
##        print(self.imageHeight)
##        print(self.imageSrc)
##        print(self.imageSrcLocation)
        return

