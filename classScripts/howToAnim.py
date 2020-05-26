import maya.cmds as cmds
import pymel.core as pm
import sys
import os
import anim
reload(anim)
source = anim.AnimCopy()

source.copyAnim(
            filename = r"C:\Users\sgood\Documents\maya\projects\default\data",
            capture = "*_CTRL",
            locName = "a02_LOC"
            )

source.pasteAnimPlusRename(
            filename = r"C:\Users\sgood\Documents\maya\projects\default\data",
            locName = "roboto_LOC",
            version = "_vA_"
            )
source.pasteAnim(
            filename = r"C:\Users\sgood\Documents\maya\projects\default\data",
            locName = "a02_LOC",
            version = "_vB_"
            )

# import characters                        
pathA = r"Q:\17148_Atomu\02_asset\publish\rigs\wacici"            
pathB = r"Q:\17148_Atomu\02_asset\publish\rigs\limo"
rigVersionA = "\\wacici_sgRig_A.ma"   
rigVersionB = "\\wacici_sgRig_B.ma"         
def loadRig(pathA, rigVersion):
    cmds.file(pathA + rigVersion, r=True, dns=True, f=True)    
loadRig(pathA, rigVersionA)
loadRig(pathA, rigVersionB)