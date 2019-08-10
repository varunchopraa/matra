'''

    Author: Varun Chopra
    Date of completion: 08/07/2019
    Description: This python script is responsible for hosting all the necessary files essential for the functioning of the tool using a CherryPy server.

'''

import cherrypy
import transliterate as xlit

class Input(object): 
    
    @cherrypy.expose()
    def index(self):
        #Hosting index page
        return file("index.html")

    @cherrypy.expose()
    def demo(self):
        #Hosting demo page
        return file("demo.html")
               
    @cherrypy.expose() 
    def transliterate(self, flag, inp, lang):
        #Calling transliteration function
        return xlit._transliterate(flag, inp, lang)

    @cherrypy.expose()
    def script(self):
        #Hosting javascript file
        return file("javascripts/xlit.js")

    @cherrypy.expose()
    def title(self):
        #Hosting title gif
        return file("matra_title/matra_title.gif")
    
cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': 8090})
cherrypy.quickstart(Input(), "/")