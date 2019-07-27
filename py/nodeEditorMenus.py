"""
Support for menus in the Node Editor panel.
"""
import maya
maya.utils.loadStringResourcesForModule(__name__)


from maya import cmds, mel
import maya.app.general.nodeEditorRendererMenus as nodeEditorRendererMenus
import maya

nEd = cmds.nodeEditor

#
#   Node editor work area marking menu creation
#

# This method is meant to be used when a particular string Id is needed more than
# once in this file.  The Maya Python pre-parser will report a warning when a
# duplicate string Id is detected.
def _loadUIString(strId):
    try:
        return {
            'kEditTexture': maya.stringTable['y_nodeEditorMenus.kEditTexture' ],
            'kSelectStream': maya.stringTable['y_nodeEditorMenus.kSelectStream' ],
            'kSelectUpDownstream': maya.stringTable['y_nodeEditorMenus.kSelectUpDownstream' ],
            'kSelectUpDownstreamAnnot': maya.stringTable['y_nodeEditorMenus.kSelectUpDownstreamAnnot' ],
            'kSelectUpstream': maya.stringTable['y_nodeEditorMenus.kSelectUpstream' ],
            'kSelectUpstreamAnnot': maya.stringTable['y_nodeEditorMenus.kSelectUpstreamAnnot' ],
            'kSelectDownstream': maya.stringTable['y_nodeEditorMenus.kSelectDownstream' ],
            'kSelectDownstreamAnnot': maya.stringTable['y_nodeEditorMenus.kSelectDownstreamAnnot' ],
            'kToggleSelectedSwatch': maya.stringTable['y_nodeEditorMenus.kToggleSelectedSwatch' ],
            'kToggleSelectedSwatchAnnot': maya.stringTable['y_nodeEditorMenus.kToggleSelectedSwatchAnnot' ],
            'kEditCustomAttrList': maya.stringTable['y_nodeEditorMenus.kEditCustomAttrList' ],
            'kEditCustomAttrListAnnot': maya.stringTable['y_nodeEditorMenus.kEditCustomAttrListAnnot' ],
            'kSoloMaterial' : maya.stringTable[ 'y_nodeEditorMenus.kSoloMaterial'  ],
            'kRemoveMaterialSoloing' : maya.stringTable[ 'y_nodeEditorMenus.kRemoveMaterialSoloing'  ],
        }[strId]
    except KeyError:
        return " "

def _syncDisplayMenu(ned, menu):
    """
    Syncs the Display menu UI control state to its editor.
    """
    shapes = nEd(ned, q=True, showShapes=True)
    if shapes:
        sgShapes = nEd(ned, q=True, showSGShapes=True)
        if not sgShapes:
            item = '%s|%sSSGMMI' % (menu,ned)
        else:
            item = '%s|%sSSMMI' % (menu,ned)
    else:
        item = '%s|%sNSMMI' % (menu,ned)

    cmds.menuItem(item, e=True, radioButton=True)

    item = '%s|%sSTMMI' % (menu,ned)
    transforms = nEd(ned, q=True, showTransforms=True)
    cmds.menuItem(item, e=True, checkBox=transforms)

    item = '%s|%sETSMMI' % (menu,ned)
    extToShapes = nEd(ned, q=True, extendToShapes=True)
    cmds.menuItem(item, e=True, checkBox=extToShapes)

def _syncShapeMenuState(ned, menu):
    """
    Syncs the editor to the menu state.
    """
    item = '%s|%sSSMMI' % (menu,ned)
    all = cmds.menuItem(item, q=True, radioButton=True)
    if all:
        nEd(ned, e=True, showShapes=True, showSGShapes=True)
    else:
        item = '%s|%sSSGMMI' % (menu,ned)
        noSG = cmds.menuItem(item, q=True, radioButton=True)
        if noSG:
            nEd(ned, e=True, showShapes=True, showSGShapes=False)
        else:
            nEd(ned, e=True, showShapes=False, showSGShapes=False)

def _createDisplayMenu(ned, menu):
    """
    Builds the Display menu for the panel.
    """
    transformsMenuItem = '%sSTMMI' % (ned)
    extendsMenuItem = '%sETSMMI' % (ned)

    def syncCB(*args):
        _syncDisplayMenu(ned, menu)

    def showShapeCB(*args):
        _syncShapeMenuState(ned, menu)

    def transformsCB(*args):
        transforms = cmds.menuItem(transformsMenuItem, q=True, checkBox=True)
        nEd(ned, e=True, showTransforms=transforms)

    def extendsCB(*args):
        shapesExt = cmds.menuItem(extendsMenuItem, q=True, checkBox=True)
        nEd(ned, e=True, extendToShapes=shapesExt)

    cmds.menuItem(menu, e=True, pmc=syncCB)

    cmds.radioMenuItemCollection()

    item = '%sSSMMI' % (ned)
    cmds.menuItem(item, label= maya.stringTable['y_nodeEditorMenus.kAllShapes'], radioButton=False,
    ann= maya.stringTable['y_nodeEditorMenus.kAllShapesAnnot' ],
    c = showShapeCB)

    item = '%sSSGMMI' % (ned)
    cmds.menuItem(item, label= maya.stringTable[ 'y_nodeEditorMenus.kAllShapesExceptShadingGroupMembers' ], radioButton=False,
    ann= maya.stringTable['y_nodeEditorMenus.kAllShapesExceptShadingGroupMembersAnnot' ],
    c = showShapeCB)

    item = '%sNSMMI' % (ned)
    cmds.menuItem(item, label= maya.stringTable[ 'y_nodeEditorMenus.kNoShapes'  ], radioButton=False,
    ann= maya.stringTable['y_nodeEditorMenus.kNoShapesAnnot' ],
    c = showShapeCB)

    cmds.menuItem( divider=True )

    cmds.menuItem(transformsMenuItem, label= maya.stringTable['y_nodeEditorMenus.kTransforms'], checkBox = False,
    ann= maya.stringTable['y_nodeEditorMenus.kTransformsAnnot' ],
    c = transformsCB)

    cmds.menuItem(extendsMenuItem, label= maya.stringTable['y_nodeEditorMenus.kExtendToShapes'], checkBox = False,
    ann= maya.stringTable['y_nodeEditorMenus.kExtendToShapesAnnot' ],
    c = extendsCB)

    cmds.setParent('..', menu=True)

