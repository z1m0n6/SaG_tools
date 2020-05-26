"""
buile the eyes
"""

import maya.cmds as cmds
import pymel.core as pm
import maya.OpenMaya as OpenMaya
import time
from rig_lib3 import controls

reload(controls)

def getUParam(pnt = [], crv = None):

    point = OpenMaya.MPoint(pnt[0],pnt[1],pnt[2])
    curveFn = OpenMaya.MFnNurbsCurve(getDagPath(crv))
    paramUtill=OpenMaya.MScriptUtil()
    paramPtr=paramUtill.asDoublePtr()
    isOnCurve = curveFn.isPointOnCurve(point)
    if isOnCurve == True:
        
        curveFn.getParamAtPoint(point , paramPtr,0.001,OpenMaya.MSpace.kObject )
    else :
        point = curveFn.closestPoint(point,paramPtr,0.001,OpenMaya.MSpace.kObject)
        curveFn.getParamAtPoint(point , paramPtr,0.001,OpenMaya.MSpace.kObject )
    
    param = paramUtill.getDouble(paramPtr)  
    return param

def getDagPath(objectName):
    
    if isinstance(objectName, list)==True:
        oNodeList=[]
        for o in objectName:
            selectionList = OpenMaya.MSelectionList()
            print selectionList
            selectionList.add(o)
            oNode = OpenMaya.MDagPath()
            selectionList.getDagPath(0, oNode)
            oNodeList.append(oNode)
        return oNodeList
    else:
        selectionList = OpenMaya.MSelectionList()
        selectionList.add(objectName)
        oNode = OpenMaya.MDagPath()
        selectionList.getDagPath(0, oNode)
        return oNode

