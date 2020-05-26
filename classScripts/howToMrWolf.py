"""
fixing bad geo from Adreas Hoppen to enable auto Rigging.

copy mrWolf Script into  - C:\Users\yourName\Documents\maya\scripts
"""

#=========================================================
# import code
#=========================================================
import pymel.core as pm
import fixMe
reload(fixMe)
char = fixMe.MrWolf()

#=========================================================
# run code on character example 1
#=========================================================
char.makeItSo(
        inPath = r"Q:\17144_MRMC_Sports\02_asset\character\Linda_Telek\take03\01_mesh\01_wip\pre_export",
        name = r"\Linda_Talek",
        ext = ".fbx",
        outPath = r"Q:\17144_MRMC_Sports\02_asset\character\Linda_Telek\take03\01_mesh\01_wip/pre_export\\"
        )

#=========================================================
# run code on character example 2
#=========================================================     
char.makeItSo(
        inPath = r"Q:\17144_MRMC_Sports\02_asset\character\Dipesh_Gurung\take03\02_publish\v02",
        name = r"\Dipesh_Gurung",
        ext = ".fbx",
        outPath = r"Q:\17144_MRMC_Sports\02_asset\character\Dipesh_Gurung\take03\02_publish\v02\\"
        )