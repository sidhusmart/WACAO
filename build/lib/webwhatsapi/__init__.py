"""
WhatsAPI module
"""
# -*- coding: utf-8 -*-

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

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.sum_basic import SumBasicSummarizer as Summarizer
from sumy.summarizers.kl import KLSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.random import RandomSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
#from sumy.summarizers.lsa import LsaSummarizer as Summarizer
#from sumy.summarizers.edmundson import EdmundsonSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

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

    def wishBirthday(self, text):
        summarizeKeyword = 'hbd -'

        text = text.lower()

        groupStart = text.index(summarizeKeyword)

        groupName = text[groupStart+6:].strip()

        birthdayMessage = "Hey " + groupName + ", Here's wishing you a great birthday. Hope you have many many wonderful years ahead"

        self.send_to_whatsapp_id(groupName, birthdayMessage)

    def summarizeChats(self, text):
        summarizeKeyword = 'summarize -'

        text = text.lower()

        groupStart = text.index(summarizeKeyword)

        groupName = text[groupStart+11:].strip()

        self.view_unread_from_group(groupName)

    def view_unread_from_group(self, groupName):
        try:
            script_path = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            script_path = os.getcwd()
        script = open(os.path.join(script_path, "js_scripts/get_unread_messages_from_group.js"), "r").read()
        Store = self.driver.execute_script(script, groupName)
        messages = Store[0]['messages']
        self.analyzeChats(messages, groupName)

    def analyzeChats(self, messages, groupName):
        # WordCount Implementation
        inputLine = ''
        for message in messages:
            if '\\/' not in message:
                inputLine = inputLine + message['message'] + '. '
        # blob = TextBlob(inputLine)
        # wordCounts = blob.word_counts
        # sortedWordCounts = sorted(wordCounts, key=wordCounts.get, reverse=True)
        # outputLine = " ".join(sortedWordCounts[:5])
        # outputLine = groupName.capitalize() + " summarized as " + outputLine
        # self.send_to_whatsapp_id("WACAO!",outputLine)

        LANGUAGE = "english"
        SENTENCES_COUNT = '20%'

        outputLine = groupName.capitalize() + " summarized as: \n"
        parser = PlaintextParser.from_string(inputLine, Tokenizer(LANGUAGE))
        stemmer = Stemmer(LANGUAGE)
        summarizer = LsaSummarizer(stemmer)
        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)
        for sentence in summarizer(parser.document, SENTENCES_COUNT):
            outputLine = outputLine + unicode(str(sentence), "utf-8") + "\n"
        self.send_to_whatsapp_id("WACAO!",outputLine)
        # print "sum_basic:"
        # print outputLine

        ## Trying different parsers
        # outputLine = groupName.capitalize() + " summarized as: \n"
        # parser = PlaintextParser.from_string(inputLine, Tokenizer(LANGUAGE))
        # stemmer = Stemmer(LANGUAGE)
        # summarizer = KLSummarizer(stemmer)
        # summarizer.stop_words = get_stop_words(LANGUAGE)
        # for sentence in summarizer(parser.document, SENTENCES_COUNT):
        #     outputLine = outputLine + unicode(str(sentence), "utf-8") + "\n"
        # print "KLSummarizer:"
        # print outputLine

        ## Trying different parsers
        # outputLine = groupName.capitalize() + " summarized as: \n"
        # parser = PlaintextParser.from_string(inputLine, Tokenizer(LANGUAGE))
        # stemmer = Stemmer(LANGUAGE)
        # summarizer = LexRankSummarizer(stemmer)
        # summarizer.stop_words = get_stop_words(LANGUAGE)
        # for sentence in summarizer(parser.document, SENTENCES_COUNT):
        #     outputLine = outputLine + unicode(str(sentence), "utf-8") + "\n"
        # print "LexRankSummarizer:"
        # print outputLine

        ## Trying different parsers
        # outputLine = groupName.capitalize() + " summarized as: \n"
        # parser = PlaintextParser.from_string(inputLine, Tokenizer(LANGUAGE))
        # stemmer = Stemmer(LANGUAGE)
        # summarizer = LsaSummarizer(stemmer)
        # summarizer.stop_words = get_stop_words(LANGUAGE)
        # for sentence in summarizer(parser.document, SENTENCES_COUNT):
        #     outputLine = outputLine + unicode(str(sentence), "utf-8") + "\n"
        # print "LsaSummarizer:"
        # print outputLine

        ## Trying different parsers
        # outputLine = groupName.capitalize() + " summarized as: \n"
        # parser = PlaintextParser.from_string(inputLine, Tokenizer(LANGUAGE))
        # stemmer = Stemmer(LANGUAGE)
        # summarizer = LuhnSummarizer(stemmer)
        # summarizer.stop_words = get_stop_words(LANGUAGE)
        # for sentence in summarizer(parser.document, SENTENCES_COUNT):
        #     outputLine = outputLine + unicode(str(sentence), "utf-8") + "\n"
        # print "LuhnSummarizer:"
        # print outputLine

        ## Trying different parsers
        # outputLine = groupName.capitalize() + " summarized as: \n"
        # parser = PlaintextParser.from_string(inputLine, Tokenizer(LANGUAGE))
        # stemmer = Stemmer(LANGUAGE)
        # summarizer = LuhnSummarizer(stemmer)
        # summarizer.stop_words = get_stop_words(LANGUAGE)
        # for sentence in summarizer(parser.document, SENTENCES_COUNT):
        #     outputLine = outputLine + unicode(str(sentence), "utf-8") + "\n"
        # print "LuhnSummarizer:"
        # print outputLine

        ## Trying different parsers
        # outputLine = groupName.capitalize() + " summarized as: \n"
        # parser = PlaintextParser.from_string(inputLine, Tokenizer(LANGUAGE))
        # stemmer = Stemmer(LANGUAGE)
        # summarizer = RandomSummarizer(stemmer)
        # summarizer.stop_words = get_stop_words(LANGUAGE)
        # for sentence in summarizer(parser.document, SENTENCES_COUNT):
        #     outputLine = outputLine + unicode(str(sentence), "utf-8") + "\n"
        # print "RandomSummarizer:"
        # print outputLine

        ## Trying different parsers
        # outputLine = groupName.capitalize() + " summarized as: \n"
        # parser = PlaintextParser.from_string(inputLine, Tokenizer(LANGUAGE))
        # stemmer = Stemmer(LANGUAGE)
        # summarizer = TextRankSummarizer(stemmer)
        # summarizer.stop_words = get_stop_words(LANGUAGE)
        # for sentence in summarizer(parser.document, SENTENCES_COUNT):
        #     outputLine = outputLine + unicode(str(sentence), "utf-8") + "\n"
        # print "TextRankSummarizer:"
        # print outputLine        

        # parser = PlaintextParser.from_string(inputLine, Tokenizer(LANGUAGE))
        # stemmer = Stemmer(LANGUAGE)
        # summarizer = Summarizer(stemmer)
        # summarizer.null_words = get_stop_words(LANGUAGE)
        # summarizer.bonus_words = parser.significant_words
        # summarizer.stigma_words = parser.stigma_words
        # for sentence in Summarizer(inputLine, SENTENCES_COUNT):
        #     print sentence

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
                        key = str(message['timestamp']) + '-' + message['message'].encode('utf-8','ignore')
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
                            if ('HBD' in text):
                                self.wishBirthday(text)

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




