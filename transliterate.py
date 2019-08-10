'''

    Author: Varun Chopra
    Date of completion: 26/07/2019
    Description: This is the python script that performs the actual transliteration for both real-time input as well as copy-pasted text.

'''


#!/usr/bin/python
# -*- coding: utf-8 -*-

import startquill_cherry as start
import json

#For copy-pasted text
def pasted(inp, lang):

    try:
        out_string = ''
        d = dict()
        out_string = start.quillCherry.processString(inp, lang)
        d['options'] = ''
        d['itrans'] = out_string
        d = json.dumps(d)
        return d

    except:
        print("Exception raised: An unsupported character has been entered.\nThe exception was handled successfully.")

#For real-time input
def real_time(inp, lang):

    d = dict()
    try:

        #For first word
        if inp.count(' ') <= 1 and ( inp[-1] not in ['.',',','?','-'] ):
            inp = inp.strip(' ')
            out_string = start.quillCherry.processString(inp, lang) + ' '
            ret = json.loads(start.quillCherry.processWordJSON(inp, lang))
            opt = ret['twords'][0]['options']
            opt.insert(0, ret['itrans'])

        #For all words after the first word
        else:
            out_string = start.quillCherry.processString(inp, lang)
            inp_temp = inp.replace('\n',' ').replace('\r','')
            inp_rsplit = inp_temp[:-1].rsplit(' ', 1)
            #print("inp_rsplit: %s" % inp_rsplit)
            inp_rsplit[1] = inp_rsplit[1].replace('\n','').replace('\r', '')
            #print("inp_rsplit after replacing /r/n: %s" % inp_rsplit)
            ret = json.loads(start.quillCherry.processWordJSON(inp_rsplit[1], lang))

            #list of all options
            opt = ret['twords'][0]['options']                   
            opt.insert(0, ret['itrans'])
            #print("all options:")
            #for item in opt:
                #print(item)
            
            #print("best option: %s" % out_string)
            
        d['options'] = opt
        d['itrans'] = out_string
        d = json.dumps(d)
        return d

    except:
        print("Exception raised: An unsupported character has been entered.\nThe exception was handled successfully.")


def _transliterate(flag, inp, lang):

    #Copy-pasted data
    if flag == True:
        return pasted(inp, lang)

    #Entering one word at a time
    else:
        return real_time(inp, lang)