"""
class for linking limbs to auto controllers
"""

import pymel.core as pm
import time

joints1 = []
joints2 = []
limbGRP = []
xGRP = []

class Limbs(object):

    def timeTaken(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            func(*args, **kwargs)
            end = time.time()
            print(str(func) + " > Time taken : ", end-start)
        return wrapper

    @timeTaken    
    def limbCapsControl(self, limbJoint, limbLocs):            
        for num, x in enumerate(limbLocs):
            oldname = limbJoint.split("_")
            newname = oldname[0] + "_" + oldname[1] + "_cap_" + str(num) + "_" + oldname[2]
            newname2 = oldname[0] + "_" + oldname[1] + "_cap_" + str(num) + "_GRP"
            jnt = pm.createNode("joint", n=newname)
            grp = pm.group(n=newname2)
            pos1 = pm.xform(limbJoint, q=1, ws=1, matrix=1)
            pm.xform(grp, ws=1, matrix=pos1)
            joints1.append(jnt)
            limbGRP.append(grp)
            pm.parent(grp, limbJoint)

        for num, x in enumerate(limbLocs):
            oldname = limbJoint.split("_")
            newname = oldname[0] + "_" + oldname[1] + "_capEnd_" + str(num) + "_" + oldname[2]
            jnt2 = pm.createNode("joint", n=newname)
            pos1 = pm.xform(x, q=1, ws=1, matrix=1)
            pm.xform(jnt2, ws=1, matrix=pos1)
            joints2.append(jnt2)
        
        for x, y in sorted(zip(joints1, joints2)):
            pm.parent(y,x)
        for x in joints1:
            pm.joint(x, e=True,  oj="none", zso=True)
        for x in joints1:
            pm.joint(x, e=True,  oj="xyz", zso=True)
        for x in joints2:
            pm.joint(x, e=True,  oj="none", ch=True, zso=True)
            
    @timeTaken        
    def controlObjs(self, capEnds):   
        for x in capEnds:
            oldname = x.split("_")
            newname = oldname[0] + "_" + oldname[1] + "_" + oldname[2] + "_" + oldname[3]
            pos = pm.xform(x, q=1, ws=1, matrix=True)
            loc = pm.spaceLocator(name=newname + "_LOC")
            grp2 = pm.group(name=newname + "_GRP")
            pm.parent(loc, grp2)
            pm.xform(grp2, ws=1, matrix=pos)
            xGRP.append(grp2)

        for x, y in sorted(zip(xGRP, limbGRP)):
            pm.parent(x,y)

    @timeTaken    
    def openCons(self, capEnds, capEndsLOC, cons, parentCons):
        for x in capEndsLOC:
            pm.parentConstraint(cons, x, mo=1)
        endLoc = pm.listRelatives(capEndsLOC, allDescendents=True, type="transform")
        endLoc2 = pm.ls(endLoc[0], endLoc[2])
        orinetJnts = pm.listRelatives(capEnds, parent=True, type="transform")
        for x, y in sorted(zip(orinetJnts, endLoc2)):
            pm.orientConstraint(y,x)
        for x, y in sorted(zip(capEndsLOC, parentCons)):
            pm.setAttr(x + "_parentConstraint1" + y, .3)

    @timeTaken 
    def cleanUp(self, limbLocs, cons, capEndsLOC):
        pm.delete(limbLocs)
        for x in cons:
            pm.setAttr(x + ".visibility", 0)
        above = pm.listRelatives(capEndsLOC, parent=True, type="transform")
        for x in above:
            pm.setAttr(x + ".visibility", 0)

    def makeItSo(self, limbJoint, limbLocs, capEnds, capEndsLOC, cons, parentCons):
        self.limbCapsControl(limbJoint, limbLocs),
        self.controlObjs(capEnds),
        self.openCons(capEnds, capEndsLOC, cons, parentCons),
        self.cleanUp(limbLocs, cons, capEndsLOC)

