#GUI build for UVIndex checker
#Will download data from ARPANSA website when run and provide UV rating at current time


#Importing the relevant modules:
#tkinter to build window
#requests to download xml data
#ElementTree to parse xml file
#os to remove xml file on window destruction

import tkinter as tk
import requests as rq
import xml.etree.ElementTree as et
import os

#Creating application as a class
class IndexChecker(tk.Tk):
    def __init__(self, *args):
        tk.Tk.__init__(self, *args)
        
        self.title ('UV Index Checker V2.0')
        self.resizable ('false', 'false')
        
        #Creates an empty label at the top of the window.
        #Will be filled with the results.
        self.Index =tk.Label (
        text ='',
        font =('arial', '25', 'bold'),
        foreground ='orange',
        background ='black',
        width ='15',
        height ='3'
        )
        self.Index.grid(sticky ='nsew')


        #Creates a button which calls the ARPANSARetrieval self function.
        self.Retrieval = tk.Button (self,
        text = 'Get UV Index',
        font = ('arial', '25', 'bold'),
        fg = 'white',
        bg = 'black',
        width = '15',
        borderwidth ='2',
        command = self.ARPANSARetrieval
        )
        self.Retrieval.grid(sticky ='nsew')
        
        #Creates a button which calls the Deletexml self function.
        self.Exit = tk.Button (self,
        text = 'Exit',
        font = ('arial', '25', 'bold'),
        fg ='white',
        bg ='black',
        width = '15',
        borderwidth ='2',
        command = self.Deletexml
        )
        self.Exit.grid(sticky='nsew')
        


    #Defines the self function for downloading and parsing the xml data.
    #Uses Requests library to download, and ElementTree to parse.
    def ARPANSARetrieval(self):
        url = ('https://uvdata.arpansa.gov.au/xml/uvvalues.xml')
        r = rq.get (url)
        
        #Creates a new xml file in the location of this script.
        #Propagates content based on downloaded xml data.
        with open ('UVDATA.xml', 'wb') as self.UVDATA:
            self.UVDATA.write(r.content)
            self.UVDATA = ('UVDATA.xml')
                      
        
        #Uses ElementTree to parse xml iteratively.
        #Looks for 'time' and 'index' values assigned to 'Melbourne'.
        tree = et.parse(self.UVDATA)
        root = tree.getroot()
        for child in root.iter():
            locationofinterest = str(child.attrib)
            lc = locationofinterest
            if 'Melbourne' in lc:
                for y in child.iter('time'):
                    time = y.text
                for x in child.iter('index'):
                    #Needs to select part of the lc string because it contains characters
                    #prior to 'Melbourne'.
                    self.Index ['text'] =(lc[8:17] + '''\n''' + time + '''\n''' + x.text)
    
    #Defines the delete self function.
    #Deletes the xml file if it exists.
    #Error checking closes window regardless of file existence.
    def Deletexml(self):
        try:
            os.remove(self.UVDATA)
            self.destroy()
        except:
            self.destroy()


#Calls the application class without any arguments
#and keeps the window active until exited by user.
IndexChecker().mainloop()

