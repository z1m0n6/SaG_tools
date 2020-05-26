"""
anim class for copy and pasting animation keys. make sure you have no namespaces and not set driven keys
"""
import maya.cmds as cmds
import pymel.core as pm
import time

class AnimCopy(object):

	#self.__init__.doesItWirk()

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
	def copyAnim(self, filename, capture, locName):
	    if pm.objExists(locName)==False:
	        sourceLOC = pm.spaceLocator(name=locName)
	    for item in ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"]:
	        pm.setAttr((locName + "." + item), lock=True, keyable=False)
	        
	    ## get list of keyable attributes and connections

	    ctlList = pm.ls(capture)
	         
	    for ctl in ctlList:
	        attrList = pm.listAttr(ctl, unlocked=True, keyable=True)
	        if attrList != None:
	            for attr in attrList:
	                if pm.objExists(sourceLOC + "." + ctl + "___" + attr)==False:
	                    pm.addAttr(sourceLOC, longName=(ctl + "___" + attr), attributeType="double")
	                    pm.setAttr((sourceLOC + "." + ctl + "___" + attr), keyable=True)
	                connList = pm.listConnections((ctl + "." + attr), source=True, destination=False)
	                if connList==None:
	                    pm.setAttr((sourceLOC + "." + ctl + "___" + attr), pm.getAttr(ctl + "___" + attr))
	                else:
	                    for conn in connList:
	                        if "animCurve" in pm.nodeType(conn):
	                            print (ctl + "." + attr + " has animation attached to it")
	                            pm.connectAttr((conn + ".output"), (sourceLOC + "." + ctl + "___" + attr))
	                            
	    print "----SUCCESS----"

	    pm.select(sourceLOC, replace=True)
	    cmds.file(filename + "\\" + locName, type="mayaAscii", force=True, exportSelected=True)

	@timeTaken	
	def copyAnimBones(self):
	    locName = "source_LOC"
	    if pm.objExists(locName)==False:
	        sourceLOC = pm.spaceLocator(name=locName)
	    for item in ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"]:
	        pm.setAttr((locName + "." + item), lock=True, keyable=False)
	        

	    ## get list of keyable attributes and connections

	    boneList = pm.listRelatives("moCapSource", allDescendents=True, type="joint")
	         
	    for bone in boneList:
	        attrList = pm.listAttr(bone, unlocked=True, keyable=True)
	        if attrList != None:
	            for attr in attrList:
	                if pm.objExists(sourceLOC + "." + bone + "___" + attr)==False:
	                    pm.addAttr(sourceLOC, longName=(bone + "___" + attr), attributeType="double")
	                    pm.setAttr((sourceLOC + "." + bone + "___" + attr), keyable=True)
	                connList = pm.listConnections((bone + "." + attr), source=True, destination=False)
	                if connList==None:
	                    pm.setAttr((sourceLOC + "." + bone + "___" + attr), pm.getAttr(bone + "___" + attr))
	                else:
	                    for conn in connList:
	                        if "animCurve" in pm.nodeType(conn):
	                            print (bone + "." + attr + " has animation attached to it")
	                            pm.connectAttr((conn + ".output"), (sourceLOC + "." + bone + "___" + attr))
	                            

	    print "----SUCCESS----"

	    filename = r"C:\Users\SimonG\Documents\maya\projects\default\data\source_LOC.ma"
	    pm.select(sourceLOC, replace=True)
	    cmds.file(filename, type="mayaAscii", force=True, exportSelected=True)

	import maya.cmds as cmds
	import pymel.core as pm

	def isKeyable(self, name):
	    keyable = False
	    if pm.getAttr(name, lock=True)==False and pm.listConnections(name, source=True, destination=False, skipConversionNodes=True)!=None:
	        keyable = True
		return keyable
		

	@timeTaken
	def pasteAnim(self):
		#rename bonlist
		boneList = pm.listRelatives("moCapSource", allDescendents=True, type="joint")
		for x in boneList:
			oldName= x.split()
			newName= oldName[0] + "_ORIG"
			pm.rename(oldName, newName)
		# imports	
		inPath = r"C:\Users\SimonG\Documents\maya\projects\default\data\baseCaptuary.ma"
		cmds.file(inPath , i=True, f=True)
		filename = r"C:\Users\SimonG\Documents\maya\projects\default\data\source_LOC.ma"
		cmds.file(filename, i=True, type="mayaAscii", ignoreVersion=True, rpr="animExport", mergeNamespacesOnClash=False, pr=True)
		
		locName = "source_LOC"
		locAttrList = cmds.listAttr(locName, keyable=True)

		for locAttr in locAttrList:
			objName = locAttr.split("___")[0]
			attrName = locAttr.split("___")[1]
	        
			if cmds.objExists(objName + "." + attrName):
				print (locName + "." + locAttr)
				connList = cmds.listConnections(locName + "." + locAttr, source=True, destination=False, skipConversionNodes=True)
				if self.isKeyable(objName + "." + attrName):
					if connList != None:
						if "animCurve" in cmds.nodeType(connList[0]):
							cmds.connectAttr((connList[0] + ".output"), (objName + "." + attrName))
						else:
							value = pm.getAttr(locName + "." + locAttr)
							pm.setAttr((objName + "." + attrName), value)
							print (objName + "." + attrName)
				else:
					print (objName + "." + attrName + " has connections incoming or is locked!  skipping....")                        
			else:
				print ("cant find " + objName + "." + attrName + " in the scene !    Skipping....")

		if cmds.objExists(locName):
			cmds.delete(locName)
		
		# rename target joints
		boneList = pm.listRelatives("targetSource", allDescendents=True, type="joint")
		for x in boneList:
			oldName= x.split()
			newName= oldName[0] + "_TARGET"
			pm.rename(oldName, newName)

		print "Success!"   
