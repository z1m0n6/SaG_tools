"""
make versions of import
"""

import maya.cmds as cmds
import pymel.core as pm
import time

class MakeVersions(object):

    def timeTaken(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            func(*args, **kwargs)
            end = time.time()
            print(str(func) + " > Time taken : ", end-start)
            #print("args are : ", args)
            #print("keyword args are : ", kwargs)
        return wrapper

    @timeTaken
    def versionUP(self, name, version):

        list = pm.ls(
                    "*_CTO",
                    "*_CTRL",
                    "*_GRP",
                    "*_JNT",
                    "*_LOC",
                    "*_PLY",
                    "_grp",
                    "*_GOFF",
                    "*_fol",
                    "*CTO_*",
                    "*GOFF_*",
                    "*_poseOffset",
                    "*GRP_*",
                    "*IKH_*",
                    "*_ikh",
                    "*_crv",
                    "*JNT_"
                    )
        char = name + "_rig_GRP"

        if pm.objExists(char):
            for x in list:
                new=x.rpartition("_")
                modified=new[0] + "_v" + version + "_" + new[-1]
                pm.rename(x, modified)
