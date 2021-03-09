import sys
import os
import argparse
import math
import datetime
import matplotlib
matplotlib.use('pdf') # for non-interactive back-end
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import numpy.ma as ma
import glob

plot_dict = {}

def pullArgs(runFiles, magnetList, dest = None, out = None) :
    print "Pulling info from", ', '.join(runFiles)

    if dest == None and out == None:
        parser = argparse.ArgumentParser( description="runScript" )
        parser.add_argument( '--dest', type=str, default="", help='destination path for output file, include trailing /' )
        parser.add_argument( '--o', type=str, default="MagnetResidualPlot", help='output filename' )
        
        try :
            namespace = parser.parse_args()
            dest = namespace.dest
            out = namespace.o
         
        except BaseException as ex:
          raise
          sys.exit()
    else :

        if not os.path.exists(dest):
            os.makedirs(dest)

        ManyArgs = {}
        for f1 in runFiles :
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

              CC = dest.split("/")[-1]

              Args = {#"inFile": inFile, 
                      "output":os.path.join(dest,out),
                      "daystart":daystart,
                      "CC":CC,
                      "dayend":dayend,
                      "timestart":timestart,
                      "timeend":timeend,
                      "datetimestart":datetimestart,
                      "datetimeend":datetimeend,
                      "xLists":{},
                      "yLists":{},
                     }
              # Create empty lists for data
              for magnet in magnetList:
                  Args["xLists"][magnet] = []
                  Args["yLists"][magnet] = []

              ManyArgs[run] = Args
    
            except ValueError: 
                #print "skipped weird type : "
                #print line
                continue

        return ManyArgs


def clearLists(ManyArgs):
     for run in ManyArgs.keys():
         ManyArgs[run]["xLists"] = {}
         ManyArgs[run]["yLists"] = {}


def CheckAllinFiles(runFiles, inDirs, ManyArgs, magnet):
     # runFiles contains files which record all run settings
     # inFiles contains files with all HallProbe measurements
     # ManyArgs contains our pulled info on runs

     print "Finding hall probe measurements for magnet:", magnet

     inFiles = [os.path.join(i,magnet) for i in inDirs]
 
     current_run = None

     for f1 in inFiles :
         f = open(f1, 'r')

         for line in f :
             if "#" in line :
               continue
             if not line.strip() :
               continue

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

             if current_run is not None: 
                 if ManyArgs[current_run]["datetimestart"] < adatetime \
                 and ManyArgs[current_run]["datetimeend"] > adatetime:
                     ManyArgs[current_run]["xLists"][magnet].append(adatetime)
                     ManyArgs[current_run]["yLists"][magnet].append(afield)
                     continue
                 else:
                     current_run = None
                     print "Run number no longer matches with arrow of time. Sounds like a problem."
                     print "Scanning over all runs.."

             for run in ManyArgs.keys(): 
                 if ManyArgs[run]["datetimestart"] < adatetime \
                 and ManyArgs[run]["datetimeend"] > adatetime:
                     ManyArgs[run]["xLists"][magnet].append(adatetime)
                     ManyArgs[run]["yLists"][magnet].append(afield)
                 else:
                     continue
         f.close()

def collateData(ManyArgs, magnet, collatedDict, foundMagnets):
    totalTime = datetime.timedelta(0.)
    totalField = 0.
    totalFieldSq = 0.
    totalEntries = 0
    for run in ManyArgs.keys():
        xList = ManyArgs[run]["xLists"][magnet]
        yList = ManyArgs[run]["yLists"][magnet]
        for i in range(len(xList)):
            if i == 0:
                time = datetime.timedelta(0.)
            else:
                time = xList[i] - xList[i-1]
            field = yList[i]

            totalTime += time
            totalField += field
            totalFieldSq += field*field
            totalEntries += 1

    print "Magnet: ", magnet
    print "totalTime: ", totalTime
    #print "totalField: ", totalField
    print "totalEntries: ", totalEntries
    if totalEntries != 0:
        meanField = totalField/totalEntries
        sqFieldmean = totalFieldSq/totalEntries
        print "mean Field: ", meanField 
        FieldStdDev = sqFieldmean - meanField*meanField
        print "Field Std Dev: ", FieldStdDev

        if meanField < 1e-9 and meanField > -1e-9:
            print "Mean field too small for", magnet, "excluding"
            return

        if magnet not in collatedDict.keys():
            collatedDict[magnet] = {"totalTime":totalTime,
                                      "totalField":totalField,
                                      "totalEntries":totalEntries,
                                      "meanField":meanField,
                                      "fieldStdDev":FieldStdDev,
                                     }
            foundMagnets.append(magnet)
        else:
            print "[ERROR]: Dict already contains data for magnet", magnet



