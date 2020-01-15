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

# Tipo de render: "surface" o "wireframe"
tipo_de_render = "wireframe"

# Tipo de partículas: gamma, e+ ó e-
tipo_de_particulas = "gamma"

# Número de partículas en el haz
numero_de_particulas = 20

# Energía de las particulas (en MeV)
energia_de_las_particulas = 100

# Grosor del fantoma (en cm)
grosor_del_fantoma = 30

# Material del fantoma
# La lista de materiales la tienes en el enunciado
# http://geant4.cern.ch/geant4/UserDocumentation/UsersGuides/ForApplicationDeveloper/BackupVersions/V9.4/html/apas09.html
# Aquí tienes algunos: G4_Al, G4_Si, G4_Ar, G4_Cu, G4_Fe, G4_Ge, G4_Ag, G4_W, G4_Au, G4_Pb, G4_AIR, G4_Galactic, G4_WATER H_2O, G4_CESIUM_IODIDE, G4_SODIUM_IODIDE, G4_PLASTIC_SC_VINYLTOLUENE, G4_MYLAR
material_del_fantoma = "G4_Pb"
material_del_fantoma = "G4_WATER"
#material_del_fantoma = "G4_Cu"

# Colores de las trazas para que las puedas seguir en el diagrama 3D
color_electrones = "red"
color_positrones = "blue"
color_fotones = "white"
color_protones = "blue"

rand_engine = Ranlux64Engine()
HepRandom.setTheEngine(rand_engine)
HepRandom.setTheSeed(20050830L)

g4py.NISTmaterials.Construct()
g4py.ezgeom.Construct()  
g4py.EMSTDpl.Construct()
g4py.ParticleGun.Construct()

# El espacio hasta llegar al fantoma, supongamos que es aire, pero también
# puedes simular que es el vacío intergaláctico con "G4_Galactic"
air = G4Material.GetMaterial("G4_AIR")
vacio = G4Material.GetMaterial("G4_Galactic")
#g4py.ezgeom.SetWorldMaterial(air)
g4py.ezgeom.SetWorldMaterial(vacio)
g4py.ezgeom.ResizeWorld(121.*cm, 121.*cm, 400.*cm)

# Definimos un fantoma y lo situamos en la escena
phantom_material = G4Material.GetMaterial(material_del_fantoma)
phantom = G4EzVolume("PhantomBox")
phantom_zwidth = grosor_del_fantoma*cm
phantom_zlocation = 100.*cm
phantom.CreateBoxVolume(phantom_material, 120.0 * cm, 120.0 * cm, phantom_zwidth)
phantom.SetColor(0., 0.9, 1.0)
phantom_box_pv = phantom.PlaceIt(G4ThreeVector(0.*cm, 0.*cm, phantom_zlocation))

# Creamos un haz de partículas y lo dirigimos contra el fantoma
beam = g4py.MedicalBeam.Construct()
beam.particle = tipo_de_particulas
beam.kineticE = energia_de_las_particulas*MeV
beam.sourcePosition = G4ThreeVector(0.*cm, 0.*cm, -90.*cm)
beam.fieldXY = [120.*cm, 120.*cm]
beam.SSD = 190.*cm

# http://geant4.slac.stanford.edu/Presentations/vis/G4VisCommands.pdf
# http://geant4.slac.stanford.edu/Presentations/vis/G4VisAdvanced.pdf

# Los siguientes comandos son para generar la escena en un fichero VRML
gApplyUICommand("/run/initialize")
gApplyUICommand("/vis/viewer/flush")
gApplyUICommand("/vis/open VRML2FILE")
gApplyUICommand("/vis/viewer/refresh")
gApplyUICommand("/vis/scene/create")
gApplyUICommand("/vis/scene/add/volume")
gApplyUICommand("/vis/drawVolume")
gApplyUICommand("/vis/modeling/trajectories/create/drawByParticleID")
gApplyUICommand("/vis/modeling/trajectories/drawByParticleID-0/set gamma " + color_fotones)
gApplyUICommand("/vis/modeling/trajectories/drawByParticleID-0/set proton " + color_protones) 
gApplyUICommand("/vis/modeling/trajectories/drawByParticleID-0/set e- " + color_electrones) 
gApplyUICommand("/vis/modeling/trajectories/drawByParticleID-0/set e+ " + color_positrones) 
gApplyUICommand("/vis/sceneHandler/attach")
gApplyUICommand("/vis/viewer/set/style " + tipo_de_render)
gApplyUICommand("/vis/viewer/set/viewpointThetaPhi 70. 10.")
gApplyUICommand("/vis/viewer/zoom 1.")
gApplyUICommand("/tracking/storeTrajectory 1")
gApplyUICommand("/vis/scene/add/trajectories")
gApplyUICommand("/vis/scene/add/hits")
gApplyUICommand("/vis/scene/add/trajectories smooth")
gApplyUICommand("/vis/scene/endOfEventAction accumulate")
gRunManager.Initialize()
gRunManager.BeamOn(numero_de_particulas)
os.rename("g4_00.wrl", "simulacion.wrl")