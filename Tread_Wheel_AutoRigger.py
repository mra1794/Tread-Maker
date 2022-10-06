import maya.cmds as cmds
import maya.mel as mel
import sys

### Variables ####
rigWinName = 'Tread & Wheels Rigger'
confirmMessage = 'Please make sure the your model is facing down Z+ axis, and that it is correctly placed on top of the origin.'
treadCurve=['']
wireOBJ=['']
default=['']


def rigWin():#Define the main window for the rigging script
    if cmds.window(rigWinName, q=1, ex=1):
        cmds.deleteUI(rigWinName)
    cmds.window(rigWinName, w=600, sizeable=0)
    form = cmds.formLayout()#Tab form in window
    tabs = cmds.tabLayout(innerMarginWidth=2, innerMarginHeight=2)
    cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )
    
    tab1 = cmds.rowColumnLayout() ###Tread tab
    cmds.text('Welcome to the treadmaker')
    cmds.separator(w=400, h=20)

    #CREATE CURVE
    rigWin.text1 = cmds.text('Would you like to create a new curve or use your own curve?')
    rigWin.initBtn = cmds.button(l='Generate a new curve', c='initFunc()', w=200, h=45, vis=1)
    cmds.separator(horizontal=0, w=10)
    #OWN CURVE
    rigWin.OwnCurveBtn=cmds.button(l='Use my own curve', c='ownCurve()', w=200, h=45, vis=1)
    cmds.separator(w=400, h=20)
    #GENERATE
    rigWin.text2 = cmds.text('1.- First set the locators where you want to create the curve', en=0, al='left')
    #PREFIX
    rigWin.textBox=cmds.text('2.- Now please write a name for your tread', vis=1, en=0, al='left')
    rigWin.prefix = cmds.textFieldGrp(l='Prefix for treads:              ', vis=1, en=0)
    rigWin.makeCurveBtn = cmds.button(l='GENERATE CURVE', c='makeCurve()', w=100, h=70, vis=1, en=0)

    #SPAN COUNT
    rigWin.SelTxt = cmds.text("Before anything make sure you select a curve", vis=1, en=0)
    rigWin.SelBTN = cmds.button("Confirm Selection", c="selectedCurve=cmds.ls(sl=True)", vis=1, en=0)
    rigWin.SpanTxt = cmds.text("Now set how many Edit Points would you like to get", vis=1, en=0)
    rigWin.SpanCount = cmds.intSliderGrp(min=3,max=100,cc="SpanChange()",f=True, vis=1, en=0)
    cmds.separator(w=400, h=20)
    #EDIT POINTS
    rigWin.EPTxt = cmds.text("You can create Edit Points controls by clicking here", vis=1, en=0)
    rigWin.EP = cmds.button("EP Ctrl Maker",c="EPC()", vis=1, en=0)
    cmds.separator(w=400, h=20)
    #LOCATORS FOR OBJ
    rigWin.text3 = cmds.text("You can change the number of locators by playing with this slider",vis=1, en=0)
    rigWin.ReSpanCount=cmds.intSliderGrp(min=3,max=100,cc="ReSpanner()",f=True, vis=1, en=0)
    cmds.separator(w=500)
    #SELECTING OBJ
    rigWin.ObjText = cmds.textFieldButtonGrp(bl="Pick Tread OBJ",bc="pickingOBJ()",ed=True, vis=1, en=0)
    cmds.separator(w=400, h=20)
    #NUMBER OF TREADS
    rigWin.copyNum = cmds.intSliderGrp(l='# of copies for the treads:', min=10, max=750, v=35, f=1, vis=1, en=0, cc='prev()')
    rigWin.previewCB = cmds.checkBox(l='Preview Treads', v=0, vis=1, en=0, cc='prev()')
    cmds.separator(w=400, h=20)
    #RESET BUTTON
    rigWin.resetBtn = cmds.button(l='Reset All', c='resetLoc()', enable=0, vis=1, h=40)
    cmds.separator(w=400, h=20)
    #FINALIZE
    rigWin.finBtn = cmds.button(l='Finalize Tread', c='finalizeTread()', vis=1, en=0)
    cmds.separator()
    cmds.showWindow()
    cmds.setParent('..')
    
    tab2 = cmds.rowColumnLayout() ### Wheels
    cmds.text('Welcome to the wheels rigger')
    cmds.separator(w=400, h=20)
    cmds.text(l="Select the wheels you want to control together and click button")
    cmds.separator(w=350)
    rigWin.RadioSel=cmds.radioButtonGrp(l="Choose Direction for the arrow", la3=["X","Y","Z"], nrb=3, sl=3)
    cmds.separator(w=350)
    #cmds.button(l="MakeArrow", c="ArrowDrop()")
    #cmds.separator(w=400, h=20)
    cmds.text(l="Select the rotation speed for wheels")
    rigWin.RotSpeed=cmds.intSliderGrp(f=True, v=1, min=1, max=100, sbm="You are setting the rotation multiplier")
    rigWin.radioselection=cmds.radioButtonGrp(rigWin.RadioSel, q=True, sl=True)
    cmds.separator(w=400, h=20)
    cmds.button(l="Create Wheels Control", c="WheelSelection()")
    cmds.button(l="Reset",c="resetAll()")
    cmds.setParent('..')
    
    cmds.tabLayout(tabs, edit=True, tabLabel=((tab1, 'Tread Rig'), (tab2, 'Wheels')) )
    cmds.showWindow()