def changeNodeLib(ned, createNodeWin):
    ''' 
    change to the current node library
    '''
    runtimeLib = cmds.nodeEditor(ned, q=True, vnnRuntime=True);
    if runtimeLib == "" :
        runtimeLib = "Hypershade";
        
    mel.eval('changeNodeLibrary("' + str(createNodeWin) + '", "' + str(runtimeLib) + '", false)')

def createNodeEditorMarkingMenu(ned):
    """
    Build work area marking menu
    """
    selectionMenuItem = '%sSOSMMI' % (ned)
    creationMenuItem = '%sSOCMMI' % (ned)
    additiveMenuItem = '%sADGMMI' % (ned)
    pinnedMenuItem = '%sPBDMMI' % (ned)
    lockButtonitem = '%sLCB' % (ned)

    def graphCB(*args):
        nEd(ned, e=True, shaderNetworks=True)

    def createNodeCB(*args):
        createNodeWin = mel.eval('string $nodeWinName = `createNodeWindow`')
        changeNodeLib(ned, createNodeWin)

    def selectAllCB(*args):
        nEd(ned, e=True, selectAll=True)

    def selectUpDownstreamCB(*args):
        nEd(ned, e=True, selectUpstream=True, selectDownstream=True)

    def selectUpstreamCB(*args):
        nEd(ned, e=True, selectUpstream=True)

    def selectDownstreamCB(*args):
        nEd(ned, e=True, selectDownstream=True)

    def toggleSelectedSwatchCB(*args):
        nEd(ned, e=True, toggleSwatchSize="")

    def rearrangeCB(*args):
        nEd(ned, e=True, frameAll=True, layout=True)

    def clearCB(*args):
        nEd(ned, e=True, rootNode='')

    def syncOnSelectionCB(*args):
        syncOnSel = cmds.menuItem(selectionMenuItem, q=True, checkBox=True)
        nEd(ned, e=True, syncedSelection=syncOnSel)

    def addOnCreateCB(*args):
        addOnCrt = cmds.menuItem(creationMenuItem, q=True, checkBox=True)
        nEd(ned, e=True, addNewNodes=addOnCrt)
        if cmds.iconTextButton(lockButtonitem, exists=True):
            if addOnCrt:
                lockImage = "nodeGrapherUnlocked.png"
            else:
                lockImage = "nodeGrapherLocked.png"
            cmds.iconTextButton(lockButtonitem, e=True, i1=lockImage)

    def additiveGraphingModeCB(*args):
        additiveMode = cmds.menuItem(additiveMenuItem, q=True, checkBox=True)
        nEd(ned, e=True, additiveGraphingMode=additiveMode)

    def pinByDefaultCB(*args):
        pinned = cmds.menuItem(pinnedMenuItem, q=True, checkBox=True)
        nEd(ned, e=True, defaultPinnedState=pinned)
        
    def hyperShadeCB(*args):
        mel.eval('HypershadeWindow')

    def hyperGraphCB(*args):
        mel.eval('HypergraphDGWindow')

    def unSoloCB(*args):
        cmds.soloMaterial(unsolo=True)

    def soloLastCB(*args):
        cmds.soloMaterial(last=True)

    inContainer = nEd(ned, q=True, inContainerView=True)

    cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kCreateNode' ], radialPosition = 'N',
    ann= maya.stringTable[ 'y_nodeEditorMenus.kCreateNodeAnnot' ],
    c = createNodeCB)

    cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kSelectAll' ], radialPosition = 'E',
    ann= maya.stringTable['y_nodeEditorMenus.kSelectAllAnnot' ],
    c = selectAllCB)

    cmds.menuItem(label= _loadUIString('kSelectStream'), radialPosition = 'W',
    subMenu = True)

    cmds.menuItem(label= _loadUIString('kSelectUpDownstream'), radialPosition = 'W',
    ann= _loadUIString('kSelectUpDownstreamAnnot'),
    c = selectUpDownstreamCB)

    cmds.menuItem(label= _loadUIString('kSelectUpstream'), radialPosition = 'N',
    ann= _loadUIString('kSelectUpstreamAnnot'),
    c = selectUpstreamCB)

    cmds.menuItem(label= _loadUIString('kSelectDownstream'), radialPosition = 'S',
    ann= _loadUIString('kSelectDownstreamAnnot'),
    c = selectDownstreamCB)

    cmds.setParent('..', menu=True)

    inLookDev = (nEd(ned, q=True, editorMode=True) == "lookdev")
    if inLookDev:
        cmds.menuItem(label=_loadUIString('kRemoveMaterialSoloing'), radialPosition = 'SE', c = unSoloCB, version = '2016', enable = (not inContainer))
        cmds.menuItem(label=maya.stringTable[ 'y_nodeEditorMenus.kSoloLastConnection'  ], radialPosition = 'SW', c = soloLastCB, version = '2016', enable = (not inContainer))

    cmds.menuItem(label= maya.stringTable[ 'y_nodeEditorMenus.kGraphMaterialsOnViewportSelection'  ], radialPosition = 'S',
    ann= maya.stringTable['y_nodeEditorMenus.kGraphMaterialsOnViewportSelectionAnnot' ],
    c = graphCB, enable = (not inContainer))

    selection = nEd(ned, q=True, syncedSelection=True)
    cmds.menuItem(selectionMenuItem, label= maya.stringTable['y_nodeEditorMenus.kSyncOnSelection' ], checkBox = selection,
    ann= maya.stringTable[ 'y_nodeEditorMenus.kSyncOnSelectionAnnot'  ],
    c = syncOnSelectionCB, enable = (not inContainer))

    creation = nEd(ned, q=True, addNewNodes=True)
    cmds.menuItem(creationMenuItem, label= maya.stringTable['y_nodeEditorMenus.kAddOnCreate' ], checkBox = creation,
    ann= maya.stringTable['y_nodeEditorMenus.kAddOnCreateAnnot' ],
    c = addOnCreateCB, enable = (not inContainer))

    additive = nEd(ned, q=True, additiveGraphingMode=True)
    cmds.menuItem(additiveMenuItem, label= maya.stringTable['y_nodeEditorMenus.kAdditiveGraphingMode' ], checkBox = additive,
    ann = maya.stringTable['y_nodeEditorMenus.kAdditiveGraphingModeannot' ],
    c = additiveGraphingModeCB, enable = (not inContainer))

    pinned = nEd(ned, q=True, defaultPinnedState=True)
    cmds.menuItem(pinnedMenuItem, label= maya.stringTable['y_nodeEditorMenus.kPinByDefault' ], checkBox = pinned,
    ann= maya.stringTable['y_nodeEditorMenus.kPinByDefaultAnn' ],
    c = pinByDefaultCB, enable = (not inContainer))

    displayMenuItem = '%sDMMI' % (ned)
    cmds.menuItem(displayMenuItem, label= maya.stringTable['y_nodeEditorMenus.kDisplay' ], subMenu = True, enable = (not inContainer))

    _createDisplayMenu(ned, displayMenuItem)

    parent = cmds.setParent(q=True, menu=True)
    showMenuItem = mel.eval('filterUICreateMenu("%s", "%s")' % (ned, parent))
    cmds.menuItem(showMenuItem, e=True, enable = (not inContainer))

    selectionList = cmds.ls(selection=True)
    if len(selectionList) > 0:
        def createCB(*args):
            mel.eval('createContainerWithNodes(`ls -sl`)')

        def createTransCB(*args):
            cmds.container(type='dagContainer', includeHierarchyBelow=True, includeTransform=True, force=True, addNode=selectionList)

        def removeCB(*args):
            mel.eval('removeNodesFromContainer(`ls -sl`, "", 0)')

        cmds.menuItem( divider=True )

        cmds.menuItem(label= _loadUIString('kToggleSelectedSwatch'),
        ann= _loadUIString('kToggleSelectedSwatchAnnot'),
        c = toggleSelectedSwatchCB)

        cmds.menuItem( divider=True )

    if ned != maya.mel.eval('$temp = $gHypershadeNodeEditor'):
        cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kHypershade' ],
        ann= maya.stringTable['y_nodeEditorMenus.kHypershadeAnnot' ],
        c = hyperShadeCB, enable = (not inContainer))

    cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kHypergraph' ],
    ann= maya.stringTable[ 'y_nodeEditorMenus.kHypergraphAnnot' ],
    c = hyperGraphCB, enable = (not inContainer))

