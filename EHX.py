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
import PySimpleGUI as Psg
from logging import INFO as INFO
from logging import basicConfig as logger
from logging import info as log_info
from logging import warning as log_warning
from logging import error as log_error

# ######################################################################### ###
# ########################## Globals and Setup ############################ ###
# ######################################################################### ###

logger(filename='EHX.log', level=INFO)
log_info("Launched EHX v1.0")

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
            if len(self.elementlist) > 1:
                ecountpopup = Psg.PopupOKCancel("Multiple Elements "
                                          "Found!: {}".format(len(
                                            self.elementlist)))
                if ecountpopup == "OK":
                    pass
                elif ecountpopup == "Cancel":
                    return
                else:
                    return

        except TypeError:
            self.elementlist.append(element)

        if len(self.elementstore) == 1:
            log_info("Single Element Store Needs to be Emptied")
            try:
                log_info("Removing Previous Element from Single Store")
                self.highlight_remove(element)
                log_info("Single Removed:".format(element))
            except (NoSuchElementException,
                    TypeError,
                    StaleElementReferenceException) as elem_remove_error:
                log_error(elem_remove_error)
            self.elementstore.clear()
            log_info("Emptied Single Element from Store")

        if len(self.elementstore) > 1:
            log_info("Multiple Element Store Needs to be Emptied")
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
            log_info("Element Issue")
            Psg.PopupError("Error with Element(s)\n"
                           "[Not Found, or Other Error]")

    def highlight_remove_multi(self):
        for item in self.elementstore:
            log_info("Iterating through elements".format(item))
            try:
                log_info("Removing Previous Element from Store")
                self.highlight_remove(item)
                log_info("Multiple Removed:".format(item))
            except (NoSuchElementException,
                    TypeError, WebDriverException,
                    StaleElementReferenceException) as elem_remove_error:
                log_error(elem_remove_error)
        self.elementstore.clear()
        log_info("Emptied Multiple Elements from Store")
        global waitWindow_active
        waitWindow_active = False
        waitWindow.Close()

    def stylize(self, parent, element, style):
            try:
                self.engine.execute_script("arguments[0].setAttribute('style',"
                                           " arguments[1]);", element, style)
            except (NoSuchElementException, TypeError, WebDriverException,
                    StaleElementReferenceException) as style_error:
                log_error(style_error)
                #Psg.PopupError(style_error)

    def highlight_remove(self, element):
        try:
            parent = element._parent
            self.stylize_remove(parent, element, " ;")
            log_info("Element Removed")
        except (NoSuchElementException, TypeError, WebDriverException):
            log_error("Could not Remove Element Highlight")

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
            log_warning(
                    "Issue Instantiating Browser: {}".format(browser_error))
            Psg.PopupError(browser_error)

    def open_site(self):
            self.engine.get(self.siteaddress)


# ######################################################################### ###
# ###########         GUI: Layouts and Declarations             ########### ###
# ######################################################################### ###

bconfig_b64 = "iVBORw0KGgoAAAANSUhEUgAAAQ0AAAATCAYAAACKuVhXAAAAAXNSR0IArs4c6Q"\
              "AAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAG/SURBVHhe7d"\
              "gBj4MgDAVgvf//n7172b2kIS20RB1u70uWTS2lArJs+7Ztx99LRCTl5/9dRCRFm"\
              "4aIlGjTEJGS5f/TOI64vH1H+QLeOF05Pra/qB/GfNo8fep9ZeGu46dyEd4kffvE"\
              "WXePz6eOvdZUjn6ePFy00HGsxS9XwKp6rbqFjb5J+dnjtWkxppcHRnFn9WXzjDD"\
              "PqM1sPW1eL24U49UW9QeIt9e9YxjlIC+urWkmpr0OUU2jmr1cq0Kl/l0sJDvQNg"\
              "7XeNx+ttrz1WOy5zMxxHPQaxvJxGfrydaS6RMq7TPnRvkA16I4GuWJ2lG1fXuex"\
              "4Bz2X5X8aifJxhUvsAOvsXrNrYKub38tm8b4/VlYxgXYVsvz93e3f+saAwr83Cn"\
              "p46z/tOYwEXJSY8Wo42zL7kP50Xjfx5tGg1vUdlz7QZhF6K3cVht2zNEfV/R11l"\
              "szdk6776XbF3fCLO39Mj0Jm70sPI6zcbN5BnFZGvJ8vKdUQ/14tqaZ+6NbSq5sv"\
              "1EcdCLrdRCo5heLdD2uSJU2L8LkRvwYXrCQ/PttGnIW3jfuNownkGbhoiU6I9QE"\
              "SnRpiEiJdo0RKRg234BdvZxNkLIpLoAAAAASUVORK5CYII="
