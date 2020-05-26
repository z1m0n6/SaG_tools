"""
class for building bsMan face
(C) sgoodchild@hotmail.com
"""

import pymel.core as pm
import maya.cmds as cmds
import time
from rig_lib3 import controls
import eyeRig

reload(controls)
reload(eyeRig)
neutral = "callum_Neutral"
charName = "cal"

class FaceBuilder(object):

    def my_decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            func(*args, **kwargs)
            end = time.time()
            print(str(func) + " >>>>>>> Time taken : ", end-start)
        return wrapper

    #====================================================================================
    # import faceShapes and create a blendShape head with all connected, save out blendHead
    #====================================================================================

    @my_decorator
    def createBlendNode(self, name):

        #new Scene
        #cmds.file(new=True, f=True)

        pathOfFiles = r"E:/sgScripts/project/" + charName + "/model/face/faceShapes"
        fileType = "obj"

        files = cmds.getFileList(folder=pathOfFiles, filespec="*.{}".format(fileType))
        if len(files) == 0:
            cmds.warning("No files found")
        else:
            for x in files:
                cmds.file(pathOfFiles + "/" + x, i=1, dns=1)
        print "------------complete-faceShape-imports--------------"

        headPath = r"E:\sgScripts\project\\" + charName + r"\model\face\faceNeutralShape\\" + neutral + r".obj"
        head = cmds.file(headPath, i=1, dns=1)
        pm.rename(neutral, "bsMan_fRig_PLY")

        fShapes = []
        for x in files:
            item = x.split(".")
            fShapes.append(item[0])
        pm.select(fShapes)
        pm.blendShape(fShapes, "bsMan_fRig_PLY", name="faceShapes_BSN")
        pm.delete(fShapes)
        print "------------complete---blending-Of-faceShapes--------------"

        blendPath = r"E:\sgScripts\project\\" + charName + r"\model\face\faceBlended"
        pm.select(clear=True)
        pm.select("bsMan_fRig_PLY")
        cmds.file(blendPath + "\\" + name, type="mayaAscii", f=1, es=1)
        print "------------complete---exporting-Of-blendNode--------------"
        pm.delete("bsMan_fRig_PLY")

    #====================================================================================
    # create New scene and bring in All parts
    #====================================================================================
    @my_decorator
    def importFiles(self):
        #new Scene
        #cmds.file(new=True, f=True)

        # import head
        #headPath = r"E:\sgScripts\project\dave\model\dave_head.ma"
        #cmds.file(headPath, i=1, dns=1)
        
        # import guides
        guidePath = r"E:\sgScripts\project\\" + charName + r"\guide\\" + charName + r"_faceGuide.ma"
        cmds.file(guidePath, i=1, dns=1)

        # import BlendNode
        blendPath = r"E:\sgScripts\project\\" + charName + r"\model\face\faceBlended\bsMan_blendNode.ma"
        cmds.file(blendPath, i=1, dns=1)

        cmds.viewFit()
    
    #build folicles
    @my_decorator
    def buildFolicles(self, head):
        
        follicleGrp = pm.group(
                            name="faceFolicle_GRP",
                            empty=True,
                            #parent=moduleObjs["partsStaticGRP"]
                            )

        closestPointNode = pm.createNode("closestPointOnMesh", name="closestFacePoint_CTO")
        pm.connectAttr(head + ".worldMesh", closestPointNode + ".inMesh")
        
        guides = pm.ls("*_GUIDE")
        
        for number, guide in enumerate(guides):
            guidePos = pm.xform(guide, query=True, translation=True, worldSpace=True)
            pm.setAttr(closestPointNode + ".inPosition", guidePos[0], guidePos[1], guidePos[2])
            uParam = pm.getAttr(closestPointNode + ".parameterU")
            vParam = pm.getAttr(closestPointNode + ".parameterV")

            oldName = guide.split("_")
            newName = oldName[0] + "_" + oldName[1] + "_"

            folic = pm.createNode("follicle", name="{0}{1:02d}_folShape".format(newName, number))
            folicTrans = pm.listRelatives(folic, p=1)[0]
            folicParent = folicTrans
            pm.parent(folicParent, follicleGrp)
            pm.connectAttr(head + ".worldMatrix", folic + ".inputWorldMatrix")
            pm.connectAttr(head + ".outMesh", folic + ".inputMesh")
        
            pm.connectAttr(folic + ".outTranslate", folicParent + ".t")
            pm.connectAttr(folic + ".outRotate", folicParent + ".r")
        
            pm.setAttr(folic + ".parameterU", uParam)
            pm.setAttr(folic + ".parameterV", vParam)
        
            pm.parentConstraint(folicParent, guide, mo=True)
            pm.setAttr(folic + ".visibility", 0)
            pm.setAttr(folic + ".flipDirection", 1)
        
        pm.delete(closestPointNode)
        pm.delete(guides)

    # attach contrl shapes
    @my_decorator
    def fControl(self, newName, num):
        circ = controls.roundZ(curveScale=.2)
        pm.rename(circ, newName + "{0:02d}_fCTL".format(num))
        border = controls.square2()
        pm.hide(border)
        pm.rename(border, newName + "{0:02d}_fBDR".format(num))
        grp = pm.group(circ, border, n=newName + "{0:02d}_fGRP".format(num))
        grp2 = pm.group(grp, n=newName + "offSet_{0:02d}_fGRP".format(num))
        grp3 = pm.group(empty=True, n=newName + "woldSpace_{0:02d}_fGRP".format(num))
        pm.parent(grp2, grp3)
        pm.setAttr(str(grp) + ".tz", -0.3)

    @my_decorator
    def placement(self):
        grp2 = pm.ls("*offSet*")
        fols = pm.ls("*_fol")
        for num, fol in enumerate(fols):
            pos = pm.xform(fol, q=1, ws=1, t=True)
            oldName = fol.split("_")
            newName = oldName[0] + "_" + oldName[1] + "_"
            ctl = self.fControl(newName, num)
            pm.xform(grp2, ws=1, t=pos)
            loc = pm.spaceLocator(n="loc_{}".format(num))
            pm.setAttr(loc + ".visibility", 0)
            pm.xform(loc, ws=1, t=pos)
            pm.pointConstraint(fol, loc)
            pm.orientConstraint(fol, loc)
        
        
        ctls = pm.ls("*fCTL", type="transform")
        for x in ctls:
            pm.transformLimits(x, tx=(-1,1), etx=(1,0))
            pm.transformLimits(x, tx=(-1,1), etx=(1,1))
            pm.transformLimits(x, ty=(-1,1), ety=(1,0))
            pm.transformLimits(x, ty=(-1,1), ety=(1,1))
            #if:
                #pm.transformLimits(x, ty=(-1,1), ety=(1,0))
                #pm.transformLimits(x, ty=(-1,1), ety=(1,1))

        grp3 = pm.ls("*woldSpace*", type="transform")
        locs = pm.ls("loc_?", "loc_??", type="transform")
        for x, y in sorted(zip(grp3, locs)):
            pm.parent(y,x)
        grp2 = pm.ls("*offSet*")
        for x, y in sorted(zip(grp2, locs)):
            pm.connectAttr(y + ".translate", x + ".translate", force=True)
            pm.connectAttr(y + ".rotate", x + ".rotate", force=True)
        #for x in grp2:
            #pm.delete(pm.normalConstraint("C_body_PLY", x,  weight=1, aimVector=[0,0,1], upVector=[0,1,0], worldUpType="vector", worldUpVector=[0,1,0]))

        #grp =
        #for x in grp:
            #pm.orientConstraint("C_body_PLY", x, mo=True)
        pm.group(grp3, name="bsMan_faceRig_low_control_GRP")

    #def getInfo(self, GRPname):
        #ctrls = []
        #inf = pm.listRelatives(str(GRPname), allDescendents=True, type="transform")
        #for x in inf:
            #ctl = pm.listRelatives(x, allDescendents=True, type="nurbsCurve")
            #ctrls.append(ctl)
        #for x in ctrls:
            #print x
            #y = pm.ls(type="transform")
            #print y

    #def organiseGRPS(self):
        #self.getInfo("bsMan_faceRig_low_control_GRP")

    @my_decorator
    def linkTheHooks(self):
        faceShapesGeo="bsMan_fRig_PLY"
        faceGeo="C_head_low_PLY"
        faceShapesGeoHis=pm.listHistory(faceShapesGeo)
        faceShapesBls=cmds.ls(faceShapesGeoHis, type="blendShape")[0]
        targetIndeces=pm.getAttr(faceShapesBls + ".weight", multiIndices=1)
        bsShapeNames=[pm.aliasAttr("{0}.weight[{1}]".format(faceShapesBls, num), query=True)for num in targetIndeces]

        faceBlendGRP = pm.group(empty=True, n="faceBlends_hooks")
        for x in bsShapeNames:
            pm.addAttr(faceBlendGRP, sn=x)
        hooks = pm.PyNode("faceBlends_hooks")
        # Check every blendshape for matching hook names.
        allBlends = pm.ls(type='blendShape')
        for newBlend in allBlends:
            for eachShape in newBlend.w:
                shapeName = eachShape.getAlias()
                if hooks.hasAttr(shapeName):
                    hookAttr = hooks.attr(shapeName)
                    try:
                        hookAttr.connect(eachShape, force=True)
                    except:
                        continue

        pm.blendShape(faceShapesGeo, faceGeo, weight=[0,1])
        pm.setAttr(faceShapesGeo + ".visibility", 0)

    #def makingContact(self):
        #condition = pm.createNode("condition", name= "{0}" + "_" + "{1}" + "_COND".format(x, num))
        #multiply = pm.createNode("multiplyDivide", name= "{0}" + "_" + "{1}" + "_MULTI".format(x, num))

    #def incorperateEyes(self):
        #aye = eyeRig.LookAtMe()
        #aye.makeItSo()


    def makeItSo(self,):
        self.createBlendNode(name = "bsMan_blendNode"),
        self.importFiles(),
        self.buildFolicles(head = "C_body_PLY"),
        self.placement(),
        self.linkTheHooks(),
        #self.makingContact(),
        #self.incorperateEyes(),
        #self.organiseGRPS(),
        

        