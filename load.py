from __future__ import print_function

import glob
import os
import sys
import time
import webbrowser
from time import gmtime

import Tkinter as tk
import myNotebook as nb
from config import config

import jsonlines

journal_dir = config.get('journaldir') or config.default_journal_dir
out_dir = config.get('outdir') or config.default_out_dir
outfilename = 'all_' + time.strftime("%Y-%m-%d" + "T" + "%H-%M-%S" + "Z", gmtime()) + ".csv"
jdir = os.path.join(journal_dir + "\\Journal.*.log")
this = sys.modules[__name__]	# For holding module globals

## Initial table layout for non-list objects. Might ultimately use this or similar
## or perhaps include multiple layout options

# table_objects = (
#     "timestamp",
#     "BodyName",
#     "event",
#     "DistanceFromArrivalLS",
#     "StarType",
#     "StellarMass",
#     "AbsoluteMagnitude",
#     "Age_MY",
#     "Luminosity",
#     "Radius",
#     "RotationPeriod",
#     "SurfaceTemperature",
#     "TidalLock",
#     "TerraformState",
#     "PlanetClass",
#     "Volcanism",
#     "SurfaceGravity",
#     "SurfacePressure",
#     "Landable",
#     "MassEM",
#     "SemiMajorAxis",
#     "Eccentricity",
#     "OrbitalInclination",
#     "Periapsis",
#     "OrbitalPeriod",
#     "AxialTilt",
#     "Atmosphere"
# )
table_objectsEDD1 = (
    "timestamp",
    "BodyName",
    "event",
    "DistanceFromArrivalLS",
    "StarType",
    "StellarMass",
    "AbsoluteMagnitude",
    "Age_MY",
    "Luminosity",
    "Radius",
    "RotationPeriod",
    "SurfaceTemperature",
    "TidalLock",
    "TerraformState",
    "PlanetClass",
    "Atmosphere"
)
table_objectsEDD2 = (
    "Volcanism",
    "SurfaceGravity",
    "SurfacePressure",
    "Landable",
    "MassEM",
    "SemiMajorAxis",
    "Eccentricity",
    "OrbitalInclination",
    "Periapsis",
    "OrbitalPeriod",
    "AxialTilt"
)
table_atmosphere = (
    "Iron",
    "Silicates",
    "SulphurDioxide",
    "CarbonDioxide",
    "Nitrogen",
    "Oxygen",
    "Water",
    "Argon",
    "Ammonia",
    "Methane",
    "Hydrogen",
    "Helium"
)
table_materials = (
    "carbon",
    "iron",
    "nickel",
    "phosphorus",
    "sulphur",
    "arsenic",
    "chromium",
    "germanium",
    "manganese",
    "selenium",
    "vanadium",
    "zinc",
    "zirconium",
    "cadmium",
    "mercury",
    "molybdenum",
    "niobium",
    "tin",
    "tungsten",
    "antimony",
    "polonium",
    "ruthenium",
    "technetium",
    "tellurium",
    "yttrium"
)
table_rings = (
    "Rings/0/Name",
    "Rings/0/RingClass",
    "Rings/0/MassMT",
    "Rings/0/InnerRad",
    "Rings/0/OuterRad",
    "Rings/1/Name",
    "Rings/1/RingClass",
    "Rings/1/MassMT",
    "Rings/1/InnerRad",
    "Rings/1/OuterRad",
    "Rings/2/Name",
    "Rings/2/RingClass",
    "Rings/2/MassMT",
    "Rings/2/InnerRad",
    "Rings/2/OuterRad",
    "ReserveLevel"
)

def plugin_start():
   """
   Load this plugin into EDMC
   """
   print("I am loaded!")
   return "EDDx"

def openGithub(event):
    webbrowser.open_new(r"https://github.com/CmdrTaen/EDDx")

