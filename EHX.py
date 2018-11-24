# ______________________________#
################################
############  EHX  #############
########################v1.0####

# Element Hunter X
# Copyright github.com/eagleEggs
# Contact: https://github.com/eagleEggs/EHX/issues
# EHX is a submodule of Test Anatomy: https://github.com/eagleEggs/Test-Anatomy

################################
################################


# Selenium:
from selenium import webdriver # selenium web driver

# GUI:
import PySimpleGUI as sg # tkinter alt

# System:
import logging # logging system


logging.basicConfig(filename='EHX.log', level=logging.INFO)
logging.info("Launched EHX")


#######################################
### Engine: Master Controller Class ###
#######################################

class Engine(object):
	def __init__(self, browserName, siteAddress):
		self.browserName = browserName
		self.siteAddress = siteAddress
		self.elementStore = "" # used for tracking and removing elements for HL

		if values['browsertype'] == "Internet Explorer":
			self.engine = webdriver.Ie()
		elif values['browsertype'] == "Firefox":
			self.engine = webdriver.Firefox()
		elif values['browsertype'] == "Chrome":
			self.engine = webdriver.Chrome()


	def Highlight(self, element):
		try:
			if self.elementStore is not "":
				logging.error("Highlight: Removing Previous Element from Store")
				self.HighlightRemove(self.elementStore)
		except:
			logging.error("Highlight: Issue with Element Store")
		try:
			self.elementStore = element
			parent = element._parent
			self.Stylize(parent, element,"background: {}; border: 3px solid {};".format(values["colortype"], values["colortype"]))
		except:
			logging.error("Could not Highlight Element")
			sg.PopupError("Highlight: There was an issue Highlighting, Check Element")

	def Stylize(self, parent, element, style):
		try:
			self.engine.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, style)  # reference: https://gist.github.com/dariodiaz/3104601
		except:
			logging.error("Could not Stylize Element")

	def HighlightRemove(self, element):
		try:
			parent = element._parent
			self.StylizeRemove(parent, element, " ;") # blanking out html style
		except:
			logging.error("Could not Remove Element Highlight")

	def StylizeRemove(self, parent, element, style):
		self.engine.execute_script("arguments[0].setAttribute('style', arguments[1])", element, style)

################################
### Browser Controller Class ###
################################

class BrowserController(Engine):
	def __init__(self, *args):
		super(BrowserController, self).__init__(*args)

	def openSite(self):
		self.engine.get(self.siteAddress)


################################
###      Shelve Storage      ###
################################



################################
###     Scratchpad Page      ###
################################

ddVals = ["Internet Explorer","Firefox", "Chrome"]
ddElements = ["CSS Selector", "XPATH", "ID"]
ddCols = ["Red", "Green", "Orchid", "Aqua", "Aquamarine ", "Orange", "Tomato", "Salmon", "Yellow", "Blue", "Plum", "PeachPuff"]


col11 = [[
		 sg.Image(filename="images/bconfig.png")],
         [sg.InputText('https://www.github.com/eagleEggs/EHX', key='appuri', do_not_clear=True, size = (37, 10))],
		 #sg.ReadButton('', key = "saveurl", border_width=0, size = (1, 1), image_filename="save.png", tooltip = "Save URL")],
		 #[sg.InputCombo(urlhist, key = "urlshelf", size = (35, 10))], # shelf drop down - URL's
         [sg.InputCombo(ddVals, key = "browsertype", size = (35, 10))],
		 [sg.ReadButton("", border_width=0, tooltip='Start Testing Environment', key = "Launch", size = (33, 2), image_filename="images/HLlaunch.png")],
		 [sg.Image(filename="images/econfig.png")],
		 [sg.Multiline(".text-gray-dark", size=(35,2), enter_submits=True, key='enterElement', do_not_clear=True)],
		 #sg.ReadButton('', key = "saveelement", border_width=0, size = (1, 1), image_filename="save.png", tooltip = "Save Element")],
		 #[sg.InputCombo(elementhist, key = "elementshelf", size = (35, 10))], # shelf drop down - Elements

		 [sg.InputCombo(ddElements, key = "elementtype", size=(35,10))],
		 [sg.InputCombo(ddCols, key="colortype", size=(35, 10))],
		 [sg.ReadButton('', key = "highlight", border_width=0, size = (33, 5), image_filename="images/HLimg.png", tooltip = "Highlight Element")],
		 [sg.T("")],
		 [sg.Image(filename = "images/HLlogo.png")],
		 [sg.Image(filename="images/license.png")]]


#############################################
###    testStream Layout and Rendering    ###
#############################################

tab11 = [[sg.Column(col11, pad=(0, 0))]]
layout = [[sg.Column(col11, size = (0, 0))]]
window = sg.Window("EHX (v1.3)", no_titlebar=False, auto_size_text=True).Layout(layout).Finalize()
lite = "" # shell to wait for app to create var for engine


while True:

	b, values = window.Read()  # read input values from GUI

	if b == "Launch":
		try:
			app = BrowserController(values["browsertype"], values["appuri"])
			app.openSite()
			logging.info("Instantiating Application")
		except:
			logging.warning("Issue Instantiating Application")


	if b == "highlight":  # this grabs content from sb3 and puts it in script form for highlighting through API
		logging.info("Highlighting Button Pressed")

		if values['elementtype'] == "CSS Selector":
			logging.info("Highlighting Button Pressed, CSS")
			try:
				scriptvar = str.strip(values['enterElement'])
				exec("lite = app.engine.find_element_by_css_selector(\"{}\")\napp.Highlight(lite)".format(scriptvar))
				logging.info("Highlighting Button Pressed, CSS, Successful")
			except:
				logging.error("Highlight Button Pressed But Failed Executing Command, CSS")
				sg.PopupError("There was an issue Highlighting, Check Element")

		if values['elementtype'] == "XPATH":
			logging.info("Highlighting Button Pressed, XPATH")
			try:
				scriptvar = str.strip(values['enterElement'])
				exec("lite = app.engine.find_element_by_xpath(\"{}\")\napp.Highlight(lite)".format(scriptvar))
				logging.info("Highlighting Button Pressed, XPATH, Successful")
			except:
				logging.error("Highlight Button Pressed But Failed Executing Command, XPATH")
				sg.PopupError("There was an issue Highlighting, Check Element")

		if values['elementtype'] == "ID":
			logging.info("Highlighting Button Pressed, ID")
			try:
				scriptvar = str.strip(values['enterElement'])
				exec("lite = app.engine.find_element_by_id(\"{}\")\napp.Highlight(lite)".format(scriptvar))
				logging.info("Highlighting Button Pressed, ID, Successful")
			except:
				logging.error("Highlight Button Pressed But Failed Executing Command, ID")
				sg.PopupError("There was an issue Highlighting, Check Element")



	if b is None:
		break
