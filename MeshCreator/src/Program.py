import sys  
import math

import matplotlib   
matplotlib.use('GTK')   
from matplotlib.figure import Figure   
from matplotlib.axes import Subplot   
from matplotlib.backends.backend_gtk import FigureCanvasGTK, NavigationToolbar   
from matplotlib.numerix import arange, sin, pi   

try:   
    import pygtk
    pygtk.require("2.0")
except:   
    pass

try:   
    import gtk   
    import gtk.glade
    import cairo
    from gtk import gdk
except:   
    sys.exit(1)
    
from Pslg import Pslg, GridPoint, Segment, Hole, Region
import ElementAwarePslg
import PslgIo

class PSLGView:
    pointDrawingSize = 2
    pointBorderSize = 4
    crossSize = 5
    crossBorderSize = 7
    
    def __init__(self, drawingArea):
        self.drawingArea = drawingArea
        self.pslg = Pslg()
        self.viewport = [(0, 0, 1.0)]
        self.selected = None
        
    def getSegmentsAsLinesList(self):
        psglSegments = self.pslg.getSegmentsAsLinesList()
        canvasSegments = []
        for psglSegment in psglSegments:
            canvasStartPoint = self.psglToCanvas(*psglSegment[0:2])
            canvasEndPoint = self.psglToCanvas(*psglSegment[2:4]) 
            canvasSegments.append((canvasStartPoint[0], 
                                   canvasStartPoint[1],
                                   canvasEndPoint[0],
                                   canvasEndPoint[1],
                                   psglSegment[4]))
        return canvasSegments
    
    def getPointsAsList(self):
        psglPoints = self.pslg.getPointsAsList()
        canvasPoints = []
        for psglPoint in psglPoints:
            canvasPoints.append(self.psglToCanvas(*psglPoint))
        return canvasPoints
        
    def getSelected(self):
        return self.selected
        
    def getHolesAsList(self):
        psglHoles = self.pslg.getHolesAsList()
        canvasHoles = []
        for psglHole in psglHoles:
            canvasHoles.append(self.psglToCanvas(*psglHole))
        return canvasHoles
    
    def getRegionsAsList(self):
        psglRegions = self.pslg.getRegionsAsList()
        canvasRegions = []
        for psglRegion in psglRegions:
            canvasRegions.append(self.psglToCanvas(*psglRegion))
        return canvasRegions
        
    def canvasToPsgl(self, x, y):
        allocation = self.drawingArea.get_allocation()
        curretViewport = self.viewport[-1]
        
        uniformX = x / allocation.width
        uniformY = y / allocation.height
        
        returnX = curretViewport[0] + uniformX / curretViewport[2]
        returnY = curretViewport[1] + uniformY / curretViewport[2]
        
        return (returnX, 1.0 - returnY) 
    
    def psglToCanvas(self, x, y):
        size = self.drawingArea.get_allocation()
        curretViewport = self.viewport[-1]
        
        invX = x
        invY = 1 - y
        
        returnX = int((invX - curretViewport[0]) * curretViewport[2] * size.width )
        returnY = int((invY - curretViewport[1]) * curretViewport[2] * size.height)
        
        return (returnX, returnY)
    
    def calculateDelta(self, canvasDelta):
        size = self.drawingArea.get_allocation()
        curretViewport = self.viewport[-1]        
        return canvasDelta / (curretViewport[2] * size.width)
    
    def getCurrentFactor(self):
        return self.viewport[-1][2]
    
    def tryToSelectPoint(self, x, y):
        (psglX, psglY) = self.canvasToPsgl(x, y)
        psglDelta = self.calculateDelta(PSLGView.pointBorderSize)
        
        if self.selected is not None and self.selected.__class__ is GridPoint:
            selectedDist = math.sqrt((self.selected.x - psglX) ** 2 + (self.selected.y - psglY) ** 2)
            if(selectedDist < psglDelta):
                return
        
        for point in self.pslg.points:
            dist = math.sqrt((point.x - psglX) ** 2 + (point.y - psglY) ** 2)
            if(dist < psglDelta):
                self.selected = point
                self.invalidateDrawingArea()
                return
        
        if self.selected is None:
            return
        
        self.selected = None
        self.invalidateDrawingArea()
        return

    def tryToSelectSegment(self, x, y):
        (psglX, psglY) = self.canvasToPsgl(x, y)
               
        if self.selected is not None and self.selected.__class__ is Segment:
            if self.isPointOnSegment(self.selected, (psglX, psglY)):
                return
        
        for segment in self.pslg.segments:
            if self.isPointOnSegment(segment, (psglX, psglY)):
                self.selected = segment
                self.invalidateDrawingArea()
                return
        
        if self.selected is None:
            return
        
        self.selected = None
        self.invalidateDrawingArea()
        return
    
    def isPointOnSegment(self, segment, point):
        factor = self.viewport[-1][2]
        startPoint = (segment.startpoint.x, segment.startpoint.y)
        endPoint = (segment.endpoint.x, segment.endpoint.y)
        
        startEndVector = (endPoint[0] - startPoint[0], endPoint[1] - startPoint[1])
        endStartVector = (startPoint[0] - endPoint[0], startPoint[1] - endPoint[1])
        startPointVector = (point[0] - startPoint[0], point[1] - startPoint[1])
        endPointVector = (point[0] - endPoint[0], point[1] - endPoint[1])
        
        crossProduct = startEndVector[0] * startPointVector[1] - startEndVector[1] * startPointVector[0]
        if abs(crossProduct) <= 1E-3 / factor:
            #startEndVector * startPointVector
            dot1 = startEndVector[0] * startPointVector[0] + startEndVector[1] * startPointVector[1]
            #endStartVector * endPointVector
            dot2 = endStartVector[0] * endPointVector[0] + endStartVector[1] * endPointVector[1]
            if dot1 > 0 and dot2 > 0:
                return True
        return False
    
    def tryToSelectHole(self, x, y):       
        (psglX, psglY) = self.canvasToPsgl(x, y)
        psglDelta = self.calculateDelta(PSLGView.crossBorderSize)
        
        if self.selected is not None and self.selected.__class__ is Hole:
            selectedDist = math.sqrt((self.selected.x - psglX) ** 2 + (self.selected.y - psglY) ** 2)
            if(selectedDist < psglDelta):
                return
        
        for hole in self.pslg.holes:
            dist = math.sqrt((hole.x - psglX) ** 2 + (hole.y - psglY) ** 2)
            if(dist < psglDelta):
                self.selected = hole
                self.invalidateDrawingArea()
                return
        
        if self.selected is None:
            return
        
        self.selected = None
        self.invalidateDrawingArea()
        return

    def tryToSelectRegion(self, x, y):       
        (psglX, psglY) = self.canvasToPsgl(x, y)
        psglDelta = self.calculateDelta(PSLGView.crossBorderSize)
        
        if self.selected is not None and self.selected.__class__ is Region:
            selectedDist = math.sqrt((self.selected.x - psglX) ** 2 + (self.selected.y - psglY) ** 2)
            if(selectedDist < psglDelta):
                return
        
        for region in self.pslg.regions:
            dist = math.sqrt((region.x - psglX) ** 2 + (region.y - psglY) ** 2)
            if(dist < psglDelta):
                self.selected = region
                self.invalidateDrawingArea()
                return
        
        if self.selected is None:
            return
        
        self.selected = None
        self.invalidateDrawingArea()
        return
    
    def forceDeselect(self):
        if self.selected is not None:
            self.selected = None
            self.invalidateDrawingArea()            

    def zoomIn(self, x, y):
        if(len(self.viewport) > 4):
            return
               
        allocation = self.drawingArea.get_allocation()
        oldX = self.viewport[-1][0]
        oldY = self.viewport[-1][1]
        oldFactor = self.viewport[-1][2]
              
        uniformX = x / allocation.width
        uniformY = y / allocation.height
        
        newX = max(oldX + uniformX / oldFactor - 1 / (4 * oldFactor), 0)
        newY = max(oldY + uniformY / oldFactor - 1 / (4 * oldFactor), 0)
        newFactor = 2 * oldFactor
        
        if newX + 1/newFactor > 1:
            newX = 1 - 1/newFactor
        if newY + 1/newFactor > 1:
            newY = 1 - 1/newFactor
        
        self.viewport.append((newX, newY, newFactor))
        self.invalidateDrawingArea()
        
    def zoomOut(self):
        if(len(self.viewport) > 1):
            self.viewport.pop()
            self.invalidateDrawingArea()
        
    def pan(self, dx, dy):        
        allocation = self.drawingArea.get_allocation()
        currentViewport = self.viewport.pop()
        
        uniformDeltaX = dx / allocation.width * 0.2
        uniformDeltaY = dy / allocation.height * 0.2
        
        newX = max(currentViewport[0] + uniformDeltaX, 0)
        newY = max(currentViewport[1] + uniformDeltaY, 0)
        factor = currentViewport[2]
        
        if newX + 1/factor > 1:
            newX = 1 - 1/factor
        if newY + 1/factor > 1:
            newY = 1 - 1/factor
    
        self.viewport.append((newX, newY, factor))
        self.invalidateDrawingArea()
    
    def invalidateDrawingArea(self):
        allocation = self.drawingArea.get_allocation()
        self.drawingArea.window.invalidate_rect(gdk.Rectangle(0, 0, allocation.width, allocation.height), False)

    def addPoint(self, x, y):
        (psglX, psglY) = self.canvasToPsgl(x, y)
        if self.selected is None or self.selected.__class__ is not GridPoint:
            self.pslg.points.append(GridPoint(psglX, psglY))
            self.invalidateDrawingArea()

    def removePoint(self, point):
        if point is None:
            return
        toBeRemoved = []
        for segment in self.pslg.segments:
            if segment.startpoint is point or segment.endpoint is point:
                toBeRemoved.append(segment)
        for removedSegment in toBeRemoved:
            self.pslg.segments.remove(removedSegment)
        self.pslg.points.remove(point)
        self.invalidateDrawingArea()

    def assignBoundaryMarkerToPoint(self, point, boundaryMarker):
        if point is None:
            return
        point.boundaryMarker = boundaryMarker

    def removeBoundaryMarkerFromPoint(self, point):
        if point is None:
            return
        point.boundaryMarker = None

    def addSegment(self, startPoint, endPoint):
        if startPoint is None or endPoint is None:
            return
        newSegment = Segment(startPoint, endPoint)
        if self.pslg.segments.count(newSegment) == 0:
            self.pslg.segments.append(newSegment)
            self.invalidateDrawingArea()

    def removeSelectedSegment(self):
        self.pslg.segments.remove(self.selected)
        self.forceDeselect()

    def addHole(self, x, y):
        (psglX, psglY) = self.canvasToPsgl(x, y)
        if self.selected is None or self.selected.__class__ is not Hole:
            self.pslg.holes.append(Hole(psglX, psglY))
            self.invalidateDrawingArea()

    def removeSelectedHole(self):
        self.pslg.holes.remove(self.selected)
        self.forceDeselect()

    def addRegion(self, x, y):
        (psglX, psglY) = self.canvasToPsgl(x, y)
        if self.selected is None or self.selected.__class__ is not Region:
            self.pslg.regions.append(Region(psglX, psglY))
            self.invalidateDrawingArea()
        
    def removeRegion(self, region):
        if region is None:
            return
        self.pslg.regions.remove(region)
        self.forceDeselect()
        
    def assignIdToRegion(self, region, regionId):
        if region is None:
            return
        region.id = regionId
        
    def removeIdFromRegion(self, region):
        if region is None:
            return
        region.id = None
        
    def new(self):
        self.pslg = Pslg()
        self.viewport = [(0, 0, 1.0)]
        self.selected = None
        self.invalidateDrawingArea()
    
    def save(self, filename):
        file = open(filename, "w")        
        try:
            PslgIo.saveToFile(file, self.pslg)
        finally:
            file.close()
        
    def load(self, filename):
        self.pslg = Pslg()
        self.viewport = [(0, 0, 1.0)]
        self.selected = None
        file = open(filename, "r")
        try:
            PslgIo.readFromFile(file, self.pslg, filename)
            self.invalidateDrawingArea()
        finally:
            file.close()
        
