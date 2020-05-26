import maya.cmds as cmds
import maya.mel as mel

def link():
    allSourceChar = cmds.optionMenuGrp("hikSourceList", query=True, itemListLong=True)
    i=1
    for item in allSourceChar:
        print " - - - - - - - - " + item
        optMenu = "hikSourceList|OptionMenu"
        sourceChar = cmds.menuItem(item, query=True, label=True)
        print "------->" + sourceChar
        
        if sourceChar == " capRig":
            cmds.optionMenu(optMenu, edit=True, select=i)
            mel.eval('hikUpdateCurrentSourceFromUI()')
            mel.eval('hikUpdateContextualUI()')
            mel.eval('hikControlRigSelectionChangedCallback')
            break
                
        i+=1
        