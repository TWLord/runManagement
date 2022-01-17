import time
import importlib
import sys
import math
import os
import json
import re

import ROOT

import Configuration
import maus_cpp.globals
import maus_cpp.material
import maus_cpp.field as field

import xboa.common

def initialise_maus():
    configuration = Configuration.Configuration().\
                                          getConfigJSON(command_line_args=True)
    maus_cpp.globals.birth(configuration)

class LoadGlobals(object):
    def __init__(self, geom_dir):
        self.geom_dir = geom_dir
        self.tracker_file = None

    def get_global_tracker_pos(self):
        f = open(os.path.join(self.geom_dir, "ParentGeometryFile.dat"), "r")
        line = f.readline()
        while "Tracker0" not in line:
            #print line
            line = f.readline()
        loc = line.split()
        posline = f.readline()
        posline = f.readline()
        rotline = f.readline()
        pos = posline.split()[1:4]
        rot = rotline.split()[1:4]
        f.close()
        self.tracker_file = loc
        return loc, pos, rot
        
    def get_tracker_locals(self):
        f = open(os.path.join(self.geom_dir, "Tracker0.dat"), "r")
        fstr = f.read()
        #for line in fstr.split("\n"):
        #    larray = line.split():
        #    if len(larray) > 1:
        #        larray[0] = "\""+str(larray[0]) + "\""
        #        larray[1] = "\""+str(larray[0]) + "\""
        #        
        #        
        #    print line

        #fstr.replace(" ", ":")
        #fstr = re.sub(
        #    pattern='\[(\w*)\]\n',
        #    repl='"\\1":',
        #    string=fstr
        #)
        #fstr = re.sub( 'Module (\w.*)\n', '\n"Module \\1":\n', fstr )
        #fstr = re.sub( 'Module (\w.*)\n', '\n"Module \\1":\n', fstr )
        fstr = re.sub( 'Module (.*)\n', '"Module\\1":\n', fstr )
        fstr = re.sub( '\}\n(\w)', '},\n\\1', fstr )
        fstr = re.sub( '\n(\w.*)\s(\w.*)\n', '\n"\\1":"\\2",\n', fstr )
        fstr = re.sub( '\n(\w.*)\s(\w.*)\n', '\n"\\1":"\\2",\n', fstr )
        fstr = re.sub( '\n\s*(\w.*)\s(\w.*)\n', '\n"\\1":"\\2",\n', fstr )
        fstr = re.sub( '\n\s*(\w.*)\s(\w.*)\n', '\n"\\1":"\\2",\n', fstr )
        fstr = re.sub( '\n} \/\/.*\n', '\n}, \n', fstr )
        fstr = re.sub( '\n\n', '\n', fstr )
        fstr = re.sub( '\n{\n', '{\n', fstr )
        fstr = re.sub( '\n {\n', '{\n', fstr )
        fstr = re.sub( '\n }\n', '\n}\n', fstr )
        fstr = re.sub( '\n },\n', '\n},\n', fstr )
        #fstr = re.sub( ':{', ': {', fstr )
        #fstr = re.sub( '\n\s.*(\w.*)\s(\w.*)\n([^}])', '"\\1":"\\2",\\3\n', fstr )
        #fstr = re.sub( '\n"(Module.+?),', '\n"\\1 :', fstr )
        #fstr = re.sub( '\}\n(\w)', '},\\1', fstr )

        print fstr
        fstr = "{\n"+fstr+"\n}"
        print fstr.splitlines()[11]
        print fstr.splitlines()[12]
        print fstr.splitlines()[13]
        tracker_dict = json.loads(fstr)
    
    def get_coords(self):
        loc, pos, rot = self.get_global_tracker_pos()
        print loc, pos, rot
        self.get_tracker_locals()

if __name__ == "__main__":
    #file_name = "/storage/epp2/mice/phumhf/MC/MAUSv3.3.2/09760v4/00001_sim.root"
    geom_dir = "/storage/epp2/phumhf/MICE/Geometries/runnumber_09883/"
    globject = LoadGlobals(geom_dir)
    globject.get_coords()
    

