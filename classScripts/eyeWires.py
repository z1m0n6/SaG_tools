"""
link the wires
"""
import maya.cmds as cmds
import pymel.core as pm
import maya.OpenMaya as OpenMaya
import time


def my_decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(str(func) + " >>>>>>> Time taken : ", end-start)
    return wrapper

@my_decorator
def onAWire(locs, crv):
    locs = pm.listRelatives(locs, children=True, type="transform")
    crv = crv 
    for x in locs:
        pos = pm.xform(x, q=1, ws=1, t=1)
        u = getUParam(pos, crv)
        #create point on curve node. Make sure Locators have suffix of _LOX
        name= x.replace("_LOC", "_PCI")
        pci = pm.createNode("pointOnCurveInfo", n=name)
        pm.connectAttr(crv + ".worldSpace", pci + ".inputCurve")
        pm.setAttr(pci + ".parameter", u)
        pm.connectAttr(pci + ".position", x + ".t")

def makeItSo(locs, crv):
    onAWire(locs, crv)