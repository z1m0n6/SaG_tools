"""
class for linking limbs to auto controllers
"""
import pymel.core as pm

def prep():
    # create locators and parent to each limb
    topBot = ["l_legLowerTwistPart_3_JNT",
            "l_legUpperTwistPart_3_JNT",
            "r_legLowerTwistPart_3_JNT",
            "r_legUpperTwistPart_3_JNT",
            "l_armUpperTwistPart_3_JNT",
            "l_armLowerTwistPart_3_JNT",
            "r_armUpperTwistPart_3_JNT",
            "r_armLowerTwistPart_3_JNT"]
            
    for num,x in enumerate(topBot):
        oldName = x.split("_")
        newName = oldName[0] + "_" + oldName[1] + "_" + str(num) + "_GRP"
        newName2 = oldName[0] + "_" + oldName[1] + "_" + str(num) + "_LOC"
        grp = pm.group(em=1, n=newName)
        loc = pm.spaceLocator(n=newName2)
        pm.parent(loc, grp)
        pos = pm.xform(x, q=1, ws=1, matrix=True)
        pm.xform(grp, ws=1, matrix=pos)
    
    offsetGRPS = ["l_legLowerTwistPart_0_GRP",
            "l_legUpperTwistPart_1_GRP",
            "r_legLowerTwistPart_2_GRP",
            "r_legUpperTwistPart_3_GRP",
            "l_armUpperTwistPart_4_GRP",
            "l_armLowerTwistPart_5_GRP",
            "r_armUpperTwistPart_6_GRP",
            "r_armLowerTwistPart_7_GRP"]
    
    for x, y in sorted(zip(topBot, offsetGRPS)):
        pm.parent(y,x)
        
    # move out from parent joint 10 units    
    for x in offsetGRPS[0:4]:
        pm.setAttr(x + ".visibility", 1)
        locs = pm.listRelatives(x, children=True, type="transform")
        for y in locs:
            pm.setAttr(y + ".translateZ", 10)
    for x in offsetGRPS[4:8]:
        pm.setAttr(x + ".visibility", 1)
        locs = pm.listRelatives(x, children=True, type="transform")
        for y in locs:
            if y.startswith("l"):
                pm.setAttr(y + ".translateY", -10)
            else:
                pm.setAttr(y + ".translateY", 10)
                
    limbGuide = r"E:\sgScripts\project\roboto\guide\limbCaps.ma"           
    cmds.file(limbGuide, i=1, dns=1)
    
def runLimbsSetup():
    #=========================================================
    # import code
    #=========================================================
    import robotLimbCaps
    reload(robotLimbCaps)
    limb = robotLimbCaps.Limbs()
    
    #=========================================================
    # run code on character example 1
    #=========================================================
    limb.makeItSo(
            limbJoint = "l_knee1_JNT",
            limbLocs = ["l_kneeCap_bot_GUIDE", "l_kneeCap_top_GUIDE"],
            capEnds = ["l_knee1_capEnd_0_JNT", "l_knee1_capEnd_1_JNT"],
            cons = ["l_legLowerTwistPart_0_LOC", "l_legUpperTwistPart_1_LOC"],
            capEndsLOC = ["l_knee1_capEnd_0_GRP", "l_knee1_capEnd_1_GRP"],
            parentCons = [".l_legUpperTwistPart_1_LOCW1", ".l_legLowerTwistPart_0_LOCW0"]
            )
            
    limb.makeItSo(
            limbJoint = "r_knee1_JNT",
            limbLocs = ["r_kneeCap_bot_GUIDE", "r_kneeCap_top_GUIDE"],
            capEnds = ["r_knee1_capEnd_0_JNT", "r_knee1_capEnd_1_JNT"],
            cons = ["r_legLowerTwistPart_2_LOC", "r_legUpperTwistPart_3_LOC"],
            capEndsLOC = ["r_knee1_capEnd_0_GRP", "r_knee1_capEnd_1_GRP"],
            parentCons = [".r_legUpperTwistPart_3_LOCW1", ".r_legLowerTwistPart_2_LOCW0"]
            )
            
    limb.makeItSo(
            limbJoint = "l_elbow1_JNT",
            limbLocs = ["l_elbow_bot_GUIDE", "l_elbow_top_GUIDE"],
            capEnds = ["l_elbow1_capEnd_0_JNT", "l_elbow1_capEnd_1_JNT"],
            cons = ["l_armUpperTwistPart_4_LOC", "l_armLowerTwistPart_5_LOC"],
            capEndsLOC = ["l_elbow1_capEnd_0_GRP", "l_elbow1_capEnd_1_GRP"],
            parentCons = [".l_armUpperTwistPart_4_LOCW0", ".l_armLowerTwistPart_5_LOCW1"]
            )
        
    limb.makeItSo(
            limbJoint = "r_elbow1_JNT",
            limbLocs = ["r_elbow_bot_GUIDE", "r_elbow_top_GUIDE"],
            capEnds = ["r_elbow1_capEnd_0_JNT", "r_elbow1_capEnd_1_JNT"],
            cons = ["r_armUpperTwistPart_6_LOC", "r_armLowerTwistPart_7_LOC"],
            capEndsLOC = ["r_elbow1_capEnd_0_GRP", "r_elbow1_capEnd_1_GRP"],
            parentCons = [".r_armUpperTwistPart_6_LOCW0", ".r_armLowerTwistPart_7_LOCW1"]
            )
prep()
runLimbsSetup()