confirmVar = cmds.confirmDialog(t='Before Anything', m='Please ensure your model is placed along Z+', 
                                b=['Yes', 'No'], db='Yes', cb='No')
if confirmVar=='No':
    cmds.confirmDialog(m='Then you must reorient your model to face down Z+ axis and re-run the script')
else:
    rigWin()

    
### FUNCTIONS ###
def initFunc():#dump 2 locators for user
    if cmds.objExists('TreadFront_ASPLOC*'):#check if previosly undeleted ones exist and delete
        cmds.lockNode('TreadFront_ASPLOC*', lock=0)
        cmds.delete('TreadFront_ASPLOC*')
    if cmds.objExists('TreadBack_ASPLOC*'):
        cmds.lockNode('TreadBack_ASPLOC*', lock=0)
        cmds.delete('TreadBack_ASPLOC*')
    if cmds.objExists('FrontEnd_LOC_ASPGRP*'):
        cmds.lockNode('FrontEnd_LOC_ASPGRP*', lock=0)
        cmds.delete('FrontEnd_LOC_ASPGRP*')
    #Create locators
    initFunc.fronLoc = cmds.spaceLocator(n='TreadFront_ASPLOC')
    cmds.scale(5,5,5)
    cmds.move(0,0,10,r=1)
    initFunc.endLoc = cmds.spaceLocator(n='TreadBack_ASPLOC')
    cmds.scale(5,5,5)
    cmds.move(0,0,-10,r=1)
    initFunc.locGRP = cmds.group(initFunc.fronLoc[0], initFunc.endLoc[0], n='FrontEnd_LOC_ASPGRP')
    cmds.confirmDialog(m='Place the 2 locators at the front and back of your treads')
    #aim locators to each other
    cmds.aimConstraint(initFunc.fronLoc, initFunc.endLoc, mo=1, aim=(0,0,-1), upVector=(0,1,0), wut="vector", wu=(0,1,0))
    cmds.aimConstraint(initFunc.endLoc, initFunc.fronLoc, mo=1, aim=(0,0,1), upVector=(0,1,0), wut="vector", wu=(0,1,0))
    #lock rotations
    cmds.setAttr(initFunc.fronLoc[0]+'.rotate', lock=1)
    cmds.setAttr(initFunc.endLoc[0]+'.rotate', lock=1)
    #lock nodes
    cmds.lockNode(initFunc.fronLoc[0], lock=1)
    cmds.lockNode(initFunc.endLoc[0], lock=1)
    cmds.lockNode(initFunc.locGRP, lock=1)
    #Enable/Disable buttons
    cmds.text(rigWin.text1,e=1, en=0)
    cmds.button(rigWin.initBtn, e=1, enable=0)
    cmds.button(rigWin.OwnCurveBtn, e=1, vis=1, en=0)
    cmds.text(rigWin.text2,e=1, en=1)
    cmds.text(rigWin.textBox, e=1, en=1)
    cmds.textFieldGrp(rigWin.prefix, e=1, en=1)
    cmds.button(rigWin.resetBtn, e=1, enable=1)
    cmds.button(rigWin.makeCurveBtn, e=1, vis=1, en=1)

