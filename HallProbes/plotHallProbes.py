import sys
import os
import argparse
import math
import datetime
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import glob

# Globals

def getArgs() :
    parser = argparse.ArgumentParser( description="runScript" )

    parser.add_argument( 'hallprobeFile', nargs='+', help='txt file(s) '+\
                                            'containing run information')

    parser.add_argument( '--optics', type=str, default="", help='Select by optics' )

    parser.add_argument( '--momentum', type=str, default="", help='Select by momentum' )

    parser.add_argument( '--emittance', type=str, default="", help='Select by emittance' )

    parser.add_argument( '--absorber', type=str, default="", help='Select by absorber' )

    parser.add_argument( '--magnet', type=str, default="", help='Select by magnet mode' )

    parser.add_argument( '--CC', type=str, default="", help='Select by cooling channel' )
    parser.add_argument( '--daystart', type=str, default="", help='Select starting day to plot' )
    parser.add_argument( '--dayend', type=str, default="", help='Select ending day to plot' )
    parser.add_argument( '--timestart', type=str, default="", help='Select starting time to plot' )
    parser.add_argument( '--timeend', type=str, default="", help='Select ending time to plot' )

    parser.add_argument( '--dest', type=str, default="", help='destination path for output file, include trailing /' )
    if len(sys.argv) < 5:
        print "Usage: python plotHallProbes.py --options step4-runs.txt"
        #print "options : --optics .. --momentum .. --absorber .. --magnet .. --CC .. --dest .. "
        print "options : --daystart MM/DD/YYYY.. --dayend .. --timestart .. --timeend .. --CC .. --dest .. "
        sys.exit(1)
    
    try :
        namespace = parser.parse_args()

        inFile = namespace.hallprobeFile

        dest = namespace.dest

        daystart = namespace.daystart
        dayend = namespace.dayend
        timestart = namespace.timestart
        timeend = namespace.timeend

        ds = [int(i) for i in namespace.daystart.split("/") ]
        #daystart = datetime.datetime(ds[0], ds[1], ds[2])
        de = [int(i) for i in namespace.dayend.split("/") ]
        #dayend= datetime.datetime(de[0], de[1], de[2])

        #daystart = datetime.datetime(int(ds[0]), int(ds[1]), int(ds[2]))
        #de = (namespace.dayend.split("/"))
        #dayend= datetime.datetime(int(de[0]), int(de[1]), int(de[2]))
        #dayend = namespace.dayend(namespace.daystart.split("/"))

        ts = [int(float(i)) for i in namespace.timestart.split(":")]
        te = [int(float(i)) for i in namespace.timeend.split(":")]
        #timeend = namespace.timeend

        datetimestart = datetime.datetime(ds[2], ds[0], ds[1], ts[0], ts[1], ts[2])
        datetimeend = datetime.datetime(de[2], de[0], de[1], te[0], te[1], te[2])
        #datetimestart = datetime.datetime(namespace.daystart.split("/"), namespace.timestart.split(":"))
        #datetimeend = namespace.dayend(namespace.daystart.split("/"), namespace.timeend.split(":"))


        optics = namespace.optics
        absorber = namespace.absorber
        magnet = namespace.magnet
        CC = namespace.CC
        momentum = namespace.momentum
        emittance = namespace.emittance

    except BaseException as ex:
      raise
    else :
      Args = {"inFile": inFile, 
              "dest":dest,
              "daystart":daystart,
              "dayend":dayend,
              "timestart":timestart,
              "timeend":timeend,
              "datetimestart":datetimestart,
              "datetimeend":datetimeend
             }
      print "Args parsed"
      return Args


def pullArgs(runFile, inFile) :

    parser = argparse.ArgumentParser( description="runScript" )

    #parser.add_argument( 'hallprobeFile', nargs='+', help='txt file(s) '+\
    #                                        'containing run information')

    parser.add_argument( '--runs', type=str, default="", help='location of run file to guide plotter' )

    parser.add_argument( '--CC', type=str, default="", help='Select by cooling channel' )
    parser.add_argument( '--daystart', type=str, default="", help='Select starting day to plot' )
    parser.add_argument( '--dayend', type=str, default="", help='Select ending day to plot' )
    parser.add_argument( '--timestart', type=str, default="", help='Select starting time to plot' )
    parser.add_argument( '--timeend', type=str, default="", help='Select ending time to plot' )

    parser.add_argument( '--dest', type=str, default="", help='destination path for output file, include trailing /' )
    #if len(sys.argv) < 2:
    #    print "Usage: python plotHallProbes.py --runsrunfile step4-runs.txt"
    #    sys.exit(1)
    
    try :
        namespace = parser.parse_args()

        #inFile = namespace.hallprobeFile

        dest = namespace.dest

        #runFile = namespace.runs

    except BaseException as ex:
      raise
    else :
        ManyArgs = {}
        for f1 in runFile :
          f = open(f1, 'r')

          for line in f :
            if "#" in line : 
              continue
            if not line.strip() :
              continue
            #print "printing.."
            #print line

            info = line.split("|")
            try : 
            #if line:
              run = info[0]
              daystart = info[1].split()[0]
              timestart = info[1].split()[1]
              dayend = info[8].split()[0]
              timeend = info[8].split()[1]

              tmpdate = [int(i) for i in info[1].split()[0].split("-")]
              tmptime = [int(float(i)) for i in info[1].split()[1].split(":")]
              datetimestart = datetime.datetime(tmpdate[0], tmpdate[1], tmpdate[2], tmptime[0], tmptime[1], tmptime[2])

              tmpdate = [int(i) for i in info[8].split()[0].split("-")]
              tmptime = [int(float(i)) for i in info[8].split()[1].split(":")]
              datetimeend = datetime.datetime(tmpdate[0], tmpdate[1], tmpdate[2], tmptime[0], tmptime[1], tmptime[2])

              Args = {"inFile": inFile, 
                      "dest":dest,
                      "daystart":daystart,
                      "dayend":dayend,
                      "timestart":timestart,
                      "timeend":timeend,
                      "datetimestart":datetimestart,
                      "datetimeend":datetimeend
                     }
              ManyArgs[run] = Args
    
            except ValueError: 
                #print "skipped weird type : "
                #print line
                continue

        return ManyArgs