class DummyState:
    def __init__(self, view):
        self.view = view
    def leftDown(self, event):
        pass
    def rightDown(self, event):
        pass
    def leftUp(self, event):
        pass
    def rightUp(self, event):
        pass
    def mouseMove(self, event):
        self.view.tryToSelectPoint(event.x, event.y)            
    def mouseExit(self):
        self.view.forceDeselect()

class ZoomState:   
    def __init__(self, view):
        self.view = view
    def leftDown(self, event):
        self.view.zoomIn(event.x, event.y)
    def rightDown(self, event):
        self.view.zoomOut()
    def leftUp(self, event):
        pass
    def rightUp(self, event):
        pass    
    def mouseMove(self, event):
        pass
    def mouseExit(self):
        pass
        
class PanState:   
    def __init__(self, view):
        self.view = view
        self.prevPoint = None        
    def leftDown(self, event):
        self.prevPoint = (event.x, event.y)
    def rightDown(self, event):
        pass
    def leftUp(self, event):
        if self.prevPoint is not None:
            self.view.pan(*self.getPanVector(event.x, event.y))
        self.prevPoint = None
    def rightUp(self, event):
        pass
    def mouseMove(self, event):
        if self.prevPoint is not None:
            self.view.pan(*self.getPanVector(event.x, event.y))
            self.prevPoint = (event.x, event.y)
    def mouseExit(self):
        pass            
    def getPanVector(self, x, y):
        return (self.prevPoint[0] - x, self.prevPoint[1] - y)
        
