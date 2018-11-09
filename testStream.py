# ______________________________#
################################
########  testStream  ##########
########################v0.03###

# Fluid Test Building


################################
################################


# Selenium:
from selenium import webdriver

# GUI:
import PySimpleGUI as sg
from tkinter import Tk

# System:
from operator import *
import logging


logging.basicConfig(filename='testStream.log', level=logging.INFO)
logging.info("Launched testStream")


#######################################
### Engine: Master Controller Class ###
#######################################

class Engine(object):
	def __init__(self, browserName, siteAddress):

		self.browserName = browserName
		self.siteAddress = siteAddress
		self.style = ""

		if values['browsertype'] == "Internet Explorer":
			self.engine = webdriver.Ie()
		elif values['browsertype'] == "Firefox":
			self.engine = webdriver.Firefox()
		elif values['browsertype'] == "Chrome":
			self.engine = webdriver.Chrome()


	def Highlight(self, element):
		parent = element._parent
		#self.style = element.getAttribute("style")
		print(self.style)
		self.Stylize(parent, element, "background: pink; border: 3px solid red;")

	def Stylize(self, parent, element, style):
		self.engine.execute_script("arguments[0].setAttribute('style', arguments[1]);", element,
		                           style)  # reference: https://gist.github.com/dariodiaz/3104601

	def HighlightRemove(self, element):
		parent = element._parent
		self.StylizeRemove(parent, element, self.style)

	def StylizeRemove(self, parent, element, style):
		self.engine.execute_script("arguments[0].setAttribute('style', arguments[1]);", element,
		                           style)

################################
### Browser Controller Class ###
################################

class BrowserController(Engine):
	def __init__(self, *args):
		super(BrowserController, self).__init__(*args)

	def openSite(self):
		self.engine.get(self.siteAddress)



################################
###     Scratchpad Page      ###
################################

ddVals = ["Internet Explorer","Firefox", "Chrome"]
ddElements = ["CSS Selector", "XPATH", "ID"]

col11 = [[
         #sg.T("Configure, Paste, and Click")],
         sg.Text("Element Hunter X", justification="right", size = (32, 1))],
         [sg.InputText('Enter URL', key='appuri', do_not_clear=True, size = (35, 10))],
         [sg.Text('Options:')], [sg.InputCombo(ddVals, key = "browsertype", size=(15,10)),
		 sg.ReadButton("Launch Browser", border_width=0, tooltip='Start Testing Environment', key = "Launch")],
		 #[sg.Text('Code Generation:')],
         #[sg.Multiline("", size=(110, 15), enter_submits=True, key='scratchbox1', do_not_clear=True)],
		 [sg.InputCombo(ddElements, key = "elementtype", size=(15,10)), sg.ReadButton('Highlight', border_width=0)],
		 [sg.Text('Notes:')],
         [sg.Multiline("", size=(35,10), enter_submits=True, key='scratchbox3', do_not_clear=True)],  # store mint here to paste easily into sb1
		 [sg.Text('github.com/eagleEggs | License GPL v3', size = (32, 1))]]


#############################################
###    testStream Layout and Rendering    ###
#############################################

tab11 = [[sg.Column(col11, pad=(0, 0))]]

layout = [[sg.Column(col11, size = (0, 0))]]

window = sg.Window("Topanga EHX", no_titlebar=False, auto_size_text=True).Layout(layout).Finalize()

#scratchBox1 = window.FindElement('scratchbox1')

clips = Tk()

clips.withdraw()

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


	if b == "Highlight":  # this grabs content from sb3 and puts it in script form for highlighting through API

		if values['elementtype'] == "CSS Selector":
			try:
				board = clips.clipboard_get()
				scriptvar = str.strip(board)
				exec("lite = app.engine.find_element_by_css_selector(\"{}\")\napp.Highlight(lite)".format(scriptvar))
				logging.info("Scratchbox: Executed Command Successfully")
			except:
				logging.info("Scratchbox: Failed Executing Command")


		if values['elementtype'] == "XPATH":
			try:
				board = clips.clipboard_get()
				scriptvar = str.strip(board)
				exec("lite = app.engine.find_element_by_xpath(\"{}\")\napp.Highlight(lite)".format(scriptvar))
				logging.info("Scratchbox: Executed Command Successfully")
			except:
				logging.info("Scratchbox: Failed Executing Command")

		if values['elementtype'] == "ID":
			try:
				board = clips.clipboard_get()
				scriptvar = str.strip(board)
				exec("lite = app.engine.find_element_by_id(\"{}\")\napp.Highlight(lite)".format(scriptvar))
				logging.info("Scratchbox: Executed Command Successfully")
			except:
				logging.info("Scratchbox: Failed Executing Command")

	#if b == "Highlight Element":
	#	try:
	#		cmdresult = exec(values['scratchbox1'])
	#		logging.info("Scratchbox: Executed Command Successfully")
	#	except:
	#		logging.info("Scratchbox: Failed Executing Command")

	#if b == "Remove Highlight":
	#	if lite:
	#		app.HighlightRemove(lite)



	if b is None:
		break