def runPlotter(Args, run = None):

     # Makes code slow, but maybe who cares?
     exec ""
     # Remove it and change Args updates if this becomes problematic
     locals().update(Args)

     fig, (legendU, SSU, SSD, legendD) = plt.subplots(1, 4, gridspec_kw={"width_ratios":[1,4,4,1]})
     fig.set_figheight(4.8)
     fig.set_figwidth(12.8)
     #fig.set_figheight(12.8)
     #fig.set_figwidth(36.8)

     outname = dest+"plot"+(daystart+","+timestart+"to"+dayend+","+timeend).replace("/","_")
     if run :
       outname = dest+"plot"+run+"fields"
     #outname = dest+"plot"+inFile
     #newf = open(outname, "w+")

     for f1 in inFile :
      f = open(f1, 'r')
      noruns = True

      x = []
      day = []
      time = []
      field = []

      for line in f :
        Use = False 
        if "#" in line : 
          continue
        if not line.strip() :
          continue
        #print "printing.."
        #print line

        info = line.split()
        try : 
         adate = [int(float(i)) for i in info[0].split("/")]
         atime = [int(float(i)) for i in info[1].split(":")]
         #adatetime = datetime.datetime(info[0].split("/"), info[1].split(":") )
         adatetime = datetime.datetime(adate[2], adate[0], adate[1], atime[0], atime[1], atime[2])
         afield = float(info[2])
        except ValueError: 
          #print "skipped weird type : "
          #print line
          continue

         #if [type(i) in adate, atime, afield is not int]
         #all(isinstance(x, int) for x in adate, atime, afield)
         #  continue

        if not Use :
          #if adate >= daystart and adate <= dayend and atime >= timestart and atime <= timeend : 
          if adatetime >= datetimestart and adatetime <= datetimeend :
              Use = True
          else : 
            Use = False

        if Use :
          #if adate >= daystart and adate <= dayend and atime >= timestart and atime <= timeend : 
          if adatetime >= datetimestart and adatetime <= datetimeend :

            x.append(adatetime)
            day.append(adate)
            time.append(atime)
            field.append(afield)
          else :
            f.close()
            break

        
      if len(x) :
        if "SSU" in f1 : 
          SSU.plot(x, field, label = f1.split("/")[-1])
          if run :
            print run
            print f1.split("/")[-1]
            print x[-1]
            print field[-1]
            #SSU.text(x[-1], field[-1], f1.split("/")[-1])
        if "SSD" in f1 : 
          SSD.plot(x, field, label = f1.split("/")[-1])
          if run :
            print run
            print f1.split("/")[-1]
            print x[-1]
            print field[-1]
            #SSD.text(x[-1], field[-1], f1.split("/")[-1])

     #fig.set_title("Field over time")
     SSU.set_title("SSU Field")
     SSD.set_title("SSD Field")
     if run : 
       #plt.legend(bbox_to_anchor=(1.04,1), loc="upper left")
       #fig.legend(loc=7)
       hU,lU = SSU.get_legend_handles_labels()
       hD,lD = SSD.get_legend_handles_labels()
       l1 = legendU.legend(hU,lU, bbox_to_anchor=(0.0,1.02), loc="upper right", borderaxespad=0)
       l2 = legendD.legend(hD,lD, bbox_to_anchor=(1.0,1.02), loc="upper left", borderaxespad=0)
       legendU.axis("off")
       legendD.axis("off")
       #SSU.legend()
       #SSD.legend()
       fig.suptitle("Run "+run)
     plt.tight_layout()
     #plt.show()
     fig.savefig(outname+".png", bbox_extra_artists=(l1,l2), bbox_inches='tight' )
     plt.close()

     #newf.close()
      #if noruns: 
      #  os.remove(outname)

if __name__ == "__main__":

  runwithArgs = False
  #rf = "/home/phumhf/MICE/runManagement/sortedsolenoidbyCC/sorted-solenoid2017-02-6/sorted263*ABS*solenoid2017-02-6.txt"
  rf = "/home/phumhf/MICE/runManagement/sortedsolenoidbyCC/sorted-solenoid2017-02-6/sorted264*ABS*6-140*solenoid2017-02-6.txt"
  runFile = [str(i) for i in glob.glob(rf)]
  inF = "/data/mice/phumhf/HallProbes/2017_0*/*:B"
  #inFile = glob.glob(inF)
  print "runs found in file(s) : "
  print [i for i in runFile]
  print "Hall probe readings found in files : "
  inFile = [str(i) for i in glob.glob(inF)]
  print [i for i in inFile]

  if runwithArgs :
    Args = getArgs()
    runPlotter(Args)

  else :
    ManyArgs = pullArgs(runFile, inFile)
    for key in ManyArgs :
        run = key
        Args = ManyArgs[key]
        runPlotter(Args, run)
  
