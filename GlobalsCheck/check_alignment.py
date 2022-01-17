import time
import importlib
import sys
import math
import os

import ROOT

import Configuration
import maus_cpp.globals
import maus_cpp.material
import maus_cpp.field as field # MAUS field map calls

import xboa.common

def initialise_maus():
    configuration = Configuration.Configuration().\
                                          getConfigJSON(command_line_args=True)
    maus_cpp.globals.birth(configuration)

def plot_dir():
    if os.path.exists("./plots/"):
        print "using ./plots"
    else:
        os.makedirs("./plots/")

MATERIAL_LIST = []
def material_to_colour(material):
    global MATERIAL_LIST
    if material[0:3] == "G4_":
        material = material[3:]
    if material not in MATERIAL_LIST:
        MATERIAL_LIST.append(material)
    if material in ("Galactic"):
        return None
    elif material in ("AIR"):
        return ROOT.kYellow
    elif material in ("He"):
        return ROOT.kYellow+1
    if material in ("Fe"): # "kill volumes"
        return 1 # black
    if material in ("MYLAR", "POLYSTYRENE", "NYLON-6-6", "POLYCARBONATE", "POLYVINYL_TOLUENE", "POLYURETHANE", "G10"):
        return 8 # dark green
    if material in ("Al", "ALUMINUM"):
        return ROOT.kOrange # orange/mustard
    if material in ("Zn", "Cu", "W", "TUNGSTEN", "BRASS", "STEEL", "IRON", "TAM1000"):
        return 2 # red
    if material in ("lH2", "MICE_LITHIUM_HYDRIDE", "LITHIUM_HYDRIDE", "TrackerGlue", "TUFNOL"):
        return 4 # blue
    print "UNRECOGNISED MATERIAL", material
    return 1

PRINT_VOLUMES = False # True
THETA = math.pi/4.
def get_material_start_recursive(x, y, z0, z1, mat0, mat1, z_tolerance):
    if abs(z0-z1) < z_tolerance/2.:
        #print "\n\n"
        return z0
    new_z = (z0+z1)/2.
    maus_cpp.material.set_position(x, y, new_z)
    new_material = maus_cpp.material.get_material_data()['name']
    #print "    0:", z0, mat0, "** 1:", z1, mat1, "** new:", new_z, new_material,
    if new_material == mat0:
        z0 = new_z
    else:
        z1 = new_z
    #print " ... ", z0, z1
    return get_material_start_recursive(x, y, z0, z1, mat0, mat1, z_tolerance)

def get_materials(radius, z_start, z_end, z_step, THETA):
    #global PRINT_VOLUMES, THETA
    global PRINT_VOLUMES 
    x = radius*math.cos(THETA)
    y = radius*math.sin(THETA)
    material = None
    volume = None
    material_start = []
    n_steps = int((z_end-z_start)/z_step)
    for i in range(n_steps):
        z = z_step*i+z_start
        maus_cpp.material.set_position(x, y, z)
        material_data = maus_cpp.material.get_material_data()
        new_material = material_data['name']
        new_volume = material_data['volume']
        if new_material != material:
            if material == None:
                z_boundary = z
            else:
                z_boundary = get_material_start_recursive(x, y, z-z_step, z,
                                                       material, new_material,
                                                       1e-6)
            material = new_material
            material_start.append({"x":x, "y":y, "z":z_boundary,
                                   "material":material,
                                   "volume":new_volume})
        if PRINT_VOLUMES and new_volume != volume:
            volume = new_volume
            print (volume+" "+material+" "+str(round(z_boundary, 4))+"  "),
    if PRINT_VOLUMES:
        print
    return material_start

ROOT_GRAPHS = []
def plot_tracker():
  for THETA in [math.pi/4., math.pi/2., 3*math.pi/4., math.pi]:
    global ROOT_GRAPHS, PRINT_VOLUMES
    r_start = 145.
    r_end = 155.
    r_step = 0.1
    z_start = 13800.
    z_end = 15080.
    z_step = 0.1
    n_steps = int((r_end-r_start)/r_step)

    name = "tracker1_"+str(THETA)
    canvas = xboa.common.make_root_canvas(name)
    canvas.SetWindowSize(1900, 1000)
    title = name+" z_step: "+str(z_step)+" r_step: "+str(r_step)
    hist = ROOT.TH2D(name, title+";z [mm]; x [mm]", 1000, z_start, z_end, 1000, r_start, r_end)
    hist.SetStats(False)
    hist.Draw()
    ROOT_GRAPHS.append(hist)

    for i in range(n_steps): # radial steps
        r = r_step*i+r_start
        materials = get_materials(r, z_start,z_end, z_step, THETA)
        #print "At radius", r, "found", len(materials), "materials using", len(ROOT_GRAPHS), "root objects"
        #print "At radius", r, "found", len(materials), "materials"
        for i, material in enumerate(materials):
            if material['material'] == 'G4_Galactic':
                continue
            colour = material_to_colour(material["material"])
            if colour == None:
                continue
            z_min = material["z"]
            if abs(r) > 1e-9:
                radius = (material["x"]**2+material["y"]**2)**0.5*r/abs(r)
            else:
                radius = 0.
            if i+1 >= len(materials):
                z_max = z_end+1
            else:
                z_max = materials[i+1]["z"]
            if i == 0:
                z_min -= 1
            #print material["material"], round(z_min), round(z_max), colour, "   ",
            graph = ROOT.TGraph(2)
            graph.SetPoint(0, z_min, radius)
            graph.SetPoint(1, z_max, radius)
            graph.SetLineColor(colour)
            graph.SetMarkerColor(colour)
            graph.SetMarkerStyle(6)
            graph.SetLineWidth(2)
            graph.Draw("plsame")
            ROOT_GRAPHS.append(graph)
            if i % 10 == 0:
                canvas.Update()
    print

    canvas.Update()
    for format in "png", "eps", "root":
        canvas.Print("./"+name+"."+format)