#
#   Node item marking menu creation
#

def _isClassified(node, classification):
    type = cmds.nodeType(node)
    classified = cmds.getClassification(type, satisfies=classification)
    return classified

def _addPlace3dTextureMenuItems(ned, node):
    """
    Check for place3dTexture node and create necessary menu items
    """
    type = cmds.nodeType(node)
    if type == 'place3dTexture':
        _createPlace3dTextureMenuItems(node)
        return True
    else:
        return False

def _addShaderMenuItems(ned, node):
    """
    Check for shader node and create necessary menu items
    """
    isShader = _isClassified(node, 'shader')
    if isShader:
        _createShaderMenuItems(ned, node)
        return True
    else:
        return False

def _addTextureMenuItems(ned, node):
    """
    Check for texture node and create necessary menu items
    """
    isTexture = _isClassified(node, 'texture')
    if isTexture:
        type = cmds.nodeType(node)
        if type == 'psdFileTex':
            _createPsdFileTexMenuItems(ned, node)
        elif type == 'file':
            _createFileMenuItems(ned, node)
        else:
            _createTextureMenuItems(ned, node)
        return True
    else:
        return False

def _addUtilityMenuItems(ned, node):
    """
    Check for utility node and create necessary menu items
    """
    isUtility = _isClassified(node, 'utility')
    if isUtility:
        _createUtilityMenuItems(ned, node)
        return True
    else:
        return False

def _addLightMenuItems(ned, node):
    """
    Check for light node and create necessary menu items
    """
    isLight = _isClassified(node, 'light')
    if isLight:
        _createLightMenuItems(node)
        return True
    else:
        return False

def _addBakeSetMenuItems(ned, node):
    """
    Check for bake set node and create necessary menu items
    """
    type = cmds.nodeType(node)
    if type == 'textureBakeSet' or type == 'vertexBakeSet':
        _createBakeSetMenuItems(node)
        return True
    else:
        return False

def _addAnimClipMenuItems(ned, node):
    """
    Check for anim clip node and create necessary menu items
    """
    type = cmds.nodeType(node)
    if type == 'animClip':
        _createAnimClipMenuItems(node)
        return True
    else:
        return False

def _addColorProfileMenuItems(ned, node):
    """
    Check for color profile node and create necessary menu items
    """
    type = cmds.nodeType(node)
    if type == 'colorProfile':
        _createColorProfileMenuItems(node)

customExclusiveNodeItemMenuCallbacks = [_addPlace3dTextureMenuItems, _addShaderMenuItems, nodeEditorRendererMenus.addMrShaderMenuItems, _addTextureMenuItems, _addUtilityMenuItems, _addLightMenuItems, _addBakeSetMenuItems, _addAnimClipMenuItems]

customInclusiveNodeItemMenuCallbacks = [_addColorProfileMenuItems]

def _addCustomNodeItemMenus(ned, node):
    """
    Add custom menu items to the node item marking menu
    """
    for callback in customExclusiveNodeItemMenuCallbacks:
        added = callback(ned, node)
        if added:
            break

    for callback in customInclusiveNodeItemMenuCallbacks:
        callback(ned, node)

def _createPlace3dTextureMenuItems(node):
    """
    Create node item marking menu items specific to shader nodes
    """
    def fitCB(*args):
        mel.eval('source "AEplace3dTextureTemplate.mel"; PSfitPlacementToGroup "%s";' % node)

    cmds.menuItem(label=maya.stringTable[ 'y_nodeEditorMenus.kFitToGroupBoundingBox'  ], c = fitCB)

    selectionList = cmds.ls(selection=True)
    if len(selectionList) > 0:
        def parentCB(*args):
            cmds.parent(node, selectionList[0])

        parentPlacementString = cmds.format(maya.stringTable[ 'y_nodeEditorMenus.kParentPlacement'  ], stringArg=selectionList[0])
        cmds.menuItem(label=parentPlacementString, c = parentCB)
    else:
        cmds.menuItem(label=maya.stringTable[ 'y_nodeEditorMenus.kParentPlacementToSelection'  ], enable=False)

    cmds.menuItem( divider=True )

