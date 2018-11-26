# ######################################################################### ###
# ########################## Element Hunter X v1.0 ######################## ###
# ######################################################################### ###

# License: GPL v3
# Copyright github.com/eagleEggs
# Contact: https://github.com/eagleEggs/EHX/issues
# EHX is a submodule of Test Anatomy: https://github.com/eagleEggs/Test-Anatomy

# References for Style Override Function:
# https://gist.github.com/dariodiaz/3104601
# https://gist.github.com/marciomazza/3086536

# ######################################################################### ###
# ############################### Imports ################################# ###
# ######################################################################### ###

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidArgumentException
import PySimpleGUI as Sg
import logging

# ######################################################################### ###
# ########################## Globals and Setup ############################ ###
# ######################################################################### ###

logging.basicConfig(filename='EHX.log', level=logging.INFO)
logging.info("LAUNCHed EHX v1.0")

LIGHT = ""
DD_BROWSERS = ["Internet Explorer", "Firefox", "Chrome"]
DD_ELEMENTS = ["CSS Selector", "XPATH", "ID"]
DD_COLORS = ["Red", "Green", "Orchid", "Aqua", "Aquamarine ", "Orange", "Tomato",
                    "Salmon", "Yellow", "Blue", "Plum", "PeachPuff"]

# ######################################################################### ###
# ###########          Engine: Master Controller Class          ########### ###
# ######################################################################### ###


class Engine(object):
    def __init__(self, browsername, siteaddress):
        self.browsername = browsername
        self.siteaddress = siteaddress
        self.elementstore = ""

        if values['BROWSERTYPE'] == "Internet Explorer":
            self.engine = webdriver.Ie()
        elif values['BROWSERTYPE'] == "Firefox":
            self.engine = webdriver.Firefox()
        elif values['BROWSERTYPE'] == "Chrome":
            self.engine = webdriver.Chrome()

    def highlight(self, element):
        try:
            if self.elementstore is not "":
                logging.error("Removing Previous Element from Store")
                self.highlight_remove(self.elementstore)
        except:
            logging.error("Issue with Element Store")
        try:
            self.elementstore = element
            parent = element._parent
            self.stylize(parent, element,
                         "background: {}; ""border: 3px solid {};"
                         "".format(
                                 values["COLOR_TYPE"], values["COLOR_TYPE"]))
        except:
            logging.error("Could not Highlight Element")
            Sg.PopupError("There was an issue Highlighting, Check Element")

    def stylize(self, parent, element, style):
        try:
            self.engine.execute_script("arguments[0].setAttribute('style',"
                                       " arguments[1]);", element, style)
        except:
            logging.error("Could not Stylize Element")

    def highlight_remove(self, element):
        try:
            parent = element._parent
            self.stylize_remove(parent, element, " ;")
        except:
            logging.error("Could not Remove Element Highlight")

    def stylize_remove(self, parent, element, style):
        self.engine.execute_script("arguments[0].setAttribute('style',"
                                   " arguments[1])", element, style)

# ######################################################################### ###
# ###########            Browser Controller Class               ########### ###
# ######################################################################### ###


class BrowserController(Engine):
    def __init__(self, *args):
        super(BrowserController, self).__init__(*args)

    def open_site(self):
        try:
            self.engine.get(self.siteaddress)
        except InvalidArgumentException:
            logging.warning("Issue Instantiating Browser, Check URL")
            Sg.PopupError("Issue Instantiating Browser, Check URL and Inputs")
            self.engine.close()



# ######################################################################### ###
# ###########         GUI: Layouts and Declarations             ########### ###
# ######################################################################### ###


EHX_COLUMN = [[
         Sg.Image(filename="images/bconfig.png")],
         [Sg.InputText('https://www.github.com/eagleEggs/EHX', key='APP_URL',
                       do_not_clear=True, size=(37, 10))],
         [Sg.InputCombo(DD_BROWSERS, key="BROWSERTYPE", size=(35, 10))],
         [Sg.ReadButton("", border_width=0,
                        tooltip='Start Testing Environment', key="LAUNCH",
                        size=(33, 2), image_filename="images/HLlaunch.png")],
         [Sg.Image(filename="images/econfig.png")],
         [Sg.Multiline(".text-gray-dark", size=(36, 2), enter_submits=True,
                       key='ENTER_ELEMENT', do_not_clear=True)],
         [Sg.InputCombo(DD_ELEMENTS, key="ELEMENT_TYPE", size=(35, 10))],
         [Sg.InputCombo(DD_COLORS, key="COLOR_TYPE", size=(35, 10))],
         [Sg.ReadButton('', key="HIGHLIGHT", border_width=0, size=(33, 5),
                        image_filename="images/HLimg.png",
                        tooltip="Highlight Element")],
         [Sg.T("")],
         [Sg.Image(filename="images/HLlogo.png")],
         [Sg.Image(filename="images/license.png")]]

layout = [[Sg.Column(EHX_COLUMN, size=(0, 0))]]
window = Sg.Window("EHX v1.0", no_titlebar=False,
                   auto_size_text=True).Layout(layout).Finalize()

# ######################################################################### ###
# ###########               GUI: Main Loop                      ########### ###
# ######################################################################### ###

while True:

    b, values = window.Read()

    if b == "LAUNCH":
        try:
            APP = BrowserController(values["BROWSERTYPE"], values["APP_URL"])
        except (NameError, KeyError):
            APP = ""
            logging.warning("Issue Instantiating Browser, Check URL and Inputs")
            Sg.PopupError("Issue Instantiating Browser, Check URL and Inputs")
            break
        APP.open_site()
        logging.info("Instantiating Application")

    if b == "HIGHLIGHT":
        logging.info("Highlighting Button Pressed")

        if values['ELEMENT_TYPE'] == "CSS Selector":
            logging.info("Highlighting Button Pressed, CSS")
            try:
                SCRIPTVAR = str.strip(values['ENTER_ELEMENT'])
                exec("LIGHT = APP.engine.find_element_by_css_selector(\"{}\")\n"
                     "APP.highlight(LIGHT)".format(SCRIPTVAR))
                logging.info("Highlighting Button Pressed, CSS, Successful")
            except NoSuchElementException:
                logging.error("Highlight Button Pressed But Failed Executing "
                              "Command, CSS")
                Sg.PopupError("There was an issue Highlighting, Check Element")

        if values['ELEMENT_TYPE'] == "XPATH":
            logging.info("Highlighting Button Pressed, XPATH")
            try:
                SCRIPTVAR = str.strip(values['ENTER_ELEMENT'])
                exec("LIGHT = APP.engine.find_element_by_xpath(\"{}\")\n"
                     "APP.highlight(LIGHT)".format(SCRIPTVAR))
                logging.info("Highlighting Button Pressed, XPATH, Successful")
            except NoSuchElementException:
                logging.error("Highlight Button Pressed But Failed Executing "
                              "Command, XPATH")
                Sg.PopupError("There was an issue Highlighting, Check Element")

        if values['ELEMENT_TYPE'] == "ID":
            logging.info("Highlighting Button Pressed, ID")
            try:
                SCRIPTVAR = str.strip(values['ENTER_ELEMENT'])
                exec("LIGHT = APP.engine.find_element_by_id(\"{}\")\n"
                     "APP.highlight(LIGHT)".format(SCRIPTVAR))
                logging.info("Highlighting Button Pressed, ID, Successful")
            except NoSuchElementException:
                logging.error("Highlight Button Pressed But Failed Executing "
                              "Command, ID")
                Sg.PopupError("There was an issue Highlighting, Check Element")

    if b is None:
        break