def runPlotter(ManyArgs, magnet, collatedDict):

    magnetList = []
    if type(magnet) == list:
        magnetList = magnet
    else:
        magnetList.append(magnet)


    fig, (legendU, SSU, SSD, legendD) = plt.subplots(1, 4, gridspec_kw={"width_ratios":[1,4,4,1]})
    fig.set_figheight(4.8)
    fig.set_figwidth(12.8)
    SSU.xaxis.set_major_locator(plt.MaxNLocator(4))
    SSD.xaxis.set_major_locator(plt.MaxNLocator(4))
    SSU.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    SSD.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

    figR, (legendUR, SSUR, SSDR, legendDR) = plt.subplots(1, 4, gridspec_kw={"width_ratios":[1,4,4,1]})
    figR.set_figheight(4.8)
    figR.set_figwidth(12.8)
    for plot in [SSUR, SSDR]:
        plot.set_xlabel('Run Number')
        plot.set_ylabel('Hall Probe Deviation From Mean (T)')

    figA = plot_dict["all"]['figure']
    SSUA = plot_dict["all"]['plot_one']
    SSDA = plot_dict["all"]['plot_two']
    legendUA = plot_dict["all"]['legend_one']
    legendDA = plot_dict["all"]['legend_two']
    

    outname = ManyArgs[ManyArgs.keys()[-1]]["output"]
    CC = ManyArgs[ManyArgs.keys()[-1]]["CC"]

    runlist = sorted([int(run) for run in ManyArgs.keys()])
    runlist = [str(run) for run in runlist]

    plots_ok = False
    for magnet in magnetList:
        print "-Plotting runs for magnet:", magnet
        # Set up per magnet plots
        fig2, (legendM, SSM) = plt.subplots(1, 2, gridspec_kw={"width_ratios":[1,4]})
        fig2.set_figheight(4.8)
        fig2.set_figwidth(12.8)
        SSM.xaxis.set_major_locator(plt.MaxNLocator(7))
        SSM.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

        # Set up run x axis plot 
        fig3, (legendR, SSR) = plt.subplots(1, 2, gridspec_kw={"width_ratios":[1,4]})
        fig3.set_figheight(4.8)
        fig3.set_figwidth(12.8)
        #SSR.xaxis.set_major_locator(plt.MaxNLocator(4))
        #SSR.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))


        meanFieldStr = str(round(collatedDict[magnet]["meanField"],5))
        x = []
        runx = []
        field = []
        mask_points = []
        #for run in ManyArgs.keys(): 
        for run in runlist:
            #print "-- Plotting run", run
            #x = ManyArgs[run]["xLists"][magnet]
            #field = [f - collatedDict[magnet]["meanField"] for f in ManyArgs[run]["yLists"][magnet]]
            # Unconverted datetime variable
            x += ManyArgs[run]["xLists"][magnet]
            xlist = ManyArgs[run]["xLists"][magnet]
            runx += [int(run) + float(i)/len(xlist) for i in range(len(xlist))]
            #print "Run x-vals:"
            #print runx
            # Converted datetime
            #x += [matplotlib.dates.date2num(x) for x in ManyArgs[run]["xLists"][magnet]]
            field += [f - collatedDict[magnet]["meanField"] for f in ManyArgs[run]["yLists"][magnet]]
        if len(x):
            # Setup masked array to do linebreaks between runs
            xarr = ma.array(x)

            SSM.plot(xarr, field, label = magnet+", mean field "+meanFieldStr, linestyle='None', marker='o')
            plot_setup(fig2, SSM, legendM, magnet+" Residual Over Runs", outname+magnet) #, magnet+", mean field "+meanFieldStr)
            SSR.plot(runx, field, label = magnet+", mean field "+meanFieldStr, linestyle='None', marker='o')
            plot_setup(fig3, SSR, legendR, magnet+" Residual Over Runs", outname+magnet+'_runs') #, magnet+", mean field "+meanFieldStr)
            if "SSU" in magnet : 
              #SSU.plot(xarr, field, label = magnet+", mean field "+meanFieldStr)
              #SSU.plot(x, field, label = magnet+", mean field "+meanFieldStr)
              SSU.plot(x, field, label = magnet+", mean field "+meanFieldStr, linestyle='None', marker='x')
              SSUR.plot(runx, field, label = magnet+", mean field "+meanFieldStr, linestyle='None', marker='x')
              SSUA.plot(runx, field, label = magnet+", "+CC+", mean field "+meanFieldStr, linestyle='None', marker='x')
              print magnet
            if "SSD" in magnet: 
              #SSD.plot(xarr, field, label = magnet+", mean field "+meanFieldStr)
              SSD.plot(xarr, field, label = magnet+", mean field "+meanFieldStr, linestyle='None', marker='x')
              SSDR.plot(runx, field, label = magnet+", mean field "+meanFieldStr, linestyle='None', marker='x')
              SSDA.plot(runx, field, label = magnet+", "+CC+", mean field "+meanFieldStr, linestyle='None', marker='x')
              print magnet
            plots_ok = True
            
    if plots_ok:
        plot_setup2(fig, SSU, SSD, legendU, legendD, "SSU Field Residual Over Runs", "SSD Field Residual Over Runs", outname) 
        plot_setup2(figR, SSUR, SSDR, legendUR, legendDR, "SSU Field Residual Over Runs", "SSD Field Residual Over Runs", outname+'_runs') 

