#cmds.artAttrCtx('currentCtx', e=1, value=0.1)
import pymel.core as pm
import maya.mel as mel

cmds.file(new=True, f=True)
#==============================================================================
# import the heads
#==============================================================================
blendFilePath = r"E:\sgScripts\project\dave\model\face\faceShapes\Iain_head_LipsOO.obj"
cmds.file(blendFilePath, i=1, dns=1)

nuetralFilePath = r"E:\sgScripts\project\dave\model\face\faceNeutralShape\Iain_head_neutral.obj"
cmds.file(nuetralFilePath, i=1, dns=1)

#==============================================================================
# blend the heads
#==============================================================================
blending = pm.blendShape("Iain_head_LipsOO", "Iain_head_neutral", weight=([0, 1.0],[1, 1.0]), foc=True)
pm.delete("Iain_head_LipsOO")
pm.select("Iain_head_neutral", r=True)
mapPath = r"E:/sgScripts/project/dave" + "/" + "textures/faceData/l_lipsOO.iff"
mel.eval("ArtPaintBlendShapeWeightsToolOptions();")
mel.eval('artImportAttrMapCB artAttrCtx "{0}" "image";'.format(mapPath))
pm.select("Iain_head_neutral", r=True)
pm.delete(all=True, ch=True)
#delete history so no blendNode is ther

#==============================================================================
# export the sided head
#==============================================================================
blendPath = r"E:\sgScripts\project\dave\model\face\faceBlended"
pm.select(clear=True)
pm.select("Iain_head_neutral")
name = "l_lipsOO"
pm.rename("Iain_head_neutral", name)
cmds.file(blendPath + "\\" + name, type="mayaAscii", f=1, es=1)