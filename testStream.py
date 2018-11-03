# ______________________________#
################################
########  testStream  ##########
########################v0.01###

# Fluid Test Building


################################
################################


# Selenium:
from selenium import webdriver

# GUI:
import PySimpleGUI as sg

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

		if values['browsertype'] == "FF":
			self.engine = webdriver.Firefox()
		else:
			self.engine = webdriver.Ie()

	def GetWebElement(self, elementType, tagValue):
		self.elementType = elementType.lower()
		self.tagValue = tagValue

		if self.elementType == "css":
			self.engine.find_element_by_css_selector(self.tagValue)

		if self.elementType == "xpath":
			self.engine.find_element_by_xpath(self.tagValue)

	def ClickWebElement(self, elementType, tagValue):
		self.elementType = elementType.lower()
		self.tagValue = tagValue

		if eq(self.elementType, "css"):
			self.engine.find_element_by_css_selector(self.tagValue).click()

		if eq(self.elementType, "xpath"):
			self.engine.find_element_by_xpath(self.tagValue).click()

	def Highlight(self, element):
		parent = element._parent
		self.Stylize(parent, element, "background: pink; border: 3px solid red;")

	def Stylize(self, parent, element, style):
		self.engine.execute_script("arguments[0].setAttribute('style', arguments[1]);", element,
		                           style)  # reference: https://gist.github.com/dariodiaz/3104601

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

col11 = [[sg.T("Generate Highlight Code or modify it to execute any Selenium API action:")],
		 [sg.Text('URL:     '),
         sg.InputText('https://github.com/eagleEggs', key='appuri', do_not_clear=True),
		 sg.ReadButton("Launch Browser", border_width=0, tooltip='Start Testing Environment')],
		 [sg.Text('IE|FF|C:', key = "browsertype"),
         sg.InputText('FF', key='browsertype', do_not_clear=True)],
         [sg.Multiline("Code will generate here", size=(110, 15), enter_submits=True, key='scratchbox1', do_not_clear=True)],
         [sg.Multiline("Paste your element here", size=(110, 3), enter_submits=True, key='scratchbox3', do_not_clear=True)],  # store mint here to paste easily into sb1
         [sg.ReadButton('Load Highlight Code', border_width=0), sg.ReadButton('Highlight Element', border_width=0)]]


#############################################
###    testStream Layout and Rendering    ###
#############################################

tab11 = [[sg.Column(col11, pad=(0, 0))]]

layout = [[sg.Column(col11, size = (0, 0))]]

window = sg.Window("testStream", no_titlebar=False, auto_size_text=True).Layout(
		layout).Finalize()

scratchBox1 = window.FindElement('scratchbox1')




while True:

	b, values = window.Read()  # read input values from GUI

	if b == "Launch Browser":

		try:
			app = BrowserController(values["browsertype"], values["appuri"])
			app.openSite()

			logging.info("Instantiating Application")

		except:
			logging.warning("Issue Instantiating Application")


	if b == "Load Highlight Code":  # this grabs content from sb3 and puts it in script form for highlighting through API
		scriptvar = str.strip((values['scratchbox3']))
		scriptcontent1 = "lite = app.engine.find_element_by_css_selector({})\napp.Highlight(lite)".format(scriptvar)
		scratchBox1.Update(scriptcontent1)

	if b == "Highlight Element":
		try:
			cmdresult = exec(values['scratchbox1'])
			logging.info("Scratchbox: Executed Command Successfully")
		except:
			logging.info("Scratchbox: Failed Executing Command")



	if b is None:
		break