class PointsState:
    def __init__(self, view, popupTree, boundaryMarkerSpinbutton):
        #Assigne members
        self.view = view
        self.popup = popupTree.get_widget("pointsMenu")
        self.boundaryMarkerSpinbutton = boundaryMarkerSpinbutton
        self.selectedPoint = None
        
        #Get menu items
        removePointMenuItem = popupTree.get_widget("removePointMenuitem")
        assignBoundaryMenuItem = popupTree.get_widget("assignBoundaryMenuitem")
        removeMarkerAssignmentMenuitem = popupTree.get_widget("removeMarkerAssignmentMenuitem")
        
        #Connect signals
        self.popup.connect("deactivate", self.onPointsMenuDeactivate)
        removePointMenuItem.connect("activate", self.onRemovePointMenuItemActivate)
        assignBoundaryMenuItem.connect("activate", self.onAssignBoundaryMenuItemActivate)
        removeMarkerAssignmentMenuitem.connect("activate", self.onRemoveMarkerAssignmentMenuItemActivate)        
    def leftDown(self, event):
        self.view.addPoint(event.x, event.y)
        self.view.tryToSelectPoint(event.x, event.y)
    def rightDown(self, event):
        if self.view.selected is not None and self.view.selected.__class__ is GridPoint:
            self.selectedPoint = self.view.selected
            self.popup.popup(None, None, None, event.button, event.time)
    def leftUp(self, event):
        pass
    def rightUp(self, event):
        pass
    def mouseMove(self, event):
        self.view.tryToSelectPoint(event.x, event.y)      
    def mouseExit(self):
        self.view.forceDeselect()
    def onPointsMenuDeactivate(self, widget):
        self.view.forceDeselect()
    def onRemovePointMenuItemActivate(self, widget):
        self.view.removePoint(self.selectedPoint)
        self.selectedPoint = None
    def onAssignBoundaryMenuItemActivate(self, widget):
        boundaryMarker = self.boundaryMarkerSpinbutton.get_value_as_int()
        self.view.assignBoundaryMarkerToPoint(self.selectedPoint, boundaryMarker)
        self.selectedPoint = None
    def onRemoveMarkerAssignmentMenuItemActivate(self, widget):
        self.view.removeBoundaryMarkerFromPoint(self.selectedPoint)
        self.selectedPoint = None
        