def plot_setup2(figure, plot_one, plot_two, legend_one, legend_two, title_one, title_two, filename):
        plot_one.set_title(title_one)
        plot_two.set_title(title_two)
        hU,lU = plot_one.get_legend_handles_labels()
        hD,lD = plot_two.get_legend_handles_labels()
        l1 = legend_one.legend(hU,lU, bbox_to_anchor=(0.0,1.02), loc="upper right", borderaxespad=0)
        l2 = legend_two.legend(hD,lD, bbox_to_anchor=(1.0,1.02), loc="upper left", borderaxespad=0)
        legend_one.axis("off")
        legend_two.axis("off")
        plt.tight_layout()
        figure.savefig(filename+".png", bbox_extra_artists=(l1,l2), bbox_inches='tight' )
        plt.close(figure)


def plot_setup(figure, aplot, alegend, title, filename):
    filename = filename.replace(":","-")
    aplot.set_title(title)
    hU,lU = aplot.get_legend_handles_labels()
    l1 = alegend.legend(hU,lU, bbox_to_anchor=(0.0,1.02), loc="upper right", borderaxespad=0)
    alegend.axis("off")
    plt.tight_layout()
    plt.show()
    figure.savefig(filename+".png", bbox_extra_artists=(l1,), bbox_inches='tight' )
    plt.close(figure)


def init_mother_plot():

    fig, (legendU, SSU, SSD, legendD) = plt.subplots(1, 4, gridspec_kw={"width_ratios":[1,4,4,1]})
    fig.set_figheight(4.8)
    fig.set_figwidth(12.8)

    for plot in [SSU, SSD]:
        plot.set_xlabel('Run Number')
        plot.set_ylabel('Hall Probe Deviation From Mean (T)')


    plot_dict["all"] = {'figure':fig,
                        'legend_one':legendU,
                        'legend_two':legendD,
                        'plot_one':SSU,
                        'plot_two':SSD,
                       }