def plugin_prefs(parent, cmdr, is_beta):
   """
   Return a TK Frame for adding to the EDMC settings dialog.
   """
   this.mysetting = tk.IntVar(value=config.getint("MyPluginSetting"))	# Retrieve saved value from config
   frame = nb.Frame(parent)
   frameMain = nb.Frame(frame)
   frameMain.grid(row=0, column=0, sticky=tk.W)
   frameBottom = nb.Frame(frame)
   frameBottom.grid(row=1, column=0, sticky=tk.SW)

   # this.emptyFrame = nb.Frame(frame)
   nb.Label(frameMain, text="").grid(row=0, column=0,sticky=tk.W)
   nb.Label(frameMain, text="Journal Dir: ").grid(row=1, column=0,sticky=tk.W)
   nb.Label(frameMain, text=journal_dir).grid(row=1, column=1,sticky=tk.W)
   nb.Label(frameMain, text="Save Dir: ").grid(row=2, column=0,sticky=tk.W)
   nb.Label(frameMain, text=out_dir).grid(row=2, column=1,sticky=tk.W)
   nb.Label(frameMain, text="").grid(row=3, column=0,sticky=tk.W)
   exButt = nb.Button(frameMain, text="Export Scans",width=20)
   exButt.grid(row=4, column=1,rowspan=3,columnspan=2,sticky=tk.W)
   exButt.config(width=50,command=journal_export)
   nb.Label(frameMain, text="\nCreates a CSV file of all journals regardless of cmdr.").grid(row=7,column=1,columnspan=2,sticky=tk.W)
   nb.Label(frameMain, text="The layout mimics the output and order that ").grid(column=1,columnspan=2,sticky=tk.W)
   nb.Label(frameMain, text="EDDiscovery produces, (since some tools depend on that)").grid(column=1,columnspan=2,sticky=tk.W)
   nb.Label(frameMain, text="but also includes all planetary and stellar ring data.").grid(column=1,columnspan=2,sticky=tk.W)
   nb.Label(frameMain).grid(row=11)  # spacer
   nb.Label(frameMain, text="Need this to output something that it isn't? Click on the ").grid(row=12,column=1,columnspan=2,sticky=tk.W)  # spacer
   nb.Label(frameMain, text="Github link below.").grid(column=1,columnspan=2,sticky=tk.W)  # spacer

   nb.Label(frameBottom).grid(row=0)  # spacer
   nb.Label(frameBottom, text="EDDx was created by Cmdr. Taen who kn(ew|ows) basically nothing about programming.").grid(row=1,columnspan=3,sticky=tk.SW)
   nb.Label(frameBottom, text="Last Updated: 2018-01-12 -- Version 1.0").grid(row=3,columnspan=3,sticky=tk.SW)
   nb.Label(frameBottom).grid(row=2)  # spacer
   link = nb.Label(frameBottom, text="Open the Github page for this plugin", fg="blue", cursor="hand2")
   link.grid(row=5, column=0, sticky=tk.W)
   link.bind("<Button-1>", openGithub)
   return frame

# def prefs_changed(cmdr, is_beta):
#    """
#    Save settings.
#    """
#    config.set('MyPluginSetting', this.mysetting.getint())


