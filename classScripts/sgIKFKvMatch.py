"""
anim class for copy and pasting animation keys. make sure you use the SaG loader
"""
import maya.cmds as cmds
import pymel.core as pm
import time

class SgIKFKMatch(object):

    def timeTaken(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            func(*args, **kwargs)
            end = time.time()
            print(str(func) + " > Time taken : ", end-start)
            #print("args are : ", args)
            #print("keyword args are : ", kwargs)
        return wrapper

    def originalState(self):
        ikSwitches = ["l_armSwitch_CTRL", "r_armSwitch_CTRL", "l_legSwitch_CTRL", "r_legSwitch_CTRL"]
        originalState = []
        # find out if they are in IK or FK mode and store in a list
        for x in ikSwitches:
            switches = pm.PyNode(x)
            conns = switches.fkIkBlend.get()
            originalState.append(conns)
            # set all conntrols to FK mode for IKFK switch to work
            #switches.fkIkBlend.set(0)
        return originalState

    @timeTaken
    def FKIKMatch(self, a, b):
        sel = pm.ls(a, b)
        if len( sel ) != 2:
            pm.error("Please select two list")
        A = a
        B = b
        orig = pm.getAttr(a + ".fkIkBlend")
        pm.setAttr(a + ".fkIkBlend", 1)
        # get matrix of B and apply it to A
        Bmatrix = pm.xform(B, query=True, worldSpace=True, matrix=True)
        pm.xform(A, worldSpace=True, matrix=Bmatrix)
        pm.setAttr(a + ".fkIkBlend", orig)

    @timeTaken
    def IKFKMatch(self, ik_CTRL, side, version, arm=None, foot=None):
        # do the matching
        if arm:
            orig = pm.getAttr(side + "_armSwitch" + "_v" + version + "_CTRL" + ".fkIkBlend")
            pm.setAttr(side + "_armSwitch" + "_v"  + version + "_CTRL" + ".fkIkBlend", 0)
            # make sure you are in FK mode and use CTRL selection not a GOFF
            shoulder = pm.createNode("joint", name="{0}".format(side) + "_tempShoulder")
            elbow = pm.createNode("joint", name="{0}".format(side) + "_tempElbow")
            wrist = pm.createNode("joint", name="{0}".format(side) + "_tempWrist")
            
            oShoulder = pm.xform("{0}".format(side) + "_shoulder1" + "_v"  + version + "_JNT", query=True, ws=True, matrix=True)
            oElbow = pm.xform("{0}".format(side) + "_elbow1" + "_v"  + version + "_JNT", query=True, ws=True, matrix=True)
            oWrist = pm.xform("{0}".format(side) + "_hand1" + "_v"  + version + "_JNT", query=True, ws=True, matrix=True)
            
            pm.xform(shoulder, ws=True, matrix=oShoulder)
            pm.xform(elbow, ws=True, matrix=oElbow)
            pm.xform(wrist, ws=True, matrix=oWrist)
            
            pm.parent(wrist, elbow)
            pm.parent(elbow,shoulder)
            
            pos = pm.xform("{0}".format(side) + "_armFk_2" + "_v"  + version + "_CTRL", query=True, ws=True, rp=True)
            pm.move("{0}".format(side) + "_armPv" + "_v"  + version + "_CTRL", pos, rpr=True)

            tempWrist1 = pm.xform("{0}".format(side) + "_tempWrist", query=True, ws=True, matrix=True)
            tempWrist2 = pm.xform("{0}".format(side) + "_tempWrist", query=True, ws=True, ro=True)
            pm.xform(ik_CTRL, ws=True, matrix=tempWrist1)
            pm.xform(ik_CTRL, ws=True, ro=tempWrist2)

            pm.setAttr(side + "_armSwitch" + "_v"  + version + "_CTRL" + ".fkIkBlend", orig)

        if foot:
            orig = pm.getAttr(side + "_legSwitch" + "_v"  + version + "_CTRL" + ".fkIkBlend")
            pm.setAttr(side + "_legSwitch" + "_v"  + version + "_CTRL" + ".fkIkBlend", 0)
            hip = pm.createNode("joint", name="{0}".format(side) + "_tempHip")
            knee = pm.createNode("joint", name="{0}".format(side) + "_tempKnee")
            foot = pm.createNode("joint", name="{0}".format(side) + "_tempFoot")

            oHip = pm.xform("{0}".format(side) + "_hip1" + "_v"  + version + "_JNT", query=True, ws=True, matrix=True)
            oKnee = pm.xform("{0}".format(side) + "_knee1" + "_v"  + version + "_JNT", query=True, ws=True, matrix=True)
            oFoot = pm.xform("{0}".format(side) + "_foot1" + "_v"  + version + "_JNT", query=True, ws=True, matrix=True)
            
            pm.xform(hip, ws=True, matrix=oHip)
            pm.xform(knee, ws=True, matrix=oKnee)
            pm.xform(foot, ws=True, matrix=oFoot)
            
            pm.parent(foot, knee)
            pm.parent(knee, hip)

            tempFoot1 = pm.xform("{0}".format(side) + "_tempFoot", query=True, ws=True, matrix=True)
            pm.xform(ik_CTRL, ws=True, matrix=tempFoot1)

            pm.setAttr(side + "_legSwitch" + "_v"  + version + "_CTRL" + ".fkIkBlend", orig)

        try:
            pm.delete(hip, knee, foot)
        except:
            pass
        try:
            pm.delete(shoulder, elbow, wrist)
        except: 
            pass
              