econfig_b64 = "iVBORw0KGgoAAAANSUhEUgAAAQ0AAAATCAYAAACKuVhXAAAAAXNSR0IArs4c6QA"\
              "AAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsIAAA7CARUoSoAAAAG2SURBVHhe7d"\
              "uLisQgDAVQu///z929zATEjSYpWkx7D5RlfMSorWUG9iilnH8XEZHLz/cvEZELD"\
              "w0iCuGhQUQhW/+mcZ7j1I4D6X/UbevyN9DWaeUaeNZa2jxtL546rwjM/P8dtxFt"\
              "k3obl21DZ+QbWZ8Zsq2x11PntULKryfYWG5u/0bn+tBKuLM+d96m6gfDehuM6qW"\
              "uJW2terEyjpb3iMSw+t2Zc9tGy603HqB9Xa99BiuG0Nq1OV1p09ZDLycrZy3Wzp"\
              "CtPpNNeDZUSNvehlvl1qZeiYMyb78oT3/v2PIZUObt1xPp7ymz4gHqeu2EFafXT"\
              "0T7t+XyGVDmHXcnab6ezFhUbFB9XeWNk+lGEBlzBskbf+s5ePfqblnXGVL9ptHe"\
              "EFHSv72itBi4aC9ySHCP5kr5Q+ist8ZOca7EkIeg7Tcjn1XqnL153j0Xb15vhR3"\
              "cdnWsjes9NKJ+s1htZo3ljSPq9m2dlzZmHWtWztY4YI2lkT6RWN5xeu1g1DaSi7"\
              "DajHKBdsxdIcvxTIgWk4cpy0Pzdjw06HbaG5cHRh48NIgohP+wRkQhPDSIKISHB"\
              "hEFlPILao1uJC9WkZwAAAAASUVORK5CYII="
highlight_b64 = "iVBORw0KGgoAAAANSUhEUgAAAQ0AAABECAIAAAAUUPdPAAAAAXNSR0IArs4c6"\
                "QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJDSURBVH"\
                "he7dxNTiJRFIBR7Tg3zRzDBtiBCXMMzN2C7sAFsAYXQHDugA3gDnAhMiehX7p"\
                "eExp/rompelXknEStK06/XF6R8gwInaev3W5XDZyM7XZ7cXGRB37mPEk/dAJf"\
                "SJn8ypfA53QCMZ1ATCcQ0wnEdAIxnUBMJxDTCcR0AjGdQEwnENMJxHQCMZ1AT"\
                "CdttNlsHh4eRqNR+p5/RVGe02qdKpKnp6dqvL6+fn5+rq4pwnNarXMUSfLy8j"\
                "KdTvNAIfZJu6zX6/R2Kw8HbJWC7JPWGQ6HH/aQtsrj42MeaJxOWiG93dpn8Nn"\
                "qSKsmX9E4nZRXnUmS/TnkfSqXl5c3Nzd5oHE6Kezw4H54ZD9MJUUym83G43E1"\
                "UkY6x1PE29vb3d3d7/9NJpP88m63Wq0Gg8FiscgzJaRG3O8q5v0t4L3DZZL+L"\
                "O2T6poi/D/IYr6IpOJGcHu4L1xGGEmyXq+Xy2UeKE0nTftOJA7ubaOTRn0/kt"\
                "vb2zzTAjppjki6SycNEUmn6aQJIuk6ndROJCdAJ/USyWnQSY1EcjJ8Hl+j+/t"\
                "7kZwAn8fXK0UyHo/n8/mHJYikQ3RSr+FwmFK5urrK8z8i6RadNOFoq4ikc3TS"\
                "hMOtIpIuco6vUa/XS4X0+/1qfH193Ww2Iukcz5/UK3WSr/6ySTpKJ/U6eoAkL"\
                "Za0XvJAd+gEYikT53iI6QRiOoGYTiCmE4jpBGI6gZhOIKYTiOkEYjqBmE4gph"\
                "OI6QRiOoGYTiCmE4jpBGI6gZhOAPi5s7M/ap4J17A2YsAAAAAASUVORK5CYII="
