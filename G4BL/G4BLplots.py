import io
import os
import sys
import json
import copy
import time
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

template_dict = {
  'x':[],
  'y':[],
  'z':[],
  'px':[],
  'py':[],
  'pz':[]
}

pos_dict = {
  'x':'x',
  'y':'y',
  'z':'z'
}

mom_dict = {
  'x':'px',
  'y':'py',
  'z':'pz'
}

pdg_pid_to_name  = {0:'none', 11:'e-', 12:'electron neutrino', 13:'mu-', 14:'muon neutrino', 22:'photon', 111:'pi0', 211:'pi+', 321:'K+', 2112:'neutron', 2212:'proton', 1000010020:'deuterium', 1000010030:'tritium', 1000020030:'3He', 1000020040:'4He', 130:'K0L', 310:'K0S', 311:'K0', 3122:'lambda',
-11:'e+', -12:'electron antineutrino', -13:'mu+', -14:'muon antineutrino', -211:'pi-', -321:'K-', -2112:'antineutron', -2212:'antiproton', -3122:'antilambda'}


axes_limits = {
  'x':(-250, 250),
  'y':(-100, 100),
  'z':(1025, 1027),
  'px':(-40, 40),
  'py':(-40, 40),
  'pz':(150, 330)

}

def pull_file(filename):
    data_file = open(filename)
    jsdict = json.load(data_file)
    return jsdict


def show_keys(obj):
    print "Keys in dict:"
    for key in obj.keys():
        print key
  
def set_labels(axs1, axs2):
    axs1[0].set_title(r'x Position')
    axs1[0].set_xlabel(r'x [mm]')
    axs1[1].set_title(r'y Position')
    axs1[1].set_xlabel(r'y [mm]')
    axs1[2].set_title(r'z Position')
    axs1[2].set_xlabel(r'z [mm]')
    axs2[0].set_title(r'x Momentum')
    axs2[0].set_xlabel(r'px [MeV/c]')
    axs2[1].set_title(r'y Momentum')
    axs2[1].set_xlabel(r'py [MeV/c]')
    axs2[2].set_title(r'z Momentum')
    axs2[2].set_xlabel(r'pz [MeV/c]')


def get_axes(data_dict, var):
    #print 'var', var
    #print 'datamin:', min(data_dict[var]), 'manual_lim:', axes_limits[var][0]
    #print 'datamax:', max(data_dict[var]), 'manual_lim:', axes_limits[var][1]
    var_low = max(min(data_dict[var]), axes_limits[var][0])
    var_high = min(max(data_dict[var]), axes_limits[var][1])
    #print 'lo, hi:', var_low, var_high
    if var_low > var_high:
        #print "var low > var high"
        #print "returning", min(data_dict[var]), max(data_dict[var])
        return min(data_dict[var]), max(data_dict[var])
    return (var_low, var_high)

def get_axes_pid(data_dict, var):
    var_low = max(min(data_dict[var]), axes_limits[var][0])
    var_high = min(max(data_dict[var]), axes_limits[var][1])
    if var_low > var_high:
        return min(data_dict[var]), max(data_dict[var])
    return (var_low, var_high)