def journal_export():

    alltab = table_objectsEDD1 + table_atmosphere + table_objectsEDD2 + table_materials + table_rings
    with open(os.path.join(out_dir, outfilename), 'wb') as outfile:
        print(*alltab, sep=',', file=outfile)
        for filename in glob.glob(jdir):
            if filename == outfilename:
                # don't want to copy the output into the output
                continue
            with jsonlines.open(filename) as reader:
                for line in reader.iter(type=dict,skip_invalid=True):
                    if line.get("event", None) == "Scan":
                        dict_objects = {}
                        matvalues = list()
                        ringvalues = list()
                        atmosvalues = list()
                        objectvalues1 = list()
                        objectvalues2 = list()
                        remainder = list()
                        if isinstance(line, dict):
                            for getkeys in line.keys():
                                if getkeys != "Materials" and getkeys != "Rings" and getkeys != "AtmosphereComposition":
                                    dict_objects[getkeys] = line.get(getkeys)
                                if getkeys == "Materials":
                                    matkeys = line.get(getkeys)
                                    ## Collect the materials as they were recorded in the journals prior to
                                    ## 2017-04-11 (2.2 release? Or was it 2.3??)
                                    if isinstance(line.get(getkeys), dict):
                                        for key2 in table_materials:
                                            if key2 not in matkeys:
                                                matvalues.append("")
                                            else:
                                                value = str(matkeys[key2])
                                                matvalues.append(value)
                                    elif isinstance(line.get(getkeys), list):
                                        materials = list(table_materials)
                                        for i in range(len(list(table_materials))):
                                            for j in range(len(list(matkeys))):
                                                if materials[i] == matkeys[j]['Name']:
                                                    matvalues.append(matkeys[j]['Percent'])
                                                    mathelper = matkeys[j]['Name']
                                            if materials[i] != mathelper:
                                                matvalues.append("")
                                elif isinstance(line.get(getkeys), list):
                                    ## Yes, this isn't terrible elegant. I'll improve this as
                                    ## I get better at working in Python.
                                    ringkeys = line.get(getkeys)
                                    if getkeys == "Rings":
                                        for j in ringkeys:
                                            ## Getting these things in the correct order in 2.7 was... fun.
                                            ## # In 3.6 it was a single line of code.
                                            ringname = j['Name'].encode("ascii")
                                            ringvalues.append(ringname)
                                            ringclass = j['RingClass'].encode("ascii")
                                            ringvalues.append(ringclass)
                                            ringvalues.append(j['MassMT'])
                                            ringvalues.append(j['InnerRad'])
                                            ringvalues.append(j['OuterRad'])
                                    elif getkeys == "AtmosphereComposition":
                                        atmokeys = line.get(getkeys)
                                        atmosphere = list(table_atmosphere)
                                        atmocount = 0
                                        for i in range(len(list(table_atmosphere))):
                                            if atmosphere[i] == atmokeys[atmocount]['Name']:
                                                atmosvalues.append(atmokeys[atmocount]['Percent'])
                                                if len(list(atmokeys)) == 1:
                                                    atmocount = atmocount
                                                elif len(list(atmokeys)) == atmocount + 1:
                                                    atmocount = atmocount
                                                else:
                                                    atmocount = atmocount + 1
                                            else:
                                                atmosvalues.append("")
                                else:
                                    remainder.append(line.get(getkeys))

                        # Check if the object lacks atmosphere, materials, or rings
                        #  and fill in the blanks
                        if atmosvalues == []:
                            for key2 in table_atmosphere:
                                if key2 not in atmosvalues:
                                    atmosvalues.append("")
                        if matvalues == []:
                            for key2 in table_materials:
                                if key2 not in matvalues:
                                    matvalues.append("")
                        for key2 in table_rings:
                            if key2 not in ringvalues:
                                ringvalues.append("")

                        # Get the object values and place them in the correct location
                        # unless they don't exist, in which case fillin the blanks
                        objects = dict_objects
                        for objkey in table_objectsEDD1:
                            if objkey not in objects:
                                objectvalues1.append("")
                            else:
                                objvalue = str(objects[objkey])
                                objectvalues1.append(objvalue)
                        for objkey in table_objectsEDD2:
                            if objkey not in objects:
                                objectvalues2.append("")
                            else:
                                objvalue = str(objects[objkey])
                                objectvalues2.append(objvalue)
                        # Print out the rows of data
                        allval = objectvalues1 + atmosvalues + objectvalues2 + matvalues + ringvalues
                        #
                        print(*allval, sep=',', file=outfile)

                        ## Keeping this line for simple testing.
                        # print(*allval,sep=',')
                    outfile.closed