def check_fields():
    r_start = 0.
    r_end = 20.
    #r_end = 2.
    r_step = 0.05 # 1
    n_steps = int((r_end-r_start)/r_step)

    theta_start = 0.
    theta_end = 2*math.pi
    theta_step = 0.01
    theta_steps = int((theta_end-theta_start)/theta_step)
    #z_start = 13800.
    #z_end = 15080.
    #z_step = 0.1
    print "r_steps:", n_steps, "t_steps:", theta_steps

    tku_offset = -3.
    tkd_offset = 8.
    z_list = [
        (15068.0-1100.+tku_offset, None, "tku_5"),
        (15068.0-750.+tku_offset, None, "tku_4"),
        (15068.0-450.+tku_offset, None, "tku_3"),
        (15068.0-200.+tku_offset, None, "tku_2"),
        (15068.0+tku_offset, None, "tku_tp"),
        (18836.8+tkd_offset, None, "tkd_tp"),
        (18836.8+200.+tkd_offset, None, "tkd_2"),
        (18836.8+450.+tkd_offset, None, "tkd_3"),
        (18836.8+750.+tkd_offset, None, "tkd_4"),
        (18836.8+1100.+tkd_offset, None, "tkd_5"),
    ]

    for z_pos, dummy, name in z_list:
        canvas = xboa.common.make_root_canvas(name)
        canvas.SetWindowSize(1900, 1000)
        #title = name+" z_step: "+str(z_step)+" r_step: "+str(r_step)
        title = name+" r_step: "+str(r_step)+" theta_step: "+str(theta_step)

        #hist = ROOT.TH2D(name, title+";x [mm]; y [mm]", 1000, -r_end, r_end, 1000, -r_end, r_end)
        #hist.SetStats(False)
        #hist.Draw()
        #ROOT_GRAPHS.append(hist)

        point = 0

        graph = ROOT.TGraph2D()
        graph.SetTitle( title+";x [mm]; y [mm]; Bz [T]" )
        ROOT_GRAPHS.append(graph)

        for i in range(n_steps):
            r = r_step*i + r_start
            print 'r:', r
            for j in range(theta_steps):
                theta = theta_step*j + theta_start 
                x_pos = r*math.cos(theta) 
                y_pos = r*math.sin(theta) 
                #graph = ROOT.TGraph2D()#3)
                (bx_field, by_field, bz_field, ex_field, ey_field, ez_field) = \
                                         field.get_field_value(x_pos, y_pos, z_pos, 0.)
                #graph = ROOT.TGraph2D(1)
                bx_field *= 1e3
                by_field *= 1e3
                bz_field *= 1e3

                print point, x_pos, y_pos, bz_field
                graph.SetPoint(point, x_pos, y_pos, bz_field)
                #print point, bx_field, by_field, bz_field
                point += 1

                #graph.Draw("plsame")
                #ROOT_GRAPHS.append(graph)
                #if i % 10 == 0:
                #    canvas.Update()

        #graph.Draw("sameplc")
        #graph.Draw("surf1")
        #canvas.SetTheta(45.)
        #canvas.SetPhi(60.)
        graph.Draw("PCOL Z")
        for format in "png", "pdf", "root":
            canvas.Print("plots/"+name+"."+format)

        canvas.SetTheta(0.)
        canvas.SetPhi(0.)
        canvas.Update()
        for format in "png", "pdf":
            canvas.Print("plots/"+name+"x."+format)
        canvas.SetTheta(0.)
        canvas.SetPhi(90.)
        canvas.Update()
        for format in "png", "pdf":
            canvas.Print("plots/"+name+"y."+format)

        #graph.Draw("PCOL Z")
        #canvas.Update()
        #for format in "png", "pdf", "root":
        #    canvas.Print("plots/"+name+"."+format)
        #for option in ["CONT", "COLZ"]:
        #    graph.Draw(option)
        #    for format in "png", "pdf", "root":
        #        canvas.Print("plots/"+name+"_"+option+"."+format)



if __name__ == "__main__":
    initialise_maus()
    plot_dir()
    #plot_tracker()
    #check_fields()
    check_tracker()


    #--simulation_geometry_filename /storage/epp2/phumhf/MICE/Geometries/runnumber_09883/ParentGeometryFile.dat
