import sgIKFKvMatch
reload(sgIKFKvMatch)

ikfk = sgIKFKvMatch.SgIKFKMatch()

ikfk.IKFKMatch(ik_CTRL="l_armmainIk_vA_CTRL", side="l", version="A", arm=True, foot=False)
ikfk.IKFKMatch(ik_CTRL="r_armmainIk_vA_CTRL", side="r", version="A", arm=True, foot=False)
ikfk.IKFKMatch(ik_CTRL="l_legmainIk_vA_CTRL", side="l", version="B", arm=False, foot=True)
ikfk.IKFKMatch(ik_CTRL="r_legmainIk_vA_CTRL", side="r", version="A", arm=False, foot=True)

ikfk.IKFKMatch(ik_CTRL="l_armmainIk_vB_CTRL", side="l", version="B", arm=True, foot=False)
ikfk.IKFKMatch(ik_CTRL="r_armmainIk_vB_CTRL", side="r", version="B", arm=True, foot=False)
ikfk.IKFKMatch(ik_CTRL="l_legmainIk_vB_CTRL", side="l", version="B", arm=False, foot=True)
ikfk.IKFKMatch(ik_CTRL="r_legmainIk_vB_CTRL", side="r", version="B", arm=False, foot=True)


ikfk.FKIKMatch("l_armFk_1_CTRL", "l_shoulder1_JNT")
ikfk.FKIKMatch("l_armFk_2_CTRL", "l_elbow1_JNT")
ikfk.FKIKMatch("l_armFk_3_CTRL", "l_hand1_JNT")

import pymel.core as pm
ctrls = pm.ls("moCap_*_vA_CTRL")
pm.select(ctrls)

ctrlsA = pm.ls("l_armmainIk_vA_CTRL", "r_armmainIk_vA_CTRL", "l_legmainIk_vA_CTRL", "r_legmainIk_vA_CTRL")
pm.select(ctrlsA)

ctrlsB = pm.ls("l_armmainIk_vB_CTRL", "r_armmainIk_vB_CTRL", "l_legmainIk_vB_CTRL", "r_legmainIk_vB_CTRL")
pm.select(ctrlsB)

ab = "_vA"
pm.setAttr("r_legSwitch" + ab + "_CTRL.fkIkBlend", 0)
pm.setAttr("r_armSwitch" + ab + "_CTRL.fkIkBlend", 0)
pm.setAttr("l_armSwitch" + ab + "_CTRL.fkIkBlend", 0)
pm.setAttr("l_legSwitch" + ab + "_CTRL.fkIkBlend", 0)
ab = "_vB"
pm.setAttr("r_legSwitch" + ab + "_CTRL.fkIkBlend", 1)
pm.setAttr("r_armSwitch" + ab + "_CTRL.fkIkBlend", 1)
pm.setAttr("l_armSwitch" + ab + "_CTRL.fkIkBlend", 1)
pm.setAttr("l_legSwitch" + ab + "_CTRL.fkIkBlend", 1)