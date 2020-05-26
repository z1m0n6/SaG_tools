import maya.cmds as cmds
import pymel.core as pm
import sys
import os
import skel
import skelT
import sgWrchHIK
import hikLinks
reload(skel)
reload(skelT)
reload(sgWrchHIK)
reload(hikLinks)

skeleton = skel.BaseSkel()
skeleton.makeItSo(
        inPath = r"D:\sgScripts\project\dave\rig",
        rigVersion = r"\\001_dave_sgRig_v016.ma",
        folder = "targetJoints_GRP"
        )
        
skeletonT = skelT.BaseSkel()
skeletonT.makeItSo(
        inPath = r"D:\sgScripts\project\dave\rig",
        rigVersion = r"\\001_dave_sgRig_v016.ma",
        folder = "animTargetJoints_GRP"
        )
        
wrchRig = sgWrchHIK.WrchHIK()
wrchRig.makeItSo(
        inPath = r"D:\sgScripts\project\dave\rig",
        rigVersion = r"\\001_dave_sgRig_v016.ma",
        jsonPath = r"D:\sgScripts\project\dave\skeleton"
        )
pm.select(clear=True)
hikLinks.link()