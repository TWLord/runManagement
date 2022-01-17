import ROOT

station_list = []
station_list += ["tku_"+str(i) for i in range(2,6)]
station_list += ["tkd_"+str(i) for i in range(2,6)]
station_list += ["tku_tp", "tkd_tp"]

for station in station_list:
    #rfile = ROOT.TFile("plots/tku_5.root")
    rfile = ROOT.TFile("plots/"+station+".root")
    rfile.ls
    ##c1 = rfile.Get("tku_5-0;1")
    keys = [key.GetName() for key in ROOT.gDirectory.GetListOfKeys()]
    for key in keys:
        if station in key:
            c1_name = key
    c1 = rfile.Get(c1_name)
    for obj in c1.GetListOfPrimitives():
        print obj.GetName()
        if obj.GetName() == "Graph2D":
            g1 = obj
    
    g1.ls()
    g1.Draw()
    g1.GetZmin()
    #ix = ROOT.Int()
    #iy = ROOT.Int()
    #iz = ROOT.Int()
    #ix = ROOT.Long()
    #iy = ROOT.Long()
    #iz = ROOT.Long()
    #g1.GetHistogram().GetMinimumBin(ix,iy,iz)
    
    x = g1.GetX()
    y = g1.GetY()
    z = g1.GetZ()
    
    z_min = 1e9
    index = 0
    N = g1.GetN()
    #for i, val in enumerate(z):
    for i in range(N):
        val = z[i]
        #print i, val
        if val < z_min:
            z_min = val
            index = i
    #print index, z_min
    
    print station, x[index], y[index], z[index]
    #ix = ROOT.Double()
    #iy = ROOT.Double()
    #iz = ROOT.Double()
    #g1.GetPoint(index, ix, iy, iz)
    #print ix, iy, iz
    
    
    
    
    
    #print g1.GetHistogram().GetXaxis().GetBinCenter(ix)
