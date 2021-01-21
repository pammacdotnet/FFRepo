#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Geant4
from Geant4 import *
import g4py.NISTmaterials
import g4py.ezgeom
from g4py.ezgeom import G4EzVolume
import g4py.EMSTDpl
import g4py.ParticleGun
import g4py.MedicalBeam
import os.path
import sys 
import getopt

particle_type = "gamma"
particle_count = 20
particle_energy = 1
phantom_thickness = 20
material = "G4_WATER"
wrl_file = "simulation.wrl"

opts, args = getopt.getopt(sys.argv[1:], '', ['type=', 'count=', 'energy=', 'size=', 'material=', 'wrl='])
for opt, arg in opts:
    if opt in ('--type'):
        particle_type = arg
    elif opt in ('--count'):
        particle_count = int(arg)
    elif opt in ('--energy'):
        particle_energy = float(arg)
    elif opt in ('--size'):
        phantom_thickness = int(arg)
    elif opt in ('--material'):
        material = arg
    elif opt in ('--wrl'):
        wrl_file = arg

# Phantom material
electron_color = "red"
positron_color = "yellow"
photon_color = "white"

rand_engine = Ranlux64Engine()
HepRandom.setTheEngine(rand_engine)
HepRandom.setTheSeed(20050830L)
g4py.NISTmaterials.Construct()
g4py.ezgeom.Construct()  
g4py.EMSTDpl.Construct()
g4py.ParticleGun.Construct()

# World definition
emptiness = G4Material.GetMaterial("G4_Galactic")
g4py.ezgeom.SetWorldMaterial(emptiness)
g4py.ezgeom.ResizeWorld(121.*cm, 121.*cm, 400.*cm)

# Phantom definition
phantom_material = G4Material.GetMaterial(material)
phantom = G4EzVolume("PhantomBox")
phantom_zwidth = phantom_thickness*cm
phantom_zlocation = 100.*cm
phantom.CreateBoxVolume(phantom_material, 120.0 * cm, 120.0 * cm, phantom_zwidth)
phantom.SetColor(0., 0.9, 1.0)
phantom_box_pv = phantom.PlaceIt(G4ThreeVector(0.*cm, 0.*cm, phantom_zlocation))

# Beam definition
beam = g4py.MedicalBeam.Construct()
beam.particle = particle_type
beam.kineticE = particle_energy*MeV
beam.sourcePosition = G4ThreeVector(0.*cm, 0.*cm, -90.*cm)
beam.fieldXY = [120.*cm, 120.*cm]
beam.SSD = 190.*cm

# Visualization commands
gApplyUICommand("/run/initialize")
gApplyUICommand("/vis/viewer/flush")
gApplyUICommand("/vis/open VRML2FILE")
gApplyUICommand("/vis/viewer/refresh")
gApplyUICommand("/vis/scene/create")
gApplyUICommand("/vis/scene/add/volume")
gApplyUICommand("/vis/drawVolume")
gApplyUICommand("/vis/modeling/trajectories/create/drawByParticleID")
gApplyUICommand("/vis/modeling/trajectories/drawByParticleID-0/set gamma " + photon_color)
gApplyUICommand("/vis/modeling/trajectories/drawByParticleID-0/set e- " + electron_color) 
gApplyUICommand("/vis/modeling/trajectories/drawByParticleID-0/set e+ " + positron_color) 
gApplyUICommand("/vis/sceneHandler/attach")
gApplyUICommand("/vis/viewer/set/style wireframe")
gApplyUICommand("/vis/viewer/set/viewpointThetaPhi 70. 10.")
gApplyUICommand("/vis/viewer/zoom 1.")
gApplyUICommand("/tracking/storeTrajectory 1")
gApplyUICommand("/vis/scene/add/trajectories")
gApplyUICommand("/vis/scene/add/hits")
gApplyUICommand("/vis/scene/add/trajectories smooth")
gApplyUICommand("/vis/scene/endOfEventAction accumulate")

# Run simulation
gRunManager.Initialize()
gRunManager.BeamOn(particle_count)
os.rename("g4_00.wrl", wrl_file)