def _createShaderMenuItems(ned, node):
    """
    Create node item marking menu items specific to shader nodes
    """
    def refreshCB(*args):
        mel.eval('updateFileNodeSwatch("%s")' % (node))

    layer = mel.eval('currentRenderLayerLabel()');
    if len(layer) > 0 and layer != 'masterLayer':
        def assignCB(*args):
            mel.eval('hookShaderOverride("%s", "", "%s")' % (layer, node))

        assignMaterialOverString = cmds.format(maya.stringTable[ 'y_nodeEditorMenus.kAssignMaterialOverride'  ], stringArg=layer)
        cmds.menuItem(label=assignMaterialOverString, radialPosition = 'W', c = assignCB)

    cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kShaderGenSwatch' ], radialPosition = 'SW',
    ann= maya.stringTable['y_nodeEditorMenus.kShaderGenSwatchAnnot' ],
    c = refreshCB)

    # # DAYU CUSTOM COMMAND
    # cmds.menuItem(label='Assign To GPU', radialPosition='NW',
    #               c='print Assign To GPU')

    shadingGroupArray = cmds.listConnections(node, source=False, destination=True, type='shadingEngine')
    groupSize = 0
    if shadingGroupArray:
        if len(shadingGroupArray) > 1:
            # Remove any duplicates by making the list a set
            shadingGroupArray = list(set(shadingGroupArray))
            shadingGroupArray.sort()
        groupSize = len(shadingGroupArray)

    # DAYU CUSTOM MENU
    import fitment as ft
    reload(ft)
    ft.add_hypershade_mouse()
    cmds.menuItem(divider=True)

    if groupSize <= 1:
        removeMenuItem = '%sROMMI' % (ned)

        def assignCB(*args):
            cmds.hyperShade(assign=node)

        def assignOceanCB(*args):
            mel.eval('assignOceanShader "%s"' % (node))

        def paintCB(*args):
            mel.eval('shaderPaintTool "%s"' % (node))

        def selectCB(*args):
            cmds.hyperShade(objects=node)

        def soloCB(*args):
            cmds.soloMaterial(node="%s" % (node))

        def unSoloCB(*args):
            cmds.soloMaterial(unsolo=True)

        def frameCB(*args):
            cmds.hyperShade(objects=node)
            mel.eval('fitAllPanels -selected')

        def removeCB(*args):
            mel.eval('buildMaterialRemoveOverrideMenu -shader "%s" "%s"' % (node, removeMenuItem))

        assignMaterialSelString = maya.stringTable[ 'y_nodeEditorMenus.kAssignMaterialToViewportSelection'  ]
        type = cmds.nodeType(node)
        if type == 'oceanShader':
            cmds.menuItem(label=assignMaterialSelString, radialPosition = 'N', c = assignOceanCB)
        else:
            cmds.menuItem(label=assignMaterialSelString, radialPosition = 'N', c = assignCB)

            cmds.menuItem(label=maya.stringTable[ 'y_nodeEditorMenus.kPaintAssignShader'  ], radialPosition = 'NE',
            c = paintCB)

        cmds.menuItem(label=maya.stringTable[ 'y_nodeEditorMenus.kSelectObjectsWithMaterial'  ], radialPosition = 'E',
        c = selectCB)

        inLookDev = (nEd(ned, q=True, editorMode=True) == "lookdev")
        if inLookDev:
            cmds.menuItem(label=_loadUIString('kSoloMaterial'), radialPosition = 'S', c = soloCB, version = '2016')
            cmds.menuItem(label=_loadUIString('kRemoveMaterialSoloing'), radialPosition = 'SE', c = unSoloCB, version = '2016')

        cmds.menuItem(label=maya.stringTable[ 'y_nodeEditorMenus.kFrameObjectsWithMaterial'  ], c = frameCB)

        cmds.menuItem( divider=True )

        cmds.menuItem(removeMenuItem, label= maya.stringTable['y_nodeEditorMenus.kRemoveMaterialOverride' ],
        subMenu = True, pmc = removeCB)

        cmds.setParent('..', menu=True)

        cmds.menuItem( divider=True )
    else:
        assignToSelectionString = maya.stringTable[ 'y_nodeEditorMenus.kAssignToViewportSelection'  ]
        selectObjString = maya.stringTable[ 'y_nodeEditorMenus.kSelectObjects'  ]
        frameObjString = maya.stringTable[ 'y_nodeEditorMenus.kFrameObjects'  ]
        radialItemIndex = groupSize - 1
        for member in shadingGroupArray:
            shader = member
            def assignCB(*args):
                cmds.hyperShade(assign=shader)

            def selectCB(*args):
                cmds.hyperShade(objects=shader)

            def frameCB(*args):
                cmds.hyperShade(objects=shader)
                mel.eval('fitAllPanels -selected')

            assignToSelectionStrFmt = cmds.format(assignToSelectionString, stringArg=member)
            assignToSelMenuItem = cmds.menuItem(label=assignToSelectionStrFmt, c = assignCB)

            selectObjStrFmt = cmds.format(selectObjString, stringArg=member)
            selectObjMenuItem = cmds.menuItem(label=selectObjStrFmt, c = selectCB)

            if member == shadingGroupArray[radialItemIndex]:
                cmds.menuItem(assignToSelMenuItem, e=True, radialPosition='N')
                cmds.menuItem(selectObjMenuItem, e=True, radialPosition='E')

            frameObjStrFmt = cmds.format(frameObjString, stringArg=member)
            cmds.menuItem(label=frameObjStrFmt, c = frameCB)

        cmds.menuItem( divider=True )

def _createPsdFileTexMenuItems(ned, node):
    """
    Create node item marking menu items specific to psd file nodes
    """
    def convertLayerCB(*args):
        mel.eval('hypergraphConvertPsdToLTNetwork "%s"' % (node))

    def convertFileCB(*args):
        mel.eval('hypergraphConvertPsdToFile "%s"' % (node))

    def editCB(*args):
        mel.eval('hyperShadeEditTexture "%s"' % (node))

    cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kConvertToLayeredTexture' ], radialPosition = 'SW',
    ann= maya.stringTable['y_nodeEditorMenus.kConvertToLayeredTextureAnnot' ],
    c = convertLayerCB)

    cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kConvertToFileTexture' ], radialPosition = 'NW',
    ann= maya.stringTable['y_nodeEditorMenus.kConvertToFileTextureAnnot' ],
    c = convertFileCB)

    cmds.menuItem(label= _loadUIString('kEditTexture'), radialPosition = 'SE',
    ann= (mel.eval('getRunTimeCommandAnnotation ("EditTexture")')),
    c = editCB)

    _createTextureMenuItems(ned, node)

