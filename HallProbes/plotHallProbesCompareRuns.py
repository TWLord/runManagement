import sys
import os
import argparse
import math
import datetime
import matplotlib
matplotlib.use('pdf') # for non-interactive back-end
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

def runComparePlotter(ManyArgs, inFiles) : 

 for f1 in inFiles :
   sublist = []
   sublist = [i for i in inFiles if str(i.split("/")[-1]) in f1 and i not in sublist] 
   #sublist.append(sublist[0].replace("SSD","SSU"))
   print "plotting for hall probes : "
   print [i for i in sublist]

   datagood = []
   databad = []
   badplots = 0

    #for f1 in inFiles :
   for f1 in sublist :
    fig, (legendU, SSU, SSD, legendD) = plt.subplots(1, 4, gridspec_kw={"width_ratios":[1,4,4,1]})
    fig.set_figheight(4.8)
    fig.set_figwidth(12.8)
    dest = ManyArgs[ManyArgs.keys()[0]]["dest"]
    outname = dest+"plot"+f1.split("/")[-1].replace(":","-")+"fields"

    #for f1 in sublist :
    for key in ManyArgs.keys() :
     run = key
     #if run is not "9906" :
     #  continue
     Args = ManyArgs[key]
     # Makes code slow, but maybe who cares?
     exec ""
     # Remove it and change Args updates if this becomes problematic
     locals().update(Args)

     #fig.set_figheight(12.8)
     #fig.set_figwidth(36.8)

     #outname = dest+"plot"+(daystart+","+timestart+"to"+dayend+","+timeend).replace("/","_")
     #if run :
     #outname = dest+"plot"+inFile
     #newf = open(outname, "w+")

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

     #if len(field) :
     if len(x) :
        #field = [(val-field[-1]) for val in field] 
        x = [(val-x[0]).total_seconds() for val in x] 
        print "found values in : " + str(f1) + " for run " + run
     else :
        print "no value found in : " + str(f1) + " for run " + run
        
     if len(x) :
      if len(datagood) :
        if ( abs(field[-1] - datagood[-1]) < abs(datagood[-1]*0.05) and
            abs(field[0] - datagood[0]) < abs(datagood[0]*0.05) and
            abs(field[0] - field[-1]) < abs(datagood[0]*0.005) ) : 
          SSU.plot(x, field, label = run)
          if run :
            print run
            print f1.split("/")[-1]
            print x[-1]
            print field[-1]
            #SSU.text(x[-1], field[-1], f1.split("/")[-1])
        else : 
          SSD.plot(x, field, label = run+" : "+str(x[-1])+" seconds")
          badplots += 1
          fig2, (badplot, badlegend) = plt.subplots(1, 2, gridspec_kw={"width_ratios":[4,1]})
          fig2.set_figheight(4.8)
          fig2.set_figwidth(12.8)
          badplot.plot(x, field, label = run+" : "+str(x[-1])+" seconds")
          hb,lb = badplot.get_legend_handles_labels()
          parsedlb = badlegend.legend(hb,lb, bbox_to_anchor=(1.0,1.02), loc="upper left", borderaxespad=0)
          badlegend.axis("off")
          badplot.set_title("Fields Between Runs - Disagree")
          fig2.suptitle("Probe "+sublist[0].split("/")[-1])
          plt.tight_layout()
          fig2.savefig(outname+"bad"+str(badplots)+".png", bbox_extra_artists=[parsedlb], bbox_inches='tight' )
          plt.close(fig2)

          if run :
            print run
            print f1.split("/")[-1]
            print x[-1]
            print field[-1]
            #SSD.text(x[-1], field[-1], f1.split("/")[-1])
      else : 
        datagood.append(field[-1])

   #fig.set_title("Field over time")
   SSU.set_title("Field Across Runs")
   SSD.set_title("Field Across Runs")
   if True : 
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
      #fig.suptitle("Magnet "+f1.split("/")[-1])
      fig.suptitle("Probe "+sublist[0].split("/")[-1])
   plt.tight_layout()
   #plt.show()
   fig.savefig(outname+".png", bbox_extra_artists=(l1,l2), bbox_inches='tight' )
   #fig.close()
   plt.close()

   #newf.close()
    #if noruns: 
    #  os.remove(outname)

if __name__ == "__main__":

  runwithArgs = False
  rf = "/home/phumhf/MICE/runManagement/sortedsolenoidbyCC/sorted-solenoid2017-02-6/sorted2*ABS*solenoid2017-02-6.txt"
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
    #for i in inFile :
    #ManyArgs = pullArgs(runFile, {i})
    runComparePlotter(ManyArgs, inFile)
  
