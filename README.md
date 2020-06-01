# browser-prototype
text based browser

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
