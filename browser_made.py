#!/usr/bin/env python
"""
This program is a simple text-based internet browser, created as a study task
for course, provided by hyperskill.org. So, also functionality of this code
is strongly  limited by study plan requirements. Some lines could be joined
in one-liner, but sometimes, I have splitted them for better readibility
reasons.
When starting to use a Program, user runs a Program from the command line
and inputs a name for a directory where downloaded pages
will be saved (e.g. $python browser.py dir).
This directory emulates a cash memory.
To make a first connection with any site, user must
input domain name and extension (e.g. sitename.com), but all
necessary prefixes, like "https://" will be added automatically.
If connection is sucessful, the html-code of page will be displayed
and saved in the "cashe memory", so next time you can call for page
providing just this name. So, input, e.g.: sitename will open a page
sitename.com.
NB! If you are not very familiar with use of command line, just replace
function main() with this code by copy/paste method:
    def main():
        arg = 'dir'
        browser = Browser(arg)
        browser.action()
Browser has feature 'back' which returns a previous sucessfully
connected page. To use this feature, just print 'back' (using no quotation!)
instead of domain name, but to correctly leave a program- type'exit'.
Unfortunately, at the moment, browser does not work with sites, which do not
run under https protocol. This was implemented, but has been removed as
automated testing software did not let such code throuhg.

"""

from os import mkdir
import sys
from collections import deque
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

history = deque()
web_pages = []

def leave():
    '''Exit programm '''
    return sys.exit()

class Browser:

    def __init__(self, dir_name):

        self.dir_name = dir_name
        try:
            mkdir(self.dir_name)
        except FileExistsError:
            pass

    def get_url(self):
        '''receives input from user, and transforms it to
        complete https address '''
        prfix = 'https://'
        url = input()  # prompt ommited by intent as testing requires it
        if '.' in url:
            if not prfix in url:
                url = prfix + url
        return url


    def clean_text(self, url):
        '''connects to internet, downloads  page, and
         parses html to plain text, removing also CSS and Java artefacts'''
        r = requests.get(url)
        text = r.text
        text = BeautifulSoup(r.content, 'html.parser')
        [x.extract() for x in text.find_all('script')]
        [x.extract() for x in text.find_all('style')]
        [x.extract() for x in text.find_all('meta')]
        [x.extract() for x in text.find_all('noscript')]
        return text

    def page_back(self):
        '''Emulating "Back" function '''
        if len(history) == 1:
            url = history[0]
            tekst = self.clean_text(url.encode('utf-8'))
            print(tekst)
            self.action()
        elif len(history) > 1:
            url = (history.pop())
            tekst = self.clean_text(url.encode('utf-8'))
            print(tekst)
            history.append(url)
            web_pages.append(url)
            self.action()

        else:
            self.action()

    def action(self):
        '''Main engine of browser. It manages stack, provides
         writing into "cashe memory", and obtaining an info
         from it. It also provides control if requested URL
         has been inputted correctly'''
        while True:
            url = self.get_url()
            if url.lower() == 'back':
                if len(history) > 0:
                    history.pop()
                    self.page_back()
            if url.lower() == 'exit':
                leave()
            elif '.' in url:
                try:
                    short_url = url.split('//', 1)[-1]        ## made 3 lines
                    shorter_url = short_url.split('.', 1)[1]  ## for better
                    shortest_url = shorter_url.split('.')[0]  ##readibility reasons
                    history.append(url)
                    web_pages.append(url)
                    tekst = self.clean_text(url)
                    tekst = tekst.get_text()
                    print(tekst)
                    with open(f'{self.dir_name}\\{shortest_url}.txt', 'w', encoding='utf-8') as f:
                        f.write(tekst)

                except ConnectionError:
                    print('error. Page can not be connected or does not exist')
            else:
                short_url = url.split('//', 1)[-1]

                if url != 'back':
                    try:

                        with open(f'{self.dir_name}\\{short_url}.txt', 'r', encoding='utf-8') as f:
                            for line in f:
                                print(line.split('\n')[0])
                        for item in web_pages:
                            if url in item:
                                url = item
                        history.append(url)

                    except FileNotFoundError:
                        if len(history) > 0:
                            history.pop()
                        print('Error: Incorrect URL')


def main():
    arg = sys.argv
    browser = Browser(arg[1])
    browser.action()


if __name__ == '__main__':
    main()