if __name__ == "__main__":

    plot_settings = []

    inDirLoc = "/data/mice/phumhf/HallProbes/20*/"
    #inDirLoc = "/data/mice/phumhf/HallProbes/2017_*/"
    """for direc in glob.glob(inDirLoc):
        #print direc
        dest = direc.split("/")[-2]
        plot_settings.append({"dest":os.path.join("2017-02-5",dest),
                              "rf":"/home/phumhf/MICE/runManagement/solenoidbyCC/sorted-solenoid2017-02-5.txt",
                              "inD":direc,})"""

    #plot_settings.append({"dest":os.path.join("allCycles/","2017-02-6"),
    #                          "rf":"/home/phumhf/MICE/runManagement/cleanedsolenoidbyCC/sorted-solenoid2017-02-6.txt",
    #                          "inD":inDirLoc})

    #CClist = ["2017-02-6", "2017-02-5", "2017-02-2", "2016-05-1", "2016-05-1-SSUSSD", "2016-04-2.4a", "2016-04-1.7", "2016-04-1.5", "2016-04-1.2", "M2D-flip-2017-02-5"]
    #CClist = ["2016-05-1", "2016-05-1-SSUSSD", "2016-04-2.4a", "2016-04-1.7", "2016-04-1.5", "2016-04-1.2", "M2D-flip-2017-02-5"]
    #CClist = ["2017-02-6", "2017-02-5", "2017-02-2",]

    # The bad ones..
    # 2016-05-1 - testing stuff only
    # 2016-05-1-SSUSSD - short usage, no probe data

    # The OK ones.. - still testing 2016-04-2.4a onwards
    CClist = ["2017-02-6", "2017-02-5", "2017-02-2", "2016-04-2.4a", "2016-04-1.7", "2016-04-1.5", "2016-04-1.2", "M2D-flip-2017-02-5"]
    #CClist = ["2017-02-6",]
    for CC in CClist: 
        plot_settings.append({"dest":os.path.join("allCycles/",CC),
                              "rf":"/home/phumhf/MICE/runManagement/cleanedsolenoidbyCC/sorted-solenoid"+CC+".txt",
                              "inD":inDirLoc})


    # fill plot_dict with mother plot
    init_mother_plot()

    for setting in plot_settings:
        dest = setting["dest"]
        rf = setting["rf"]
        inD = setting["inD"]
        CC = dest.split("/")[-1]

        #rf = "/home/phumhf/MICE/runManagement/sortedsolenoidbyCC/sorted-solenoid2017-02-6/sorted2*ABS*solenoid2017-02-6.txt"
        #rf = "/home/phumhf/MICE/runManagement/solenoidbyCC/sorted-solenoid*.txt"
        #rf = "/home/phumhf/MICE/runManagement/solenoidbyCC/sorted-solenoid2017-02-6.txt"
        runFiles = [str(i) for i in glob.glob(rf)]
        print "run file(s) : "
        print [i for i in runFiles]
      

        #magnetListFile = "/home/phumhf/MICE/runManagement/HallProbes/Hall_probes.txt"
        magnetListFile = "/home/phumhf/MICE/runManagement/HallProbes/Hall_probes_edit.txt"
        mf = open(magnetListFile, 'r')
        magnetList = [] 
        for line in mf:
            magnetList.append(line.strip())
        print "Doing magnets:"
        print magnetList
      
        #inD = "/data/mice/phumhf/HallProbes/2017_03/"
        #inD = "/data/mice/phumhf/HallProbes/2017_0*/"
        #inD = "/data/mice/phumhf/HallProbes/20*/"
        print "\nHall probe readings found in folder(s) : "
        inDirs = [str(i) for i in glob.glob(inD)]
        print ',\n'.join(inDirs)
      
        out = "MagnetResidualPlot"
        ManyArgs = pullArgs(runFiles, magnetList, dest, out)
        #ManyArgs = pullArgs(runFiles, magnetList)
        print "Pulled info for", len(ManyArgs.keys()), "runs:"
        print ', '.join(sorted([run for run in ManyArgs.keys()]))
        expectedTotalTime = datetime.timedelta(0.)
        for run in ManyArgs.keys():
            expectedTotalTime += ManyArgs[run]["datetimeend"] - ManyArgs[run]["datetimestart"]
        print "Scanning For Expected Total Run-Time:", expectedTotalTime
       
        collatedDict = {}
        foundMagnets = []
        for magnet in magnetList:
            CheckAllinFiles(runFiles, inDirs, ManyArgs, magnet)
            collateData(ManyArgs, magnet, collatedDict, foundMagnets)
            #runPlotter(ManyArgs, magnet)
        runPlotter(ManyArgs, foundMagnets, collatedDict)
        #runPlotter(ManyArgs, magnetList, collatedDict)
            #clearLists(ManyArgs)

    All = plot_dict['all']
    plot_setup2(All['figure'], All['plot_one'], All['plot_two'], All['legend_one'], All['legend_two'], "SSU Field Residual Over Runs", "SSD Field Residual Over Runs", 'allCycles/'+out+'_all')
