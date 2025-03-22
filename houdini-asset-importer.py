import hou
import os

from PySide2.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QCheckBox, QLineEdit, QLabel
from PySide2.QtCore import Qt

class AssetLoader(QWidget):
    def __init__(self):
        super().__init__(None, Qt.WindowStaysOnTopHint)
        
        # general setup
        self.setWindowTitle("Asset Loader")
        self.resize(500, 400)
        
        # ui elements
        self.spacer = QLabel()
        
        self.geometryNetworkNameLabel = QLabel("Geometry Network Name")
        self.geometryNetworkNameText = QLineEdit()
        self.geometryNetworkNameText.textChanged.connect(self.handleCheckNetworkName)
        self.geometryNetworkNameLayout = QHBoxLayout()
        self.geometryNetworkNameLayout.addWidget(self.geometryNetworkNameLabel)
        self.geometryNetworkNameLayout.addWidget(self.geometryNetworkNameText)
        
        self.selectAssetsButton = QPushButton("Select Assets")
        self.selectAssetsButton.clicked.connect(self.handleSelectAssets)
        self.clearListButton = QPushButton("Clear List")
        self.clearListButton.clicked.connect(self.handleClearList)
        self.selectAssetsLayout = QHBoxLayout()
        self.selectAssetsLayout.addWidget(self.selectAssetsButton)
        self.selectAssetsLayout.addWidget(self.clearListButton)
        
        self.assetListTextEdit = QTextEdit()
        self.assetListTextEdit.setReadOnly(True)

        self.prependCheckbox = QCheckBox("Prepend to asset name")
        self.prependCheckbox.clicked.connect(self.handlePrepend)
        self.prependText = QLineEdit()
        self.prependText.setEnabled(False)
        self.prependText.textChanged.connect(self.handleAssetTextChange)
        self.prependLayout = QHBoxLayout()
        self.prependLayout.addWidget(self.prependCheckbox)
        self.prependLayout.addWidget(self.prependText)
        
        self.renameCheckbox = QCheckBox("Rename assets")
        self.renameCheckbox.clicked.connect(self.handleRename)
        self.renameText = QLineEdit()
        self.renameText.setEnabled(False)
        self.renameText.textChanged.connect(self.handleAssetTextChange)
        self.threePadCheckbox = QCheckBox("3 pad")
        self.threePadCheckbox.clicked.connect(self.handleThreePad)
        self.fourPadCheckbox = QCheckBox("4 pad")
        self.fourPadCheckbox.clicked.connect(self.handleFourPad)
        self.renameLayout = QHBoxLayout()
        self.renameLayout.addWidget(self.renameCheckbox)
        self.renameLayout.addWidget(self.renameText)
        self.renameLayout.addWidget(self.threePadCheckbox)
        self.renameLayout.addWidget(self.fourPadCheckbox)
        
        self.appendCheckbox = QCheckBox("Append to asset name")
        self.appendCheckbox.clicked.connect(self.handleAppend)
        self.appendText = QLineEdit()
        self.appendText.setEnabled(False)
        self.appendText.textChanged.connect(self.handleAssetTextChange)
        self.appendLayout = QHBoxLayout()
        self.appendLayout.addWidget(self.appendCheckbox)
        self.appendLayout.addWidget(self.appendText)
        
        self.organizeByLabel = QLabel("Organize by: ")
        self.singleGeometryCheck = QCheckBox("Single Geometry Node")
        self.multipleGeometryCheck = QCheckBox("Multiple Geometry Nodes")
        self.subnetCheck = QCheckBox("Subnets")
        
        self.loadAssetsButton = QPushButton("Load Assets")
        self.loadAssetsButton.clicked.connect(self.handleLoadAssets)
        
        # add elements to layout
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.geometryNetworkNameLayout)
        self.layout.addLayout(self.selectAssetsLayout)
        self.layout.addWidget(self.assetListTextEdit)
        self.layout.addWidget(self.spacer)
        self.layout.addLayout(self.prependLayout)
        self.layout.addLayout(self.renameLayout)
        self.layout.addLayout(self.appendLayout)
        self.layout.addWidget(self.spacer)
        self.layout.addWidget(self.spacer)
        self.layout.addWidget(self.loadAssetsButton)
        
        self.setLayout(self.layout)
        
        # styles
        self.spacer.setStyleSheet("font-size: 4px;")
        
        # internal class data
        self.paths = []
        self.originalFilenameListText = []
        self.originalAssetListText = []
        self.assetListText = []
        self.assetNames = []
        self.geometryNetworkName = "Assets"
        
    def updateAssetList(self):
        self.assetListTextEdit.setPlainText("")
        for item in self.assetListText:
            self.assetListTextEdit.append(item)
        
    def handleSelectAssets(self):        
        startDir = "C:\Working\HoudiniAssetManager\TestAssets"
        
        fileString = hou.ui.selectFile(start_directory=startDir, title="Select files", multiple_select=True)
        
        for file in fileString.split(" "):
            if file != ";":
                self.paths.append(file)
                filename = os.path.basename(file)
                asset = filename.split(".")[0]
                self.originalFilenameListText.append(filename)
                self.originalAssetListText.append(asset)
                self.assetNames.append(asset)
                
        self.handleAssetTextChange()
        
    def handleClearList(self):
        self.paths = []
        self.originalFilenameListText = []
        self.originalAssetListText = []
        self.assetListText = []
        self.assetNames = []
        self.handleAssetTextChange()
        
    def handleLoadAssets(self):
        if self.paths:
            context = hou.node("/obj")
            if self.geometryNetworkNameText.text():
                self.geometryNetworkName = self.geometryNetworkNameText.text()
            geometryNode = context.createNode("geo", self.geometryNetworkName)
            
            index = 0
            for file in self.paths:
                assetName = self.assetNames[index]
                
                fileNode = geometryNode.createNode("file")
                fileNode.parm("file").set(file)
                fileNode.parent().collapseIntoSubnet((fileNode,), subnet_name=assetName)
                index += 1
                
            geometryNode.layoutChildren()
            
    def handlePrepend(self):
        if self.prependCheckbox.isChecked():
            self.prependText.setEnabled(True)
            self.handleAssetTextChange()
        else:
            self.prependText.setEnabled(False)
            self.handleAssetTextChange()
            
    def handleRename(self):
        if self.renameCheckbox.isChecked():
            self.renameText.setEnabled(True)
            self.threePadCheckbox.setChecked(True)
            self.handleAssetTextChange()
        else:
            self.renameText.setEnabled(False)
            self.threePadCheckbox.setChecked(False)
            self.fourPadCheckbox.setChecked(False)
            self.handleAssetTextChange()
            
    def handleAppend(self):
        if self.appendCheckbox.isChecked():
            self.appendText.setEnabled(True)
            self.handleAssetTextChange()
        else:
            self.appendText.setEnabled(False)
            self.handleAssetTextChange()
            
    def handleAssetTextChange(self):
        prepend = ""
        append = ""
        
        if self.prependCheckbox.isChecked():
            prepend = self.prependText.text()
        if self.appendCheckbox.isChecked():
            append = self.appendText.text()
        updatedItems = []
        self.assetListText = self.originalAssetListText
        self.assetNames = []
        index = 0
        
        for item in self.assetListText:
            if self.renameCheckbox.isChecked() and self.renameText.text():
                if not self.threePadCheckbox.isChecked() and not self.fourPadCheckbox.isChecked():
                    rename = f"{self.renameText.text()}{index}"
                else:
                    rename = f"{self.renameText.text()}"
            else:
                rename = f"{self.originalAssetListText[index]}"
            formattedAssetName = f"{prepend}{rename}{append}"
            
            if self.renameCheckbox.isChecked():
                if self.threePadCheckbox.isChecked():
                    formattedAssetName = f"{prepend}{rename}{self.getThreePad(index)}{append}"
                elif self.fourPadCheckbox.isChecked():
                    formattedAssetName = f"{prepend}{rename}{self.getFourPad(index)}{append}"
                    
            updatedItems.append(f"{self.originalFilenameListText[index]}    ->    {formattedAssetName}")
            self.assetNames.append(formattedAssetName)
            index += 1

        self.assetListText = updatedItems
        self.updateAssetList()
        
    def getThreePad(self, number):
        if number <= 9:
            return f"00{number}"
        elif number <= 99:
            return f"0{number}"
        elif number <= 999:
            return f"{number}"
        elif number > 9999:
            print("AssetLoader supports a maximum of 9999 assets")
    
    def getFourPad(self, number):
        if number <= 9:
            return f"000{number}"
        elif number <= 99:
            return f"00{number}"
        elif number <= 999:
            return f"0{number}"
        elif number > 9999:
            print("AssetLoader supports a maximum of 9999 assets")
        
    def handleThreePad(self):
        if self.fourPadCheckbox.isChecked():
            self.fourPadCheckbox.setChecked(False)
        self.handleAssetTextChange()

    def handleFourPad(self):
        if self.threePadCheckbox.isChecked():
            self.threePadCheckbox.setChecked(False)
        self.handleAssetTextChange()
        
    def handleCheckNetworkName(self):
        geometryNodes = []
        for node in hou.node("/obj/").children():
            geometryNodes.append(str(node))
            
        if self.geometryNetworkNameText.text() in geometryNodes:
            self.geometryNetworkNameText.setStyleSheet("color: orange;")
        else:
            self.geometryNetworkNameText.setStyleSheet("color: white;")
        
app = AssetLoader()
app.show()