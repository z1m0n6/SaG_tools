# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# content       = class for building the face of a character from many blendShapes 
#
# version       = 0.0.1
# date          = 07.05.2020
#
# how to        = head = buildFace.FaceBuilder()
#                 head.makeItSo()
# dependencies  = rig_lib3
#
# auther        = Simon Goodchild <sgoodchild@hotmail.com>
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


import time
import maya.mel as mel
import pymel.core as pm
import maya.cmds as cmds

import eyeRig
from rig_lib3 import controls

import yaml

reload(controls)
reload(eyeRig)


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
# VARIABLES
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
config_path = "E:/sgScripts/project/tools/io_lib/buildFace_config.yml"

with open(config_path, "r") as config:
    inData = yaml.load(config)

FILE_TYPE           = inData["FILE_TYPE"]
CHAR_NAME           = inData["CHAR_NAME"]
NEUTRAL             = inData["NEUTRAL"]

FOLDER              = inData["PATH"] ["FOLDER"] 

FACE_SHAPES         = FOLDER + "/" + CHAR_NAME + inData["PATH"] ["FACE_SHAPES"] 
OUT_BLEND           = FOLDER + "/" + CHAR_NAME + inData["PATH"] ["OUT_BLEND"]
GUIDES              = FOLDER + "/" + CHAR_NAME + inData["PATH"] ["GUIDES"] + CHAR_NAME + "_faceGuide.ma"
IN_BLEND            = FOLDER + "/" + CHAR_NAME + inData["PATH"] ["IN_BLEND"]
NHEAD               = FOLDER + "/" + CHAR_NAME + inData["PATH"] ["HEAD"] + "/" + NEUTRAL + "." + FILE_TYPE

HEAD                = inData["NAME"] ["HEAD"]
FACE_SHAPES_GEO     = inData["NAME"] ["FACE_SHAPES_GEO"]
FACE_GEO            = inData["NAME"] ["FACE_GEO"]
BSMAN_NAME          = inData["NAME"] ["BSMAN_NAME"]

#====================================================================================
# wrapper to tell me how long a function has taken to execute
#====================================================================================

