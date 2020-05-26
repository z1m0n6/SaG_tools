from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import os
import sgIKFKMatch
reload(sgIKFKMatch)

def maya_main_window():
    """
    Return the Maya window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)
    
class OpenImportDialog(QtWidgets.QDialog):
    
    FILE_FILTERS = "Maya (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;FBX (*.fbx);;All Files (*.*)"
    
    selected_filter = "FBX (*.fbx)"
    
    def __init__(self, parent=maya_main_window()):
        super(OpenImportDialog, self).__init__(parent)
        
        self.setWindowTitle("MatchMe")
        self.setMinimumSize(600, 80)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        
        self.create_widgets()
        self.create_layout()
        self.create_connections()
        
    def create_widgets(self):
        self.filepath_le = QtWidgets.QLineEdit()
        
        self.open_rb = QtWidgets.QRadioButton("Open")
        self.open_rb.setChecked(True)
        
        self.force_cb = QtWidgets.QCheckBox("Force")

        self.filepath2_le = QtWidgets.QLineEdit()

        self.filepath3_le = QtWidgets.QLineEdit()

        self.filepath4_le = QtWidgets.QLineEdit()
        
        self.apply_btn = QtWidgets.QPushButton("Apply")
        self.close_btn = QtWidgets.QPushButton("Close")

    def create_layout(self):
        file_path_layout = QtWidgets.QHBoxLayout()
        file_path_layout.addWidget(self.filepath_le)

        radio_btn_layout = QtWidgets.QHBoxLayout()
        radio_btn_layout.addWidget(self.open_rb)

        file_path_layout2 = QtWidgets.QHBoxLayout()
        file_path_layout2.addWidget(self.filepath2_le)

        file_path_layout3 = QtWidgets.QHBoxLayout()
        file_path_layout3.addWidget(self.filepath3_le)

        file_path_layout4 = QtWidgets.QHBoxLayout()
        file_path_layout4.addWidget(self.filepath4_le)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("IK_CTRL:", file_path_layout)

        form_layout.addRow("side:", file_path_layout2)

        form_layout.addRow("arm:", file_path_layout3)

        form_layout.addRow("leg:", file_path_layout4)

        form_layout.addRow("", radio_btn_layout)
        form_layout.addRow("", self.force_cb)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.apply_btn)
        button_layout.addWidget(self.close_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        
    def create_connections(self):
        
        self.apply_btn.clicked.connect(self.load_file)
        self.close_btn.clicked.connect(self.close)

    def update_force_visibility(self, checked):
        self.force_cb.setVisible(checked)
        
    def load_file(self):
        file_path = self.filepath_le.text()
        if not file_path:
            return

        file_path2 = self.filepath2_le.text()
        if not file_path2:
            return

        file_path3 = self.filepath3_le.text()
        if not file_path3:
            return

        file_path4 = self.filepath4_le.text()
        if not file_path4:
            return

        file_path_layout = self.filepath_le.text()
        if not file_path:
            return

        file_path_layout2 = self.filepath2_le.text()
        if not file_path2:
            return

        file_path_layout3 = self.filepath3_le.text()
        if not file_path3:
            return

        file_path_layout4 = self.filepath4_le.text()
        if not file_path4:
            return
            
        file_info = QtCore.QFileInfo(file_path)
        if not file_info.exists():
            om.MGlobal.displayError("File does not exist: {0}".format(file_path))
            return
        
        if self.open_rb.isChecked():
            self.matchPose(file_path, file_path2, file_path3, file_path4)
        else:
            pass
        
    def matchPose(self, file_path, file_path2, file_path3, file_path4):

        ikfk = sgIKFKMatch.SgIKFKMatch()
        ikfk.IKFKMatch(
                ik_CTRL = file_path,
                side = file_path2,
                arm = file_path3,
                foot = file_path4
                )
        
if __name__ == "__main__":
    
    try:
        open_import_dialog.close() 
        open_import_dialog.deleteLater()
    except:
        pass
    
    open_import_dialog = OpenImportDialog()
    open_import_dialog.show()