launch_b64 = "iVBORw0KGgoAAAANSUhEUgAAAQ0AAABECAIAAAAUUPdPAAAAAXNSR0IArs4c6QAA"\
             "AARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAL6SURBVHhe7dtB"\
             "aiJBGIbhZHCfE9gniOA+QvZZuG/wAIIHCHT2ggcQep8Q91m4D/QBBA8g6AncB5xv"\
             "UjUSNPo7aKqqh/eBJF2a7UvVb9tXAEzX+tlsNm6B/8bHx0ej0fALnOda9IdOgCOU"\
             "yS9/CeAwOgFsdALY6ASw0QlgoxPARieAjU4AG50ANjoBbHQC2OgEsNEJYKMTwEYn"\
             "gI1O6mE+n5dlWVWVXyMsntNK2nq9Vh7T6VSdaPn29tbpdNxbCIbnGdOlrUN5TCYT"\
             "peJeubm5WSwW7hoh8Txjup6enrSTbCORPM/9FYKjk4SoitFo5K7v7u7cxdbDw4O/"\
             "QnB0kgodtO7v79WJzlpa9vt997rTarWYTCKik/i0jRRF0e12l8ulljpu6XeWZZra"\
             "P9//YycbBMYcH5kiGQwGGtn9+tN4PHbTiN7V9qKtRq9ojnfvIjA+74pMG8h2G9kx"\
             "HA7ZQxJBJzEdicTRTKJdRdhJ4qKTaHSgUiTu7uFxLy8vfNIVlzJhjo9jNBqdEokK"\
             "IZIUsJ9EoKm91+v5xWE6bs1mMw5d0bGfRPD1ZuJxfMaVDvaTH6QkyrLcOV+tVqtT"\
             "Tlz9fn84HPoFomKO/0GKpCgKd3P9XxFJUjh3/ZT9SHSCyrLML47K8/zx8dEvkAY6"\
             "ubxvIzlxf3A7CWNJaujkwg5Fot9HbimK/kGDO5GkiU4u7NtIdJR6fX31L32n0+m8"\
             "v7/r3/waiWGOv7CdbzQ2m81Wq6WLdrt9aD9hak8cn3cFUlVVt9v1iz2a2hncU8bn"\
             "XYHsjxx6xe0zqAU6CUFJuIeulIdGEe0ez8/Pt7e37l2kj04CUR6zTwpGA4lm/a/j"\
             "PhJHJ+FkWab95Jz79IiFTkLb2UkYVGqBTkLTfuKv/t5d4QmT9NFJNC4S7i3WAp3E"\
             "QST1QicREEntcD8+tLIs1QmR1AjfWwFsfG8FOAmdADY6AWx0AtjoBLDRCWCjE8BG"\
             "J4CNTgAbnQA2OgFsdALY6ASw0QlgoxPARicAgPNdXf0Gncg4cIIetisAAAAASUVO"\
             "RK5CYII="