def time_Taken(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(str(func) + " >>>>>>> Time taken : ", end-start)
    return wrapper


class FaceBuilder(object):

    #====================================================================================
    # create New scene and bring in All parts
    #====================================================================================

    @time_Taken
    def importFiles(self):
        # import guides
        cmds.file(GUIDES, i=True, defaultNamespace=True)
        # import BlendNode
        cmds.file(IN_BLEND, i=True, defaultNamespace=True)

        cmds.viewFit()


    #====================================================================================
    # import faceShapes and create a blendShape head with all connected, save out blendHead
    #====================================================================================

    @time_Taken
    def createFaceBlends(self):
        print FACE_SHAPES
        files = cmds.getFileList(folder=FACE_SHAPES , filespec="*.{}".format(FILE_TYPE))
        print files
        
        if files:
            for shape in files:
                cmds.file(FACE_SHAPES + "/" + shape, i=True, defaultNamespace=True)
        else:
            cmds.warning("No files found")

        print ("------------complete-faceShape-imports--------------")

        cmds.file(NHEAD, i=True, defaultNamespace=True)
        pm.rename(inData["NEUTRAL"], "bsMan_fRig_PLY")

        fShapes = []
        for shape in files:
            item = shape.split(".")
            fShapes.append(item[0])

        pm.select(fShapes)
        pm.blendShape(fShapes, "bsMan_fRig_PLY", name="faceShapes_BSN")
        pm.delete(fShapes)

        print ("------------complete---blending-Of-faceShapes--------------")
        
        pm.select(clear=True)
        pm.select("bsMan_fRig_PLY")
        cmds.file(OUT_BLEND + "/" + inData["NAME"] ["BSMAN_NAME"], type="mayaAscii", force=True, exportSelected=True)

        print ("------------complete---exporting-Of-blendNode--------------")

        pm.delete("bsMan_fRig_PLY")


    #====================================================================================
    # create folicles on surface of head geo for controls to be parented to
    #====================================================================================

    @time_Taken
    def buildFolicles(self):
        
        follicleGrp = pm.group( name="faceFolicle_GRP",
                                empty=True )

        closestPointNode = pm.createNode("closestPointOnMesh", name="closestFacePoint_CTO")
        pm.connectAttr(HEAD + ".worldMesh", closestPointNode + ".inMesh")
        
        guides = pm.ls("*_GUIDE")
        
        for number, guide in enumerate(guides):
            guidePos = pm.xform(guide, query=True, translation=True, worldSpace=True)
            pm.setAttr(closestPointNode + ".inPosition", guidePos[0], guidePos[1], guidePos[2])
            uParam = pm.getAttr(closestPointNode + ".parameterU")
            vParam = pm.getAttr(closestPointNode + ".parameterV")

            oldName = guide.split("_")
            newName = oldName[0] + "_" + oldName[1] + "_"

            folic = pm.createNode("follicle", name="{0}{1:02d}_folShape".format(newName, number))
            folicTrans = pm.listRelatives(folic, parent=True)[0]
            folicParent = folicTrans
            pm.parent(folicParent, follicleGrp)
            pm.connectAttr(HEAD + ".worldMatrix", folic + ".inputWorldMatrix")
            pm.connectAttr(HEAD + ".outMesh", folic + ".inputMesh")
        
            pm.connectAttr(folic + ".outTranslate", folicParent + ".t")
            pm.connectAttr(folic + ".outRotate", folicParent + ".r")
        
            pm.setAttr(folic + ".parameterU", uParam)
            pm.setAttr(folic + ".parameterV", vParam)
        
            pm.parentConstraint(folicParent, guide, maintainOffset=True)
            pm.setAttr(folic + ".visibility", 0)
            pm.setAttr(folic + ".flipDirection", 1)
        
        pm.delete(closestPointNode)
        pm.delete(guides)


    #====================================================================================
    # create the control shapes 
    #====================================================================================

    @time_Taken
    def fControl(self, newName, num):
        circ = controls.roundZ(curveScale=.2)
        pm.rename(circ, newName + "fCTL")

        border = controls.square2()
        pm.hide(border)
        pm.rename(border, newName + "{0:02d}_fBDR".format(num))
        # create Groups
        grp = pm.group(circ, border, name=newName + "{0:02d}_fGRP".format(num))
        grp2 = pm.group(grp, name=newName + "offSet_{0:02d}_fGRP".format(num))
        grp3 = pm.group(empty=True, name=newName + "woldSpace_{0:02d}_fGRP".format(num))

        pm.parent(grp2, grp3)
        pm.setAttr(str(grp) + ".tz", -0.3)


    #====================================================================================
    # parent the controls shapes to the folicles and creat the offset groups
    #====================================================================================

    @time_Taken
    def placement(self):
        grp2 = pm.ls("*offSet*")
        fols = pm.ls("*_fol")
        for num, fol in enumerate(fols):
            pos = pm.xform(fol, query=True, worldSpace=True, translation=True)
            oldName = fol.split("_")
            newName = oldName[0] + "_" + oldName[1] + "_"

            self.fControl(newName, num)
            pm.xform(grp2, worldSpace=True, translation=pos)
            loc = pm.spaceLocator(name="loc_{}".format(num))
            pm.setAttr(loc + ".visibility", 0)
            pm.xform(loc, worldSpace=True, translation=pos)

            pm.pointConstraint(fol, loc)
            pm.orientConstraint(fol, loc)
        
        ctls = pm.ls("*fCTL", type="transform")
        for x in ctls:
            pm.transformLimits(x, translationX=(-1,1), enableTranslationX=(1,0))
            pm.transformLimits(x, translationX=(-1,1), enableTranslationX=(1,1))
            pm.transformLimits(x, translationY=(-1,1), enableTranslationY=(1,0))
            pm.transformLimits(x, translationY=(-1,1), enableTranslationY=(1,1))
            pm.transformLimits(x, translationZ=(-1,1), enableTranslationZ=(1,0))
            pm.transformLimits(x, translationZ=(-1,1), enableTranslationZ=(1,1))

        grp3 = pm.ls("*woldSpace*", type="transform")
        locs = pm.ls("loc_?", "loc_??", type="transform")

        for x, y in sorted(zip(grp3, locs)):
            pm.parent(y,x)

        grp2 = pm.ls("*offSet*")

        for x, y in sorted(zip(grp2, locs)):
            pm.connectAttr(y + ".translate", x + ".translate", force=True)
            pm.connectAttr(y + ".rotate", x + ".rotate", force=True)

        pm.group(grp3, name="bsMan_faceRig_low_control_GRP")


    #====================================================================================
    # connect the hook names to the corresponding face blendshape
    #====================================================================================

    @time_Taken
    def linkTheHooks(self):
        conditionNode = []
        multiplyNode = []

        faceShapesGeoHis = pm.listHistory(FACE_SHAPES_GEO)
        faceShapesBls = pm.ls(faceShapesGeoHis, type="blendShape")[0]
        targetIndeces = pm.getAttr(faceShapesBls + ".weight", multiIndices=1)
        bsShapeNames = [pm.aliasAttr("{0}.weight[{1}]".format(faceShapesBls, num), query=True)for num in targetIndeces]

        faceBlendGRP = pm.group(empty=True, name="faceBlends_hooks")
        for x in bsShapeNames:
            pm.addAttr(faceBlendGRP, shortName=x)
        hooks = pm.PyNode("faceBlends_hooks")
        # Check every blendshape for matching hook names.
        allBlends = pm.ls(type='blendShape')
        for newBlend in allBlends:
            for eachShape in newBlend.w:
                shapeName = eachShape.getAlias()
                if hooks.hasAttr(shapeName):
                    hookAttr = hooks.attr(shapeName)
                    try:
                        #connect the hooks to the blend Node
                        hookAttr.connect(eachShape, force=True)

                        # for each faceShape creat the necesary condition and multiply nodes
                        condition = pm.createNode("condition", name= "{0}".format(shapeName) + "_COND")
                        pm.addAttr(condition, shortName=shapeName)
                        pm.setAttr(condition + ".colorIfFalseR", 0)
                        pm.setAttr(condition + ".operation", 2)

                        multiply = pm.createNode("multiplyDivide", name= "{0}".format(shapeName) + "_MULT")
                        pm.addAttr(multiply, shortName=shapeName)
                        pm.setAttr(multiply + ".input2Y", -1)

                        # connect the x, y outputs to the faceBlends hooks
                        name = "l_pullDown", "r_pullDown", "l_frown", "r_frown", "l_lipsPullOut", "r_lipsPullsOut", "r_narrow", "l_cheekPuff", "r_cheekPuff", "l_top_rollIn", "r_top_rollIn", "l_bot_rollOut", "r_bot_rollOut"
                        #, "l_bot_rollOut", "r_bot_rollOut"
                        if multiply.startswith(name):
                            pm.connectAttr(multiply + ".outputY", hookAttr)
                        else:
                            pm.connectAttr(multiply + ".outputX", hookAttr)

                        # make the lists for future ref
                        conditionNode.append(condition)
                        multiplyNode.append(multiply)
                    except:
                        pass
        # linking the correct condition to the multiply node                    
        for x, y in zip(conditionNode, multiplyNode):
            pm.connectAttr(x + ".outColorR", y + ".input1X", force=True)
            pm.connectAttr(x + ".outColorG", y + ".input1Y", force=True)

        pm.blendShape(FACE_SHAPES_GEO, FACE_GEO, weight=[0,1])
        pm.setAttr(FACE_SHAPES_GEO + ".visibility", 0)


    #====================================================================================
    # connect the blendshapes to the face controls
    #====================================================================================

    def linkTheControls(self):

        # *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
        # VARIABLES
        first = ".firstTerm"
        colourTrueR = ".colorIfTrueR"
        colourFalseG = ".colorIfFalseG"

        tx = ".translateX"
        ty = ".translateY"
        tz = ".translateZ"

        sides = "l_", "r_"
        outPut = tx, ty, tz
        inPut = [first, colourTrueR, colourFalseG]

        # create multiple connection in one line
        for x in inPut:
            for side in sides:
                pm.connectAttr(side + "lowerLipBack_fCTL" + str(outPut[1]), side + "pullDown_COND" + str(x), force=True)
                pm.connectAttr(side + "upperLipBack_fCTL" + str(outPut[1]), side + "sneer_COND" + str(x), force=True)
                
                pm.connectAttr(side + "lipCorner_fCTL" + str(outPut[1]), side + "smile_COND" + str(x), force=True)
                pm.connectAttr(side + "lipCorner_fCTL" + str(outPut[0]), side + "narrow_COND" + str(x), force=True)
                pm.connectAttr(side + "lipCorner_fCTL" + str(outPut[1]), side + "frown_COND" + str(x), force=True)
                pm.connectAttr(side + "lipCorner_fCTL" + str(outPut[0]), side + "lipsPullOut_COND" + str(x), force=True)
                
                pm.connectAttr(side + "cheek_fCTL" + str(outPut[2]), side + "cheekSuck_COND" + str(x), force=True)
                pm.connectAttr(side + "cheek_fCTL" + str(outPut[2]), side + "cheekPuff_COND" + str(x), force=True)

                pm.connectAttr("c_upperLip_fCTL" + str(outPut[1]), side + "top_rollOut_COND" + str(x), force=True)
                pm.connectAttr("c_lowerLip_fCTL" + str(outPut[1]), side + "bot_rollOut_COND" + str(x), force=True)
                pm.connectAttr("c_upperLip_fCTL" + str(outPut[1]), side + "top_rollIn_COND" + str(x), force=True)
                pm.connectAttr("c_lowerLip_fCTL" + str(outPut[1]), side + "bot_rollIn_COND" + str(x), force=True)
   

    def makeItSo(self):
        self.createFaceBlends()
        self.importFiles(),
        self.buildFolicles(),
        self.placement(),
        self.linkTheHooks(),
        self.linkTheControls()


        

        