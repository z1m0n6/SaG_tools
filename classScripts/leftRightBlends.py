# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# content       = imports left blendshape duplicates it and mirrors it to make right blendshape
#
# version       = 0.0.1
# date          = 07.05.2020
#
# how to        = import leftRightBlends
#                 reload(leftRightBlends)
#                 blends = leftRightBlends.SeparateFaceLR()
#                 blends.makeItSo(
#                                   neutralHead         = "callum_neutral",
#                                   blendShapeHead      = "callum_head_CheeksPuff",
#                                   newName             = "l_CheeksPuff",
#                                   mapName             = "leftFront.tif" 
#                                   )
#
#                 blends.makeItSo(
#                                   neutralHead         = "callum_neutral",
#                                   blendShapeHead      = "callum_head_CheeksPuff",
#                                   newName             = "r_CheeksPuff",
#                                   mapName             = "rightFront.tif" 
#                                   )
#
# auther        = Simon Goodchild <sgoodchild@hotmail.com>
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


import maya.mel as mel
import pymel.core as pm
import maya.cmds as cmds

import time


# *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
# VARIABLES

FOLDER_PATH          = "E:/sgScripts/project/"
CHAR_NAME            = "cal"

MAP_PATH             = FOLDER_PATH + CHAR_NAME + "/" + "textures/faceData/"
IN_BLEND_PATH        = FOLDER_PATH + CHAR_NAME + r"\\model\face\faceShapes" + r"\\"
OUT_BLEND_PATH       = FOLDER_PATH + CHAR_NAME + r"\\model\face\l_r_faceShapes" + r"\\"
NEUTRAL_PATH         = FOLDER_PATH + CHAR_NAME + r"\\model\face\faceNeutralShape" + r"\\"


class SeparateFaceLR(object):

    def timeTaken(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            func(*args, **kwargs)
            end = time.time()
            print(str(func) + " > Time taken : ", end-start)
        return wrapper


    #======================================================================================================
    # import the heads
    #======================================================================================================
    @timeTaken
    def importFiles(self, neutralHead, blendShapeHead):
        cmds.file(new=True, f=True)

        cmds.file(IN_BLEND_PATH + blendShapeHead + ".obj", i=1, dns=1)
        print (IN_BLEND_PATH + blendShapeHead)
        cmds.file(NEUTRAL_PATH + neutralHead + ".obj", i=1, dns=1)


    #=======================================================================================================
    # blend the heads
    #=======================================================================================================
    @timeTaken
    def mirrorBlendShape(self, mapName, blendShapeHead, neutralHead):
        pm.blendShape(blendShapeHead, neutralHead, weight=([0, 1.0],[1, 1.0]), foc=True)
        pm.delete(blendShapeHead)

        pm.select(neutralHead, r=True)
        mel.eval("ArtPaintBlendShapeWeightsToolOptions();")
        mel.eval('artImportAttrMapCB artAttrCtx "{0}" "image";'.format(MAP_PATH + mapName))

        pm.select(neutralHead, r=True)
        pm.delete(all=True, ch=True)

        # set map settings to 1080 for better resolution


    #======================================================================================================
    # rename and export mirror blendShape
    #======================================================================================================
    @timeTaken
    def renameExportShape(self, neutralHead, newName):
        pm.select(clear=True)

        pm.select(neutralHead)
        pm.rename(neutralHead, newName)
        cmds.file(OUT_BLEND_PATH + "\\" + newName, type="OBJexport", f=1, es=1)


    #======================================================================================================
    # execute the code
    #======================================================================================================
    @timeTaken
    def makeItSo(self, neutralHead, blendShapeHead, mapName, newName):
        self.importFiles(neutralHead, blendShapeHead)
        self.mirrorBlendShape(mapName, blendShapeHead, neutralHead)
        self.renameExportShape(neutralHead, newName)