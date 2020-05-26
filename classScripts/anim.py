"""
anim class for copy and pasting animation keys. make sure you have no namespaces and not set driven keys
"""
import maya.cmds as cmds
import pymel.core as pm
import time

class AnimCopy(object):

	def my_decorator(func):
		def wrapper(*args, **kwargs):
			start = time.time()
			func(*args, **kwargs)
			end = time.time()
			print(str(func) + " > Time taken : ", end-start)
			#print("args are : ", args)
			#print("keyword args are : ", kwargs)
		return wrapper
	#===============================================================================================
	# copy animation
	#===============================================================================================
	@my_decorator	
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

	#===============================================================================================
	# paste animation
	#===============================================================================================

	import maya.cmds as cmds
	import pymel.core as pm

	def isKeyable(self, name):
	    keyable = False
	    if pm.getAttr(name, lock=True)==False and pm.listConnections(name, source=True, destination=False, skipConversionNodes=True)!=None:
	        keyable = True
		return keyable

	@my_decorator
	def pasteAnim(self, filename, locName):
		# imports	
		cmds.file(filename + "\\" + locName + ".ma", i=True, type="mayaAscii", ignoreVersion=True, rpr="animExport", mergeNamespacesOnClash=False, pr=True)
		
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

		print "Success!"  

# IF YOU NEED TO CHANGE THE NAME	
		
	@my_decorator
	def pasteAnimPlusRename(self, filename, locName, version):
		# imports	
		cmds.file(filename + "\\" + locName + ".ma", i=True, type="mayaAscii", ignoreVersion=True, rpr="animExport", mergeNamespacesOnClash=False, pr=True)
		
		locAttrList = cmds.listAttr(locName, keyable=True)

		for locAttr in locAttrList:
			item = locAttr.split("___")[0]
			old = item.rpartition("_")
			new = old[0] + version + old[-1]
			objName = new

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

		print "Success!"   