def _createFileMenuItems(ned, node):
    """
    Create node item marking menu items specific to file nodes
    """
    def editCB(*args):
        mel.eval('hyperShadeEditTexture "%s"' % (node))

    def reloadCB(*args):
        attrName = '%s.fileTextureName' % (node)
        name = cmds.getAttr(attrName)
        cmds.setAttr(attrName, name, type='string')

    _createTextureMenuItems(ned, node)

    cmds.menuItem(label= _loadUIString('kEditTexture'), radialPosition = 'SE',
    ann= (mel.eval('getRunTimeCommandAnnotation ("EditTexture")')),
    c = editCB)

    cmds.menuItem(label= maya.stringTable[ 'y_nodeEditorMenus.kReloadImageFile'  ],
    c = reloadCB)

    cmds.menuItem( divider=True )

def _createTextureUtilityMenuItems(ned, node):
    """
    Create node item marking menu items common to both texture and utility nodes
    """
    def assignCB(*args):
        mel.eval('hypergraphAssignTextureToSelection "%s"' % node)

    if not cmds.about(ltVersion=True):
        def testCB(*args):
            cmds.select(node, replace=True)
            mel.eval('TestTexture')    

    def soloCB(*args):
        cmds.soloMaterial(node="%s" % (node))

    def unSoloCB(*args):
        cmds.soloMaterial(unsolo=True)


    cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kAssignTextureMaterialToSelection' ],
    radialPosition = 'N',
    c = assignCB)

    inLookDev = (nEd(ned, q=True, editorMode=True) == "lookdev")
    if inLookDev:
        cmds.menuItem(label=_loadUIString('kSoloMaterial'), radialPosition = 'S', c = soloCB, version = '2016')
        cmds.menuItem(label=_loadUIString('kRemoveMaterialSoloing'), radialPosition = 'SE', c = unSoloCB, version = '2016')

    if not cmds.about(ltVersion=True):
        cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kTestTexture' ], radialPosition = 'W',
        ann= (mel.eval('getRunTimeCommandAnnotation ("TestTexture")')),
        c = testCB)    
  
        def renderCB(*args):       
            cmds.select(node, replace=True)
            mel.eval('RenderTextureRange')
        cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kRenderTextureRange' ], radialPosition = 'E',
        ann= (mel.eval('getRunTimeCommandAnnotation ("RenderTextureRange")')),
        c = renderCB)

def _createTextureMenuItems(ned, node):
    """
    Create node item marking menu items specific to texture nodes
    """
    def refreshCB(*args):
        mel.eval('updateFileNodeSwatch("%s")' % (node))

    def soloCB(*args):
        cmds.soloMaterial(node="%s" % (node))

    def unSoloCB(*args):
        cmds.soloMaterial(unsolo=True)

    _createTextureUtilityMenuItems(ned, node)

    cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kTextureGenSwatch' ], radialPosition = 'SW',
    ann= maya.stringTable['y_nodeEditorMenus.kTextureGenSwatchAnnot' ],
    c = refreshCB)

    inLookDev = (nEd(ned, q=True, editorMode=True) == "lookdev")
    if inLookDev:
        cmds.menuItem(label=_loadUIString('kSoloMaterial'), radialPosition = 'S', c = soloCB, version = '2016')
        cmds.menuItem(label=_loadUIString('kRemoveMaterialSoloing'), radialPosition = 'SE', c = unSoloCB, version = '2016')

def _createUtilityMenuItems(ned, node):
    """
    Create node item marking menu items specific to utility nodes
    """
    connections = cmds.listConnections(node, source=False, destination=True)
    if connections and len(connections) > 1:
        _createTextureUtilityMenuItems(ned, node)

def _createLightMenuItems(node):
    """
    Create node item marking menu items specific to light nodes
    """
    def makeCB(*args):
        cmds.lightlink(make=True, light=node, useActiveObjects=True)

    def breakCB(*args):
        cmds.lightlink(b=True, light=node, useActiveObjects=True)

    def selectCB(*args):
        mel.eval('selectObjectsIlluminatedBy "%s"' % (node))

    def frameCB(*args):
        mel.eval('selectObjectsIlluminatedBy "%s"; fitAllPanels -selected' % (node))

    cmds.menuItem(label= maya.stringTable[ 'y_nodeEditorMenus.kMakeLinksWithSelectedViewportObjects'  ],
    c = makeCB)

    cmds.menuItem(label= maya.stringTable[ 'y_nodeEditorMenus.kBreakLinksWithSelectedViewportObjects'  ],
    c = breakCB)

    cmds.menuItem( divider=True )

    cmds.menuItem(label= maya.stringTable[ 'y_nodeEditorMenus.kSelectObjectsIlluminatedByLight'  ],
    radialPosition = 'E',
    c = selectCB)

    cmds.menuItem(label= maya.stringTable[ 'y_nodeEditorMenus.kFrameObjectsIlluminatedByLight'  ],
    c = frameCB)

    cmds.menuItem( divider=True )

def _createBakeSetMenuItems(node):
    """
    Create node item marking menu items specific to bake set nodes
    """
    def assignCB(*args):
        selectionList = cmds.ls(dagObjects=True, objectsOnly=True, geometry=True, selection=True)
        if len(selectionList) > 0:
            cmds.sets(selectionList, forceElement=node)

    def selectCB(*args):
        cmds.select(node)

    def frameCB(*args):
        cmds.select(node)
        mel.eval('fitAllPanels -selected')

    cmds.menuItem(label= maya.stringTable[ 'y_nodeEditorMenus.kAssignViewportSelectionToBakeSet'  ],
    radialPosition = 'N',
    c = assignCB)

    cmds.menuItem(label= maya.stringTable[ 'y_nodeEditorMenus.kSelectObjectsInBakeSet'  ],
    radialPosition = 'E',
    c = selectCB)

    cmds.menuItem(label= maya.stringTable[ 'y_nodeEditorMenus.kFrameObjectsInBakeSet'  ],
    c = frameCB)

    cmds.menuItem( divider=True )

