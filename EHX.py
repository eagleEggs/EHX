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
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import StaleElementReferenceException
import _thread as thread
import PySimpleGUI as Sg
import logging

# ######################################################################### ###
# ########################## Globals and Setup ############################ ###
# ######################################################################### ###

logging.basicConfig(filename='EHX.log', level=logging.INFO)
logging.info("Launched EHX v1.0")

LIGHT = ""
DD_BROWSERS = ["Internet Explorer", "Firefox", "Chrome"]
DD_ELEMENTS_DICT = {"CSS Selector": "find_element_by_css_selector",
                    "XPATH": "find_elements_by_xpath",
                    "ID": "find_elements_by_id",
                    "Class Name": "find_elements_by_class_name",
                    "Name": "find_elements_by_name"}
DD_ELEMENTS = ["CSS Selector", "XPATH", "ID", "Class Name", "Name"]
DD_COLORS = ["Red", "Green", "Orchid", "Aqua", "Aquamarine ", "Orange",
             "Tomato", "Salmon", "Yellow", "Blue", "Plum", "PeachPuff"]
global waitWindow_active
waitWindow_active = False
# ######################################################################### ###
# ###########          Engine: Master Controller Class          ########### ###
# ######################################################################### ###


class Engine(object):
    def __init__(self, browsername, siteaddress):
        self.browsername = browsername
        self.siteaddress = siteaddress
        self.elementlist = []
        self.elementstore = []

    def highlight(self, element):
        try:
            for elements in element:
                self.elementlist.append(elements)
        except TypeError:
            self.elementlist.append(element)

        if len(self.elementstore) == 1:
            logging.info("Single Element Store Needs to be Emptied")
            try:
                logging.info("Removing Previous Element from Single Store")
                self.highlight_remove(element)
                logging.info("Single Removed:".format(element))
            except (NoSuchElementException,
                    TypeError,
                    StaleElementReferenceException) as elem_remove_error:
                logging.error(elem_remove_error)
            self.elementstore.clear()
            logging.info("Emptied Single Element from Store")

        if len(self.elementstore) > 1:
            global waitWindow_active
            logging.info("Multiple Element Store Needs to be Emptied")
            thread.start_new_thread(self.highlight_remove_multi, ())

        thread.start_new_thread(self.highlight_add, ())

    def highlight_add(self):
        global waitWindow_active
        waitWindow_active = True
        try:
            for item in self.elementlist:
                parent = item._parent
                self.stylize(parent, item,
                             "background: {}; ""border: 3px solid {};"
                             "".format(
                                    values["COLOR_TYPE"],
                                    values["COLOR_TYPE"]))
                self.elementstore.append(item)
            self.elementlist.clear()
            waitWindow_active = False
            waitWindow.Close()

        except (NoSuchElementException, AttributeError, WebDriverException):
            logging.info("Element Issue")
            Sg.PopupError("Error with Element(s)\n[Not Found, or Other Error]")

    def highlight_remove_multi(self):
        for item in self.elementstore:
            logging.info("Iterating through elements".format(item))
            try:
                logging.info("Removing Previous Element from Store")
                self.highlight_remove(item)
                logging.info("Multiple Removed:".format(item))
            except (NoSuchElementException,
                    TypeError, WebDriverException,
                    StaleElementReferenceException) as elem_remove_error:
                logging.error(elem_remove_error)
        self.elementstore.clear()
        logging.info("Emptied Multiple Elements from Store")
        global waitWindow_active
        waitWindow_active = False
        waitWindow.Close()

    def stylize(self, parent, element, style):
            try:
                self.engine.execute_script("arguments[0].setAttribute('style',"
                                           " arguments[1]);", element, style)
            except (NoSuchElementException, TypeError, WebDriverException,
                    StaleElementReferenceException) as style_error:
                logging.error(style_error)
                #Sg.PopupError(style_error)

    def highlight_remove(self, element):
        try:
            parent = element._parent
            self.stylize_remove(parent, element, " ;")
            logging.info("Element Removed")
        except (NoSuchElementException, TypeError, WebDriverException):
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

        try:
            if values['BROWSERTYPE'] == "Internet Explorer":
                self.engine = webdriver.Ie()
                self.open_site()
            elif values['BROWSERTYPE'] == "Firefox":
                self.engine = webdriver.Firefox()
                self.open_site()
            elif values['BROWSERTYPE'] == "Chrome":
                self.engine = webdriver.Chrome()
                self.open_site()
        except (AttributeError, WebDriverException,
                NoSuchWindowException, TypeError) as browser_error:
            logging.warning(
                    "Issue Instantiating Browser: {}".format(browser_error))
            Sg.PopupError(browser_error)

    def open_site(self):
            self.engine.get(self.siteaddress)


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
    try:
        b, values = window.Read(timeout=100)

        if b == "LAUNCH":
            APP = BrowserController(values["BROWSERTYPE"], values["APP_URL"])
            logging.info("Instantiating Application")

        if b == "HIGHLIGHT":

            logging.info("Highlighting Button Pressed")

            waitWindow = Sg.Window(
                    'EHX | Processing Element(s)...', grab_anywhere=False,
                    no_titlebar=False).Layout(
                    [[Sg.T("Please Wait, Processing Element(s)...")],
                    [Sg.T("This May Take a Minute.")]])

            try:
                SCRIPTVAR = str.strip(values['ENTER_ELEMENT'])
                exec("LIGHT=APP.engine.{}(\"{}\")\n"
                     "APP.highlight(LIGHT)".format(
                        str.strip(DD_ELEMENTS_DICT[values['ELEMENT_TYPE']]),
                        SCRIPTVAR))
                logging.info("Highlighting Button Pressed, {}, Successful".format(
                        values['ELEMENT_TYPE']))

            except (NoSuchElementException, KeyError, AttributeError) as error:
                logging.error("Highlight Button Pressed But Failed Executing "
                              "Command, {}".format(values['ELEMENT_TYPE']))
                logging.error(error)
                Sg.PopupError("There was an issue Highlighting, Check Element")

        if waitWindow_active:
            try:
                b1, values1 = waitWindow.Read(timeout=0)
            except RuntimeError:
                logging.error("GUI Main Loop Runtime Error")

        if b is None:
            break

    except RuntimeError:
        Sg.PopupError("Error with GUI Loop\nWhile Processing Element(s)")