if __name__ == "__main__":
    plt.ioff()
    
    # Official G4BL Chunks
    #G4BL_path = "/data/mice/phumhf/G4BLChunks/Mausv3.3.2"
    #run = "9763"
    #tmpname = "G4BLoutput_10_200M3_Test1v3_"
    #outdir = "G4BLchunks_"+run
    #outfname = "G4BLchunksPIDplot"
    #ownMC = False

    # Own MC prod  
    #/data/mice/phumhf/analMC/09763_v20/0/G4BLoutputsimulation99.json 
    G4BL_path = "/data/mice/phumhf/analMC/"
    run = "09763_v20"
    tmpname = "G4BLoutputsimulation99"
    outdir = "OwnG4BL_"+run
    outfname = "G4BLchunksPIDplot"
    ownMC = True


    if not os.path.exists(outdir):
        os.makedirs(outdir)

    outname = os.path.join(outdir, outfname)

    fig, (axs1, axs2) = plt.subplots(2,3, tight_layout=True)
    fig.set_figheight(12.8)
    fig.set_figwidth(18.8)
    set_labels(axs1, axs2)

    events = 0
    data = {}

    # official MC
    #for i, num in enumerate(range(100, 400)):
    #for i, num in enumerate(range(100, 101)):
    # own MC
    for i, num in enumerate(range(0, 150)):
    #for i, num in enumerate(range(0, 1)):
        print "file", i
        if ownMC:
            try:
                json_dir = os.path.join(G4BL_path, run)
                jsdict = pull_file(os.path.join(json_dir, str(num), tmpname+".json"))
            except:
                continue
        else:
            try:
                json_dir = os.path.join(G4BL_path, run)
                jsdict = pull_file(os.path.join(json_dir, tmpname+str(num)+".json"))
            except:
                continue
        #show_keys(jsdict)
        #print "first entry in mc_events"
        #print jsdict['mc_events'][0] 

        #show_keys(jsdict['mc_events'][0]['primary'])
        #print 'pos', jsdict['mc_events'][0]['primary']['position']
        #print 'mom', jsdict['mc_events'][0]['primary']['momentum']
        print "Adding", len(jsdict['mc_events']), 'mc events'

        for num, event in enumerate(jsdict['mc_events']): 
            # keep track of pid events
            pid = event['primary']['particle_id']
            if pid not in data.keys():
                data[pid] = copy.deepcopy(template_dict)
            events += 1

            # update dicts
            for key in pos_dict.keys():
                data[pid][pos_dict[key]].append(event['primary']['position'][key])
            for key in mom_dict.keys():
                data[pid][mom_dict[key]].append(event['primary']['momentum'][key])

            if events % 100000 == 0:
                print events, 'events added'

                # Update plots as we go 
                #for axs in axs1, axs2:
                #  for ax in axs:
                #    ax.cla()

                #set_labels(axs1, axs2)

                #for pid in data.keys():
                #    if pid in pdg_pid_to_name:
                #        label = pdg_pid_to_name[pid]
                #    else:
                #        label = str(pid)
                #    axs1[0].hist(data[pid]['x'], bins=100, label=label, range=get_axes(data[pid], 'x'))
                #    axs1[1].hist(data[pid]['y'], bins=100, label=label, range=get_axes(data[pid], 'y'))
                #    axs1[2].hist(data[pid]['z'], bins=100, label=label)
                #    axs2[0].hist(data[pid]['px'], bins=100, label=label, range=get_axes(data[pid], 'px'))
                #    axs2[1].hist(data[pid]['py'], bins=100, label=label, range=get_axes(data[pid], 'py'))
                #    axs2[2].hist(data[pid]['pz'], bins=100, label=label, range=get_axes(data[pid], 'pz'))
                #
                #for axs in axs1, axs2:
                #  for ax in axs:
                #    ax.legend()
                #
                #plt.pause(0.5)

    print "DONE analysing ... ", events, 'events'
    print "PRINTING PLOTS ... "

    # Print all plots at the end
    set_labels(axs1, axs2)

    for pid in data.keys():
        if pid in pdg_pid_to_name:
            label = pdg_pid_to_name[pid]
        else:
            label = str(pid)
        axs1[0].hist(data[pid]['x'], bins=100, label=label, range=get_axes(data[pid], 'x'))
        axs1[1].hist(data[pid]['y'], bins=100, label=label, range=get_axes(data[pid], 'y'))
        axs1[2].hist(data[pid]['z'], bins=100, label=label)
        axs2[0].hist(data[pid]['px'], bins=100, label=label, range=get_axes(data[pid], 'px'))
        axs2[1].hist(data[pid]['py'], bins=100, label=label, range=get_axes(data[pid], 'py'))
        axs2[2].hist(data[pid]['pz'], bins=100, label=label, range=get_axes(data[pid], 'pz'))

    for axs in axs1, axs2:
      for ax in axs:
        ax.legend()

    plt.savefig(outname+".png")
    plt.close()

    for pid in data.keys():
        if pid in pdg_pid_to_name:
            label = pdg_pid_to_name[pid]
        else:
            label = str(pid)

        print "printing :", label


        fig, ax = plt.subplots(tight_layout=True)
        fig.set_figheight(6.4) # 12.8)
        fig.set_figwidth(9.4) # 18.8)
        ax.set_title(r'x Position')
        ax.set_xlabel(r'x [mm]')
        hist = ax.hist(data[pid]['x'], bins=100, label=label, range=(get_axes(data[pid], 'x')))
        ax.legend()
        plt.savefig(outname+'_'+label+"_x.png")
        plt.close()

        fig, ax = plt.subplots(tight_layout=True)
        fig.set_figheight(6.4) #(12.8)
        fig.set_figwidth(9.4) # 18.8)
        ax.set_title(r'y Position')
        ax.set_xlabel(r'y [mm]')
        hist = ax.hist(data[pid]['y'], bins=100, label=label, range=(get_axes(data[pid], 'y')))
        ax.legend()
        plt.savefig(outname+'_'+label+"_y.png")
        plt.close()

        fig, ax = plt.subplots(tight_layout=True)
        fig.set_figheight(6.4) #(12.8)
        fig.set_figwidth(9.4) # 18.8)
        ax.set_title(r'z Position')
        ax.set_xlabel(r'z [mm]')
        hist = ax.hist(data[pid]['z'], bins=100, label=label)
        ax.legend()
        plt.savefig(outname+'_'+label+"_z.png")
        plt.close()

        fig, ax = plt.subplots(tight_layout=True)
        fig.set_figheight(6.4) #(12.8)
        fig.set_figwidth(9.4) # 18.8)
        ax.set_title(r'x Momentum')
        ax.set_xlabel(r'px [MeV/c]')
        hist = ax.hist(data[pid]['px'], bins=100, label=label, range=(get_axes(data[pid], 'px')))
        ax.legend()
        plt.savefig(outname+'_'+label+"_px.png")
        plt.close()

        fig, ax = plt.subplots(tight_layout=True)
        fig.set_figheight(6.4) #(12.8)
        fig.set_figwidth(9.4) # 18.8)
        ax.set_title(r'y Momentum')
        ax.set_xlabel(r'py [MeV/c]')
        hist = ax.hist(data[pid]['py'], bins=100, label=label, range=(get_axes(data[pid], 'py')))
        ax.legend()
        plt.savefig(outname+'_'+label+"_py.png")
        plt.close()

        fig, ax = plt.subplots(tight_layout=True)
        fig.set_figheight(6.4) #(12.8)
        fig.set_figwidth(9.4) # 18.8)
        ax.set_title(r'z Momentum')
        ax.set_xlabel(r'pz [MeV/c]')
        hist = ax.hist(data[pid]['pz'], bins=100, label=label, range=(get_axes(data[pid], 'pz')))
        ax.legend()
        plt.savefig(outname+'_'+label+"_pz.png")
        plt.close()

    print "DONE"     
    #plt.show()
        

        