#RESET
def resetLoc():#delete locators
    try:
        cmds.lockNode(initFunc.fronLoc[0], lock=0)
        cmds.lockNode(initFunc.endLoc[0], lock=0)
        cmds.delete(initFunc.fronLoc,initFunc.endLoc)
    except:
        pass
    #enable/disable Buttons
    cmds.text(rigWin.text1,e=1, en=1)
    cmds.button(rigWin.initBtn, e=1, enable=1)
    cmds.button(rigWin.OwnCurveBtn, e=1, vis=1, en=1)
    cmds.text(rigWin.text2,e=1, en=0)
    cmds.text(rigWin.textBox, e=1, en=0)
    cmds.textFieldGrp(rigWin.prefix, e=1, en=0)
    cmds.button(rigWin.resetBtn, e=1, enable=0)
    cmds.button(rigWin.makeCurveBtn, e=1, vis=1, en=0)
    #If they exist, delete the following:
    if cmds.objExists(initFunc.locGRP):
        cmds.lockNode(initFunc.locGRP, lock=0)
        cmds.delete(initFunc.locGRP)
    if cmds.objExists(newReSpan):
        cmds.delete(newReSpan)
    if cmds.objExists('AllLocators'):
        cmds.delete("AllLocators*")
    if cmds.objExists(treadCurve[0]):
        cmds.delete(treadCurve)
    if wireOBJ!=default:
        if cmds.objExists(wireOBJ):
            cmds.delete(wireOBJ)

#CURVE:
def makeCurve():#This function creates curve based on 2 locators
    global treadCurve, uName
    #get user name
    uName = cmds.textFieldGrp(rigWin.prefix, q=1, tx=1)
    if uName=='':
        cmds.warning('Type name for the Treads')
    else:
        frontLocPos = cmds.xform(initFunc.fronLoc[0], q=1, t=1, ws=1)
        endLocPos = cmds.xform(initFunc.endLoc[0], q=1, t=1, ws=1)
        distToolVar = cmds.distanceDimension(sp=frontLocPos, ep=endLocPos)#get distance
        distVar = cmds.getAttr(distToolVar+'.distance')
        curveRadius = distVar/2
        distToolVar = distToolVar.replace('nShape', 'n')
        cmds.delete(distToolVar)
        #create curve
        treadCurve = cmds.circle(n='%s_CRV'%uName, r=curveRadius, nr=(1,0,0), ch=0)
        #position curve
        cmds.parentConstraint(initFunc.fronLoc[0], initFunc.endLoc[0], treadCurve, n='curveConDel', mo=0)
        cmds.delete('curveConDel')
        cmds.select(treadCurve, r=1)
        cmds.FreezeTransformations()
        #cmds.textFieldButtonGrp(makeWindow.objText, e=1, enable=1, vis=1)
        cmds.confirmDialog(m='Select and load the object to duplicate along the tread curve')
        cmds.lockNode(initFunc.fronLoc[0], lock=0)
        cmds.lockNode(initFunc.endLoc[0], lock=0)
        cmds.delete(initFunc.fronLoc,initFunc.endLoc)
        #enable/disable Buttons
        cmds.text(rigWin.text2,e=1, en=0)
        cmds.text(rigWin.textBox, e=1, en=0)
        cmds.textFieldGrp(rigWin.prefix, e=1, en=0)
        cmds.button(rigWin.makeCurveBtn, e=1, vis=1, en=0)
        cmds.text(rigWin.SelTxt, e=1, vis=1, en=1)
        cmds.button(rigWin.SelBTN, e=1, vis=1, en=1)
        cmds.text(rigWin.SpanTxt, e=1, vis=1, en=1)
        cmds.intSliderGrp(rigWin.SpanCount, e=1, vis=1, en=1)
        cmds.text(rigWin.EPTxt, e=1, vis=1, en=1)
        cmds.button(rigWin.EP, e=1, vis=1, en=1)
        return treadCurve, uName
        pickingOBJ()

#OWN CURVE
def ownCurve():
    global treadCurve
    selectedCurve=cmds.ls(sl=True)
    treadCurve=selectedCurve
    #enable/disable Buttons
    cmds.text(rigWin.text1,e=1, en=0)
    cmds.button(rigWin.initBtn, e=1, enable=0)
    cmds.button(rigWin.OwnCurveBtn, e=1, vis=1, en=0)
    cmds.text(rigWin.SelTxt, e=1, vis=1, en=1)
    cmds.button(rigWin.SelBTN, e=1, vis=1, en=1)
    cmds.text(rigWin.SpanTxt, e=1, vis=1, en=1)
    cmds.intSliderGrp(rigWin.SpanCount, e=1, vis=1, en=1)
    cmds.text(rigWin.EPTxt, e=1, vis=1, en=1)
    cmds.button(rigWin.EP, e=1, vis=1, en=1)
    return treadCurve, uName
    pickingOBJ()

