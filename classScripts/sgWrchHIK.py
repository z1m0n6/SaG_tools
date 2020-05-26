import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
import time
import json
from collections import OrderedDict


class WrchHIK(object):
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
    #=================================================================
    # create a character 
    #=================================================================
    wrchBones = {}
    myRigBones = {}
    myRigBonesT = {}
    @my_decorator
    def jsonImport(self, jsonPath):
        inputFile1 = jsonPath + "\myRigBones.json"
        inputFile2 = jsonPath + "\wrchBones.json"
        inputFile3 = jsonPath + "\myRigBonesT.json"
        myRigBones = json.load(open(inputFile1), object_pairs_hook=OrderedDict)
        myRigBonesT = json.load(open(inputFile3), object_pairs_hook=OrderedDict)
        wrchBones = json.load(open(inputFile2), object_pairs_hook=OrderedDict)
        self.myRigBones = myRigBones
        self.myRigBonesT = myRigBonesT
        self.wrchBones = wrchBones

    #=================================================================
    # assign bones to hik character1 (moCap rig)
    #=================================================================
    @my_decorator
    def linkWrchHIK(self, name1):
        #mel.eval('hikCreateDefinition;')
        mel.eval('hikCreateCharacter "{0}";'.format(name1))

        mel.eval('setCharacterObject("{}","{}",0,0);'.format(self.wrchBones.values()[0], name1)) 
        mel.eval('setCharacterObject("{}","{}",8,0);'.format(self.wrchBones.values()[1], name1))
        mel.eval('setCharacterObject("{}","{}",23,0);'.format(self.wrchBones.values()[2], name1))
        mel.eval('setCharacterObject("{}","{}",20,0);'.format(self.wrchBones.values()[3], name1))
        mel.eval('setCharacterObject("{}","{}",15,0);'.format(self.wrchBones.values()[4], name1))
        mel.eval('setCharacterObject("{}","{}",9,0);'.format(self.wrchBones.values()[5], name1))
        mel.eval('setCharacterObject("{}","{}",10,0);'.format(self.wrchBones.values()[6], name1))
        mel.eval('setCharacterObject("{}","{}",11,0);'.format(self.wrchBones.values()[7], name1))
        mel.eval('setCharacterObject("{}","{}",12,0);'.format(self.wrchBones.values()[8], name1))
        mel.eval('setCharacterObject("{}","{}",13,0);'.format(self.wrchBones.values()[9], name1))
        mel.eval('setCharacterObject("{}","{}",14,0);'.format(self.wrchBones.values()[10], name1))
        mel.eval('setCharacterObject("{}","{}",2,0);'.format(self.wrchBones.values()[11], name1))
        mel.eval('setCharacterObject("{}","{}",3,0);'.format(self.wrchBones.values()[12], name1))
        mel.eval('setCharacterObject("{}","{}",4,0);'.format(self.wrchBones.values()[13], name1))
        mel.eval('setCharacterObject("{}","{}",16,0);'.format(self.wrchBones.values()[14], name1))
        mel.eval('setCharacterObject("{}","{}",5,0);'.format(self.wrchBones.values()[15], name1))
        mel.eval('setCharacterObject("{}","{}",6,0);'.format(self.wrchBones.values()[16], name1))
        mel.eval('setCharacterObject("{}","{}",7,0);'.format(self.wrchBones.values()[17], name1))
        mel.eval('setCharacterObject("{}","{}",17,0);'.format(self.wrchBones.values()[18], name1))

    #@my_decorator
    #def linkWrchTHIK(self, name4):
        #mel.eval('hikCreateDefinition;')
        #mel.eval('hikCreateCharacter "{0}";'.format(name4))

        #mel.eval('setCharacterObject("{}","{}",0,0);'.format(self.wrchBones.values()[0]+"_TARGET", name4)) 
        #mel.eval('setCharacterObject("{}","{}",1,0);'.format(self.wrchBones.values()[1]+"_TARGET", name4))
        #mel.eval('setCharacterObject("{}","{}",8,0);'.format(self.wrchBones.values()[2]+"_TARGET", name4))
        #mel.eval('setCharacterObject("{}","{}",23,0);'.format(self.wrchBones.values()[3]+"_TARGET", name4))
        #mel.eval('setCharacterObject("{}","{}",24,0);'.format(self.wrchBones.values()[4]+"_TARGET", name4))
        #mel.eval('setCharacterObject("{}","{}",25,0);'.format(self.wrchBones.values()[5]+"_TARGET", name4))
        #mel.eval('setCharacterObject("{}","{}",26,0);'.format(self.wrchBones.values()[6]+"_TARGET", name4))
        #mel.eval('setCharacterObject("{}","{}",20,0);'.format(self.wrchBones.values()[7]+"_TARGET", name4))
        #mel.eval('setCharacterObject("{}","{}",15,0);'.format(self.wrchBones.values()[8]+"_TARGET", name4))
        #mel.eval('setCharacterObject("{}","{}",18,0);'.format(self.wrchBones.values()[9]+"_TARGET", name4))
        #mel.eval('setCharacterObject("{}","{}",9,0);'.format(self.wrchBones.values()[10]+"_TARGET", name4))
        #mel.eval('setCharacterObject("{}","{}",10,0);'.format(self.wrchBones.values()[11]+"_TARGET", name4))
        #mel.eval('setCharacterObject("{}","{}",11,0);'.format(self.wrchBones.values()[12]+"_TARGET", name4))
        #mel.eval('setCharacterObject("{}","{}",19,0);'.format(self.wrchBones.values()[13]+"_TARGET", name4))
        #mel.eval('setCharacterObject("{}","{}",12,0);'.format(self.wrchBones.values()[14]+"_TARGET", name4))
        #mel.eval('setCharacterObject("{}","{}",13,0);'.format(self.wrchBones.values()[15]+"_TARGET", name4))
        #mel.eval('setCharacterObject("{}","{}",14,0);'.format(self.wrchBones.values()[16]+"_TARGET", name4))
        #mel.eval('setCharacterObject("{}","{}",2,0);'.format(self.wrchBones.values()[17]+"_TARGET", name4))
        #mel.eval('setCharacterObject("{}","{}",3,0);'.format(self.wrchBones.values()[18]+"_TARGET", name4))
        #mel.eval('setCharacterObject("{}","{}",4,0);'.format(self.wrchBones.values()[19]+"_TARGET", name4))
        #mel.eval('setCharacterObject("{}","{}",16,0);'.format(self.wrchBones.values()[20]+"_TARGET", name4))
        #mel.eval('setCharacterObject("{}","{}",5,0);'.format(self.wrchBones.values()[21]+"_TARGET", name4))
        #mel.eval('setCharacterObject("{}","{}",6,0);'.format(self.wrchBones.values()[22]+"_TARGET", name4))
        #mel.eval('setCharacterObject("{}","{}",7,0);'.format(self.wrchBones.values()[23]+"_TARGET", name4))
        #mel.eval('setCharacterObject("{}","{}",24,0);'.format(self.wrchBones.values()[24]+"_TARGET", name4))
    #=================================================================
    # assign bones to hik character1 (my rig)
    #=================================================================
    #@my_decorator
    #def linkmyRigHIK(self, name2):

        #mel.eval('hikCreateDefinition;')
        #mel.eval('hikCreateCharacter "{name}";'.format(name="myRig"))
        
        #mel.eval('setCharacterObject("{}","{}",1,0);'.format(self.myRigBones.values()[0], name2)) 
        #mel.eval('setCharacterObject("{}","{}",0,0);'.format(self.myRigBones.values()[1], name2))
        #mel.eval('setCharacterObject("{}","{}",18,0);'.format(self.myRigBones.values()[9], name2))
        #mel.eval('setCharacterObject("{}","{}",9,0);'.format(self.myRigBones.values()[10], name2))
        #mel.eval('setCharacterObject("{}","{}",10,0);'.format(self.myRigBones.values()[11], name2))
        #mel.eval('setCharacterObject("{}","{}",11,0);'.format(self.myRigBones.values()[12], name2))
        #mel.eval('setCharacterObject("{}","{}",19,0);'.format(self.myRigBones.values()[13], name2))
        #mel.eval('setCharacterObject("{}","{}",12,0);'.format(self.myRigBones.values()[14], name2))
        #mel.eval('setCharacterObject("{}","{}",13,0);'.format(self.myRigBones.values()[15], name2))
        #mel.eval('setCharacterObject("{}","{}",14,0);'.format(self.myRigBones.values()[16], name2))
        #mel.eval('setCharacterObject("{}","{}",2,0);'.format(self.myRigBones.values()[17], name2))
        #mel.eval('setCharacterObject("{}","{}",3,0);'.format(self.myRigBones.values()[18], name2))
        #mel.eval('setCharacterObject("{}","{}",4,0);'.format(self.myRigBones.values()[19], name2))
        #mel.eval('setCharacterObject("{}","{}",16,0);'.format(self.myRigBones.values()[20], name2))
        #mel.eval('setCharacterObject("{}","{}",5,0);'.format(self.myRigBones.values()[21], name2))
        #mel.eval('setCharacterObject("{}","{}",6,0);'.format(self.myRigBones.values()[22], name2))
        #mel.eval('setCharacterObject("{}","{}",7,0);'.format(self.myRigBones.values()[23], name2))
        #mel.eval('setCharacterObject("{}","{}",17,0);'.format(self.myRigBones.values()[24], name2))
        #mel.eval('setCharacterObject("{}","{}",8,0);'.format(self.myRigBones.values()[2], name2))
        #mel.eval('setCharacterObject("{}","{}",23,0);'.format(self.myRigBones.values()[3], name2))
        #mel.eval('setCharacterObject("{}","{}",24,0);'.format(self.myRigBones.values()[4], name2))
        #mel.eval('setCharacterObject("{}","{}",25,0);'.format(self.myRigBones.values()[5], name2))
        #mel.eval('setCharacterObject("{}","{}",26,0);'.format(self.myRigBones.values()[6], name2))
        #mel.eval('setCharacterObject("{}","{}",20,0);'.format(self.myRigBones.values()[7], name2))
        #mel.eval('setCharacterObject("{}","{}",15,0);'.format(self.myRigBones.values()[8], name2))

    @my_decorator
    def linkmyRigTHIK(self, name3):

        mel.eval('hikCreateDefinition;')
        mel.eval('hikCreateCharacter "{name}";'.format(name="myRigT"))
        
        mel.eval('setCharacterObject("{}","{}",1,0);'.format(self.myRigBonesT.values()[0], name3)) 
        mel.eval('setCharacterObject("{}","{}",0,0);'.format(self.myRigBonesT.values()[1], name3))
        mel.eval('setCharacterObject("{}","{}",18,0);'.format(self.myRigBonesT.values()[9], name3))
        mel.eval('setCharacterObject("{}","{}",9,0);'.format(self.myRigBonesT.values()[10], name3))
        mel.eval('setCharacterObject("{}","{}",10,0);'.format(self.myRigBonesT.values()[11], name3))
        mel.eval('setCharacterObject("{}","{}",11,0);'.format(self.myRigBonesT.values()[12], name3))
        mel.eval('setCharacterObject("{}","{}",19,0);'.format(self.myRigBonesT.values()[13], name3))
        mel.eval('setCharacterObject("{}","{}",12,0);'.format(self.myRigBonesT.values()[14], name3))
        mel.eval('setCharacterObject("{}","{}",13,0);'.format(self.myRigBonesT.values()[15], name3))
        mel.eval('setCharacterObject("{}","{}",14,0);'.format(self.myRigBonesT.values()[16], name3))
        mel.eval('setCharacterObject("{}","{}",2,0);'.format(self.myRigBonesT.values()[17], name3))
        mel.eval('setCharacterObject("{}","{}",3,0);'.format(self.myRigBonesT.values()[18], name3))
        mel.eval('setCharacterObject("{}","{}",4,0);'.format(self.myRigBonesT.values()[19], name3))
        mel.eval('setCharacterObject("{}","{}",16,0);'.format(self.myRigBonesT.values()[20], name3))
        mel.eval('setCharacterObject("{}","{}",5,0);'.format(self.myRigBonesT.values()[21], name3))
        mel.eval('setCharacterObject("{}","{}",6,0);'.format(self.myRigBonesT.values()[22], name3))
        mel.eval('setCharacterObject("{}","{}",7,0);'.format(self.myRigBonesT.values()[23], name3))
        mel.eval('setCharacterObject("{}","{}",17,0);'.format(self.myRigBonesT.values()[24], name3))
        mel.eval('setCharacterObject("{}","{}",8,0);'.format(self.myRigBonesT.values()[2], name3))
        mel.eval('setCharacterObject("{}","{}",23,0);'.format(self.myRigBonesT.values()[3], name3))
        mel.eval('setCharacterObject("{}","{}",24,0);'.format(self.myRigBonesT.values()[4], name3))
        mel.eval('setCharacterObject("{}","{}",25,0);'.format(self.myRigBonesT.values()[5], name3))
        mel.eval('setCharacterObject("{}","{}",26,0);'.format(self.myRigBonesT.values()[6], name3))
        mel.eval('setCharacterObject("{}","{}",20,0);'.format(self.myRigBonesT.values()[7], name3))
        mel.eval('setCharacterObject("{}","{}",15,0);'.format(self.myRigBonesT.values()[8], name3))

    #=================================================================
    # make cap rig drive my rig
    #=================================================================
    @my_decorator
    def hookMeUp(self, name1, name3):
        mel.eval('mayaHIKsetCharacterInput("{}","{}");'.format(name3, name1))

        
    #=================================================================
    # import my FullRig 
    #=================================================================
    @my_decorator
    def loader(self, inPath, rigVersion):
        cmds.file(inPath + rigVersion, i=True, f=True)

    #=================================================================
    # contraint to HIK stripped down version
    #=================================================================        
    @my_decorator
    def stickToRig(self, a="T"):
        lElbow = pm.xform("l_elbow1_JNT", query=True, ws=True, t=True)
        rElbow = pm.xform("r_elbow1_JNT", query=True, ws=True, t=True)
        lKnee = pm.xform("l_knee1_JNT", query=True, ws=True, t=True)
        rKnee = pm.xform("r_knee1_JNT", query=True, ws=True, t=True)
        pm.xform("moCap_l_armPv_CTRL", ws=True, t=lElbow)
        pm.xform("moCap_r_armPv_CTRL", ws=True, t=rElbow)
        pm.xform("moCap_l_legPv_CTRL", ws=True, t=lKnee)
        pm.xform("moCap_r_legPv_CTRL", ws=True, t=rKnee)

        pm.pointConstraint("l_hand1_" + a + "_JNT", "moCap_l_armmainIk_CTRL")
        pm.orientConstraint("l_hand1_" + a + "_JNT", "moCap_l_armmainIk_CTRL")
        pm.pointConstraint("r_hand1_" + a + "_JNT", "moCap_r_armmainIk_CTRL")
        pm.orientConstraint("r_hand1_" + a + "_JNT", "moCap_r_armmainIk_CTRL")
        pm.pointConstraint("spine1_" + a + "_JNT", "moCap_spineHips_CTRL")
        pm.orientConstraint("spine1_" + a + "_JNT", "moCap_spineHips_CTRL", mo=True)
        pm.pointConstraint("l_foot1_" + a + "_JNT", "moCap_l_legmainIk_CTRL")
        pm.orientConstraint("l_foot1_" + a + "_JNT", "moCap_l_legmainIk_CTRL", mo=True)
        pm.pointConstraint("r_foot1_" + a + "_JNT", "moCap_r_legmainIk_CTRL")
        pm.orientConstraint("r_foot1_" + a + "_JNT", "moCap_r_legmainIk_CTRL", mo=True)
        pm.pointConstraint("l_knee1_" + a + "_JNT", "moCap_l_legPv_CTRL")
        pm.orientConstraint("l_knee1_" + a + "_JNT", "moCap_l_legPv_CTRL", mo=True)
        pm.pointConstraint("r_knee1_" + a + "_JNT", "moCap_r_legPv_CTRL")
        pm.orientConstraint("r_knee1_" + a + "_JNT", "moCap_r_legPv_CTRL", mo=True)
        pm.pointConstraint("spine5_" + a + "_JNT", "moCap_spineChestCtrl_CTRL")
        pm.orientConstraint("spine5_" + a + "_JNT", "moCap_spineChestCtrl_CTRL", mo=True)
        pm.pointConstraint("l_clavicle1_" + a + "_JNT", "moCap_l_armClavicle_CTRL")
        pm.orientConstraint("l_clavicle1_" + a + "_JNT", "moCap_l_armClavicle_CTRL", mo=True)
        pm.pointConstraint("r_clavicle1_" + a + "_JNT", "moCap_r_armClavicle_CTRL")
        pm.orientConstraint("r_clavicle1_" + a + "_JNT", "moCap_r_armClavicle_CTRL", mo=True)
        pm.pointConstraint("neck1_" + a + "_JNT", "moCap_headMain_CTRL")
        pm.orientConstraint("neck1_" + a + "_JNT", "moCap_headMain_CTRL")
        pm.pointConstraint("l_elbow1_" + a + "_JNT", "moCap_l_armPv_CTRL")
        pm.orientConstraint("l_elbow1_" + a + "_JNT", "moCap_l_armPv_CTRL", mo=True)
        pm.pointConstraint("r_elbow1_" + a + "_JNT", "moCap_r_armPv_CTRL")
        pm.orientConstraint("r_elbow1_" + a + "_JNT", "moCap_r_armPv_CTRL", mo=True)

        pm.setAttr("l_armSwitch_CTRL.fkIkBlend", 1)
        pm.setAttr("r_armSwitch_CTRL.fkIkBlend", 1)
        pm.setAttr("r_armmainIk_CTO.rotateZ", 180)

    @my_decorator
    def link(self):
        allSourceChar = cmds.optionMenuGrp("hikSourceList", query=True, itemListLong=True)
        i=1
        for item in allSourceChar:
            print item
            optMenu = "hikSourceList|OptionMenu"
            sourceChar = cmds.menuItem(item, query=True, label=True)
            print "------>" + sourceChar
            
            if sourceChar == " capRig":
                cmds.optionMenu(optMenu, edit=True, select=i)
                mel.eval('hikUpdateCurrentSourceFromUI()')
                mel.eval('hikUpdateContextualUI()')
                mel.eval('hikControlRigSelectionChangedCallback')
                break
                    
            i+=1

    #=============================================================
    # engage
    #=============================================================
    @my_decorator
    def makeItSo(self, inPath, rigVersion, jsonPath):
        self.jsonImport(jsonPath)
        self.linkWrchHIK(name1="wrchRig")
        #self.linkWrchTHIK(name4="wrchTRig")
        #self.linkmyRigHIK(name2="myRig")
        self.linkmyRigTHIK(name3="myRigT")
        self.hookMeUp(name1="wrchRig", name3="myRigT")  
        self.loader(inPath, rigVersion)
        self.stickToRig()
    
    @my_decorator
    def link(self):
        allSourceChar = cmds.optionMenuGrp("hikSourceList", query=True, itemListLong=True)
        i=1
        for item in allSourceChar:
            print item
            optMenu = "hikSourceList|OptionMenu"
            sourceChar = cmds.menuItem(item, query=True, label=True)
            print "------>" + sourceChar
            
            if sourceChar == " capRig":
                cmds.optionMenu(optMenu, edit=True, select=i)
                mel.eval('hikUpdateCurrentSourceFromUI()')
                mel.eval('hikUpdateContextualUI()')
                mel.eval('hikControlRigSelectionChangedCallback')
                break
                    
            i+=1
    
    #inPath = r"D:\sgScripts\project\dave\rig"
    #rigVersion = "\\001_dave_sgRig_v016.ma"

