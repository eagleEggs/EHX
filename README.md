# EHX

![anim1](https://img.shields.io/badge/built%20with-python%203.7-brightgreen.svg) ![anim1](https://img.shields.io/badge/status-Stable-pink.svg) ![anim1](https://img.shields.io/badge/version-1.0-black.svg)

### What is it?

Element Hunter X (EHX) is an application which allows you to maintain a single browser session while testing elements for web automation testing. It's main purpose is to save time from recompiling and/or relaunching test from your code and waiting over and over for the browser to open and close. <br><br>

![anim1](https://github.com/eagleEggs/testStream/blob/master/EHXimg.png?)<br>

### Releases

Version 1.0: https://github.com/eagleEggs/EHX/releases <br>

### Documentation

You can view the PDF on Github here: https://github.com/eagleEggs/EHX/blob/master/EHX_1.0_Documentation.pdf

Within the main window there are two sections:

 1. Browser Configuration
 2. Element Configuration

Within Browser Configuration there are three actionable interactions:

  <b>1. URL:</b> A text input box where you can paste the URL you will be testing.<br>
  <b>2. Browser:</b> A drop down list of browsers. Choose the one you'd like to open the URL with.<br>
  <b>3. Launch Button:</b> Once the previous inputs have been completed, click the rocket ship to launch the browser to the URL chosen.<br>

Within Element Configuration there are four actionable interactions:

   <b>1. Element String:</b> Text input box where you can paste or type your element tag string (i.e. CSS, XPATH, or ID).<br>
   <b>2. Element Type:</b> A drop down where you will choose the type of element that you have pasted or typed above.<br>
  <b>3. Color:</b> A color drop down where you can choose a color of which will be highlighted within the browser.<br>
  <b>4. Highlight Button:</b> Once the previous inputs have been completed, click the rocket ship to launch the browser to the URL chosen.

Note:

 - If there is an error in highlighting the element within the browser, an error pop up will notify you. Try changing the element tag string to one that works.
 - Once you see that the element is highlighted, you know that element will work within your scripts.

### Requirements

When running Python modules: <br>
 - PySimpleGUI (TKinter alternative)<br>
 - Selenium and Python Web Browser Drivers

When running release binary: <br>
 - Selenium and Python Web Browser Drivers
 
You can download the Web Drivers here: https://www.seleniumhq.org/projects/webdriver/

### Thanks

Great code from https://gist.github.com/dariodiaz/3104601 and https://gist.github.com/marciomazza/3086536 was referenced
to build the style highlighting functionality.

### License

EHX is GPL v3<br>
Octicons (Rocket Ship and Pen icons) are MIT licensed: https://github.com/primer/octicons/blob/master/LICENSE
