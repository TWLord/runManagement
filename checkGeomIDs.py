import sys
import os
import argparse
import math
import re

if __name__ == "__main__":
    parser = argparse.ArgumentParser( description="runScript" )

    parser.add_argument( 'step4runs', nargs='+', help='txt file(s) '+\
                                            'containing run information')

    #parser.add_argument( '--optics', type=str, default="", help='Select by optics' )

    #parser.add_argument( '--momentum', type=str, default="", help='Select by momentum' )

    #parser.add_argument( '--emittance', type=str, default="", help='Select by emittance' )

    #parser.add_argument( '--absorber', type=str, default="", help='Select by absorber' )

    #parser.add_argument( '--magnet', type=str, default="", help='Select by magnet mode' )

    #parser.add_argument( '--CC', type=str, default="", help='Select by cooling channel' )

    parser.add_argument( '--dest', type=str, default="", help='destination path for output file, include trailing /' )
    if len(sys.argv) < 3:
        print "Usage: python sortStep4runs.py --options step4-runs.txt"
        print "options : --optics .. --momentum .. --absorber .. --magnet .. --CC .. --dest .. "
        sys.exit(1)
    
    try :
        namespace = parser.parse_args()

        inFile = namespace.step4runs

        Geomdir = "/data/mice/phumhf/Geometries/"

        dest = namespace.dest
        if dest == "" : 
          print "Input --dest option "
          sys.exit(1)
        if not os.path.isdir(dest) and dest != "" :
          os.mkdir(dest)

        cutnames = []

        """optics = namespace.optics
        absorber = namespace.absorber
        magnet = namespace.magnet
        CC = namespace.CC
        momentum = namespace.momentum
        emittance = namespace.emittance


        cuts = {}

        if optics != "" :
            cuts["optics"] = optics
            cutnames.append("optics")

        if emittance != "" :
            cuts["emittance"] = emittance
            cutnames.append("emittance")

        if momentum != "" :
            cuts["momentum"] = momentum
            cutnames.append("momentum")

        if absorber != "" :
            cuts["absorber"] = absorber 
            cutnames.append("absorber")

        if magnet != "" :
            cuts["magnet"] = magnet 
            cutnames.append("magnet")

        if CC != "" :
            cuts["CC"] = CC 
            cutnames.append("CC")"""

        runOpts = {
            "optics":{},
            #emittance = {}
            #momentum = {} 
            "absorber":{},
            "magnet":{},
            "CC":{},
            "GeometryID":{}
        }
        for key in runOpts.keys():
            cutnames.append(key)

    except BaseException as ex:
      raise
    else :

     for f1 in inFile :
      f = open(f1, 'r')
      noruns = True

      for line in f :
        Used = True
        inp = {}
        #settings = line.split("|")
        settings = line.replace(" ", "").split("|")

        inp["run"] = str(settings[0]).rjust(5, "0")
        #geof = open(Geomdir+"runnumber_"+run+"/Maus_Information.gdml", 'r')
        try : 
         with open(Geomdir+"runnumber_"+inp["run"]+"/Maus_Information.gdml") as geof:
          geofile = geof.readlines()
          for geoline in geofile:
            m = re.search('<GeometryID value="(.+?)">', geoline)
            if m:
              inp["GeometryID"] = m.group(1)
              break
            #else:
            #  inp["GeometryID"] = "null"
        except BaseException as ex:
          inp["GeometryID"] = "null"
           

        inp["optics"] = settings[3]
        if settings[3].find("+") != -1:
            inp["momentum"] = settings[3].split("+",1)[0]
            if inp["momentum"].find("-") != -1:
                inp["momentum"] = inp["momentum"].split("-",1)[1]
        else:
            inp["momentum"] = ""
        if settings[3].find("+") != -1:
            inp["emittance"] = settings[3].split("+",1)[0]
            if inp["emittance"].find("-") != -1:
                inp["emittance"] = inp["emittance"].split("-",1)[0]
        else:
            inp["emittance"] = ""
        inp["CC"] = settings[4]
        inp["magnet"] = settings[5]
        inp["absorber"] = settings[6]

        for cut in cutnames : 
          for key in runOpts[cut].keys() :
            if key != inp[cut] :
              Used = False 
        if not Used :
          for key in runOpts.keys():
            runOpts[key].append(inp[key])


        print line
        print inp["GeometryID"]
        #outname = dest+"/"+"sorted"+inp["GeometryID"]+"_"+inp["absorber"]+"-"+inp["optics"]+inp["emittance"]+inp["momentum"]+inp["magnet"]+inp["CC"]+".txt"
        outname = dest+"/"+"sorted"+inp["GeometryID"]+"_"+inp["absorber"]+"-"+inp["optics"]+inp["magnet"]+inp["CC"]+".txt"
        newf = open(outname, "a+")
        newf.write(line)
        noruns = False
        newf.close()

      f.close()
      if noruns: 
        os.remove(outname)
