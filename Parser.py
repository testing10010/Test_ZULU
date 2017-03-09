from PyQt5.QtWidgets import QTextEdit, QApplication
from PyQt5 import QtGui
import re
import urllib.request
from urllib.request import Request, urlopen
import textwrap
from copy import deepcopy
from Wrenderer import *

class Parser():
    def __init__(self, initWidget,mode):
        self.testMode = mode
        if mode:
            self.renderer=Renderer(initWidget,mode)
            return
        self.BACKGROUND_COLOR="FFFFFF"
        self.widget = initWidget
        self.renderer = Renderer(initWidget,mode)
        self.widget.setReadOnly(True)
        self.widget.clear()


    def renderPage(self, site):
        data = ""
        site = site.strip()
        if(re.match("[^. ]*.html", site)):
            try:
                print("found not a file")
                file = open(site, "r+", encoding="latin-1")
                data="".join(line.strip() for line in file)
            except Exception:
                return None
        else:
            if (' ' in site) or (re.match(".[a-zA-Z]$", site)):
                print("found not a site")
                site = re.sub(' ','+',site)
                site = "https://www.google.com/search?q=" + site
                #these next two lines are required to stop getting forbidden errors
                #from sites thinking we are a bot. fakes as if was opened in mozilaa
                #might need for regular opening later down the line...
                req = Request(site, headers={'User-Agent': 'Mozilla/5.0'})
                data = urlopen(req).read().decode('utf-8')
            else:
                print("found a site")
                if not(re.match("http[s]?://", site)):
                    site = "https://" + site
                try:
                    print(site)
                    print("reached")
                    i = site.find("google.com")
                    if i != -1:
                        print("google here")
                        if site.find("www") == -1:
                            site = site[:i] + "www." + site[i:]
                        print(site)
                        data = str(urllib.request.urlopen(site).read())
                        data = data[2:len(data)-1]
##                        print(data)
##                        print("the google clause")
                    else:
                        data = str(urllib.request.urlopen(site).read().decode('utf-8'))
                except Exception:
                    return None


        
            
##            elif(re.match("www.[^ ]*.com", site)):
##                site = "https://" + site
##            elif(re.match("[^ ]*.com", site)):
##                site = "https://www." + site
##            else:
##                search = site.strip()
##                search = re.sub(' ','+',search)
##                site = "https://www.google.com/search?q=" + search
##            page = "livePage.html"
##            Parser.loadURL(site, "livePage.html")
        #The void elements in HTML 4.01/XHTML 1.0 Strict are are;
        #base, br, col, hr, img, input, link, meta, and param.
        #HTML5 currently adds command, keygen, and source to that list.

        #HTML <head> tag does not print things, but puts in elements for the rest
        # of the document. tags that can be ONLY in head are:
        #<title>,<style>,<base>,<link>,<meta>,<script>,<noscript>


        
##        #tags=[]
##        #attributes=[]
##        file = open(page, "r+", encoding="latin-1")
##        data="".join(line.strip() for line in file)
##        #print(data)
        data = re.split('(<[^><]*>)', data)
##        #print(data)
        count = 0
        for token in data:
            token = token.strip()
            token = re.sub(' +',' ',token)
            token = re.sub(' >','>',token) #some cleanup that HTML parsers normally do
            if len(token) > 0:

    #will split tags from their attributes
    #re.split('([^>=<\s]+="[^><"]+"|[^>=<\s]+=[^<>="\'\s]+)', test)



