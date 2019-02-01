#coding: utf-8
#-----------------------------------------------------------------------------------------------------------------------
import wx

import os
#-----------------------------------------------------------------------------------------------------------------------
class MyGUI:
    def __init__(self):
        self.app = wx.App()

        self.frame = wx.Frame(None, title=u'PDF合并', size=(1000, 800), \
                              style=wx.DEFAULT_FRAME_STYLE)
        self.frame.CenterOnScreen()
        self.frame.Show()

        self.frame.SetAutoLayout(True)
        self.bkg = wx.Panel(self.frame, size=(1000, 400))
        self.edit_area = MyCanvas(self.frame, -1, size = (1000, 400))

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.edit_area,0,wx.EXPAND|wx.ALL,5)
        self.vbox.Add(self.bkg,1,wx.EXPAND)
        self.frame.SetSizerAndFit(self.vbox)

        #self.status_bar = wx.StatusBar(self.frame, id=-1)
        #self.frame.SetStatusBar(self.status_bar)
        #self.status_bar = self.frame.CreateStatusBar()
        #self.status_bar.SetFieldsCount(1)
        #self.status_text = u'当前日期未设定......'
        #self.status_bar.SetStatusText(self.status_text, 0)
               
        self.font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        self.font.SetPointSize(10)        
        #self.bitmap = wx.Bitmap(u'page-0.jpeg', wx.BITMAP_TYPE_JPEG)
        #self.static_img = wx.StaticBitmap(self.bkg, -1, self.bitmap, size=(200, 400), pos=(5, 5))
#-------------------------------------------------------------------   
        #self.hbox = wx.BoxSizer()                        
        #self.hbox.Add(self.import_button, proportion=0, \
        #              flag=wx.ALIGN_RIGHT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=5)
        #self.hbox.Add(self.run_button, proportion=0, \
        #              flag=wx.ALIGN_RIGHT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=5)
        #self.hbox.Add(self.export_button, proportion=0, \
        #              flag=wx.ALIGN_RIGHT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=5)
        #self.vbox = wx.BoxSizer(wx.VERTICAL)
        #self.vbox.Add(self.result_contents, proportion=0, \
        #              flag=wx.EXPAND | wx.ALL, border=15)
        #self.vbox.Add(self.static_img, proportion=0, \
        #              flag=wx.EXPAND | wx.ALL, border=15)
        #self.vbox.Add(self.hbox, proportion=0, \
        #              flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border=5)
        #self.bkg.SetSizer(self.vbox)            
#------------------------------------------------
        self.menu_bar = wx.MenuBar()
        self.menu_file = wx.Menu()
        self.menu_edit = wx.Menu()
        self.menu_view = wx.Menu()
        self.menu_help = wx.Menu()
        
        self.menu_bar.Append(self.menu_file, u'文件(&F)')
        self.menu_file.Append(101, u'导入')
        #self.menu_bar.Append(self.menu_edit, u'编辑(&E)')
        #self.menu_edit.Append(201, u'合并')
        #self.menu_bar.Append(self.menu_view, u'查看(&V)')        


        self.menu_bar.Append(self.menu_help, u'帮助(&H)')
        self.menu_help.Append(401, u'关于')

        self.frame.SetMenuBar(self.menu_bar) 

        self.frame.Bind(wx.EVT_MENU, self.importFile, id=101)
        #self.frame.Bind(wx.EVT_MENU, self.mergePDF, id=201)
        #self.frame.Bind(wx.EVT_MENU, self.export_result, id=103)
        self.frame.Bind(wx.EVT_MENU, self.OnHelp, id=401)            

    def importFile(self, event):
        self.dlg = wx.FileDialog(self.bkg,
                        message='Choose a file',
                        defaultDir=os.getcwd(),
                        defaultFile='',
                        wildcard='All files (*.*) | *.*',
                        style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR)
        self.dlg.ShowModal()
        self.file_paths = self.dlg.GetPaths()  # return a list of path
        self.file_names = self.dlg.GetFilenames()
        
        self.edit_area.DoDrawing(self.edit_area.pdc, self.file_paths)

    def OnHelp(self, event):
        self.dlg_ok = wx.MessageDialog(self.bkg, u'作者：MengZhangsu', u'软件信息', wx.OK)
        self.dlg_ok.ShowModal()
        self.dlg_ok.Destroy()

