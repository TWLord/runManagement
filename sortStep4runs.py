import sys
import os
import argparse
import math

if __name__ == "__main__":
    parser = argparse.ArgumentParser( description="runScript" )

    parser.add_argument( 'step4runs', nargs='+', help='txt file(s) '+\
                                            'containing run information')

    parser.add_argument( '--optics', type=str, default="", help='Select by optics' )

    parser.add_argument( '--momentum', type=str, default="", help='Select by momentum' )

    parser.add_argument( '--emittance', type=str, default="", help='Select by emittance' )

    parser.add_argument( '--absorber', type=str, default="", help='Select by absorber' )

    parser.add_argument( '--magnet', type=str, default="", help='Select by magnet mode' )

    parser.add_argument( '--CC', type=str, default="", help='Select by cooling channel' )

    parser.add_argument( '--dest', type=str, default="", help='destination path for output file, include trailing /' )
    if len(sys.argv) < 3:
        print "Usage: python sortStep4runs.py --options step4-runs.txt"
        print "options : --optics .. --momentum .. --absorber .. --magnet .. --CC .. --dest .. "
        sys.exit(1)
    
    try :
        namespace = parser.parse_args()

        inFile = namespace.step4runs

        dest = namespace.dest

        optics = namespace.optics
        absorber = namespace.absorber
        magnet = namespace.magnet
        CC = namespace.CC
        momentum = namespace.momentum
        emittance = namespace.emittance

        cutnames = []

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
            cutnames.append("CC")


    except BaseException as ex:
      raise
    else :

     for f1 in inFile :
      f = open(f1, 'r')
      outname = dest+"sorted"+absorber+"-"+optics+emittance+momentum+magnet+CC+".txt"
      newf = open(outname, "w+")
      noruns = True

      for line in f :
        Use = True 
        inp = {}
        settings = line.split("|")

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
          if cuts[cut] != inp[cut] :
            Use = False
        if Use :
          print line
          newf.write(line)
          noruns = False

      f.close()
      newf.close()
      if noruns: 
        os.remove(outname)