#========================================================
#      START TAG         START TAG       START TAG
#========================================================
                if re.match("<", token) and not re.match("</", token): #if it is not an end tag
                    upperToken = token.upper()
                    # Unique tags that needs to be handle
                    if re.match("<!--", upperToken):
                        # TODO deal with comments
                        self.renderer.foundTag("COMMENT_START")
                        continue
                    elif re.match("<A[ >]", upperToken):
                        # TODO deal with hyperlinks
                        self.renderer.foundTag("A")
                        # ======Split the A tag into attributes==============
                        if "HREF" in upperToken:
                            attributes=re.split(r'HREF=', upperToken)
                            for atr in attributes:
                                if re.match("^\s*\"",atr):
                                    link = (re.split("\"", atr))[1]
                                    self.renderer.foundLink(link)

                        continue
                    elif re.match("<ABBR[ >]", upperToken):
                        # TODO deal with abbreviation/acronym formatting
                        self.renderer.foundTag("ABBR")
                        continue
                    elif re.match("<ACRONYM[ >]", upperToken):
                        # TODO deal with acronym formatting
                        self.renderer.foundTag("ACRONYM")
                        #NOT SUPPORTED IN HTML5
                        continue
                    elif re.match("<ADDRESS[ >]", upperToken):
                        # TODO deal with information for the author/owner of a document formatting.
                        self.renderer.foundTag("ADDRESS")
                        continue
                    elif re.match("<APPLET[ >]", upperToken):
                        # TODO deal with embedded applets.
                        self.renderer.foundTag("APPLET")
                        #NOT SUPPORTED IN HTML5
                        continue
                    elif re.match("<AREA[ >]", upperToken):
                        # TODO deal with area inside image-maps
                        self.renderer.foundTag("AREA")
                        continue
                    elif re.match("<ARTICLE[ >]", upperToken):
                        # TODO deal with articles
                        self.renderer.foundTag("ARTICLE")
                        continue
                    elif re.match("<ASIDE[ >]", upperToken):
                        # TODO deal with content aside from the page content
                        self.renderer.foundTag("ASIDE")
                        continue
                    elif re.match("<AUDIO[ >]", upperToken):
                        # TODO deal with sound content
                        self.renderer.foundTag("AUDIO")
                        continue
                    elif re.match("<B[ >]", upperToken):
                        # TODO deal with bold text
                        self.renderer.foundTag("B")
                        continue
                    elif re.match("<BASE[ >]", upperToken):
                        # TODO deal with URL/target for all relative URLs in a document
                        self.renderer.foundTag("BASE")
                        continue
                    elif re.match("<BASEFONT[ >]", upperToken):
                        # TODO deal with default font color and such
                        self.renderer.foundTag("BASEFONT")
                        #NOT SUPPORTED IN HTML5
                        continue
                    elif re.match("<BDI[ >]", upperToken):
                        # TODO deal with the BDI tag, whatever it is...
                        self.renderer.foundTag("BDI")
                        continue
                    elif re.match("<BDO[ >]", upperToken):
                        # TODO deal with overriding text direction
                        self.renderer.foundTag("BDO")
                        continue
                    elif re.match("<BIG[ >]", upperToken):
                        # TODO deal with bigger text
                        self.renderer.foundTag("BIG")
                        #NOT SUPPORTED IN HTML5
                        continue
                    elif re.match("<BLOCKQUOTE[ >]", upperToken):
                        # TODO deal with a block quote
                        self.renderer.foundTag("BLOCKQUOTE")
                        continue
                    elif re.match("<BODY[ >]", upperToken):
                        # TODO deal with document's body

                        # ======Testing Purposes ==============
                        if self.testMode:
                            self.renderer.foundTag("BODY")
                            continue
                        # ======Split the body tag into attributes==============
                        attributes=re.split(r'\s', upperToken)
                        for atr in attributes:
                            if re.match("ALINK",atr):
                                # TODO deal with the color of links
                                continue
                            if re.match("BACKGROUND",atr):
                                # TODO insert Image as background
                                continue
                            if (re.match("BGCOLOR", atr)) and ("SCRIPT" not in self.renderer.ACTIVE_TAGS):
                                color = "ffffff"
                                try:
                                    color=re.split("\"",atr)[1]
                                    color = color.replace("#","")
                                except Exception:
                                    continue
                                self.renderer.setBackgroundColor(color)
                                continue
                            if re.match("LINK",atr):
                                # TODO deal with color of unvisited links in document
                                continue
                            if re.match("TEXT",atr):
                                # TODO deal with the color of text
                                continue
                            if re.match("VLINKS",atr):
                                # TODO deal with color of visited links
                                continue
                        self.renderer.foundTag("BODY")
                        continue
                    elif re.match("<BR[ >]", upperToken):
                        # TODO deal with single line breaks
                        self.renderer.foundTag("BR")
                        continue
                    elif re.match("<BUTTON[ >]", upperToken):
                        # TODO deal with clickable buttons
                        self.renderer.foundTag("BUTTON")
                        continue
                    elif re.match("<CANVAS[ >]", upperToken):
                        # TODO deal with canvas drawing with scripts
                        self.renderer.foundTag("CANVAS")
                        continue
                    elif re.match("<CAPTION[ >]", upperToken):
                        # TODO deal with table captions
                        self.renderer.foundTag("CAPTION")
                        continue
                    elif re.match("<CENTER[ >]", upperToken):
                        # TODO deal with centered text
                        self.renderer.foundTag("CENTER")
                        #NOT SUPPORTED IN HTML5
                        continue
                    elif re.match("<CITE[ >]", upperToken):
                        # TODO deal with work titles
                        self.renderer.foundTag("CITE")
                        continue
                    elif re.match("<CODE[ >]", upperToken):
                        # TODO deal with computer code sections
                        self.renderer.foundTag("CODE")
                        continue
                    elif re.match("<COL[ >]", upperToken):
                        # TODO deal with column properties for below
                        self.renderer.foundTag("COL")
                        continue
                    elif re.match("<COLGROUP[ >]", upperToken):
                        # TODO deal with table columns
                        self.renderer.foundTag("COLGROUP")
                        continue
                    elif re.match("<DATALIST[ >]", upperToken):
                        # TODO deal with lists of pre-defined options for input controls
                        self.renderer.foundTag("DATALIST")
                        continue
                    elif re.match("<DD[ >]", upperToken):
                        # TODO deal with description/value of terms in description lists
                        self.renderer.foundTag("DD")
                        continue
                    elif re.match("<DEL[ >]", upperToken):
                        # TODO deal with strikethrough text essentially
                        self.renderer.foundTag("DEL")
                        continue
                    elif re.match("<DETAILS[ >]", upperToken):
                        # TODO deal with additional details that the user can view or hide
                        self.renderer.foundTag("DETAILS")
                        continue
                    elif re.match("<DFN[ >]", upperToken):
                        # TODO deal with defining instance of terms
                        self.renderer.foundTag("DFN")
                        continue
                    elif re.match("<DIALOG[ >]", upperToken):
                        # TODO deal with dialog boxes
                        self.renderer.foundTag("DIALOG")
                        continue
                    elif re.match("<DIR[ >]", upperToken):
                        # TODO deal with directory lists
                        self.renderer.foundTag("DIR")
                        #NOT SUPPORTED IN HTML5
                        continue
                    elif re.match("<DIV[ >]", upperToken):
                        # TODO deal with section in documents
                        self.renderer.foundTag("DIV")
                        continue
                    elif re.match("<DL[ >]", upperToken):
                        # TODO deal with description lists
                        self.renderer.foundTag("DL")
                        continue
                    elif re.match("<DT[ >]", upperToken):
                        # TODO deal with term/names in a description list
                        self.renderer.foundTag("DT")
                        continue
                    elif re.match("<EM[ >]", upperToken):
                        # TODO deal with still italicized text
                        self.renderer.foundTag("EM")
                        continue
                    elif re.match("<FIELDSET[ >]", upperToken):
                        # TODO deal with groups related in a form
                        self.renderer.foundTag("FIELDSET")
                        continue
                    elif re.match("<FIGCAPTION[ >]", upperToken):
                        # TODO deal with captions for figure elements
                        self.renderer.foundTag("FIGCAPTION")
                        continue
                    elif re.match("<FIGURE[ >]", upperToken):
                        # TODO deal with self-contained content
                        self.renderer.foundTag("FIGURE")
                        continue
                    elif re.match("<FONT[ >]", upperToken):
                        # TODO deal with font size and shit
                        #NOT SUPPORTED IN HTML5
                        self.renderer.foundTag("FONT")
                        continue
                    elif re.match("<FOOTER[ >]", upperToken):
                        # TODO deal with footers for documents
                        self.renderer.foundTag("FOOTER")
                        continue
                    elif re.match("<FORM[ >]", upperToken):
                        # TODO deal with HTML forms
                        self.renderer.foundTag("FORM")
                        continue
                    elif re.match("<FRAME[ >]", upperToken):
                        # TODO deal with frames
                        #NOT SUPPORTED IN HTML5
                        self.renderer.foundTag("FRAME")
                        continue
                    elif re.match("<FRAMESET[ >]", upperToken):
                        # TODO deal with sets of frames
                        #NOT SUPPORTED IN HTML5
                        self.renderer.foundTag("FRAMESET")
                        continue
                    elif re.match("<H1[ >]", upperToken):
                        # TODO deal with heading 1
                        self.renderer.foundTag("H1")
                        continue
                    elif re.match("<H2[ >]", upperToken):
                        # TODO deal with heading 2
                        self.renderer.foundTag("H2")
                        continue
                    elif re.match("<H3[ >]", upperToken):
                        # TODO deal with heading 3
                        self.renderer.foundTag("H3")
                        continue
                    elif re.match("<H4[ >]", upperToken):
                        # TODO deal with heading 4
                        self.renderer.foundTag("H4")
                        continue
                    elif re.match("<H5[ >]", upperToken):
                        # TODO deal with heading 5
                        self.renderer.foundTag("H5")
                        continue
                    elif re.match("<H6[ >]", upperToken):
                        # TODO deal with heading 6
                        self.renderer.foundTag("H6")
                        continue
                    elif re.match("<HEAD[ >]", upperToken):
                        # TODO deal with head information
                        self.renderer.foundTag("HEAD")
                        continue
                    elif re.match("<HEADER[ >]", upperToken):
                        # TODO deal with headers
                        self.renderer.foundTag("HEADER")
                        continue
                    elif re.match("<HR[ >]", upperToken):
                        # TODO deal with HR(horizontal bar to seperate shit)
                        self.renderer.foundTag("HR")
                        continue
                    elif re.match("<HTML[ >]", upperToken):
                        # TODO deal with HTML roots
                        self.renderer.foundTag("HTML")
                        continue
                    elif re.match("<I[ >]", upperToken):
                        # TODO deal with italization
                        self.renderer.foundTag("I")
                        continue
                    elif re.match("<IFRAME[ >]", upperToken):
                        # TODO deal with inline frames
                        self.renderer.foundTag("IFRAME")
                        continue
                    elif re.match("<IMG[ >]", upperToken):
                        # TODO deal with images
                        w=0
                        h=0
                        src=""
                        srcLoc=0
                        attributes=re.split(r'\s', token)
                        for atr in attributes:
                            if re.match('[Ss][Rr][Cc][ ]*=',atr):
                                try:
                                    srcLoc=0
                                    src=re.split("\"",atr)[1]
                                    if (re.match("[Hh][Tt][Tt][Pp][Ss]?://", src)) or (re.match("[Ww][Ww][Ww].",src)):
                                        srcLoc=1
                                    else:
                                        srcLoc=2

                                                                          
                                except Exception:
                                    continue
                                #self.renderer.backgroundColor(color)
                                continue
                            elif re.match("ALT[ ]*=",atr):
                                continue
                            elif re.match("HEIGHT[ ]*=",atr):
                                try:
                                    h=re.split("\"",atr)[1]
                                except Exception:
                                    continue
                                continue
                            elif re.match("WIDTH[ ]*=",atr):
                                try:
                                    w=re.split("\"",atr)[1]
                                except Exception:
                                    continue
                                continue
                        print("parser" + str(src))
                        self.renderer.imageParams(w,h,src,srcLoc,site)
                        self.renderer.foundTag("IMG")
                        continue
                    elif re.match("<INPUT[ >]", upperToken):
                        # TODO deal with input control
                        self.renderer.foundTag("INPUT")
                        continue
                    elif re.match("<INS[ >]", upperToken):
                        # TODO deal with text that has been inserted into a document
                        self.renderer.foundTag("INS")
                        continue
                    elif re.match("<KBD[ >]", upperToken):
                        # TODO deal with keyboard input
                        self.renderer.foundTag("KBD")
                        continue
                    elif re.match("<KEYGEN[ >]", upperToken):
                        # TODO deal with key-pair generator fields(for forms)
                        self.renderer.foundTag("KEYGEN") 
                        continue
                    elif re.match("<LABEL[ >]", upperToken):
                        # TODO deal with label for a <input> element
                        self.renderer.foundTag("LABEL") 
                        continue
                    elif re.match("<LEGEND[ >]", upperToken):
                        # TODO deal with caption for a <fieldset> element
                        self.renderer.foundTag("LEGEND") 
                        continue
                    elif re.match("<LI[ >]", upperToken):
                        # TODO deal with list items
                        self.renderer.foundTag("LI")
                        continue
                    elif re.match("<LINK[ >]", upperToken):
                        # TODO deal with the relationship between a document and an external resource
                        #(most used to link to style sheets)
                        self.renderer.foundTag("LINK")
                        continue
                    elif re.match("<MAIN[ >]", upperToken):
                        # TODO deal with specifying main contents
                        self.renderer.foundTag("MAIN")
                        continue
                    elif re.match("<MAP[ >]", upperToken):
                        # TODO deal with client-side image maps
                        self.renderer.foundTag("MAP")
                        continue
                    elif re.match("<MARK[ >]", upperToken):
                        # TODO deal with highlighted text
                        self.renderer.foundTag("MARK")
                        continue
                    elif re.match("<MENU[ >]", upperToken):
                        # TODO deal with menus/command lists
                        self.renderer.foundTag("MENU")
                        continue
                    elif re.match("<MENUITEM[ >]", upperToken):
                        # TODO deal with commands for a popup menu(fuck this tag)
                        self.renderer.foundTag("MENUITEM")
                        continue
                    elif re.match("<META[ >]", upperToken):
                        # TODO deal with metadata
                        self.renderer.foundTag("META")
                        continue
                    elif re.match("<METER[ >]", upperToken):
                        # TODO deal with defining guages
                        self.renderer.foundTag("METER")
                        continue
                    elif re.match("<NAV[ >]", upperToken):
                        # TODO deal with navigation links list
                        self.renderer.foundTag("NAV")
                        continue
                    elif re.match("<NOFRAMES[ >]", upperToken):
                        # TODO deal with supporting non-frame users
                        #NOT SUPPORTED IN HTML5
                        self.renderer.foundTag("NOFRAMES")
                        continue
                    elif re.match("<NOSCRIPT[ >]", upperToken):
                        # TODO deal with people without client-side scripts
                        self.renderer.foundTag("NOSCRIPT")
                        continue
                    elif re.match("<OBJECT[ >]", upperToken):
                        # TODO deal with embedded objects
                        self.renderer.foundTag("OBJECT")
                        continue
                    elif re.match("<OL[ >]", upperToken):
                        # TODO deal with ordered lists
                        self.renderer.foundTag("OL")
                        continue
                    elif re.match("<OPTGROUP[ >]", upperToken):
                        # TODO deal with option groups in drop-down lists
                        self.renderer.foundTag("OPTGROUP")
                        continue
                    elif re.match("<OPTION[ >]", upperToken):
                        # TODO deal with options in drop-down lists
                        self.renderer.foundTag("OPTION")
                        continue
                    elif re.match("<OUTPUT[ >]", upperToken):
                        # TODO deal with calculation results
                        self.renderer.foundTag("OUTPUT")
                        continue
                    elif re.match("<P[ >]", upperToken):
                        # TODO deal with paragraphs
                        self.renderer.foundTag("P")
                        continue
                    elif re.match("<PARAM[ >]", upperToken):
                        # TODO deal with parameters for objects
                        self.renderer.foundTag("PARAM")
                        continue
                    elif re.match("<PICTURE[ >]", upperToken):
                        # TODO deal with containters for multiple images
                        self.renderer.foundTag("PICTURE")
                        continue
                    elif re.match("<PRE[ >]", upperToken):
                        # TODO deal with preformatted text
                        self.renderer.foundTag("PRE")
                        continue
                    elif re.match("<PROGRESS[ >]", upperToken):
                        # TODO deal with progress bars
                        self.renderer.foundTag("PROGRESS")
                        continue
                    elif re.match("<Q[ >]", upperToken):
                        # TODO deal with short quotes
                        self.renderer.foundTag("Q")
                        continue
                    elif re.match("<RP[ >]", upperToken):
                        # TODO deal with what to show in browsers that dont support below
                        self.renderer.foundTag("RP")
                        continue
                    elif re.match("<RT[ >]", upperToken):
                        # TODO deal with explination/pronunciation of below
                        self.renderer.foundTag("RT")
                        continue
                    elif re.match("<RUBY[ >]", upperToken):
                        # TODO deal with ruby annotation(asian stuff... nope...)
                        self.renderer.foundTag("RUBY")
                        continue
                    elif re.match("<S[ >]", upperToken):
                        # TODO deal with essentially strikethrough text
                        self.renderer.foundTag("S")
                        continue
                    elif re.match("<SAMP[ >]", upperToken):
                        # TODO deal with sample output from computer prog
                        self.renderer.foundTag("SAMP")
                        continue
                    elif re.match("<SCRIPT[ >]", upperToken):
                        # TODO deal with client-side script
                        self.renderer.foundTag("SCRIPT")
                        continue
                    elif re.match("<SECTION[ >]", upperToken):
                        # TODO deal with selection in documents
                        self.renderer.foundTag("SECTION")
                        continue
                    elif re.match("<SELECT[ >]", upperToken):
                        # TODO deal with drop-down lists
                        self.renderer.foundTag("SELECT")
                        continue
                    elif re.match("<SMALL[ >]", upperToken):
                        # TODO deal with smaller text
                        self.renderer.foundTag("SMALL")
                        continue
                    elif re.match("<SOURCE[ >]", upperToken):
                        # TODO deal with media resources
                        self.renderer.foundTag("SOURCE")
                        continue
                    elif re.match("<SPAN[ >]", upperToken):
                        # TODO deal with selection in documents
                        self.renderer.foundTag("SPAN")
                        continue
                    elif re.match("<STRIKE[ >]", upperToken):
                        # TODO deal with strikethrough text
                        self.renderer.foundTag("STRIKE")
                        #NOT SUPPORTED IN HTML5
                        continue
                    elif re.match("<STRONG[ >]", upperToken):
                        # TODO deal with strong text
                        self.renderer.foundTag("STRONG")
                        continue
                    elif re.match("<STYLE[ >]", upperToken):
                        # TODO deal with style information
                        self.renderer.foundTag("STYLE")
                        continue
                    elif re.match("<SUB[ >]", upperToken):
                        # TODO deal with subscripts
                        self.renderer.foundTag("SUB")
                        continue
                    elif re.match("<SUMMARY[ >]", upperToken):
                        # TODO deal with headings for <details> elements
                        self.renderer.foundTag("SUMMARY")
                        continue
                    elif re.match("<SUP[ >]", upperToken):
                        # TODO deal with superscript
                        self.renderer.foundTag("SUP")
                        continue
                    elif re.match("<TABLE[ >]", upperToken):
                        # TODO deal with tables
                        self.renderer.foundTag("TABLE")
                        continue
                    elif re.match("<TBODY[ >]", upperToken):
                        # TODO deal with grouping body content in tables
                        self.renderer.foundTag("TBODY")
                        continue
                    elif re.match("<TD[ >]", upperToken):
                        # TODO deal with table cells
                        self.renderer.foundTag("TD")
                        continue
                    elif re.match("<TEXTAREA[ >]", upperToken):
                        # TODO deal with multiline input control
                        self.renderer.foundTag("TEXTAREA")
                        continue
                    elif re.match("<TFOOT[ >]", upperToken):
                        # TODO deal with grouping footer content in tables
                        self.renderer.foundTag("TFOOT")
                        continue
                    elif re.match("<TH[ >]", upperToken):
                        # TODO deal with header cells in tables
                        self.renderer.foundTag("TH")
                        continue
                    elif re.match("<THEAD[ >]", upperToken):
                        # TODO deal with header content in tables
                        self.renderer.foundTag("THEAD")
                        continue
                    elif re.match("<TIME[ >]", upperToken):
                        # TODO deal with date/times
                        self.renderer.foundTag("TIME")
                        continue
                    elif re.match("<TITLE[ >]", upperToken):
                        # TODO deal with document titles
                        self.renderer.foundTag("TITLE")
                        continue
                    elif re.match("<TR[ >]", upperToken):
                        # TODO deal with table rows
                        self.renderer.foundTag("TR")
                        continue
                    elif re.match("<TRACK[ >]", upperToken):
                        # TODO deal with tracks for medis(audio/video)
                        self.renderer.foundTag("TRACK")
                        continue
                    elif re.match("<TT[ >]", upperToken):
                        # TODO deal with teletype
                        self.renderer.foundTag("TT")
                        #NOT SUPPORTED IN HTML5
                        continue
                    elif re.match("<U[ >]", upperToken):
                        # TODO deal with underlining
                        self.renderer.foundTag("U")
                        continue
                    elif re.match("<UL[ >]", upperToken):
                        # TODO deal with unordered list
                        self.renderer.foundTag("UL")
                        continue
                    elif re.match("<VAR[ >]", upperToken):
                        # TODO deal with variables
                        self.renderer.foundTag("VAR")
                        continue
                    elif re.match("<VIDEO[ >]", upperToken):
                        # TODO deal with video
                        self.renderer.foundTag("VIDEO")
                        continue
                    elif re.match("<WBR[ >]", upperToken):
                        # TODO deal with possible line breaks
                        self.renderer.foundTag("WBR")
                        continue
                    else: #this tag must be ridiculous
                        #so try to handle these things. (prob do nothing)
                        continue