#--------------------
hitradius = 1 

class MyCanvas(wx.ScrolledWindow):
    def __init__(self, parent, id, size = wx.DefaultSize):
        wx.ScrolledWindow.__init__(self, parent, id, (0, 0), size=size, style=wx.SUNKEN_BORDER)

        self.maxWidth  = 2000 
        self.maxHeight = 400 
        self.x = self.y = 0

        self.SetBackgroundColour("GREY")

        self.SetVirtualSize((self.maxWidth, self.maxHeight))
        self.SetScrollRate(20,20)
        
        # create a PseudoDC to record our drawing
        self.pdc = wx.PseudoDC()
        #self.DoDrawing(self.pdc)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda x:None)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouse)
        
        # vars for handling mouse clicks
        self.dragid = -1
        self.needChangePosId = -1
        self.lastpos = (0,0)
        self.direction = None #draged shape moving direction
        self.dragedshape_initpos = (0, 0)
        self.posoffset = 0
    
    def ConvertEventCoords(self, event):
        xView, yView = self.GetViewStart()
        xDelta, yDelta = self.GetScrollPixelsPerUnit()
        return (event.GetX() + (xView * xDelta),
            event.GetY() + (yView * yDelta))

    def OffsetRect(self, r):
        xView, yView = self.GetViewStart()
        xDelta, yDelta = self.GetScrollPixelsPerUnit()
        r.OffsetXY(-(xView*xDelta),-(yView*yDelta))

    def OnMouse(self, event):
        global hitradius
        if event.LeftDown():
            x,y = self.ConvertEventCoords(event)
            l = self.pdc.FindObjects(x, y, hitradius)
            for id in l:
                if not self.pdc.GetIdGreyedOut(id):
                    self.dragid = id
                    self.lastpos = (event.GetX(),event.GetY())
                    self.dragedshape_initpos = self.pdc.GetIdBounds(self.dragid)
                    break
        
        elif event.Dragging() or event.LeftUp():
            if self.dragid != -1:
                x,y = self.lastpos
                dx = event.GetX() - x
                dy = event.GetY() - y
                r = self.pdc.GetIdBounds(self.dragid)
                self.pdc.TranslateId(self.dragid, dx, dy)
                r2 = self.pdc.GetIdBounds(self.dragid)
                r = r.Union(r2)
                r.Inflate(4,4)
                self.OffsetRect(r)
                self.RefreshRect(r, False)
                self.lastpos = (event.GetX(),event.GetY())
                
                movingShape = self.pdc.GetIdBounds(self.dragid)
                if movingShape[0] - self.dragedshape_initpos[0] > 0:
                    self.direction = u'ToRight'
                elif movingShape[0] - self.dragedshape_initpos[0] < 0:
                    self.direction = u'ToLeft'
                
                if self.direction == u'ToRight':
                    l = self.pdc.FindObjects(movingShape[0] + 200, movingShape[1], hitradius)#drag to right
                    for id in l:
                        if id <> self.dragid:
                            self.needChangePosId = id
                    R = self.pdc.GetIdBounds(self.needChangePosId)
                
                    if movingShape[0] + 200 > R[0] + 100 and movingShape[0] + 200 < R[0] + 200:
                        self.pdc.TranslateId(self.needChangePosId, -220, 0)
                        self.dragedshape_initpos[0] = self.dragedshape_initpos[0] + 220
                        self.posoffset = 50
                    needRefreshR = wx.Rect(x, y, 200, 400)
                    needRefreshR.Union(R)
                    needRefreshR.Inflate(4,4)
                    self.OffsetRect(needRefreshR)
                    self.RefreshRect(needRefreshR, False)
                    self.direction = None
                
                if self.direction == u'ToLeft':
                    l = self.pdc.FindObjects(movingShape[0],movingShape[1], hitradius)#drag to left
                    for id in l:
                        if id <> self.dragid:
                            self.needChangePosId = id
                    R = self.pdc.GetIdBounds(self.needChangePosId)

                    if movingShape[0] > R[0] and movingShape[0] < R[0] + 100:
                        self.pdc.TranslateId(self.needChangePosId, 220, 0)
                        self.dragedshape_initpos[0] = self.dragedshape_initpos[0] - 220
                        self.posoffset = -50
                    needRefreshR = wx.Rect(x, y, 200, 400)
                    needRefreshR.Union(R)
                    needRefreshR.Inflate(4,4)
                    self.OffsetRect(needRefreshR)
                    self.RefreshRect(needRefreshR, False)
                    self.direction = None

                
                
            if event.LeftUp():
                r = self.pdc.GetIdBounds(self.dragid)
                self.standardreleasePos = self.checkPos(r[0] + self.posoffset, r[1] + self.posoffset)
                dx = self.standardreleasePos[0] - r[0]
                dy = self.standardreleasePos[1] - r[1]
                self.pdc.TranslateId(self.dragid, dx, dy)
                r2 = self.pdc.GetIdBounds(self.dragid)
                r = r.Union(r2)
                r.Inflate(4,4)
                self.OffsetRect(r)
                self.RefreshRect(r, False)

                self.dragid = -1
                self.needChangePosId = -1
                self.posoffset = 0

    def OnPaint(self, event):
        # Create a buffered paint DC.  It will create the real
        # wx.PaintDC and then blit the bitmap to it when dc is
        # deleted.  
        dc = wx.BufferedPaintDC(self)
        # use PrepateDC to set position correctly
        self.PrepareDC(dc)
        # we need to clear the dc BEFORE calling PrepareDC
        bg = wx.Brush(self.GetBackgroundColour())
        dc.SetBackground(bg)
        dc.Clear()
        # create a clipping rect from our position and size
        # and the Update Region
        xv, yv = self.GetViewStart()
        dx, dy = self.GetScrollPixelsPerUnit()
        x, y   = (xv * dx, yv * dy)
        rgn = self.GetUpdateRegion()
        rgn.Offset(x,y)
        r = rgn.GetBox()
        # draw to the dc using the calculated clipping rect
        self.pdc.DrawToDCClipped(dc,r)


    def DoDrawing(self, dc, file_names):
        filenames = file_names
        self.objids = []
        dc.BeginDrawing()
        pos_counter = 0

        for name in filenames:
            id = wx.NewId()
            dc.SetId(id)
            self.bitmap = wx.Bitmap(name, wx.BITMAP_TYPE_JPEG)
            image = self.bitmap.ConvertToImage()
            image.Rescale(200, 283)
            self.bitmap = image.ConvertToBitmap()
                
            w = self.bitmap.GetWidth()
            h = self.bitmap.GetHeight()

            x = pos_counter * w +  (pos_counter+1) * 20 
            y = 20 

            dc.DrawBitmap(self.bitmap,x,y)
            r = wx.Rect(x,y,w,h)
            dc.SetIdBounds(id,r)
            self.objids.append(id)
            pos_counter += 1
            self.SetVirtualSize(((pos_counter+1)*220, self.maxHeight))
        dc.EndDrawing()
        self.RefreshRect((0, 0, self.maxWidth, self.maxHeight), False)

    def checkPos(self, x, y):
        if y <> 20:
            y = 20 
        x =  int(x / 200) * 200 + (int(x / 200) + 1) * 20
        if x < 0:
            x = 20 
        return x, y

    def changePos(self, event):
        pass

#------------------------------------------------------------------------------------------------
def main():
    my_gui = MyGUI()
    my_gui.app.MainLoop()

if __name__ == '__main__':
    main()
