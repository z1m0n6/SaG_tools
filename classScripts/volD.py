"""
Volume tracking tool for use with Volumetric data sets consisting of constantly chinging vtx order.
(c) copyright June 2018, Usage by licene from sgoodchild@hotmail.com
"""

import pymel.core as pm
import maya.cmds as cmds

class VolTrk(object):

    def polygonVolume(self, a, volume=0, ch=False):

        deformer = pm.textureDeformer(a)[0]
        deformer.texture.set([1,1,1])
        deformer.pointSpace.set(1)
        deformer.direction.set(2)
        deformer.vectorSpace.set(2)
        deformer.vectorStrength.set([0,volume,0])
        if not ch:
            pm.delete(a,ch=True)

    def intersections(self, a, b):

        bDoutside = pm.duplicate(b,n="tmpBDoutside")[0]
        bDinside = pm.duplicate(b,n="tmpBDinside")[0]

        aCopyDupe = pm.duplicate(a,n="aCopyDupe")[0]

        dupes = [bDoutside, bDinside, aCopyDupe, ]

        for dupe in dupes:
            dupe.setParent(w=True)

        self.polygonVolume(bDinside, -.005)

        pm.polyColorPerVertex(bDinside,r=1,g=0,b=0,a=1,cdo=1)
        pm.polyColorPerVertex(bDoutside,r=0,g=0,b=0,a=1,cdo=1)
        bColoured = pm.polyUnite(bDoutside,bDinside,ch=False)[0]

        bColoured.setParent(w=True)
        pm.delete(bColoured,ch=True)

        pm.transferAttributes(bColoured,aCopyDupe,
                              sourceColorSet="colorSet1",
                              targetColorSet="colorSet1",
                              transferColors=True,
                              sampleSpace=0,
                              colorBorders=1)

        pm.delete(aCopyDupe,ch=True)
        pm.delete(bColoured)
        aVerts = [str(a)+".vtx["+x.split("[")[-1].split("]")[0]+"]" for x in cmds.ls(str(aCopyDupe)+".vtx[*]",fl=1) if cmds.polyColorPerVertex(x,q=1,rgb=1)[0] < .51]
        #bVerts = [str(b)+".vtx["+x.split("[")[-1].split("]")[0]+"]" for x in cmds.ls(str(bCopyDupe)+".vtx[*]",fl=1) if cmds.polyColorPerVertex(x,q=1,rgb=1)[0] < .51]

        pm.delete(aCopyDupe)

        sel = pm.select(aVerts)
        selVerts = pm.ls(sl=True)
        pm.select(a)
        Verts = pm.select( pm.polyListComponentConversion( tv=True ) )
        allVerts = pm.ls(sl=True)
        pm.select(allVerts)
        pm.select(selVerts, d=True)

    def trackIt(self, a, b):    
        first_frame = int(cmds.playbackOptions( query = True, minTime = True ))
        last_frame = int(cmds.playbackOptions( query = True, maxTime = True ))
        loc = pm.spaceLocator(name="sgSuperTracker")
        for frame in range (first_frame, last_frame+1): 
            cmds.currentTime(frame, edit=True)
            self.intersections(a, b)
            sel = pm.ls(sl=True)
            bb = pm.exactWorldBoundingBox(sel)
            pos = ((bb[0] + bb[3]) / 2, (bb[1] + bb[4]) / 2, (bb[2] + bb[5]) / 2)
            pm.xform ("sgSuperTracker", ws=True, t=pos)
            pm.setKeyframe("sgSuperTracker" + ".translate")
            pm.select(clear=True)

    def makeItSo(self, a, b):
        self.trackIt(a, b)