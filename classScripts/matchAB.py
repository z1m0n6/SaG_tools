"""
match characters in scene 
"""

import maya.cmds as cmds
import pymel.core as pm
import wrappers
from collections import OrderedDict

class AtoB(object):

        @wrappers.timeTaken
        def matchAB(self):

                keys = ["moCap_spineChestCtrl_vA_CTRL",
                        "moCap_spineHips_vA_CTRL",
                        "moCap_l_legmainIk_vA_CTRL",
                        "moCap_r_legmainIk_vA_CTRL",
                        "moCap_l_armmainIk_vA_CTRL",
                        "moCap_r_armmainIk_vA_CTRL",
                        "moCap_l_armPv_vA_CTRL",
                        "moCap_r_armPv_vA_CTRL",
                        "moCap_l_armClavicle_vA_CTRL",
                        "moCap_r_armClavicle_vA_CTRL",
                        "moCap_l_legPv_vA_CTRL",
                        "moCap_r_legPv_vA_CTRL",
                        "moCap_headMain_vA_CTRL",
                        "headMain_vA_CTRL",
                        ]
                
                values = ["moCap_spineChestCtrl_vB_CTRL",
                        "moCap_spineHips_vB_CTRL",
                        "moCap_l_legmainIk_vB_CTRL",
                        "moCap_r_legmainIk_vB_CTRL",
                        "moCap_l_armmainIk_vB_CTRL",
                        "moCap_r_armmainIk_vB_CTRL",
                        "moCap_l_armPv_vB_CTRL",
                        "moCap_r_armPv_vB_CTRL",
                        "moCap_l_armClavicle_vB_CTRL",
                        "moCap_r_armClavicle_vB_CTRL",
                        "moCap_l_legPv_vB_CTRL",
                        "moCap_r_legPv_vB_CTRL",
                        "moCap_headMain_vB_CTRL",
                        "headMain_vB_CTRL",
                        ] 
                        
                #connections = OrderedDict(sorted(zip(keys, values)))
                # or
                connections = dict(zip(keys, values))
                for k,v in connections.items():
                        pos = pm.xform(v, query=True, ws=True, matrix=True)
                        pm.xform(k, ws=True, matrix=pos)
        