def _createAnimClipMenuItems(node):
    """
    Create node item marking menu items specific to anim clip nodes
    """
    def copyCB(*args):
        mel.eval('clipCopyMenuCommand "%s"' % node)

    def instanceCB(*args):
        mel.eval('clipInstanceMenuCommand "%s"' % node)

    def duplicateCB(*args):
        cmds.select(node)
        mel.eval('clipDuplicateMenuCommand "%s"' % node)

    def exportCB(*args):
        mel.eval('doExportClipArgList 2 { "", "%s" }' % node)

    def applyCB(*args):
        mel.eval('clipApplyPoseMenuCommand "%s"' % node)

    cmds.menuItem(label= maya.stringTable[ 'y_nodeEditorMenus.kCopy'  ],
    ann= maya.stringTable['y_nodeEditorMenus.kCopyAnnot' ],
    c = copyCB)

    cmds.menuItem(label= maya.stringTable[ 'y_nodeEditorMenus.kInstance'  ],
    ann= maya.stringTable['y_nodeEditorMenus.kInstanceAnnot' ],
    c = instanceCB)

    cmds.menuItem(label= maya.stringTable[ 'y_nodeEditorMenus.kDuplicate'  ],
    ann= maya.stringTable['y_nodeEditorMenus.kDuplicateClip' ],
    c = duplicateCB)

    cmds.menuItem(label= maya.stringTable[ 'y_nodeEditorMenus.kExport'  ],
    ann= maya.stringTable['y_nodeEditorMenus.kExportClip' ],
    c = exportCB)

    cmds.menuItem(label= maya.stringTable[ 'y_nodeEditorMenus.kApplyPose'  ],
    ann= maya.stringTable['y_nodeEditorMenus.kApplyPoseAnnot' ],
    c = applyCB)

    cmds.menuItem( divider=True )

def _createColorProfileMenuItems(node):
    """
    Create node item marking menu items specific to color profile nodes
    """
    def applyCB(*args):
        mel.eval('applyColorProfileToSelection "%s"' % node)

    cmds.menuItem(label= maya.stringTable[ 'y_nodeEditorMenus.kApplyColorProfileToSelected'  ],
    ann= maya.stringTable['y_nodeEditorMenus.kApplyColorProfileToViewportSelectedAnnotaton' ],
    c = applyCB)

    cmds.menuItem( divider=True )

