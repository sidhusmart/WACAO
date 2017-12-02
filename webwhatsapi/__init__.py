"""
WhatsAPI module
"""

#from __future__ import print_function

import datetime
import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from textblob import TextBlob

class WhatsAPIDriver(object):
    _PROXY = None

    _URL = "http://web.whatsapp.com"

    _SELECTORS = {
        'firstrun': "#wrapper",
        'qrCode': "._2EZ_m > img:nth-child(4)",
        'mainPage': ".app.two",
        'chatList': ".infinite-list-viewport",
        'messageList': "#main > div > div:nth-child(1) > div > div.message-list",
        'unreadMessageBar': "#main > div > div:nth-child(1) > div > div.message-list > div.msg-unread",
        'searchBar': ".input",
        'searchCancel': ".icon-search-morph",
        'chats': ".infinite-list-item",
        'chatBar': 'div.input',
        'sendButton': 'button.icon:nth-child(3)',
        'LoadHistory': '.btn-more',
        'UnreadBadge': '.icon-meta',
        'UnreadChatBanner': '.message-list',
        'ReconnectLink': '.action',
        'WhatsappQrIcon': 'span.icon:nth-child(2)',
        'QRReloader': '.qr-wrapper-container'
    }

    _CLASSES = {
        'unreadBadge': 'icon-meta',
        'messageContent': "message-text",
        'messageList': "msg"
    }

    _ISOlanguage = {'spanish': "es",
                    'german': "de",
                    'english': "en",
                    'french': "fr",
                    'greek': "el",
                    'italian': "it",
                    'japanese': "ja"}

    _translateContacts = []

    driver = None

    def __init__(self, username="API"):
        "Initialises the browser"
        ## Proxy support not currently working
        # env_proxy = {
        #     'proxyType': ProxyType.MANUAL,
        #     'httpProxy': os.environ.get("http_proxy"),
        #     'httpsProxy': os.environ.get("https_proxy"),
        #     'ftpProxy': os.environ.get("ftp_proxy"),
        # }
        # self._PROXY = Proxy(env_proxy)
        self.driver = webdriver.Firefox()  # trying to add proxy support: webdriver.FirefoxProfile().set_proxy()) #self._PROXY))
        self.username = username
        self.driver.get(self._URL)
        self.driver.implicitly_wait(10)

    def firstrun(self):
        "Saves QRCode and waits for it to go away"
        if "Click to reload QR code" in self.driver.page_source:
            self.reloadQRCode()
        qr = self.driver.find_element_by_css_selector(self._SELECTORS['qrCode'])
        qr.screenshot(self.username + '.png')
        WebDriverWait(self.driver, 30).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, self._SELECTORS['qrCode'])))

    def view_unread(self):
        try:
            script_path = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            script_path = os.getcwd()
        script = open(os.path.join(script_path, "js_scripts/get_unread_messages.js"), "r").read()
        Store = self.driver.execute_script(script)
        return Store

    def send_to_whatsapp_id(self, id, message):
        try:
            script_path = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            script_path = os.getcwd()
        script = open(os.path.join(script_path, "js_scripts/send_message_to_whatsapp_id.js"), "r").read()
        success = self.driver.execute_script(script, id.lower(), message)
        return success

    def send_to_phone_number(self, pno, message):
        try:
            script_path = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            script_path = os.getcwd()
        script = open(os.path.join(script_path, "js_scripts/send_message_to_phone_number.js"), "r").read()
        success = self.driver.execute_script(script, pno, message)
        return success

    def get_whatsapp_id(self, pno, message):
        try:
            script_path = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            script_path = os.getcwd()
        script = open(os.path.join(script_path, "js_scripts/test.js"), "r").read()
        success = self.driver.execute_script(script, pno, message)
        return success

    def get_all_messages(self, id):
        try:
            script_path = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            script_path = os.getcwd()
        script = open(os.path.join(script_path, "js_scripts/get_all_messages.js"), "r").read()
        success = self.driver.execute_script(script, id)
        return success

    def get_n_messages(self, id, numberOfMsg):
        try:
            script_path = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            script_path = os.getcwd()
        script = open(os.path.join(script_path, "js_scripts/get_n_messages.js"), "r").read()
        success = self.driver.execute_script(script, id, numberOfMsg)
        return success

    def __unicode__(self):
        return self.username

    def __str__(self):
        return self.__unicode__()

    def reloadQRCode(self):
        self.driver.find_element_by_css_selector(self._SELECTORS['QRReloader']).click()

    def create_callback(self, callback_function):
        try:
            while True:
                messages = self.view_unread()
                if messages != []:
                    callback_function(messages)
                time.sleep(5)
        except KeyboardInterrupt:
            print "Exited"

    def manageReverseTranslation(self, text, user):
        blob = TextBlob(text)
        translatedText = str(blob.translate(to=self._ISOlanguage['english']))
        translatedText = user + ' replied - ' + translatedText
        self.send_to_whatsapp_id('WACAO!',translatedText)

    def translateMessage(self, text):
        translateKeyword = 'translate to'
        translateSep = '-'
        textSeperator = 'and send to'
        
        text = text.lower()

        langStart = text.index(translateKeyword)
        langEnd = text.index(translateSep)
        textEnd = text.index(textSeperator)

        langDetect = text[langStart+13:langEnd].strip()
        textDetect = text[langEnd+1:textEnd].strip()
        contactDetect = text[textEnd+11:].strip()

        blob = TextBlob(textDetect)
        translatedText = str(blob.translate(to=self._ISOlanguage[langDetect.strip()]))

        self.send_to_whatsapp_id(contactDetect,translatedText)
        self._translateContacts.append(contactDetect)

    def summarizeChats(self, text):
        summarizeKeyword = 'summarize -'
        messageCountKeyword = 'for last'
        chatKeyword = 'chats'

        text = text.lower()

        groupStart = text.index(summarizeKeyword)
        countStart = text.index(messageCountKeyword)
        countEnd = text.index(chatKeyword)

        groupName = text[groupStart+11:countStart].strip()
        chatHistory = text[countStart+8:countEnd].strip()

        print groupName
        print chatHistory
        chats = self.get_n_messages(groupName, chatHistory)

        print chats
        messages = chats['messages']
        print "Length: " + len(messages)
        for message in messages:
            print message['message']

    def monitorWACAO(self):
        try:
            # Creating a dictionary to store already seen messages
            messageSeen = {}
            # Keep monitoring the group for chats
            while True:
                # Listening to instructions for the Assistant
                # Hard-coded to the WACAO Assistant group - this is a group with only you in it
                chat = self.get_all_messages("WACAO!")
                if chat != []:
                    messages = chat[0]['messages']
                    for message in messages:
                        # Create a hash-key that is used to uniquely identify a message. It's timestamp plus message text 
                        key = str(message['timestamp']) + '-' + str(message['message'])
                        # If this particular message/time has been seen then don't take any action
                        if key in messageSeen:
                            continue
                        else:
                            # Add the message/time to the dictionary to not action again
                            messageSeen[key] = message['message']
                            text = message['message']
                            ############################################################
                            ##########  Take any Action with the message here ##########
                            if ('Translate to' in text):
                                self.translateMessage(text)
                            if ('Summarize' in text):
                                self.summarizeChats(text)

                # Listening to incoming messages for task specific responses
                incomingChats = self.view_unread()
                for chat in incomingChats:
                    incomingContact = chat['contact']
                    # Taking action in case of contacts responding with their messages
                    if incomingContact.lower() in self._translateContacts:
                        messages = chat['messages']
                        for message in messages:
                            self.manageReverseTranslation(message['message'], incomingContact)
                
                # Monitoring every 5 seconds
                time.sleep(5)
        except KeyboardInterrupt:
            print "Exited"

    def createDummyData(self):
        script_path = os.getcwd()
        f = open(os.path.join(script_path, "text.txt"), "r")
        for line in f:
            msg = line.split()
            i = 0
            for m in msg:
                if i < 40:
                    self.send_to_whatsapp_id('Test group',m)
                    i = i + 1

    def view_unread_from_group(self):
        try:
            script_path = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            script_path = os.getcwd()
        script = open(os.path.join(script_path, "js_scripts/get_unread_messages_from_group.js"), "r").read()
        Store = self.driver.execute_script(script, "Test")
        print Store
        messages = Store['messages']
        for message in messages:
            print message['message']


