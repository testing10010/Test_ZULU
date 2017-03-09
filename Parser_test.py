from Parser import *
#stuff

def test_parser_simple():
    parser = Parser(QTextEdit,1)
    parser.renderPage("siteTest.html")
    expected ="HTMLHEADTITLETest2/TITLE/HEADBODYCENTERIMG/CENTERHRAGoogle/APAYoutube/A/PPAFacebook/A/Pis a link to " \
              "another nifty siteH1This is a Header/H1BH4This is a Medium Header/H4Bold still working/BSend me mail " \
              "atAsupport@yourcompany.com/A.PThis is a new paragraph!PBThis is a new paragraph!/BBRBIThis is a new sentence " \
              "without a paragraph break, in bold italics./I/BHR/BODY/HTML"


    out=parser.renderer.textOutput
    assert out==expected

test_parser_simple()