logo_b64 = "iVBORw0KGgoAAAANSUhEUgAAAQ0AAAAWCAYAAADadMnkAAAAAXNSR0IArs4c6QAAAA"\
           "RnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAALySURBVHhe7ZqBkaIw"\
           "FIZ/rwaOHnRTg6PU4EgPDkVQBEMPONSAN9bAnj1Ee7h7Iaig7kkA73Zv/m+GnY0veS"\
           "SQ/HlJmAD4JRchhHSiEg3Bpggh5AMmEyMXwLfqLyGEdISiQQhxgqJBCHGCojEihzxG"\
           "nB/qFCH/JxQNJ07YpyIMcftK96fa/rk57dMnombbd9ueqly6F+s4PK+HI4dc3kOOls"\
           "fTHmmc4ou8mi8FRaMHKmyLxmbu1RbyT5guEPglsosQifhtCyBYg69mfHjk6oSZiRPo"\
           "ZYzVtP6pgVmeZAgRX4w2f6HrJBTCeAVrNbYtsF5CJxnK6jdjX+B4KeMjiDaNjv/Mn6"\
           "lbCGRnf+fyt+XEEkQPxM7mK1XbZiKDpFSINnN4l/s0noGZ6Xf+jd21Hre2ZtsOyOOd"\
           "5PVRFMZj01ZjIoukgC+CvjhKfQv/Pg8ZBI9c/wKHXAaBLyJSRyRRoJG1wnyNInnHW2"\
           "WP7GwZ2wFp8wPF9pr/uT+gzGRwRdYeKvH/w8y+HuYbk9+X8WbLvzo6cq1Hp2clwUNY"\
           "2R+IgTfHWvyWuxRbUR4VUjBeBUWjB2VmO7a9btbSZ2Tm25Uywy6uXdebL6F0iZ+NUX"\
           "7t3B5myg6m8wzufZe01jiaRGd/18hk+qak/LElKl3QRdJoXyyzdiM06IhTPZyf1WNs"\
           "GQ3tB2i4IiND0ehBe0/jTx3ZRBLNvOdwvS9j+3uMWTJc71FHBi9neNsOuZRRSoSjQB"\
           "XYkJdA0XgpZu3dHAjmau5RuDK2v8/EwLZdopUVVqGSaPCDCJAMhqLxKrwZlF9iN9aZ"\
           "31j+eixX2ngwq6byvR6SZgMy6xHvNOsxuG2n9mnJ3WkKGROKRg/aexoffadhNv0iqL"\
           "K9P9D/e4fh/ryZgi+heyLlhnxbMl2FUo/M3j/RWMrM7sJ9PYa17bTfotAKy0tYIv7W"\
           "AXypI3VjfHjkSgjpBI9cCSG9oGgQQpygaBBCnKBoEEKcoGgQQpyoTk/sv4QQ8gzgN2"\
           "1z7GdzzbkDAAAAAElFTkSuQmCC"
license_b64 = "iVBORw0KGgoAAAANSUhEUgAAAQ0AAAAZCAIAAACkQOxmAAAAAXNSR0IArs4c6QAAAAR"\
          "nQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAJMSURBVHhe7ZmJjsMgDE"\
          "Tb/f9/7roZ13IAcyWkh+ZJW5nBjA0J2utGCGlyl6/H44EBISTnfr//aUgIieE9IaQN7"\
          "wkhbXhPCGnDe/ILyC+aGpE1LPx7Fx5e0VymPv+PbP7lQ7f561jUD27N3Pp93nKe6LOn"\
          "bn5uwvUNTyP99251jrc8v1NIOrdhpCfxNHOGp5SeYLrDdzU8h3TLn7sK5E/xsof6RW/"\
          "PEb5um1d/PxEFQaQDmy3qECW24Dm3MeQTIclRQjLlh5VVCdaM5PsYgTFkOFoa2Cqve6"\
          "skX0hmk7oVf8TJksi/U/dW65Ciz6rriol/0TzR8zQokY5APi1OAgNKpOsgozIrUxpt+"\
          "LS6Z4JPzheiypxbhWKhfKGJyWxzeSVBAiiC5UTLO3UhV1YgVT705y7bvLTogQjyAxJF"\
          "816ZPT51dMH+MRsqnQ3MfdGzwF4MVfe6SlOoxQtVN7ApHUyBMwGmIFjNp/9+sp3tDp0"\
          "I0KTXgao67mMMJfcjnmhPPlf4R2y72SEiejCQOYdaOHTiRa4MAU/h+XSPXekhPvSeRE"\
          "dQPxo/a6ep4z11n8rCTqaXH6w7Ss85GKqOEK2CHvlHuo8lB2k6Xoy2i8GJJBuwEqfoJ"\
          "srQx/I56l/BL8nNvUNiDjpL5Gnm1uMAij5FklZtlddFjBor5gt1PRFB3d/TU3cpUvRZ"\
          "9ZpiZB3RG3Yuq6tE/tfsroI0wHvyC6x7k/CGgBUlIv/VdYeQZnhPCGkg14T/jyekDe8"\
          "JIW14Twhpw3tCSBveE0IIIce53f4BFdwxTe9AxYEAAAAASUVORK5CYII="