def createNodeItemMarkingMenu(ned, node):
    """
    Build node item marking menu
    """

    inContainer = nEd(ned, q=True, inContainerView=True)
    isContainerNode = nEd(ned, q=True, isContainerNode=node)

    inputsMenuItem = '%sIMMI' % (ned)
    outputsMenuItem = '%sOMMI' % (ned)
    editCustomAttrListMenuItem = '%sCALMMI' % (ned)
    if inContainer:
        type = node
    else:
        type = cmds.nodeType(node)

    def openContainerViewCB(*args):
        nEd(ned, e=True, openContainerView=[node, False])

    def openContainerViewInNewTabCB(*args):
        nEd(ned, e=True, openContainerView=[node, True])

    def resetToFactoryCB(*args):
        mel.eval('nodeEdResetToFactory')

    def graphUpDownstreamCB(*args):
        mel.eval('NodeEditorGraphUpDownstream')

    def graphUpstreamCB(*args):
        mel.eval('NodeEditorGraphUpstream')

    def graphDownstreamCB(*args):
        mel.eval('NodeEditorGraphDownstream')

    def removeUnselectedCB(*args):
        nEd(ned, e=True, removeUnselected=True)

    def removeSelectedCB(*args):
        mel.eval('NodeEditorGraphRemoveSelected')

    def removeUpstreamCB(*args):
        nEd(ned, e=True, removeUpstream=True)

    def removeDownstreamCB(*args):
        nEd(ned, e=True, removeDownstream=True)

    def selectUpDownstreamCB(*args):
        nEd(ned, e=True, selectUpstream=True, selectDownstream=True)

    def selectUpstreamCB(*args):
        nEd(ned, e=True, selectUpstream=True)

    def selectDownstreamCB(*args):
        nEd(ned, e=True, selectDownstream=True)

    def nodeCB(*args):
        mel.eval('showEditorExact "%s"' % (node))

    def inputsCB(*args):
        mel.eval('source "dagMenuProc.mel"; createHistoryMenuItems("%s", "%s");' % (inputsMenuItem, node))

    def outputsCB(*args):
        mel.eval('source "dagMenuProc.mel"; createFutureMenuItems("%s", "%s");' % (outputsMenuItem, node))

    def renameCB(*args):
        nEd(ned, e=True, renameNode=node)

    def toggleSwatchCB(*args):
        nEd(ned, e=True, toggleSwatchSize=node)

    def toggleSelectedSwatchCB(*args):
        nEd(ned, e=True, toggleSwatchSize="")

    def editCustomAttributeListCB(*args):
        editMode = cmds.menuItem(editCustomAttrListMenuItem, q=True, checkBox=True)
        if editMode:
            nEd(ned, e=True, customAttributeListEdit=[node])
        else:
            nEd(ned, e=True, customAttributeListEdit=[""])

    def showCB(*args):
        nEd(ned, e=True, showAllNodeAttributes=node)

    def addCB(*args):
        mel.eval('dynAddAttrWin( { "%s" } )' % node)

    def deleteCB(*args):
        mel.eval('dynDeleteAttrWin( { "%s" } )' % node)

    def createCB(*args):
        selectionList = cmds.ls(selection=True)
        if len(selectionList) > 0:
            mel.eval('createContainerWithNodes(`ls -sl`)')
        else:
            mel.eval('createContainerWithNodes({ "%s" })' % node)

    def createTransCB(*args):
        selectionList = cmds.ls(selection=True)
        if len(selectionList) > 0:
            cmds.container(type='dagContainer', includeHierarchyBelow=True, includeTransform=True, force=True, addNode=selectionList)
        else:
            cmds.container(type='dagContainer', includeHierarchyBelow=True, includeTransform=True, force=True, addNode=[node])

    def removeCB(*args):
        selectionList = cmds.ls(selection=True)
        if len(selectionList) > 0:
            mel.eval('removeNodesFromContainer(`ls -sl`, "", 0)')
        else:
            mel.eval('removeNodesFromContainer({ "%s" }, "", 0)' % node)

    def helpCB(*args):
        cmds.showHelp( 'Nodes/%s.html' % type, docs=True )

    def editCompoundCB(*args):
        mel.eval('nodeEdEditCompound("%s")' % node)

    def importCompoundCB(*args):
        mel.eval('nodeEdImportCompound("%s")' % node)

    def publishCompoundCB(*args):
        mel.eval('nodeEdPublishCompound("%s")' % node)

    def revertCompoundCB(*args):
        mel.eval('nodeEdRevertCompound("%s")' % node)

    def deleteCompoundCB(*args):
        mel.eval('nodeEdDeleteCompound("%s")' % node)

    menuHasCustomRadialMenuItems = False
    if not inContainer:
        nameSplit = node.rpartition('|')
        cmds.menuItem(label=('%s...' % nameSplit[2]), c = nodeCB)

        cmds.menuItem( divider=True )

        _addCustomNodeItemMenus(ned, node)

        parent = cmds.setParent(q=True, menu=True)
        customMenuItems = cmds.menu(parent, q=True, itemArray=True)

        for customMenuItem in customMenuItems:
            menuItemRadialPosition = cmds.menuItem(customMenuItem, q=True, radialPosition=True)
            if menuItemRadialPosition:
                menuHasCustomRadialMenuItems = True
                break

    customEditNode = nEd(ned, q=True, customAttributeListEdit=True)
    editMode = (node == customEditNode)

    if not editMode:
        if inContainer:
            if isContainerNode:
                cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kOpenContents' ], radialPosition = 'N',
                ann= maya.stringTable['y_nodeEditorMenus.kOpenContentsAnnot' ],
                c = openContainerViewCB)

                cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kOpenContentsInNewTab' ], radialPosition = 'E',
                ann= maya.stringTable['y_nodeEditorMenus.kOpenContentsInNewTabAnnot' ],
                c = openContainerViewInNewTabCB)
        elif not menuHasCustomRadialMenuItems:
            cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kRegraphStream' ], radialPosition = 'N',
            subMenu = True)

            cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kRegraphUpDownStream' ], radialPosition = 'W',
            ann= (mel.eval('getRunTimeCommandAnnotation ("NodeEditorGraphUpDownstream")')),
            c = graphUpDownstreamCB)

            cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kRegraphUpStream' ], radialPosition = 'N',
            ann= (mel.eval('getRunTimeCommandAnnotation ("NodeEditorGraphUpstream")')),
            c = graphUpstreamCB)

            cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kRegraphDownStream' ], radialPosition = 'S',
            ann= (mel.eval('getRunTimeCommandAnnotation ("NodeEditorGraphDownstream")')),
            c = graphDownstreamCB)

            cmds.setParent('..', menu=True)

            cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kRemoveStream' ], radialPosition = 'E',
            subMenu = True)

            cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kRemoveUnselected' ], radialPosition = 'W',
            ann= maya.stringTable['y_nodeEditorMenus.kRemoveUnselectedAnnot' ],
            c = removeUnselectedCB)

            cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kRemoveSelected' ], radialPosition = 'E',
            ann= (mel.eval('getRunTimeCommandAnnotation ("NodeEditorGraphRemoveSelected")')),
            c = removeSelectedCB)

            cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kRemoveUpStream' ], radialPosition = 'N',
            ann= maya.stringTable['y_nodeEditorMenus.kRemoveUpStreamAnnot' ],
            c = removeUpstreamCB)

            cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kRemoveDownStream' ], radialPosition = 'S',
            ann= maya.stringTable['y_nodeEditorMenus.kRemoveDownStreamAnnot' ],
            c = removeDownstreamCB)

            cmds.setParent('..', menu=True)

        nedSelectionList = nEd(ned, q=True, selectNode=True)

        if not menuHasCustomRadialMenuItems and (cmds.ls(node, selection=True) or ( nedSelectionList and node in nedSelectionList )):
            parent = cmds.setParent(q=True, menu=True)

            cmds.menuItem(label= _loadUIString('kSelectStream'), radialPosition = 'W',
            subMenu = True)

            cmds.menuItem(label= _loadUIString('kSelectUpDownstream'), radialPosition = 'W',
            ann= _loadUIString('kSelectUpDownstreamAnnot'),
            c = selectUpDownstreamCB)

            cmds.menuItem(label= _loadUIString('kSelectUpstream'), radialPosition = 'N',
            ann= _loadUIString('kSelectUpstreamAnnot'),
            c = selectUpstreamCB)

            cmds.menuItem(label= _loadUIString('kSelectDownstream'), radialPosition = 'S',
            ann= _loadUIString('kSelectDownstreamAnnot'),
            c = selectDownstreamCB)

            cmds.setParent('..', menu=True)

        parent = cmds.setParent(q=True, menu=True)

        if not inContainer:
            cmds.menuItem(inputsMenuItem, label= maya.stringTable['y_nodeEditorMenus.kInputs' ], subMenu = True)
            cmds.menu(inputsMenuItem, e=True, pmc=inputsCB)
            cmds.setParent(parent, menu=True)

            cmds.menuItem(outputsMenuItem, label= maya.stringTable['y_nodeEditorMenus.kOutputs' ], subMenu = True)
            cmds.menu(outputsMenuItem, e=True, pmc=outputsCB)
            cmds.setParent(parent, menu=True)

            cmds.menuItem( divider=True )

        cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kRename' ], c = renameCB)

        cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kToggleSwatchSize' ],
        ann= maya.stringTable['y_nodeEditorMenus.kToggleSwatchSizeAnnot' ],
        c = toggleSwatchCB)

        cmds.menuItem(label= _loadUIString('kToggleSelectedSwatch'),
        ann= _loadUIString('kToggleSelectedSwatchAnnot'),
        c = toggleSelectedSwatchCB)

        cmds.menuItem( divider=True )

    if not inContainer:
        cmds.menuItem(editCustomAttrListMenuItem, label= _loadUIString('kEditCustomAttrList'),
        ann= _loadUIString('kEditCustomAttrListAnnot'),
        checkBox = (node == customEditNode),
        c = editCustomAttributeListCB)

    if not editMode:
        cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kShowAllAttributes' ],
        ann= maya.stringTable['y_nodeEditorMenus.kShowAllAttributesAnnot' ],
        c = showCB)

        if not inContainer:
            cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kAddAttributes' ], c = addCB)

            cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kDeleteAttributes' ], c = deleteCB)

    if not inContainer:
        cmds.menuItem( divider=True )

        helpString = cmds.format(maya.stringTable[ 'y_nodeEditorMenus.kHelpMenuLabel'  ], stringArg=type)
        cmds.menuItem(label=helpString, enableCommandRepeat=False, c = helpCB)

    if inContainer:
        if isContainerNode:
            if mel.eval('nodeEdCanResetToFactory'):
                cmds.menuItem( divider=True )
            
                cmds.menuItem(label = maya.stringTable['y_nodeEditorMenus.kResetToFactory' ], 
                ann = maya.stringTable['y_nodeEditorMenus.kResetToFactoryAnn' ],
                c = resetToFactoryCB)

    if isContainerNode and inContainer:
        cmds.menuItem( divider=True )

        isReferenced = mel.eval('nodeEdIsReferenced("%s")' % node)
        canBeReverted = mel.eval('nodeEdCanBeReverted("%s")' % node)

        cmds.menuItem(label = maya.stringTable['y_nodeEditorMenus.kEditCompound' ],
            annotation = maya.stringTable['y_nodeEditorMenus.kEditCompoundAnnot' ],
            command = editCompoundCB,
            enable = True)

        cmds.menuItem(label = maya.stringTable['y_nodeEditorMenus.kImportCompound' ],
            annotation = maya.stringTable['y_nodeEditorMenus.kImportCompoundAnnot' ],
            command = importCompoundCB,
            enable = isReferenced)

        cmds.menuItem(label = maya.stringTable['y_nodeEditorMenus.kPublishCompound' ],
            annotation = maya.stringTable['y_nodeEditorMenus.kPublishCompoundAnnot' ],
            command = publishCompoundCB,
            enable = True)

        cmds.menuItem(label = maya.stringTable['y_nodeEditorMenus.kRevertCompound' ],
            annotation = maya.stringTable['y_nodeEditorMenus.kRevertCompoundAnnot' ],
            command = revertCompoundCB,
            enable = canBeReverted)

        cmds.menuItem( divider=True )

        cmds.menuItem(label = maya.stringTable['y_nodeEditorMenus.kDeleteCompound' ],
            annotation = maya.stringTable['y_nodeEditorMenus.kDeleteCompoundAnnot' ],
            command = deleteCompoundCB,
            enable = False)
