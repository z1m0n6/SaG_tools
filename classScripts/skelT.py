import pymel.core as pm
import maya.cmds as cmds
import time

class BaseSkel(object):
    
    """
    my class test
    """

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
    # load
    #=============================================================
    @my_decorator
    def loader(self, inPath, rigVersion):
        cmds.file(inPath + rigVersion, i=True, f=True)    

    #=============================================================
    # delete namespace
    #=============================================================
    @my_decorator
    def delNameSpace(self):
        defaults = ['UI', 'shared']
        namespaces = (ns for ns in pm.namespaceInfo(lon=True) if ns not in defaults)
        for ns in namespaces:
            pm.namespace(mnr=True, rm=ns)

    #=======================================================
    # delete the constraints in the rig, you may need to breakConnections in channelBox
    #=======================================================
    @my_decorator
    def breakConns(self):
        folder = "joints_GRP"
        axis = ['x', 'y', 'z']
        attrs = ['t', 'r', 's']
        jnts = cmds.listRelatives(folder, allDescendents=True, type="joint")
        for jnt in jnts:
            for ax in axis:
                for attr in attrs:
                    conns = cmds.listConnections(jnt + "." + attr + ax)
                    pm.delete(conns)

    #=======================================================
    # match and parent bones chain together
    #=======================================================  
    @my_decorator  
    # parent bones
    def cleanUp(self, folder):
        pm.delete("model_GRP", "control_GRP", "global_CTO") 
        pm.setAttr("joints_GRP.visibility", 1)
        pm.parent("joints_GRP", world=True)
        pm.delete("roboto_rig_GRP")
        pm.rename("joints_GRP", folder)

    #=======================================================
    # rename Joints to unique name
    #=======================================================
    @my_decorator
    def nameXjoint(self, folder):
        filio = pm.listRelatives("{0}".format(folder), allDescendents=True, type="joint")
        longnames = pm.ls(filio, l=True, s=0)               
        longnames.sort()
        for item in longnames[::-1]:   # this is shorthand for 'walk through the list backwards'
            shortname = item.rpartition("|")[-1]  # get the last bit of the name
            pm.rename(item, shortname.replace("_JNT","_T_JNT"))

    #=======================================================
    # tPose
    #=======================================================
    @my_decorator
    def tPose(self):
        pm.setAttr("r_shoulder1_T_JNT.rotateY", 19)
        pm.setAttr("r_shoulder1_T_JNT.rotateZ", 66)
        pm.setAttr("r_elbow1_T_JNT.rotateZ", -31)

        pm.setAttr("l_shoulder1_T_JNT.rotateY", 19)
        pm.setAttr("l_shoulder1_T_JNT.rotateZ", 66)
        pm.setAttr("l_elbow1_T_JNT.rotateZ", -31)

    #=============================================================
    # engage
    #=============================================================
    @my_decorator
    def makeItSo(self, inPath, rigVersion, folder):
        self.loader(inPath, rigVersion)
        self.delNameSpace()
        self.breakConns()
        self.cleanUp(folder)
        self.nameXjoint(folder)
        self.tPose()
    
    #inPath = r"D:\sgScripts\project\dave\rig"
    #rigVersion = "\\001_dave_sgRig_v016.ma"