class LookAtMe(object):

    def my_decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            func(*args, **kwargs)
            end = time.time()
            print(str(func) + " >>>>>>> Time taken : ", end-start)
        return wrapper

    ##############################################################################################
    # import th eeyball Models
    ##############################################################################################
    @my_decorator
    def getEyeBalls(self):

        l_eyePath = r"E:\sgScripts\project\dave\model\face\faceDressing\l_eye.obj"
        cmds.file(l_eyePath, i=1, dns=1)
        
        r_eyePath = r"E:\sgScripts\project\dave\model\face\faceDressing\r_eye.obj"
        cmds.file(r_eyePath, i=1, dns=1)

    ##############################################################################################
    # place a locator in the centre of each eye
    ##############################################################################################
    @my_decorator
    def locInCentre(self, lcentre, rcentre):
        for num, x in enumerate([lcentre, rcentre]):
            ring = pm.select(x)
            clus = pm.cluster()
            locCentre = pm.spaceLocator(n="eyeCentre_" + "{}".format(num))
            conn = pm.pointConstraint(clus, locCentre)
            pm.delete(conn)
            pm.delete(clus)

    ##############################################################################################
    # create joints from the centre of each eye to each vert around the eye
    ##############################################################################################
    @my_decorator
    def eyeRimJoints(self):
        head = "C_head_low_PLYShape"
        eyeTop0 = [
                    head + ".vtx[2541]",
                    head + ".vtx[2542]",
                    head + ".vtx[2516]",
                    head + ".vtx[2972]",
                    head + ".vtx[2515]",
                    head + ".vtx[2543]",
                    head + ".vtx[3097]",
                    head + ".vtx[2670]",
                    head + ".vtx[2413]",
                    head + ".vtx[2412]",
                    head + ".vtx[2538]",
                    head + ".vtx[2539]",
                    head + ".vtx[2380]",
                    head + ".vtx[2381]"
                    ]

        eyeBot0 = [
                    head + ".vtx[2381]",
                    head + ".vtx[2510]",
                    head + ".vtx[2511]",
                    head + ".vtx[2947]",
                    head + ".vtx[2508]",
                    head + ".vtx[2509]",
                    head + ".vtx[2540]",
                    head + ".vtx[3122]",
                    head + ".vtx[2647]",
                    head + ".vtx[2376]",
                    head + ".vtx[2375]",
                    head + ".vtx[2450]",
                    head + ".vtx[2441]",
                    head + ".vtx[2541]"
                    ]
        eyeTop1 = [
                    head + ".vtx[656]",
                    head + ".vtx[657]",
                    head + ".vtx[688]",
                    head + ".vtx[689]",
                    head + ".vtx[791]",
                    head + ".vtx[792]",
                    head + ".vtx[814]",
                    head + ".vtx[815]",
                    head + ".vtx[817]",
                    head + ".vtx[818]",
                    head + ".vtx[819]",
                    head + ".vtx[946]",
                    head + ".vtx[1248]",
                    head + ".vtx[1373]"
                    ]
        eyeBot1 = [
                    head + ".vtx[651]",
                    head + ".vtx[652]",
                    head + ".vtx[657]",
                    head + ".vtx[717]",
                    head + ".vtx[726]",
                    head + ".vtx[784]",
                    head + ".vtx[785]",
                    head + ".vtx[786]",
                    head + ".vtx[787]",
                    head + ".vtx[816]",
                    head + ".vtx[817]",
                    head + ".vtx[923]",
                    head + ".vtx[1223]",
                    head + ".vtx[1398]"
                    ]

        eyeball = ["eyeCentre_0", "eyeCentre_1"]
        eyelids = [eyeTop0, eyeBot0, eyeTop1, eyeBot1]
        
        for lid in eyelids[0:2]:
            for v in lid:
                pm.select(cl=1)
                old = v.split("_")
                num = old[3].split(".")
                before = lid[0].split("_")
                after = before[3].split(".")
                jnt = pm.joint(n=after[1] + num[1] + "end_JNT")
                pos = pm.xform (v, q=1, ws=1, t=1)
                pm.xform(jnt, ws=1, t=pos)
                posC = pm.xform(eyeball[0], q=1, ws=1, t=1)
                pm.select(cl=1)
                jntC = pm.joint(n=after[1] + num[1] + "start_JNT")
                pm.xform (jntC, ws=1, t=posC)
                pm.parent(jnt, jntC)
                pm.setAttr(jnt + ".radius", .1)
                pm.setAttr(jntC + ".radius", .1)
                #orient joints
                pm.joint (jntC, e=1, oj='xyz', secondaryAxisOrient='yup', ch=1, zso=1)

        for lid in eyelids[2:4]:
            for v in lid:
                pm.select(cl=1)
                old = v.split("_")
                num = old[3].split(".")
                before = lid[0].split("_")
                after = before[3].split(".")
                jnt = pm.joint(n=after[1] + num[1] + "end_JNT")
                pos = pm.xform (v, q=1, ws=1, t=1)
                pm.xform(jnt, ws=1, t=pos)
                posC = pm.xform(eyeball[1], q=1, ws=1, t=1)
                pm.select(cl=1)
                jntC = pm.joint(n=after[1] + num[1] + "start_JNT")
                pm.xform (jntC, ws=1, t=posC)
                pm.parent(jnt, jntC)
                pm.setAttr(jnt + ".radius", .1)
                pm.setAttr(jntC + ".radius", .1)
                #orient joints
                pm.joint (jntC, e=1, oj='xyz', secondaryAxisOrient='yup', ch=1, zso=1)

        jnts1 = pm.ls("vtx_2541*start*", "vtx_2541*end*")
        for x in jnts1:
            oldName = x.split("_")
            newName = "l_uplid_" + oldName[2] + "_" + oldName[3] + "_" + oldName[4] + "_" + oldName[5]
            pm.rename(x, newName)
        jnts2 = pm.ls("l_uplid_*start_JNT")
        pm.group(jnts2, name="l_uplid_GRP")

        jnts3 = pm.ls("vtx_2381*star*", "vtx_2381*end*")
        for x in jnts3:
            oldName = x.split("_")
            newName = "l_downlid_" + oldName[2] + "_" + oldName[3] + "_" + oldName[4] + "_" + oldName[5]
            pm.rename(x, newName)
        jnts4 = pm.ls("l_downlid_*start_JNT")
        pm.group(jnts4, name="l_downlid_GRP")

        jnts5 = pm.ls("vtx_656*start*", "vtx_656*end*")
        for x in jnts5:
            oldName = x.split("_")
            newName = "r_uplid_" + oldName[2] + "_" + oldName[3] + "_" + oldName[4] + "_" + oldName[5]
            pm.rename(x, newName)
        jnts6 = pm.ls("r_uplid_*start_JNT")
        pm.group(jnts6, name="r_uplid_GRP")

        jnts7 = pm.ls("vtx_651*start*", "vtx_651*end*")
        for x in jnts7:
            oldName = x.split("_")
            newName = "r_downlid_" + oldName[2] + "_" + oldName[3] + "_" + oldName[4] + "_" + oldName[5]
            pm.rename(x, newName)
        jnts8 = pm.ls("r_downlid_*start_JNT")
        pm.group(jnts8, name="r_downlid_GRP")

    ##############################################################################################
    # add locators at each vert around the eye and constrain the joints to them
    ##############################################################################################
    @my_decorator
    def eyeRimLocators(self):

        locUpl = pm.spaceLocator(n="l_eyeUpVec_LOC")
        locUpr = pm.spaceLocator(n="r_eyeUpVec_LOC")
        lcenter = pm.xform("eyeCentre_0", q=1, ws=1, t=1)
        pm.xform(locUpl, ws=1, t=lcenter)
        pm.move(locUpl,[0, 3, 0], r=1, os=1, wd=1)
        rcenter = pm.xform("eyeCentre_1", q=1, ws=1, t=1)
        pm.xform(locUpr, ws=1, t=rcenter)
        pm.move(locUpr,[0, 3, 0], r=1, os=1, wd=1)

        locGRP1 = []
        sel = pm.listRelatives("l_uplid_GRP", children=True, type="transform")
        for s in sel:
            x = pm.pickWalk(s, direction="down")
            loc = pm.spaceLocator()
            pm.rename(loc, loc + "_LOC")
            locGRP1.append(loc)
            pm.setAttr(loc + ".scale", .1, .1, .1)
            pos = pm.xform(x, q=1, ws=1, t=1)
            pm.xform(loc, ws=1, t=pos)
            par = pm.listRelatives(x, p=1)[0]
            pm.aimConstraint(loc, par, mo=1, weight=1, aimVector= (1,0,0), upVector = (0,1,0), worldUpType='object', worldUpObject="l_eyeUpVec_LOC")
        pm.group(locGRP1, n="l_uplid_LOC_GRP")

        locGRP2 = []
        sel = pm.listRelatives("l_downlid_GRP", children=True, type="transform")
        for s in sel:
            x = pm.pickWalk(s, direction="down")
            loc = pm.spaceLocator()
            pm.rename(loc, loc + "_LOC")
            locGRP2.append(loc)
            pm.setAttr(loc + ".scale", .1, .1, .1)
            pos = pm.xform(x, q=1, ws=1, t=1)
            pm.xform(loc, ws=1, t=pos)
            par = pm.listRelatives(x, p=1)[0]
            pm.aimConstraint(loc, par, mo=1, weight=1, aimVector= (1,0,0), upVector = (0,1,0), worldUpType='object', worldUpObject="l_eyeUpVec_LOC")
        pm.group(locGRP2, n="l_downlid_LOC_GRP")

        locGRP3 = []
        sel = pm.listRelatives("r_uplid_GRP", children=True, type="transform")
        for s in sel:
            x = pm.pickWalk(s, direction="down")
            loc = pm.spaceLocator()
            pm.rename(loc, loc + "_LOC")
            locGRP3.append(loc)
            pm.setAttr(loc + ".scale", .1, .1, .1)
            pos = pm.xform(x, q=1, ws=1, t=1)
            pm.xform(loc, ws=1, t=pos)
            par = pm.listRelatives(x, p=1)[0]
            pm.aimConstraint(loc, par, mo=1, weight=1, aimVector= (1,0,0), upVector = (0,1,0), worldUpType='object', worldUpObject="r_eyeUpVec_LOC")
        pm.group(locGRP3, n="r_uplid_LOC_GRP")

        locGRP4 = []
        sel = pm.listRelatives("r_downlid_GRP", children=True, type="transform")
        for s in sel:
            x = pm.pickWalk(s, direction="down")
            loc = pm.spaceLocator()
            pm.rename(loc, loc + "_LOC")
            locGRP4.append(loc)
            pm.setAttr(loc + ".scale", .1, .1, .1)
            pos = pm.xform(x, q=1, ws=1, t=1)
            pm.xform(loc, ws=1, t=pos)
            par = pm.listRelatives(x, p=1)[0]
            pm.aimConstraint(loc, par, mo=1, weight=1, aimVector= (1,0,0), upVector = (0,1,0), worldUpType='object', worldUpObject="r_eyeUpVec_LOC")
        pm.group(locGRP4, n="r_downlid_LOC_GRP")

    ##############################################################################################
    # creat a curve along the edge of the eye 
    ##############################################################################################
    @my_decorator
    def lineMeUp(self):
        
        locs = [
                "locator9_LOC", "locator10_LOC", "locator6_LOC", "locator13_LOC", "locator5_LOC",
                "locator11_LOC", "locator14_LOC", "locator12_LOC", "locator4_LOC", "locator3_LOC",
                "locator7_LOC", "locator8_LOC", "locator1_LOC", "locator2_LOC"
                ]
        locs = [pm.xform(loc, q=1, ws=1, translation=1) for loc in locs]
        lupCurve = pm.curve(d=1, p=locs, n="l_up_CURV") 

        locs = [
                "locator25_LOC", "locator22_LOC", "locator23_LOC", "locator21_LOC", "locator27_LOC",
                "locator20_LOC", "locator24_LOC", "locator28_LOC", "locator26_LOC", "locator16_LOC",
                "locator15_LOC", "locator19_LOC", "locator18_LOC", "locator17_LOC"
                ]

        locs = [pm.xform(loc, q=1, ws=1, translation=1) for loc in locs]
        ldownCurve = pm.curve(d=1, p=locs, n="l_down_CURV") 

        locs = [
                "locator37_LOC", "locator38_LOC", "locator34_LOC", "locator41_LOC", "locator33_LOC",
                "locator39_LOC", "locator42_LOC", "locator40_LOC", "locator32_LOC", "locator31_LOC",
                "locator35_LOC", "locator36_LOC", "locator29_LOC", "locator30_LOC"
                ]
        locs = [pm.xform(loc, q=1, ws=1, translation=1) for loc in locs]
        rupCurve = pm.curve(d=1, p=locs, n="r_up_CURV") 

        locs = [
                "locator53_LOC", "locator50_LOC", "locator51_LOC", "locator49_LOC", "locator55_LOC",
                "locator48_LOC", "locator52_LOC", "locator56_LOC", "locator54_LOC", "locator44_LOC",
                "locator43_LOC", "locator47_LOC", "locator46_LOC", "locator45_LOC"
                ]
        locs = [pm.xform(loc, q=1, ws=1, translation=1) for loc in locs]
        rdownCurve = pm.curve(d=1, p=locs, n="r_down_CURV") 

    ##############################################################################################
    # and wire deform the locators with it
    ##############################################################################################

    @my_decorator
    def onAWire1(self, locs, crv):
        locs = pm.listRelatives(locs, children=True, type="transform")
        crv = crv 
        for x in locs:
            pos = pm.xform(x, q=1, ws=1, t=1)
            u = getUParam(pos, crv)
            #create point on curve node. Make sure Locators have suffix of _LOX
            name = x.replace("_LOC", "_PCI")
            pci = pm.createNode("pointOnCurveInfo", n=name)
            pm.connectAttr(crv + ".worldSpace", pci + ".inputCurve")
            pm.setAttr(pci + ".parameter", u)
            pm.connectAttr(pci + ".position", x + ".t")

    @my_decorator
    def onAWire2(self, locs, crv):
        locs = pm.listRelatives(locs, children=True, type="transform")
        crv = crv 
        for x in locs:
            pos = pm.xform(x, q=1, ws=1, t=1)
            u = getUParam(pos, crv)
            #create point on curve node. Make sure Locators have suffix of _LOX
            name = x.replace("_LOC", "_PCI")
            pci = pm.createNode("pointOnCurveInfo", n=name)
            pm.connectAttr(crv + ".worldSpace", pci + ".inputCurve")
            pm.setAttr(pci + ".parameter", u)
            pm.connectAttr(pci + ".position", x + ".t")

    @my_decorator
    def onAWire3(self, locs, crv):
        locs = pm.listRelatives(locs, children=True, type="transform")
        crv = crv 
        for x in locs:
            pos = pm.xform(x, q=1, ws=1, t=1)
            u = getUParam(pos, crv)
            #create point on curve node. Make sure Locators have suffix of _LOX
            name = x.replace("_LOC", "_PCI")
            pci = pm.createNode("pointOnCurveInfo", n=name)
            pm.connectAttr(crv + ".worldSpace", pci + ".inputCurve")
            pm.setAttr(pci + ".parameter", u)
            pm.connectAttr(pci + ".position", x + ".t")

    @my_decorator
    def onAWire4(self, locs, crv):
        locs = pm.listRelatives(locs, children=True, type="transform")
        crv = crv 
        for x in locs:
            pos = pm.xform(x, q=1, ws=1, t=1)
            u = getUParam(pos, crv)
            #create point on curve node. Make sure Locators have suffix of _LOX
            name = x.replace("_LOC", "_PCI")
            pci = pm.createNode("pointOnCurveInfo", n=name)
            pm.connectAttr(crv + ".worldSpace", pci + ".inputCurve")
            pm.setAttr(pci + ".parameter", u)
            pm.connectAttr(pci + ".position", x + ".t")

    ##############################################################################################
    # create low res curve to drive the hiRes curve
    ##############################################################################################

    @my_decorator
    def guideMyEyes(self):
        filePath = r"E:\sgScripts\project\dave\guide\dave_eyelidCTLCurves.ma"
        cmds.file(filePath, i=1, dns=1)

        pm.wire("l_up_CURV", gw=True, en=1.000000, ce=0.000000, li=0.000000, wire="l_low_up_CURV", n="l_top_WIR")
        pm.wire("l_down_CURV", gw=True, en=1.000000, ce=0.000000, li=0.000000, wire="l_low_down_CURV", n="l_bot_WIR")
        pm.wire("r_up_CURV", gw=True, en=1.000000, ce=0.000000, li=0.000000, wire="r_low_up_CURV", n="r_top_WIR")
        pm.wire("r_down_CURV", gw=True, en=1.000000, ce=0.000000, li=0.000000, wire="r_low_down_CURV", n="r_bot_WIR")

    ##############################################################################################
    # add some controls to 
    ##############################################################################################

    @my_decorator
    def controlMyLids(self):

        filePath = r"E:\sgScripts\project\dave\guide\dave_eyelidCTLGuide.ma"
        cmds.file(filePath, i=True, dns=True)

        ctrl = []
        jnts = []
        guides = pm.ls("*_GUIDE")
        for x in guides:
            oldName = x.split("_")
            newName = oldName[0] + "_" + oldName[1] + "_" + oldName[2] + "_CTL"
            ctl = controls.roundZ(curveScale=.2)
            pm.rename(ctl, newName)
            grp = pm.group(ctl, n=newName + "_fGRP")
            grp2 = pm.group( n=newName + "_offSet_fGRP")
            zero = pm.xform("eyeCentre_0", q=1, ws=1, t=1)
            pm.xform(grp2, ws=1, t=zero)
            pm.parent(grp, grp2)
            ctrl.append(grp2)
            pos = pm.xform(x, q=1, ws=1, t=1)
            pm.xform(grp, ws=1,t=pos)
            jntName = oldName[0] + "_" + oldName[1] + "_" + oldName[2] + "_eJNT"
            jnt = pm.createNode("joint", n=jntName)
            jnts.append(jnt)
            con = pm.pointConstraint(ctl, jnt)
            pm.xform(jnt, ws=1, t=pos)

        eyelidControl = pm.group(ctrl, n="eylidControl_GRP")
        jntControl = pm.group(jnts, n="eyeLidJoints_GRP")
        pm.setAttr(jntControl + ".visibility", 0)

        pm.delete(guides)
    
    @my_decorator
    def moveTheWire(self):
        lTopWire = "l_low_up_CURV"
        lBottomWore = "l_low_down_CURV"
        rTopWire = "r_low_up_CURV"
        rBottomeWire = "r_low_down_CURV"
        lTopJNT = [ "l_eye_rCorner_eJNT", "l_eye_upRight_eJNT", "l_eye_upMiddle_eJNT", "l_eye_upLeft_eJNT", "l_eye_lCorner_eJNT"]
        lBotJNT = [ "l_eye_rCorner_eJNT", "l_eye_downRight_eJNT", "l_eye_downMiddle_eJNT", "l_eye_downLeft_eJNT", "l_eye_lCorner_eJNT"]
        rTopJNT = [ "r_eye_rCorner_eJNT", "r_eye_upRight_eJNT", "r_eye_upMiddle_eJNT", "r_eye_upLeft_eJNT", "r_eye_lCorner_eJNT"]
        rBotJNT = [ "r_eye_rCorner_eJNT", "r_eye_downRight_eJNT", "r_eye_downMiddle_eJNT", "r_eye_downLeft_eJNT", "r_eye_lCorner_eJNT"]

        pm.skinCluster(lTopJNT, lTopWire, tsb=True)
        pm.skinCluster(lBotJNT, lBottomWore, tsb=True)
        pm.skinCluster(rTopJNT, rTopWire,tsb=True)
        pm.skinCluster(rBotJNT, rBottomeWire,tsb=True)

        adj = pm.ls(["*downLeft*eJNT", "*downRight*eJNT", "*upLeft*eJNT", "*upRight*eJNT"])
        for x in adj:
            oldName = x.split("_")
            newName = oldName[0] + "_" + oldName[1] + "_" + oldName[2] + "_ADJ"
            adjGRP = pm.group(x, empty =True, n=newName)
            pm.parent(adjGRP, world=True)
            pos = pm.xform(x, q=1, ws=1, t=1)
            pm.xform(adjGRP, ws=1, t=pos)

        pm.parentConstraint(["l_eye_upMiddle_CTL", "l_eye_lCorner_CTL"], "l_eye_upLeft_ADJ")
        pm.parentConstraint(["l_eye_upMiddle_CTL", "l_eye_rCorner_CTL"], "l_eye_upRight_ADJ")
        pm.parentConstraint(["l_eye_downMiddle_CTL", "l_eye_lCorner_CTL"], "l_eye_downLeft_ADJ")
        pm.parentConstraint(["l_eye_downMiddle_CTL", "l_eye_rCorner_CTL"], "l_eye_downRight_ADJ")

        pm.parentConstraint(["r_eye_upMiddle_CTL", "r_eye_lCorner_CTL"], "r_eye_upLeft_ADJ")
        pm.parentConstraint(["r_eye_upMiddle_CTL", "r_eye_rCorner_CTL"], "r_eye_upRight_ADJ")
        pm.parentConstraint(["r_eye_downMiddle_CTL", "r_eye_lCorner_CTL"], "r_eye_downLeft_ADJ")
        pm.parentConstraint(["r_eye_downMiddle_CTL", "r_eye_rCorner_CTL"], "r_eye_downRight_ADJ")

        pm.parent("l_eye_downLeft_ADJ", "l_eye_downLeft_CTL_fGRP")
        pm.parent("l_eye_downLeft_CTL", "l_eye_downLeft_ADJ")

        pm.parent("l_eye_downRight_ADJ", "l_eye_downRight_CTL_fGRP")
        pm.parent("l_eye_downRight_CTL", "l_eye_downRight_ADJ")

        pm.parent("l_eye_upLeft_ADJ", "l_eye_upLeft_CTL_fGRP")
        pm.parent("l_eye_upLeft_CTL", "l_eye_upLeft_ADJ")

        pm.parent("l_eye_upRight_ADJ", "l_eye_upRight_CTL_fGRP")
        pm.parent("l_eye_upRight_CTL", "l_eye_upRight_ADJ")

        pm.parent("r_eye_downLeft_ADJ", "r_eye_downLeft_CTL_fGRP")
        pm.parent("r_eye_downLeft_CTL", "r_eye_downLeft_ADJ")

        pm.parent("r_eye_downRight_ADJ", "r_eye_downRight_CTL_fGRP")
        pm.parent("r_eye_downRight_CTL", "r_eye_downRight_ADJ")

        pm.parent("r_eye_upLeft_ADJ", "r_eye_upLeft_CTL_fGRP")
        pm.parent("r_eye_upLeft_CTL", "r_eye_upLeft_ADJ")

        pm.parent("r_eye_upRight_ADJ", "r_eye_upRight_CTL_fGRP")
        pm.parent("r_eye_upRight_CTL", "r_eye_upRight_ADJ")

    #@my_decorator
    #def skinMeUp(self):

        #joint = pm.createNode("joint")
        #pm.rename(joint, "baseWeight")
        #jnt = pm.ls("*end_JNT")
        #pm.skinCluster(joint, jnt, "C_head_low_PLY", tsb=True)

    @my_decorator
    def blink(self):

        dupeLeft = pm.duplicate("l_low_up_CURV", n="l_blink_CURV")
        blendLeftEye = pm.blendShape("l_low_down_CURV", "l_low_up_CURV", dupeLeft, n="l_blinkHeight_BLD")
        
        dupeRight = pm.duplicate("r_low_up_CURV", n="r_blink_CURV")
        blendRightEye = pm.blendShape("r_low_down_CURV", "r_low_up_CURV", dupeRight, n="r_blinkHeight_BLD")
        
        lBlinkHeightAttr = pm.addAttr("l_eye_upMiddle_CTL", longName="blinkHeight", attributeType="float", min=0, max=1, defaultValue=0, keyable=True)
        rBlinkHeightAttr = pm.addAttr("r_eye_upMiddle_CTL", longName="blinkHeight", attributeType="float", min=0, max=1, defaultValue=0, keyable=True)

        pm.setAttr("l_blinkHeight_BLD.l_low_up_CURV",  1)
        pm.setAttr("r_blinkHeight_BLD.r_low_up_CURV",  1)

        pm.connectAttr("l_eye_upMiddle_CTL.blinkHeight", "l_blinkHeight_BLD.l_low_up_CURV", f=1)
        rev1 = pm.shadingNode("reverse", asUtility=True, n="l_blinkHeightBS_REV")
        pm.connectAttr("l_eye_upMiddle_CTL.blinkHeight", rev1 + ".inputX", f=1)
        pm.connectAttr(rev1 + ".outputX", "l_blinkHeight_BLD.l_low_down_CURV")

        pm.connectAttr("r_eye_upMiddle_CTL.blinkHeight", "r_blinkHeight_BLD.r_low_up_CURV", f=1)
        rev2 = pm.shadingNode("reverse", asUtility=True, n="r_blinkHeightBS_REV")
        pm.connectAttr("r_eye_upMiddle_CTL.blinkHeight", rev2 + ".inputX", f=1)
        pm.connectAttr(rev2 + ".outputX", "r_blinkHeight_BLD.r_low_down_CURV")

        dupeLeftup = pm.duplicate("l_up_CURV", n="l_up_blink_CURV")
        dupeLeftdown = pm.duplicate("l_down_CURV", n="l_down_blink_CURV")

        dupeRightup = pm.duplicate("r_up_CURV", n="r_up_blink_CURV")
        dupeRightdown = pm.duplicate("r_down_CURV", n="r_down_blink_CURV")

        pm.setAttr("l_eye_upMiddle_CTL.blinkHeight", 1)
        lupw = pm.wire("l_up_blink_CURV", gw=False, en=1.000000, ce=0.000000, li=0.000000, wire="l_blink_CURV", n="l_up_blink_WIR")
        pm.setAttr(lupw[0] + ".scale[0]", 0)
        pm.setAttr("l_eye_upMiddle_CTL.blinkHeight", 0)
        ldownw = pm.wire("l_down_blink_CURV", gw=False, en=1.000000, ce=0.000000, li=0.000000, wire="l_blink_CURV", n="l_down_blink_WIR")
        pm.setAttr(ldownw[0] + ".scale[0]", 0)
        blendLeftEyeUp = pm.blendShape("l_up_blink_CURV", "l_up_CURV", n="l_blink_up_BLD")
        blendLeftEyeDown = pm.blendShape("l_down_blink_CURV", "l_down_CURV", n="l_blink_down_BLD")

        pm.setAttr("r_eye_upMiddle_CTL.blinkHeight", 1)
        rupw = pm.wire("r_up_blink_CURV", gw=False, en=1.000000, ce=0.000000, li=0.000000, wire="r_blink_CURV", n="r_up_blink_WIR")
        pm.setAttr(rupw[0] + ".scale[0]", 0)
        pm.setAttr("r_eye_upMiddle_CTL.blinkHeight", 0)
        rdownw = pm.wire("r_down_blink_CURV", gw=False, en=1.000000, ce=0.000000, li=0.000000, wire="r_blink_CURV", n="r_down_blink_WIR")
        pm.setAttr(rdownw[0] + ".scale[0]", 0)
        blendRightEyeUp = pm.blendShape("r_up_blink_CURV", "r_up_CURV", n="r_blink_up_BLD")
        blendRightEyeDown = pm.blendShape("r_down_blink_CURV", "r_down_CURV", n="r_blink_down_BLD")

        lBlinkUpAttr = pm.addAttr("l_eye_upMiddle_CTL", longName="blink", attributeType="float", min=0, max=1, defaultValue=0, keyable=True)
        lBlinkDownAttr = pm.addAttr("l_eye_downMiddle_CTL", longName="blink", attributeType="float", min=0, max=1, defaultValue=0, keyable=True)
        rBlinkUpAttr = pm.addAttr("r_eye_upMiddle_CTL", longName="blink", attributeType="float", min=0, max=1, defaultValue=0, keyable=True)
        rBlinkDownAttr = pm.addAttr("r_eye_downMiddle_CTL", longName="blink", attributeType="float", min=0, max=1, defaultValue=0, keyable=True)

        pm.connectAttr("l_eye_upMiddle_CTL.blink", "l_blink_up_BLD.l_up_blink_CURV", f=1)
        pm.connectAttr("l_eye_downMiddle_CTL.blink", "l_blink_down_BLD.l_down_blink_CURV", f=1)
        pm.connectAttr("r_eye_upMiddle_CTL.blink", "r_blink_up_BLD.r_up_blink_CURV", f=1)
        pm.connectAttr("r_eye_downMiddle_CTL.blink", "r_blink_down_BLD.r_down_blink_CURV", f=1)

        pm.setAttr("l_eye_upMiddle_CTL.blinkHeight", 0.25)
        pm.setAttr("r_eye_upMiddle_CTL.blinkHeight", 0.25)





    def makeItSo(self):
        self.getEyeBalls()
        self.locInCentre(lcentre="l_eye_PLY.vtx[315:346]", rcentre="r_eye_PLY.vtx[315:346]")
        self.eyeRimJoints()
        self.eyeRimLocators()
        self.lineMeUp()
        self.onAWire1(locs = "l_uplid_LOC_GRP", crv = "l_up_CURVShape")
        self.onAWire2(locs = "l_downlid_LOC_GRP", crv = "l_down_CURVShape")
        self.onAWire3(locs = "r_uplid_LOC_GRP", crv = "r_up_CURVShape")
        self.onAWire4(locs = "r_downlid_LOC_GRP", crv = "r_down_CURVShape")
        self.guideMyEyes()
        self.controlMyLids()
        self.moveTheWire()
        #self.skinMeUp()
        self.blink()


  