#SPAN
def SpanChange():
    global SpanCount
    NewSpan=cmds.intSliderGrp(rigWin.SpanCount,q=True,v=True)
    print ("the new span count is now: %s" %NewSpan)
    selectedCurve=cmds.ls(sl=True)
    cmds.rebuildCurve(selectedCurve,rpo=True,kep=True,rt=0,s=NewSpan)
    cmds.select(selectedCurve)

#EDIT POINTS
def EPC():
    global EPlist
    selectedCurve=cmds.ls(sl=True)
    EPlist=cmds.ls(selectedCurve[0]+".ep[*]",fl=True)
    print (EPlist)
    LocList=[]
    #now we should select each EP on the selected curve and create locators and then contraint to each EP
    for EPi in EPlist:
        cmds.select(EPi,r=True)
        cmds.pointCurveConstraint()
        cmds.CenterPivot()
        LocList.append(cmds.rename("EPCTRL1"))
    cmds.select(LocList)
    cmds.group(n="AllLocators")
    cmds.select(selectedCurve)   
    #Enable/disable Buttons
    cmds.text(rigWin.SelTxt, e=1, vis=1, en=0)
    cmds.button(rigWin.SelBTN, e=1, vis=1, en=0)
    cmds.text(rigWin.SpanTxt, e=1, vis=1, en=0)
    cmds.intSliderGrp(rigWin.SpanCount, e=1, vis=1, en=0)
    cmds.text(rigWin.EPTxt, e=1, vis=1, en=0)
    cmds.button(rigWin.EP, e=1, vis=1, en=0)
    cmds.text(rigWin.text3,e=1, en=1)
    cmds.intSliderGrp(rigWin.ReSpanCount, e=1, en=1)
    cmds.textFieldButtonGrp(rigWin.ObjText, e=1, en=1, ed=True)
    cmds.intSliderGrp(rigWin.copyNum, e=1, en=1)
    cmds.checkBox(rigWin.previewCB, e=1, en=1)

#ReSpanner FOR LOCATORS
def ReSpanner():
    global newReSpan
    cmds.delete("AllLocators*")
    newReSpan=cmds.intSliderGrp(rigWin.ReSpanCount,q=True,v=True)
    selectedCurve=cmds.ls(sl=True)
    cmds.select(selectedCurve)
    cmds.rebuildCurve(selectedCurve,rpo=True,kep=True,rt=0,s=newReSpan)
    cmds.select(selectedCurve)
    EPC()
    prev()

#Selecting OBJ
def pickingOBJ():#This function identifies tread object
    global selOBJ
    selOBJ = cmds.ls(sl=1, objectsOnly=1)
    cmds.textFieldButtonGrp(rigWin.ObjText, tx=selOBJ[0], ed=True)
    cmds.intSliderGrp(rigWin.copyNum, e=1, vis=1)
    cmds.checkBox(rigWin.previewCB, e=1, vis=1)
    cmds.button(rigWin.finBtn, e=1, vis=1)
    return selOBJ

#TREAD
def makeTankTread(): #this function uses the picked obj and number of copies and makes treads
    global wireOBJ
    #Check if things exist, if they do, delete
    if wireOBJ!=default:
        if cmds.objExists(wireOBJ):
            cmds.delete(wireOBJ)
    updateCopyNum = cmds.intSliderGrp(rigWin.copyNum, q=True, v=True) #get amount of copies from user
    #Animating picked obj around path
    treadCurve=selectedCurve
    cmds.select(selOBJ, r=1)
    cmds.select(treadCurve, add=1)
    cmds.pathAnimation(n='TreadPathAnim', follow=1, followAxis='z', upAxis='y', wut="vector",worldUpVector=(0,1,0), inverseFront=0, inverseUp=0, startTimeU=1, endTimeU=updateCopyNum)
    cmds.select(selOBJ, r=1)
    cmds.selectKey('TreadPathAnim_uValue', time=(1,updateCopyNum))
    cmds.keyTangent(itt='linear', ott='linear')
    cmds.snapshot(n='Tread_ss', i=1, ch=0, st=1, et=updateCopyNum, u='animCurve')
    cmds.DeleteMotionPaths()
    #now we combine all duplicates and delete snapshot
    cmds.select('Tread_ssGroup', r=1)
    cmds.polyUnite(n='%s_GEO'%uName, ch=0)
    wireOBJ = cmds.ls(sl=1, o=1)[0]
    cmds.select('Tread_ssGroup', r=1)
    cmds.delete()
    #Setting a wire deformer---you need to get the deformer into a func and import arguments to it
    def createWireD(geo, crv, dropoffDist=80):
        wire=cmds.wire(geo, w=crv, n='%s_wire'%uName)
        wireNode = wire[0]
        cmds.setAttr(wireNode+".dropoffDistance[0]", dropoffDist)
    
    #cmds.select('TreadFull', r=1)
    #wireOBJ = cmds.ls(sl=1, o=1)[0]
    cmds.select(treadCurve, r=1)
    wireCRV = cmds.ls(sl=1, o=1)[0]
    createWireD(wireOBJ, wireCRV, 80)
    return wireOBJ