class SegmentsState:   
    def __init__(self, view):
        self.view = view
        self.newSegmentStartPoint = None        
    def leftDown(self, event):
        if self.view.selected is not None and self.view.selected.__class__ is GridPoint:
            self.newSegmentStartPoint = self.view.selected
        else:
            self.newSegmentStartPoint = None
    def rightDown(self, event):
        if self.view.selected is not None and self.view.selected.__class__ is Segment:
            self.view.removeSelectedSegment()
            self.tryToSelect(event)
    def leftUp(self, event):
        if (self.view.selected is not None) and (self.view.selected.__class__ is GridPoint):
            startPoint = self.newSegmentStartPoint
            endPoint = self.view.selected
            if startPoint is not endPoint:
                self.view.addSegment(startPoint, endPoint)
        self.newSegmentStartPoint = None
    def rightUp(self, event):
        pass
    def mouseMove(self, event):
        self.tryToSelect(event)
    def mouseExit(self):
        self.view.forceDeselect()
    def tryToSelect(self, event):
        self.view.tryToSelectPoint(event.x, event.y)
        if self.view.selected is None:
            self.view.tryToSelectSegment(event.x, event.y)
                    
class HolesState:   
    def __init__(self, view):
        self.view = view        
    def leftDown(self, event):
        self.view.addHole(event.x, event.y)
        self.view.tryToSelectHole(event.x, event.y)
    def rightDown(self, event):
        if self.view.selected is not None and self.view.selected.__class__ is Hole:
            self.view.removeSelectedHole();
            self.view.tryToSelectHole(event.x, event.y)
    def leftUp(self, event):
        pass
    def rightUp(self, event):
        pass        
    def mouseMove(self, event):
        self.view.tryToSelectHole(event.x, event.y)
    def mouseExit(self):
        self.view.forceDeselect()
    
class RegionsState:   
    def __init__(self, view, popupTree, regionSpinButton):
        #Assign members
        self.view = view
        self.popup = popupTree.get_widget("regionsMenu")
        self.regionSpinButton = regionSpinButton
        self.selectedRegion = None
                
        #Get menu items
        removeRegionMenuitem = popupTree.get_widget("removeRegionMenuitem")
        assignRegionMenuitem = popupTree.get_widget("assignRegionMenuitem")
        removeRegionAssignmentMenuitem = popupTree.get_widget("removeRegionAssignmentMenuitem")
                
        #Connect signals
        self.popup.connect("deactivate", self.onRegionsMenuDeactivate)
        removeRegionMenuitem.connect("activate", self.onRemoveRegionMenuitemActivate)
        assignRegionMenuitem.connect("activate", self.onAssignRegionMenuitemActivate)
        removeRegionAssignmentMenuitem.connect("activate", self.onRemoveRegionAssignmentMenuItemActivate)
    def leftDown(self, event):
        self.view.addRegion(event.x, event.y)
        self.view.tryToSelectRegion(event.x, event.y)
    def rightDown(self, event):
        if self.view.selected is not None and self.view.selected.__class__ is Region:
            self.selectedRegion = self.view.selected
            self.popup.popup(None, None, None, event.button, event.time)
    def leftUp(self, event):
        pass
    def rightUp(self, event):
        pass
    def mouseMove(self, event):
        self.view.tryToSelectRegion(event.x, event.y)
    def mouseExit(self):
        self.view.forceDeselect()
    def onRegionsMenuDeactivate(self, widget):
        self.view.forceDeselect()
    def onRemoveRegionMenuitemActivate(self, widget):
        self.view.removeRegion(self.selectedRegion)
        self.selectedRegion = None
    def onAssignRegionMenuitemActivate(self, widget):
        regionId = self.regionSpinButton.get_value_as_int()
        self.view.assignIdToRegion(self.selectedRegion, regionId)
        self.selectedRegion = None
    def onRemoveRegionAssignmentMenuItemActivate(self, widget):
        self.view.removeIdFromRegion(self.selectedRegion)
        self.selectedRegion = None