#========================================================
#        END TAG         END TAG       END TAG
#========================================================
                elif re.match("</", token): #it is an end tag
                    upperToken = token.upper()
                    if re.match("</A[ >]", upperToken):
                        # TODO deal with hyperlinks
                        self.renderer.foundTag("/A")
                        continue
                    elif re.match("</ABBR[ >]", upperToken):
                        # TODO deal with abbreviation/acronym formatting
                        self.renderer.foundTag("/ABBR")
                        continue
                    elif re.match("</ACRONYM[ >]", upperToken):
                        # TODO deal with acronym formatting
                        self.renderer.foundTag("/ACRONYM")
                        #NOT SUPPORTED IN HTML5
                        continue
                    elif re.match("</ADDRESS[ >]", upperToken):
                        # TODO deal with information for the author/owner of a document formatting.
                        self.renderer.foundTag("/ADDRESS")
                        continue
                    elif re.match("</APPLET[ >]", upperToken):
                        # TODO deal with embedded applets.
                        self.renderer.foundTag("/APPLET")
                        #NOT SUPPORTED IN HTML5
                        continue
                    elif re.match("</AREA[ >]", upperToken):
                        # TODO deal with area inside image-maps
                        self.renderer.foundTag("/AREA")
                        continue
                    elif re.match("</ARTICLE[ >]", upperToken):
                        # TODO deal with articles
                        self.renderer.foundTag("/ARTICLE")
                        continue
                    elif re.match("</ASIDE[ >]", upperToken):
                        # TODO deal with content aside from the page content
                        self.renderer.foundTag("/ASIDE")
                        continue
                    elif re.match("</AUDIO[ >]", upperToken):
                        # TODO deal with sound content
                        self.renderer.foundTag("/AUDIO")
                        continue
                    elif re.match("</B[ >]", upperToken):
                        # TODO deal with bold text
                        self.renderer.foundTag("/B")
                        continue
                    elif re.match("</BASE[ >]", upperToken):
                        # TODO deal with URL/target for all relative URLs in a document
                        self.renderer.foundTag("/BASE")
                        continue
                    elif re.match("</BASEFONT[ >]", upperToken):
                        # TODO deal with default font color and such
                        self.renderer.foundTag("/BASEFONT")
                        #NOT SUPPORTED IN HTML5
                        continue
                    elif re.match("</BDI[ >]", upperToken):
                        # TODO deal with the BDI tag, whatever it is...
                        self.renderer.foundTag("/BDI")
                        continue
                    elif re.match("</BDO[ >]", upperToken):
                        # TODO deal with overriding text direction
                        self.renderer.foundTag("/BDO")
                        continue
                    elif re.match("</BIG[ >]", upperToken):
                        # TODO deal with bigger text
                        self.renderer.foundTag("/BIG")
                        #NOT SUPPORTED IN HTML5
                        continue
                    elif re.match("</BLOCKQUOTE[ >]", upperToken):
                        # TODO deal with a block quote
                        self.renderer.foundTag("/BLOCKQUOTE")
                        continue
                    elif re.match("</BODY[ >]", upperToken):
                        # TODO deal with document's body
                        self.renderer.foundTag("/BODY")
                        continue
                    elif re.match("</BR[ >]", upperToken):
                        # TODO deal with single line breaks
                        self.renderer.foundTag("/BR")
                        continue
                    elif re.match("</BUTTON[ >]", upperToken):
                        # TODO deal with clickable buttons
                        self.renderer.foundTag("/BUTTON")
                        continue
                    elif re.match("</CANVAS[ >]", upperToken):
                        # TODO deal with canvas drawing with scripts
                        self.renderer.foundTag("/CANVAS")
                        continue
                    elif re.match("</CAPTION[ >]", upperToken):
                        # TODO deal with table captions
                        self.renderer.foundTag("/CAPTION")
                        continue
                    elif re.match("</CENTER[ >]", upperToken):
                        # TODO deal with centered text
                        self.renderer.foundTag("/CENTER")
                        #NOT SUPPORTED IN HTML5
                        continue
                    elif re.match("</CITE[ >]", upperToken):
                        # TODO deal with work titles
                        self.renderer.foundTag("/CITE")
                        continue
                    elif re.match("</CODE[ >]", upperToken):
                        # TODO deal with computer code sections
                        self.renderer.foundTag("/CODE")
                        continue
                    elif re.match("</COL[ >]", upperToken):
                        # TODO deal with column properties for below
                        self.renderer.foundTag("/COL")
                        continue
                    elif re.match("</COLGROUP[ >]", upperToken):
                        # TODO deal with table columns
                        self.renderer.foundTag("/COLGROUP")
                        continue
                    elif re.match("</DATALIST[ >]", upperToken):
                        # TODO deal with lists of pre-defined options for input controls
                        self.renderer.foundTag("/DATALIST")
                        continue
                    elif re.match("</DD[ >]", upperToken):
                        # TODO deal with description/value of terms in description lists
                        self.renderer.foundTag("/DD")
                        continue
                    elif re.match("</DEL[ >]", upperToken):
                        # TODO deal with strikethrough text essentially
                        self.renderer.foundTag("/DEL")
                        continue
                    elif re.match("</DETAILS[ >]", upperToken):
                        # TODO deal with additional details that the user can view or hide
                        self.renderer.foundTag("/DETAILS")
                        continue
                    elif re.match("</DFN[ >]", upperToken):
                        # TODO deal with defining instance of terms
                        self.renderer.foundTag("/DFN")
                        continue
                    elif re.match("</DIALOG[ >]", upperToken):
                        # TODO deal with dialog boxes
                        self.renderer.foundTag("/DIALOG")
                        continue
                    elif re.match("</DIR[ >]", upperToken):
                        # TODO deal with directory lists
                        self.renderer.foundTag("/DIR")
                        #NOT SUPPORTED IN HTML5
                        continue
                    elif re.match("</DIV[ >]", upperToken):
                        # TODO deal with section in documents
                        self.renderer.foundTag("/DIV")
                        continue
                    elif re.match("</DL[ >]", upperToken):
                        # TODO deal with description lists
                        self.renderer.foundTag("/DL")
                        continue
                    elif re.match("</DT[ >]", upperToken):
                        # TODO deal with term/names in a description list
                        self.renderer.foundTag("/DT")
                        continue
                    elif re.match("</EM[ >]", upperToken):
                        # TODO deal with still italicized text
                        self.renderer.foundTag("/EM")
                        continue
                    elif re.match("</FIELDSET[ >]", upperToken):
                        # TODO deal with groups related in a form
                        self.renderer.foundTag("/FIELDSET")
                        continue
                    elif re.match("</FIGCAPTION[ >]", upperToken):
                        # TODO deal with captions for figure elements
                        self.renderer.foundTag("/FIGCAPTION")
                        continue
                    elif re.match("</FIGURE[ >]", upperToken):
                        # TODO deal with self-contained content
                        self.renderer.foundTag("/FIGURE")
                        continue
                    elif re.match("</FONT[ >]", upperToken):
                        # TODO deal with font size and shit
                        #NOT SUPPORTED IN HTML5
                        self.renderer.foundTag("/FONT")
                        continue
                    elif re.match("</FOOTER[ >]", upperToken):
                        # TODO deal with footers for documents
                        self.renderer.foundTag("/FOOTER")
                        continue
                    elif re.match("</FORM[ >]", upperToken):
                        # TODO deal with HTML forms
                        self.renderer.foundTag("/FORM")
                        continue
                    elif re.match("</FRAME[ >]", upperToken):
                        # TODO deal with frames
                        #NOT SUPPORTED IN HTML5
                        self.renderer.foundTag("/FRAME")
                        continue
                    elif re.match("</FRAMESET[ >]", upperToken):
                        # TODO deal with sets of frames
                        #NOT SUPPORTED IN HTML5
                        self.renderer.foundTag("/FRAMESET")
                        continue
                    elif re.match("</H1[ >]", upperToken):
                        # TODO deal with heading 1
                        self.renderer.foundTag("/H1")
                        continue
                    elif re.match("</H2[ >]", upperToken):
                        # TODO deal with heading 2
                        self.renderer.foundTag("/H2")
                        continue
                    elif re.match("</H3[ >]", upperToken):
                        # TODO deal with heading 3
                        self.renderer.foundTag("/H3")
                        continue
                    elif re.match("</H4[ >]", upperToken):
                        # TODO deal with heading 4
                        self.renderer.foundTag("/H4")
                        continue
                    elif re.match("</H5[ >]", upperToken):
                        # TODO deal with heading 5
                        self.renderer.foundTag("/H5")
                        continue
                    elif re.match("</H6[ >]", upperToken):
                        # TODO deal with heading 6
                        self.renderer.foundTag("/H6")
                        continue
                    elif re.match("</HEAD[ >]", upperToken):
                        # TODO deal with head information
                        self.renderer.foundTag("/HEAD")
                        continue
                    elif re.match("</HEADER[ >]", upperToken):
                        # TODO deal with headers
                        self.renderer.foundTag("/HEADER")
                        continue
                    elif re.match("</HR[ >]", upperToken):
                        # TODO deal with HR(horizontal bar to seperate shit)
                        self.renderer.foundTag("/HR")
                        continue
                    elif re.match("</HTML[ >]", upperToken):
                        # TODO deal with HTML roots
                        self.renderer.foundTag("/HTML")
                        continue
                    elif re.match("</I[ >]", upperToken):
                        # TODO deal with italization
                        self.renderer.foundTag("/I")
                        continue
                    elif re.match("</IFRAME[ >]", upperToken):
                        # TODO deal with inline frames
                        self.renderer.foundTag("/IFRAME")
                        continue
                    elif re.match("</IMG[ >]", upperToken):
                        # TODO deal with images
                        self.renderer.foundTag("/IMG")
                        continue
                    elif re.match("</INPUT[ >]", upperToken):
                        # TODO deal with input control
                        self.renderer.foundTag("/INPUT")
                        continue
                    elif re.match("</INS[ >]", upperToken):
                        # TODO deal with text that has been inserted into a document
                        self.renderer.foundTag("/INS")
                        continue
                    elif re.match("</KBD[ >]", upperToken):
                        # TODO deal with keyboard input
                        self.renderer.foundTag("/KBD")
                        continue
                    elif re.match("</KEYGEN[ >]", upperToken):
                        # TODO deal with key-pair generator fields(for forms)
                        self.renderer.foundTag("/KEYGEN") 
                        continue
                    elif re.match("</LABEL[ >]", upperToken):
                        # TODO deal with label for a </input> element
                        self.renderer.foundTag("/LABEL") 
                        continue
                    elif re.match("</LEGEND[ >]", upperToken):
                        # TODO deal with caption for a </fieldset> element
                        self.renderer.foundTag("/LEGEND") 
                        continue
                    elif re.match("</LI[ >]", upperToken):
                        # TODO deal with list items
                        self.renderer.foundTag("/LI")
                        continue
                    elif re.match("</LINK[ >]", upperToken):
                        # TODO deal with the relationship between a document and an external resource
                        #(most used to link to style sheets)
                        self.renderer.foundTag("/LINK")
                        continue
                    elif re.match("</MAIN[ >]", upperToken):
                        # TODO deal with specifying main contents
                        self.renderer.foundTag("/MAIN")
                        continue
                    elif re.match("</MAP[ >]", upperToken):
                        # TODO deal with client-side image maps
                        self.renderer.foundTag("/MAP")
                        continue
                    elif re.match("</MARK[ >]", upperToken):
                        # TODO deal with highlighted text
                        self.renderer.foundTag("/MARK")
                        continue
                    elif re.match("</MENU[ >]", upperToken):
                        # TODO deal with menus/command lists
                        self.renderer.foundTag("/MENU")
                        continue
                    elif re.match("</MENUITEM[ >]", upperToken):
                        # TODO deal with commands for a popup menu(fuck this tag)
                        self.renderer.foundTag("/MENUITEM")
                        continue
                    elif re.match("</META[ >]", upperToken):
                        # TODO deal with metadata
                        self.renderer.foundTag("/META")
                        continue
                    elif re.match("</METER[ >]", upperToken):
                        # TODO deal with defining guages
                        self.renderer.foundTag("/METER")
                        continue
                    elif re.match("</NAV[ >]", upperToken):
                        # TODO deal with navigation links list
                        self.renderer.foundTag("/NAV")
                        continue
                    elif re.match("</NOFRAMES[ >]", upperToken):
                        # TODO deal with supporting non-frame users
                        #NOT SUPPORTED IN HTML5
                        self.renderer.foundTag("/NOFRAMES")
                        continue
                    elif re.match("</NOSCRIPT[ >]", upperToken):
                        # TODO deal with people without client-side scripts
                        self.renderer.foundTag("/NOSCRIPT")
                        continue
                    elif re.match("</OBJECT[ >]", upperToken):
                        # TODO deal with embedded objects
                        self.renderer.foundTag("/OBJECT")
                        continue
                    elif re.match("</OL[ >]", upperToken):
                        # TODO deal with ordered lists
                        self.renderer.foundTag("/OL")
                        continue
                    elif re.match("</OPTGROUP[ >]", upperToken):
                        # TODO deal with option groups in drop-down lists
                        self.renderer.foundTag("/OPTGROUP")
                        continue
                    elif re.match("</OPTION[ >]", upperToken):
                        # TODO deal with options in drop-down lists
                        self.renderer.foundTag("/OPTION")
                        continue
                    elif re.match("</OUTPUT[ >]", upperToken):
                        # TODO deal with calculation results
                        self.renderer.foundTag("/OUTPUT")
                        continue
                    elif re.match("</P[ >]", upperToken):
                        # TODO deal with paragraphs
                        self.renderer.foundTag("/P")
                        continue
                    elif re.match("</PARAM[ >]", upperToken):
                        # TODO deal with parameters for objects
                        self.renderer.foundTag("/PARAM")
                        continue
                    elif re.match("</PICTURE[ >]", upperToken):
                        # TODO deal with containters for multiple images
                        self.renderer.foundTag("/PICTURE")
                        continue
                    elif re.match("</PRE[ >]", upperToken):
                        # TODO deal with preformatted text
                        self.renderer.foundTag("/PRE")
                        continue
                    elif re.match("</PROGRESS[ >]", upperToken):
                        # TODO deal with progress bars
                        self.renderer.foundTag("/PROGRESS")
                        continue
                    elif re.match("</Q[ >]", upperToken):
                        # TODO deal with short quotes
                        self.renderer.foundTag("/Q")
                        continue
                    elif re.match("</RP[ >]", upperToken):
                        # TODO deal with what to show in browsers that dont support below
                        self.renderer.foundTag("/RP")
                        continue
                    elif re.match("</RT[ >]", upperToken):
                        # TODO deal with explination/pronunciation of below
                        self.renderer.foundTag("/RT")
                        continue
                    elif re.match("</RUBY[ >]", upperToken):
                        # TODO deal with ruby annotation(asian stuff... nope...)
                        self.renderer.foundTag("/RUBY")
                        continue
                    elif re.match("</S[ >]", upperToken):
                        # TODO deal with essentially strikethrough text
                        self.renderer.foundTag("/S")
                        continue
                    elif re.match("</SAMP[ >]", upperToken):
                        # TODO deal with sample output from computer prog
                        self.renderer.foundTag("/SAMP")
                        continue
                    elif re.match("</SCRIPT[ >]", upperToken):
                        # TODO deal with client-side script
                        self.renderer.foundTag("/SCRIPT")
                        continue
                    elif re.match("</SECTION[ >]", upperToken):
                        # TODO deal with selection in documents
                        self.renderer.foundTag("/SECTION")
                        continue
                    elif re.match("</SELECT[ >]", upperToken):
                        # TODO deal with drop-down lists
                        self.renderer.foundTag("/SELECT")
                        continue
                    elif re.match("</SMALL[ >]", upperToken):
                        # TODO deal with smaller text
                        self.renderer.foundTag("/SMALL")
                        continue
                    elif re.match("</SOURCE[ >]", upperToken):
                        # TODO deal with media resources
                        self.renderer.foundTag("/SOURCE")
                        continue
                    elif re.match("</SPAN[ >]", upperToken):
                        # TODO deal with selection in documents
                        self.renderer.foundTag("/SPAN")
                        continue
                    elif re.match("</STRIKE[ >]", upperToken):
                        # TODO deal with strikethrough text
                        self.renderer.foundTag("/STRIKE")
                        #NOT SUPPORTED IN HTML5
                        continue
                    elif re.match("</STRONG[ >]", upperToken):
                        # TODO deal with strong text
                        self.renderer.foundTag("/STRONG")
                        continue
                    elif re.match("</STYLE[ >]", upperToken):
                        # TODO deal with style information
                        self.renderer.foundTag("/STYLE")
                        continue
                    elif re.match("</SUB[ >]", upperToken):
                        # TODO deal with subscripts
                        self.renderer.foundTag("/SUB")
                        continue
                    elif re.match("</SUMMARY[ >]", upperToken):
                        # TODO deal with headings for </details> elements
                        self.renderer.foundTag("/SUMMARY")
                        continue
                    elif re.match("</SUP[ >]", upperToken):
                        # TODO deal with superscript
                        self.renderer.foundTag("/SUP")
                        continue
                    elif re.match("</TABLE[ >]", upperToken):
                        # TODO deal with tables
                        self.renderer.foundTag("/TABLE")
                        continue
                    elif re.match("</TBODY[ >]", upperToken):
                        # TODO deal with grouping body content in tables
                        self.renderer.foundTag("/TBODY")
                        continue
                    elif re.match("</TD[ >]", upperToken):
                        # TODO deal with table cells
                        self.renderer.foundTag("/TD")
                        continue
                    elif re.match("</TEXTAREA[ >]", upperToken):
                        # TODO deal with multiline input control
                        self.renderer.foundTag("/TEXTAREA")
                        continue
                    elif re.match("</TFOOT[ >]", upperToken):
                        # TODO deal with grouping footer content in tables
                        self.renderer.foundTag("/TFOOT")
                        continue
                    elif re.match("</TH[ >]", upperToken):
                        # TODO deal with header cells in tables
                        self.renderer.foundTag("/TH")
                        continue
                    elif re.match("</THEAD[ >]", upperToken):
                        # TODO deal with header content in tables
                        self.renderer.foundTag("/THEAD")
                        continue
                    elif re.match("</TIME[ >]", upperToken):
                        # TODO deal with date/times
                        self.renderer.foundTag("/TIME")
                        continue
                    elif re.match("</TITLE[ >]", upperToken):
                        # TODO deal with document titles
                        self.renderer.foundTag("/TITLE")
                        continue
                    elif re.match("</TR[ >]", upperToken):
                        # TODO deal with table rows
                        self.renderer.foundTag("/TR")
                        continue
                    elif re.match("</TRACK[ >]", upperToken):
                        # TODO deal with tracks for medis(audio/video)
                        self.renderer.foundTag("/TRACK")
                        continue
                    elif re.match("</TT[ >]", upperToken):
                        # TODO deal with teletype
                        self.renderer.foundTag("/TT")
                        #NOT SUPPORTED IN HTML5
                        continue
                    elif re.match("</U[ >]", upperToken):
                        # TODO deal with underlining
                        self.renderer.foundTag("/U")
                        continue
                    elif re.match("</UL[ >]", upperToken):
                        # TODO deal with unordered list
                        self.renderer.foundTag("/UL")
                        continue
                    elif re.match("</VAR[ >]", upperToken):
                        # TODO deal with variables
                        self.renderer.foundTag("/VAR")
                        continue
                    elif re.match("</VIDEO[ >]", upperToken):
                        # TODO deal with video
                        self.renderer.foundTag("/VIDEO")
                        continue
                    elif re.match("</WBR[ >]", upperToken):
                        # TODO deal with possible line breaks
                        self.renderer.foundTag("/WBR")
                        continue
                    else: #this tag must be ridiculous
                        #so try to handle these things. (prob do nothing)
                        continue

#========================================================
#      STRING LIT         STRING LIT       STRING LIT
#========================================================
                else: #it is a string
                    self.renderer.printString(token)
                    continue

    #loads url and saves HTML to a file so it can be used by the other function.
    #TODO: save assests like images and videos.
    #DOES NOT WORK PRESENTLY
    def loadURL(url, page):
        #print(url)
        #if not re.match("https://", url):
            #url= "https://"+url
        urllib.request.urlretrieve(url, page)


#parser()