#PREVIEW
def prev():#Check if the user wants to preview the tread before finalizing
    if cmds.checkBox(rigWin.previewCB, q=1, v=1)==1:
        makeTankTread()
    else: #Check if things exist, if they do, delete
        if wireOBJ!=default:
            if cmds.objExists(wireOBJ):
                cmds.delete(wireOBJ)
    cmds.button(rigWin.finBtn, e=1, en=1)
    
def finalizeTread(): #Create final tread and close window
    makeTankTread()
    deleteVar = cmds.confirmDialog(t='Delete %s?'%selOBJ[0], m='Do you want to delete the original %s?'%selOBJ[0], b=['Yes', 'No'], defaultButton='Yes', cancelButton='No')
    if deleteVar=='Yes':
        cmds.delete(selOBJ)
    #Group objects
    cmds.select(wireOBJ, r=1)
    cmds.select(treadCurve, add=1)
    cmds.select(treadCurve[0]+'BaseWire', add=1)
    cmds.group(n='%s_GRP'%uName, w=1)
    #Delete extras
    cmds.lockNode(initFunc.locGRP, lock=0)
    cmds.lockNode(initFunc.fronLoc[0], lock=0)
    cmds.lockNode(initFunc.endLoc[0], lock=0)
    cmds.delete(initFunc.locGRP)
    cmds.button(rigWin.finBtn, e=1, vis=1, enable=0)
    cmds.button(rigWin.resetBtn, e=1, enable=0)



def resetAll():
    cmds.delete("WheelCTRL")
    cmds.select(WheelSelection.selectedWheels)
    cmds.ungroup("WheelsGroup")
    
def renamingAssets():
    cmds.rename("wheelCTRL","wheelCTRL1")
    cmds.rename("WheelsGroup","WheelsGroup1")
    
    
def WheelSelection():
    WheelSelection.selectedWheels=cmds.ls(sl=True)
    print(WheelSelection.selectedWheels)
    cmds.group(n="WheelsGroup") #AGREGAR Opcion de nombrar el grupo
    #cmds.spaceLocator(n="WheelCTRL")
    ArrowDrop()
    cmds.select("wheelCTRL")
    cmds.select("WheelsGroup", add=True)
    cmds.align(x="mid", y="min", z="mid", atl=True)
    #now we need the arrow controller to control the wheels
    cmds.select("wheelCTRL")
    RotationSpeed=cmds.intSliderGrp(rigWin.RotSpeed, q=True, v=True)
    for wheel in WheelSelection.selectedWheels:
        cmds.expression(n="rotator", s=wheel+".ry=wheelCTRL.tz*"+str(RotationSpeed))
    cmds.parentConstraint("wheelCTRL", "WheelsGroup", mo=True)
    renamingAssets()
    #cmds.scale(4.0,4.0,4.0)

def ArrowDrop():
    cmds.curve(n="wheelCTRL", d=1, p=[(-1,0,-2),(-1,0,2),(-2,0,2),(0,0,4),(2,0,2),
    (1,0,2),(1,0,-2),(2,0,-2),(0,0,-5),(-2,0,-2),(-1,0,-2)], k=[0,1,2,3,4,5,6,7,8,9,10])
    rigWin.radioselection=cmds.radioButtonGrp(rigWin.RadioSel, q=True, sl=True)
    if rigWin.radioselection==1:
        print("Direction is X")
        cmds.rotate(0,90,0)
    if rigWin.radioselection==2:
        print("Direction is Y")
        cmds.rotate(90,0,0)
    cmds.closeCurve(rpo=True)
    