#
#   Connection item marking menu creation
#

def createConnectionMarkingMenu(ned):
    """
    Build connection marking menu
    """

    inContainer = nEd(ned, q=True, inContainerView=True)

    def breakCB(*args):
        nEd(ned, e=True, breakSelectedConnections=True)

    def isolateCB(*args):
        nEd(ned, e=True, graphSelectedConnections=True, frameAll=True)

    def selectCB(*args):
        nEd(ned, e=True, selectConnectionNodes=True)

    cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kBreakConnection' ], radialPosition = 'N',
    ann= maya.stringTable[ 'y_nodeEditorMenus.kCBreakConnectionAnnot' ],
    c = breakCB)

    cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kSelectConnectedNodes' ], radialPosition = 'E',
    ann= maya.stringTable['y_nodeEditorMenus.kSelectConnectedNodesAnnot' ],
    c = selectCB)

    cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kIsolateSelectedNodes' ], radialPosition = 'W',
    ann= maya.stringTable['y_nodeEditorMenus.kIsolateSelectedNodesAnnot' ],
    c = isolateCB, enable = (not inContainer))

def createPlugMarkingMenu(ned, node, plug):
    """
    Build plug (attribute) marking menu
    """
    def hideAllCB(*args):
        nEd(ned, e=True, customAttributeListEdit=[node, "hideall"])

    def showAllCB(*args):
        nEd(ned, e=True, customAttributeListEdit=[node, "showall"])

    def previewCB(*args):
        nEd(ned, e=True, customAttributeListEdit=[node, "preview"])

    def revertCB(*args):
        nEd(ned, e=True, customAttributeListEdit=[node, "revert"])

    def resetCB(*args):
        nEd(ned, e=True, customAttributeListEdit=[node, "reset"])

    def editCustomAttributeListCB(*args):
        nEd(ned, e=True, customAttributeListEdit=[node])

    customEditNode = nEd(ned, q=True, customAttributeListEdit=True)

    if customEditNode:
        cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kPlugPreview' ],
        ann= maya.stringTable['y_nodeEditorMenus.kPlugPreviewAnnot' ],
        c = previewCB)

        cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kPlugHideAll' ],
        ann= maya.stringTable['y_nodeEditorMenus.kPlugHideAllAnnot' ],
        c = hideAllCB)

        cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kPlugShowAll' ],
        ann= maya.stringTable['y_nodeEditorMenus.kPlugShowAllAnnot' ],
        c = showAllCB)

        cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kPlugRevert' ],
        ann= maya.stringTable['y_nodeEditorMenus.kPlugRevertAnnot' ],
        c = revertCB)

        cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kPlugReset' ],
        ann= maya.stringTable['y_nodeEditorMenus.kPlugResetAnnot' ],
        c = resetCB)
    #else:
        #cmds.menuItem(label= _loadUIString('kEditCustomAttrList'),
        #ann= _loadUIString('kEditCustomAttrListAnnot'),
        #c = editCustomAttributeListCB)

def createTabContextMenu(ned, tabIndex):
    """
    Build tab context menu (markingMenu=False)
    """

    def closeTabCB(*args):
        nEd(ned, e=True, closeTab=tabIndex)

    def duplicateTabCB(*args):
        nEd(ned, e=True, duplicateTab=[tabIndex, tabIndex+1])

    def renameTabCB(*args):
        nEd(ned, e=True, renameTab=[tabIndex])

    allowNewTabs = nEd(ned, q=True, allowNewTabs=True)

    cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kCloseTab' ],
    c = closeTabCB)

    cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kDuplicateTab' ],
    enable = allowNewTabs,
    c = duplicateTabCB)

    cmds.menuItem(label= maya.stringTable['y_nodeEditorMenus.kRenameTab' ],
    c = renameTabCB)
# ===========================================================================
# Copyright 2017 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
