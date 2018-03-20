import traceback
import datetime
import json
#import req


__author__ = 'Joe Payne (GRXE)'




class GrxeObject():

    DEBUG   = True
    VERBOSE = True

    def __init__(self):
        pass

    def enable_debug(self):
        self.DEBUG = True

    def disable_debug(self):
        self.DEBUG = False

    def enable_verbose(self):
        self.VERBOSE = True

    def disable_verbose(self):
        self.VERBOSE = False

    def say(self, context, str):
        #print(' '.join(_input_to_str(txt)))
        print("%s :: %s" % (context, str))

    def debug(self, context, str):
        if self.DEBUG:
            #print(' '.join(_input_to_str(txt)))
            print("%s :: %s" % (context, str))


    def exc(self, context, str, exc=None ):
        if self.DEBUG or self.VERBOSE:
            print("Handled Exception:: %s :: %s", (context, str))

            if exc and self.DEBUG:
                print("Handled Exception Type: %s" % type(exc).__name__)

                print(traceback.format_exc())


    def verbose(self, context, str):
        if self.VERBOSE:
            print("%s :: %s" % (context, str))

'''
def wget(self, url):
    ret = requests.get(url)
    ret.raise_for_status()

    return requests.get(url)
'''

def wget(self, url, save_fn):

    ofile   = open(save_fn, 'wb')

    ret = self.wget(url)

    for bytes in ret.iter_content(self.REQ_BYTE_SIZE):
        ofile.write(bytes)

    ofile.close()
'''
def _input_to_str( *txts):

    output = []

    for txt in txts:
        output.append(str(txt))

    return output
'''

def now(self):
    return datetime.datetime.now()

def read_file(filename,mode='r'):

    tar_file    = open(filename, mode)

    lines       = tar_file.readlines()
    tar_file.close()

    return lines


def save_json(filename, json_data):

    with open(filename,"w+") as ofile:
        json.dump(json_data, ofile, indent=4)



def load_json(filename):

    with open(filename, "r") as json_file:
    #try:
        json_txt = json.load(json_file)

    json_file.close()

    return json_txt