EHX_COLUMN = [[
         Psg.Image(data=bconfig_b64)],
         [Psg.InputText('https://www.github.com/eagleEggs/EHX', key='APP_URL',
                       do_not_clear=True, size=(37, 10))],
         [Psg.InputCombo(DD_BROWSERS, key="BROWSERTYPE", size=(35, 10))],
         [Psg.ReadButton("", border_width=0,
                        tooltip='Start Testing Environment', key="LAUNCH",
                        size=(33, 2), image_data=launch_b64)],
         [Psg.Image(data=econfig_b64)],
         [Psg.Multiline(".text-gray-dark", size=(36, 2), enter_submits=True,
                       key='ENTER_ELEMENT', do_not_clear=True)],
         [Psg.InputCombo(DD_ELEMENTS, key="ELEMENT_TYPE", size=(35, 10))],
         [Psg.InputCombo(DD_COLORS, key="COLOR_TYPE", size=(35, 10))],
         [Psg.ReadButton('', key="HIGHLIGHT", border_width=0, size=(33, 5),
                        image_data=highlight_b64,
                        tooltip="Highlight Element")],
         [Psg.T("")],
         [Psg.Image(data=logo_b64)],
         [Psg.Image(data=license_b64)]]

layout = [[Psg.Column(EHX_COLUMN, size=(0, 0))]]
window = Psg.Window("EHX v1.0", no_titlebar=False,
                   auto_size_text=True).Layout(layout).Finalize()

# ######################################################################### ###
# ###########               GUI: Main Loop                      ########### ###
# ######################################################################### ###

while True:
    try:
        b, values = window.Read(timeout=100)

        if b == "LAUNCH":
            APP = BrowserController(values["BROWSERTYPE"], values["APP_URL"])
            log_info("Instantiating Application")

        if b == "HIGHLIGHT":

            log_info("Highlighting Button Pressed")

            waitWindow = Psg.Window(
                    'EHX | Processing Element(s)...', grab_anywhere=False,
                    no_titlebar=False, keep_on_top=True).Layout(
                    [[Psg.T("Please Wait, Processing Element(s)...")],
                    [Psg.T("This May Take a Minute.")]])

            try:
                SCRIPTVAR = str.strip(values['ENTER_ELEMENT'])
                exec("LIGHT=APP.engine.{}(\"{}\")\n"
                     "APP.highlight(LIGHT)".format(
                        str.strip(DD_ELEMENTS_DICT[values['ELEMENT_TYPE']]),
                        SCRIPTVAR))
                log_info("Highlighting Button Pressed, {}, Successful".format(
                        values['ELEMENT_TYPE']))



            except (NoSuchElementException, KeyError, AttributeError) as error:
                log_error("Highlight Button Pressed But Failed Executing "
                              "Command, {}".format(values['ELEMENT_TYPE']))
                log_error(error)
                Psg.PopupError("There was an issue Highlighting, "
                               "Check Element")

        if waitWindow_active:
            try:
                b1, values1 = waitWindow.Read(timeout=0)

            except RuntimeError:
                log_error("GUI Main Loop Runtime Error")

        if b is None:
            break

    except RuntimeError:
        Psg.PopupError("Error with GUI Loop\nWhile Processing Element(s)")
