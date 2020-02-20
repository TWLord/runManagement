import sys
import os
import argparse
import math
import re

from maus_cpp.mice_module import MiceModule
import maus_cpp.globals
import maus_cpp.field
import Configuration



if __name__ == "__main__":
    parser = argparse.ArgumentParser( description="runScript" )

    parser.add_argument( 'step4runs', nargs='+', help='txt file(s) '+'containing run information')

    #parser.add_argument( '--optics', type=str, default="", help='Select by optics' )

    #parser.add_argument( '--momentum', type=str, default="", help='Select by momentum' )

    #parser.add_argument( '--emittance', type=str, default="", help='Select by emittance' )

    #parser.add_argument( '--absorber', type=str, default="", help='Select by absorber' )

    #parser.add_argument( '--magnet', type=str, default="", help='Select by magnet mode' )

    #parser.add_argument( '--CC', type=str, default="", help='Select by cooling channel' )

    #parser.add_argument( '--run', type=str, default="10314", help='run number for geometry file' )

    parser.add_argument( '--dest', type=str, default="", help='destination path for output file, include trailing /' )
    if len(sys.argv) > 5:
        print "too many arguments, given "+ len(sys.argv)
        print "Usage: python sortStep4runs.py --options step4-runs.txt"
        print "options : --run .. --dest .. " 
        sys.exit(1)
    
    try :
        namespace = parser.parse_args()

        #inFile = namespace.step4runs

        AllRuns = namespace.step4runs #.split()

        #Geomdir = "/data/mice/phumhf/Geometries/runnumber_"+namespace.run+"/"

        ParentFile = "ParentGeometryFile.dat"
        TrackerFile = "Tracker0.dat"
        

        dest = namespace.dest
        #if dest == "" : 
        #  print "Input --dest option "
        #  sys.exit(1)
        #if not os.path.isdir(dest) and dest != "" :
        #  os.mkdir(dest)

    except BaseException as ex:
      raise
    else :

     runlist = {}

     for run in AllRuns : 
         print " #### Getting " + run + " Geom #### "
         Geomdir = "/data/mice/phumhf/Geometries/runnumber_"+run+"/"

         #test = os.path.expandvars("${MAUS_ROOT_DIR}/tests/py_unit/"+\
         #                      "test_maus_cpp/test_mice_modules_global_coords.dat")
         parentpath = os.path.expandvars(Geomdir+ParentFile)
         #trackerpath = os.path.expandvars(Geomdir+TrackerFile)
         #mod = MiceModule(file_name=test)
         Parent = MiceModule(file_name=parentpath)
         #Tracker = MiceModule(file_name=trackerpath)
         maus_cpp.globals.birth(Configuration.Configuration().getConfigJSON())
         #maus_cpp.globals.get_monte_carlo_mice_modules(Parent)
         maus_cpp.globals.set_monte_carlo_mice_modules(Parent)
         ###print "NEW FIELDS"
         ###print maus_cpp.field.str(True)
     
         #children = mod.get_children()
         children = Parent.get_children()
         print " --- children --- "
         print children
    
         runlist[run] = {}

         #trackerlist = {}

         for tracker in [ "Tracker0" , "Tracker1" ] :
           Tracker = [x for x in children if x.get_name().find(tracker) > -1][0] 
      
           print Tracker.get_name()
           print " --- Tracker children --- "
           print [x.get_name() for x in Tracker.get_children()]
           #print " --- children list --- "
           #print Tracker.get_children()
           tkupos = Tracker.get_property("Position", "HEP3VECTOR")
           tkurot = Tracker.get_property("Rotation", "HEP3VECTOR")
           trackervals = {
             "pos":tkupos,
             "rot":tkurot,
           }

           runlist[run][Tracker.get_name()] = trackervals
           #runlist[run][tracker] = trackervals

           print " --- doing stations --- "
           for child in Tracker.get_children() :
             station = child.get_name() 
             spos = child.get_property("Position", "HEP3VECTOR")
             srot = child.get_property("Rotation", "HEP3VECTOR")
             stationvals = {
               "pos":spos,
               "rot":srot,
             }
             print station
             runlist[run][station] = stationvals
             print " --- doing planes --- \n"
             for pchild in child.get_children() :
               plane = pchild.get_name()
               print plane
               ppos = pchild.get_property("Position", "HEP3VECTOR")
               prot = pchild.get_property("Rotation", "HEP3VECTOR")
               planevals = {
               "pos":ppos,
               "rot":prot,
               }
               runlist[run][plane] = planevals


         maus_cpp.globals.death()
         #maus_cpp.globals.death(Configuration.Configuration().getConfigJSON())
     print " --- runlist --- "
     print runlist
     #print runlist["10508"]['Tracker1Station1']
  
     """runlist = {}
     run = {
       "tku5zpos":549.9513, # in mm
       "tku5uplanezpos":0.6648,
       "tkuzpos":14515.836783,
       "tkuxpos":-0.86511378119,
       "tkuypos":3.64859277401, # in degrees
       "tkuxr":0.196047193,
       "tkuyr":179.985234111,
     }
     runlist["10314"] = run
     run2 = {
       "tku5zpos":549.9513,
       "tku5uplanezpos":0.6648,
       "tkuzpos":14512.6206533,
       "tkuxpos":-0.303448878911,
       "tkuypos":2.81635450057,
       "tkuxr":0.153845,
       "tkuyr":179.981505,
     }
     runlist["10504"] = run2"""


     from argparse import Namespace
     for run in runlist.keys() :
       #n = Namespace(**run)
       #tku5zpos = runlist[run]["tku5zpos"]
       #tku5uplanezpos = runlist[run]["tku5uplanezpos"]
       #tkuzpos = runlist[run]["tkuzpos"]
       #tkuxpos = runlist[run]["tkuxpos"]
       #tkuypos = runlist[run]["tkuypos"]
       #tkuxr = runlist[run]["tkuxr"]
       #tkuyr = runlist[run]["tkuyr"]
       print "\n --- Run " + run + " --- "
       for trkr in [ "Tracker0", "Tracker1"] :
         for stn in [ "Station1", "Station2", "Station3", "Station4", "Station5", ] :
           #for pln in [ "ViewU", "ViewV", "ViewW", ] :
           for pln in [ "ViewU", ] :
             subtrkr = trkr
             if trkr.find("0") > -1 :
               subtrkr = subtrkr.replace("0", "")
             #tku5zpos = runlist[run]["Tracker0Station1"]
             tkuSzpos = runlist[run][subtrkr+stn]['pos']['z']
             tkuSuplanezpos = runlist[run][trkr+pln+stn]['pos']['z']
             #tkuSuplanezpos = 0 
             tkuzpos = runlist[run][trkr+".dat"]['pos']['z']
             #tkuxpos = runlist[run][]
             #tkuypos = runlist[run][]
             tkuxr = runlist[run][trkr+".dat"]['rot']['x']
             tkuyr = runlist[run][trkr+".dat"]['rot']['y']
      
             value = tkuzpos + ( math.cos(math.radians(tkuxr))*math.cos(math.radians(tkuyr)) * (tkuSzpos + tkuSuplanezpos) )
             #print subtrkr + stn + " u plane z pos : " + str(value)
             print subtrkr + stn + plane + " z pos : " + str(value)