class MeshCreatorGui: 
    mousePositionContextId = "Mouse position"
    
    def __init__(self):        
        gladefile = "../ui/MeshCreator/MeshCreator.glade" 
        
        self.windowname = "MainWindow" 
        self.wTree = gtk.glade.XML(gladefile, self.windowname)
        self.statusBar = self.wTree.get_widget("StatusBar")
        self.drawingArea = self.wTree.get_widget("MainDrawingArea")
        self.boundaryMarkerSpinButton = self.wTree.get_widget("boundaryMarkerSpinButton")
        self.regionSpinButton = self.wTree.get_widget("regionSpinButton")
        self.toolboxContainer = self.wTree.get_widget("toolboxContainer")
        self.mainWindow = self.wTree.get_widget("MainWindow")
        self.background = None;
        
        self.pointsPopoupMenuTree = gtk.glade.XML(gladefile, "pointsMenu")
        pointsPopoupMenu = self.pointsPopoupMenuTree.get_widget("pointsMenu")
        pointsPopoupMenu.attach_to_widget(self.drawingArea, None)
        self.regionsPopoupMenuTree = gtk.glade.XML(gladefile, "regionsMenu")
        regionsPopoupMenu = self.regionsPopoupMenuTree.get_widget("regionsMenu")
        regionsPopoupMenu.attach_to_widget(self.drawingArea, None)
                 
        dic = {"on_MainWindow_destroy" : gtk.main_quit,
               "on_quit_activate" : gtk.main_quit,
               "on_MainDrawingArea_motion_notify" : self.onMainDrawingAreaMotion,
               "on_MainDrawingArea_leave_notify" : self.onMainDrawingAreaLeave,
               "on_MainDrawingArea_expose" : self.onMainDrawingAreaExpose,
               "on_MainDrawingArea_configure" : self.onMainDrawingAreaConfigure,
               "on_MainDrawingArea_button_press" : self.onMainDrawingAreaButtonPress,
               "on_MainDrawingArea_button_release" : self.onMainDrawingAreaButtonRelease,
               "on_zoomToggleButton_toggled" : self.onZoomToggleButtonToggled,
               "on_panToggleButton_toggled" : self.onPanToggleButtonToggled,
               "on_pointsToggleButton_toggled" : self.onPointsToggleButtonToggled,
               "on_segmentsToggleButton_toggled" : self.onSegmentsToggleButtonToggled,
               "on_holesToggleButton_toggled" : self.onHolesToggleButtonToggled,
               "on_regionsToggleButton_toggled" : self.onRegionsToggleButtonToggled,
               "on_new_activate" : self.onMenuNewActivate,
               "on_open_activate" : self.onMenuOpenActivate,
               "on_save_activate" : self.onMenuSaveActivate,
               "on_save_as_activate" : self.onMenuSaveAsActivate,
               "on_open_background_activate" : self.onMenuOpenBackgroundActivate,
               "on_close_background_activate" : self.onMenuCloseBackgroundActivate
               }
        self.wTree.signal_autoconnect(dic)
        
        self.titleBase = self.mainWindow.get_title()
        self.filename = None
        self.pslgView = PSLGView(self.drawingArea)
        self.state = DummyState(self.pslgView)
        
    def onMainDrawingAreaMotion(self, widget, event):
        self.updateStatusBar(event.x, event.y)
        self.state.mouseMove(event)            
        return True

    def onMainDrawingAreaLeave(self, widget, event):
        self.updateStatusBar(-1, -1)
        self.state.mouseExit()
        return True

    def onZoomToggleButtonToggled(self, widget):
        self.untoggleAllExcept(widget)
        if widget.get_active():
            self.state = ZoomState(self.pslgView)
        else:
            self.state = DummyState(self.pslgView)
        return True
               
    def onPanToggleButtonToggled(self, widget):
        self.untoggleAllExcept(widget)
        if widget.get_active():
            self.state = PanState(self.pslgView)
        else:
            self.state = DummyState(self.pslgView)
        return True

    def onPointsToggleButtonToggled(self, widget):
        self.untoggleAllExcept(widget)
        if widget.get_active():
            self.state = PointsState(self.pslgView, self.pointsPopoupMenuTree, self.boundaryMarkerSpinButton)
        else:
            self.state = DummyState(self.pslgView)
        return True
               
    def onSegmentsToggleButtonToggled(self, widget):
        self.untoggleAllExcept(widget)
        if widget.get_active():
            self.state = SegmentsState(self.pslgView)
        else:
            self.state = DummyState(self.pslgView)
        return True
    
    def onHolesToggleButtonToggled(self, widget):
        self.untoggleAllExcept(widget)
        if widget.get_active():
            self.state = HolesState(self.pslgView)
        else:
            self.state = DummyState(self.pslgView)
        return True
    
    def onRegionsToggleButtonToggled(self, widget):
        self.untoggleAllExcept(widget)
        if widget.get_active():
            self.state = RegionsState(self.pslgView, self.regionsPopoupMenuTree, self.regionSpinButton)
        else:
            self.state = DummyState(self.pslgView)
        return True

    def onMainDrawingAreaExpose(self, widget, event):
        allocation = self.drawingArea.get_allocation()        
        gc = self.drawingArea.window.cairo_create()
        gc.rectangle(event.area.x, event.area.y,
                     event.area.width, event.area.height)
        gc.clip()
               
        #Clear
        gc.set_line_width(1)
        gc.set_source_rgb(1,1,1)
        gc.rectangle(0, 0, allocation.width, allocation.height)
        gc.fill()
        gc.set_source_rgb(0,0,0)
        gc.rectangle(0, 0, allocation.width, allocation.height)
        gc.stroke()                            
               
        #Draw background
        if self.background is not None:
            zero = self.pslgView.psglToCanvas(0.0, 1.0)
            factor = self.pslgView.getCurrentFactor()
            newWidth = int(factor * allocation.width)
            newHeight = int(factor * allocation.height)
            
            gc.save()
            resizedPixbuf = self.background.scale_simple(newWidth, newHeight, gdk.INTERP_TILES)
            gc.set_source_pixbuf(resizedPixbuf, zero[0], zero[1])
            gc.paint()
            gc.restore()
               
        #Draw lines
        gc.set_source_rgb(0,0,0)        
        lines = self.pslgView.getSegmentsAsLinesList()
        for line in lines:
            if(line[4] == self.boundaryMarkerSpinButton.get_value_as_int()):
                gc.set_line_width(5)
            else:
                gc.set_line_width(1)
            gc.move_to(line[0], line[1])
            gc.line_to(line[2], line[3])
            gc.stroke()
         
        #Draw points
        gc.set_line_width(1)
        gc.set_source_rgb(0,0,0)
        points = self.pslgView.getPointsAsList()
        for point in points:
            gc.arc(point[0], point[1], 
                   PSLGView.pointDrawingSize, 
                   0, 2 * pi)
            gc.fill()
            
        #Draw holes
        gc.set_line_width(2)        
        gc.set_source_rgb(0,0,0)
        holes = self.pslgView.getHolesAsList()
        for hole in holes:
            gc.move_to(hole[0] - PSLGView.crossSize,
                       hole[1] - PSLGView.crossSize)
            gc.line_to(hole[0] + PSLGView.crossSize,
                       hole[1] + PSLGView.crossSize)
            gc.stroke()
            gc.move_to(hole[0] - PSLGView.crossSize,
                       hole[1] + PSLGView.crossSize)
            gc.line_to(hole[0] + PSLGView.crossSize,
                       hole[1] - PSLGView.crossSize)
            gc.stroke()
    
        #Draw regions
        gc.set_line_width(2)        
        gc.set_source_rgb(1.0,0,0)
        regions = self.pslgView.getRegionsAsList()
        for region in regions:
#            gc.set_source_rgb(0.75,0.75,0.75)            
#            gc.arc(region[0], region[1], 
#                   2, 
#                   0, 2 * pi)
#            gc.fill()            
            gc.move_to(region[0] - PSLGView.crossSize,
                       region[1] - PSLGView.crossSize)
            gc.line_to(region[0] + PSLGView.crossSize,
                       region[1] + PSLGView.crossSize)
            gc.stroke()
            gc.move_to(region[0] - PSLGView.crossSize,
                       region[1] + PSLGView.crossSize)
            gc.line_to(region[0] + PSLGView.crossSize,
                       region[1] - PSLGView.crossSize)            
            gc.stroke()
            
        #Draw selected    
        self.drawSelected(gc)
        
        #Return
        return True

    def drawSelected(self, gc):       
        #Draw slected point
        selected = self.pslgView.getSelected()
        if selected is not None and selected.__class__ is GridPoint:
            (cx, cy) = self.pslgView.psglToCanvas(selected.x, selected.y)
            gc.set_line_width(1)
            gc.set_source_rgb(1,0.6,0)
            gc.arc(cx, cy, 
                   PSLGView.pointDrawingSize, 
                   0, 2 * pi)
            gc.fill()
            if selected.boundaryMarker is not None:
                self.draw_text(gc, 
                               cx + PSLGView.pointDrawingSize, 
                               cy + PSLGView.pointDrawingSize,
                               str(selected.boundaryMarker))
            
        #Draw selected segment
        if selected is not None and selected.__class__ is Segment:
            psglStartPoint = selected.startpoint
            psglEndPoint = selected.endpoint
            (startCanvasX, startCanvasY) = self.pslgView.psglToCanvas(psglStartPoint.x, psglStartPoint.y)
            (endCanvasX, endCanvasY) = self.pslgView.psglToCanvas(psglEndPoint.x, psglEndPoint.y)
            gc.set_line_width(1)
            gc.set_source_rgb(1,0.6,0)
            gc.move_to(startCanvasX, startCanvasY)
            gc.line_to(endCanvasX, endCanvasY)
            gc.stroke()
            
        #Draw selected hole
        if selected is not None and selected.__class__ is Hole:
            (cx, cy) = self.pslgView.psglToCanvas(selected.x, selected.y)
            gc.set_line_width(2)
            gc.set_source_rgb(0.6,1,0)
            gc.move_to(cx - PSLGView.crossSize,
                       cy - PSLGView.crossSize)
            gc.line_to(cx + PSLGView.crossSize,
                       cy + PSLGView.crossSize)
            gc.stroke()
            gc.move_to(cx - PSLGView.crossSize,
                       cy + PSLGView.crossSize)
            gc.line_to(cx + PSLGView.crossSize,
                       cy - PSLGView.crossSize)
            gc.stroke()
            
        #Draw selected region
        if selected is not None and selected.__class__ is Region:
            (cx, cy) = self.pslgView.psglToCanvas(selected.x, selected.y)
            gc.set_line_width(2)
            gc.set_source_rgb(0.6,1,0)
            gc.move_to(cx - PSLGView.crossSize,
                       cy - PSLGView.crossSize)
            gc.line_to(cx + PSLGView.crossSize,
                       cy + PSLGView.crossSize)
            gc.stroke()
            gc.move_to(cx - PSLGView.crossSize,
                       cy + PSLGView.crossSize)
            gc.line_to(cx + PSLGView.crossSize,
                       cy - PSLGView.crossSize)
            gc.stroke()
            if selected.id is not None:
                self.draw_text(gc, 
                               cx + PSLGView.crossSize, 
                               cy - PSLGView.crossSize,
                               str(selected.id))

    def draw_text(self, gc, x, y, text):
        size = 10
        pad = 2
        font = "Sans"
        gc.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        gc.set_font_size(size)
        gc.set_line_width(0.5)
        gc.set_source_rgb(0,0,0)
        gc.move_to(x + pad, y + pad)
        gc.text_path(text)
        gc.fill()

    def onMainDrawingAreaConfigure(self, widget, event): 
        return True

    def onMainDrawingAreaButtonPress(self, widget, event):
        if(event.button == 1):
            self.state.leftDown(event)
        if(event.button == 3):
            self.state.rightDown(event)
        return True

    def onMainDrawingAreaButtonRelease(self, widget, event):
        if(event.button == 1):
            self.state.leftUp(event)
        if(event.button == 3):
            self.state.rightUp(event)
        return True

    def untoggleAllExcept(self, widget):
        if widget is not None and not widget.get_active():
            return
        for child in self.toolboxContainer:
            if child.__class__ is gtk.ToggleButton and child != widget:
                child.set_active(0)

    def updateStatusBar(self, eventX, eventY):
        context_id = self.statusBar.get_context_id(MeshCreatorGui.mousePositionContextId);
        self.statusBar.pop(context_id)        
        if eventX >= 0 and eventY >= 0:    
            (x, y) = self.pslgView.canvasToPsgl(eventX, eventY)
            (xC, yC) = self.pslgView.psglToCanvas(x, y)
            message = "X: " + str(x) + " Y: " + str(y) + " (" + str(xC) + ", " + str(yC) + ")"
            self.statusBar.push(context_id, message)
            
    def onMenuNewActivate(self, widget):
        self.pslgView.new()
        self.set_filename(None)
    
    def set_filename(self, filename):
        if filename is None:
            self.mainWindow.set_title(self.titleBase + " [Untitled]")
        else:
            self.mainWindow.set_title(self.titleBase + " [" + filename + "]")
        self.filename = filename
    
    def onMenuOpenActivate(self, widget):
        openFileChooser = gtk.FileChooserDialog(title="Open File", 
                                                action=gtk.FILE_CHOOSER_ACTION_OPEN, 
                                                buttons=(gtk.STOCK_CANCEL, 
                                                         gtk.RESPONSE_CANCEL, 
                                                         gtk.STOCK_OPEN, 
                                                         gtk.RESPONSE_OK)
                                                )
        
        filter = gtk.FileFilter()
        filter.set_name(".poly files")
        filter.add_pattern("*.poly")
        openFileChooser.add_filter(filter)
        
        filter = gtk.FileFilter()
        filter.set_name(".node files")
        filter.add_pattern("*.node")
        openFileChooser.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name(".ele files")
        filter.add_pattern("*.ele")
        openFileChooser.add_filter(filter)
        
        if openFileChooser.run() == gtk.RESPONSE_OK:
            try:
                choosenFilename = openFileChooser.get_filename()
                self.pslgView.load(choosenFilename)                
                self.set_filename(choosenFilename)
            except Exception, error:
                #Show error
                errorDialog = gtk.MessageDialog(buttons=gtk.BUTTONS_OK, 
                                                type=gtk.MESSAGE_ERROR)
                errorDialog.set_title("Error")
                errorDialog.set_markup("Error has occured:")
                errorDialog.format_secondary_text(str(error))
                errorDialog.run()
                errorDialog.destroy()
                #Unload file
                self.onMenuNewActivate(widget)
                raise
        openFileChooser.destroy()
    
    def onMenuSaveActivate(self, widget):
        if self.filename is None:
            self.onMenuSaveAsActivate(widget)
        else:
            self.pslgView.save(self.filename)

    def onMenuSaveAsActivate(self, widget):
        saveFileChooser = gtk.FileChooserDialog(title="Open File", 
                                                action=gtk.FILE_CHOOSER_ACTION_SAVE, 
                                                buttons=(gtk.STOCK_CANCEL, 
                                                         gtk.RESPONSE_CANCEL, 
                                                         gtk.STOCK_SAVE, 
                                                         gtk.RESPONSE_OK)
                                                )
        
        filter = gtk.FileFilter()
        filter.set_name(".poly files")
        filter.add_pattern("*.poly")
        saveFileChooser.set_do_overwrite_confirmation(True) 
        saveFileChooser.add_filter(filter)
        
        if saveFileChooser.run() == gtk.RESPONSE_OK:
            try:
                choosenFilename = saveFileChooser.get_filename()
                self.pslgView.save(choosenFilename)                
                self.set_filename(choosenFilename)
            except Exception, error:
                #Show error
                errorDialog = gtk.MessageDialog(buttons=gtk.BUTTONS_OK, 
                                                type=gtk.MESSAGE_ERROR)
                errorDialog.set_title("Error")
                errorDialog.set_markup("Error has occured:")
                errorDialog.format_secondary_text(str(error))
                errorDialog.run()
                errorDialog.destroy()
                raise
        saveFileChooser.destroy()
            
    def onMenuOpenBackgroundActivate(self, widget):
        openFileChooser = gtk.FileChooserDialog(title="Open File", 
                                                action=gtk.FILE_CHOOSER_ACTION_OPEN, 
                                                buttons=(gtk.STOCK_CANCEL, 
                                                         gtk.RESPONSE_CANCEL, 
                                                         gtk.STOCK_OPEN, 
                                                         gtk.RESPONSE_OK)
                                                )
        
        filter = gtk.FileFilter()
        filter.set_name("Image files")
        filter.add_pattern("*.bmp")
        filter.add_pattern("*.jpg")
        filter.add_pattern("*.jpeg")
        filter.add_pattern("*.gif")
        filter.add_pattern("*.png")
        openFileChooser.add_filter(filter)
        
        if openFileChooser.run() == gtk.RESPONSE_OK:
            try:
                #Read image
                choosenFilename = openFileChooser.get_filename()
                self.background = gdk.pixbuf_new_from_file(choosenFilename)
                
                #Force redraw
                self.pslgView.invalidateDrawingArea()
            except Exception, error:
                #Show error
                errorDialog = gtk.MessageDialog(buttons=gtk.BUTTONS_OK, 
                                                type=gtk.MESSAGE_ERROR)
                errorDialog.set_title("Error")
                errorDialog.set_markup("Error has occured:")
                errorDialog.format_secondary_text(str(error))
                errorDialog.run()
                errorDialog.destroy()
                #Unload file
                self.onMenuNewActivate(widget)
                raise
        openFileChooser.destroy()
 
    def onMenuCloseBackgroundActivate(self, widget):
        self.background = None
        self.pslgView.invalidateDrawingArea()
    
if __name__ == "__main__":
    MeshCreatorGui()
    gtk.main()