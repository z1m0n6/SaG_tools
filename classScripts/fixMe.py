import pymel.core as pm
import maya.cmds as cmds
import time

class MrWolf(object):
    
    """
    my class test
    """
    def newScene(self):
        cmds.file(new=True, f=True)

    def my_decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            func(*args, **kwargs)
            end = time.time()
            print(str(func) + " > Time taken : ", end-start)
            #print("args are : ", args)
            #print("keyword args are : ", kwargs)
        return wrapper

    #=============================================================
    # import the model
    #=============================================================
    @my_decorator
    def importMe(self, inPath, name, ext):
        cmds.file(new=True, f=True)
        model = inPath + name + ext
        print (model)
        cmds.file(model, i=True, f=True)

    #=============================================================
    # fix normals
    #=============================================================
    @my_decorator
    def cleanMe(self): 
        cmds.viewFit()
        object = pm.ls(tr=True)[0:6]
        for x in object:
            pm.select(x)
            pm.polyNormalPerVertex(x, ufn=True)
            pm.polySoftEdge(x, a=180, ch=1)
            pm.bakePartialHistory(x, ppt=True)
            pm.select(cl=True)

    #=============================================================
    # rename the models
    #=============================================================
    @my_decorator
    def callMe(self):
        items = pm.ls(tr=True)[0:6]
        pm.rename(items[1], items[1] + "_jaw")
        pm.rename(items[5], items[5] + "_jaw")
        for x in items:
            pm.rename(x, x.lower())
            pm.rename(x, x + "_PLY")
        pm.rename(items[0], "C_" + items[0])

    #=============================================================
    # rename assets
    #=============================================================
    @my_decorator
    def switchARoo(self):
        modelsA =["C_body_PLY", "l_eye_PLY", "r_eye_PLY", "bottom_jaw_PLY", "tongue_PLY", "top_jaw_PLY"]
        pm.select(modelsA)
        shapesInSel = pm.ls(dag=1,o=1,s=1,sl=1)
        shadingGrps = pm.listConnections(shapesInSel,type="shadingEngine")[::2]
        shaders = pm.ls(pm.listConnections(shadingGrps), materials=True)
        pm.delete(shaders)
        for x in shadingGrps:
            lambertshader = pm.rendering.shadingNode("lambert", asShader=True)
            lambertshader.outColor >> x.surfaceShader
        shaders = pm.ls(pm.listConnections(shadingGrps), materials=True)
        [pm.rename(x, y) for x, y in (zip(shadingGrps, modelsA))]
        [pm.rename(x, y) for x, y in (zip(shaders, modelsA))]

        shaderGroups = pm.ls("*_PLY*", type="shadingEngine")
        longnames = pm.ls(shaderGroups, l=True,s=0)           
        longnames.sort()
        for item in longnames[::-1]:
            shortname = item.rpartition("|")[-1]
            pm.rename(item, shortname.replace("_PLY1","_SE"))

        shaderMats = pm.ls("*_PLY*", type="lambert")
        longnames = pm.ls(shaderMats, l=True,s=0)           
        longnames.sort()
        for item in longnames[::-1]:
            shortname = item.rpartition("|")[-1]
            pm.rename(item, shortname.replace("_PLY2","_LBT"))

    #=============================================================
    # export the models
    #=============================================================
    @my_decorator
    def exportMe(self, outPath):
        parts = pm.ls("*_PLY")
        print (outPath)
        for x in parts:
            pm.select(x)
            pm.exportSelected(outPath + x, force=True, options="", type="FBX export", pr=True)

    #=============================================================
    # engage
    #=============================================================
    @my_decorator
    def makeItSo(self, inPath, name, ext, outPath):
        self.importMe(inPath, "/" + name, ext)
        self.cleanMe()
        self.callMe()
        self.switchARoo()
        self.exportMe(outPath + "/")
