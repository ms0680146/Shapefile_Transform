#coding=utf-8
#Wxpython
import os
import wx
#---讀入相關函式庫------------------------------------------------------
import shapefile
#---------------------------------------------------------------------

wildcard =  "TXT files (*.txt)|*.txt" 

########################################################################
class MyForm(wx.Frame):
 
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY,title ="Shapefile Transform",size=(450,400))

        chooseBox=wx.SingleChoiceDialog(parent=None,message=u'選擇檔案類型',caption='Shapefile Transform',choices=[u'點資料',u'線資料',u'面資料'])
        chooseBox.ShowModal()
        choice=chooseBox.GetStringSelection()

        panel = wx.Panel(self, wx.ID_ANY)
        self.currentDirectory = os.getcwd()
        
        if choice==u'點資料':
            # create the buttons and bindings
            #Step1
            wx.StaticText(parent=panel,label='Step1:',pos=(20,50))
            openFileDlgBtn = wx.Button(panel, label=u"載入點資料檔名(檔名最好是英文，例如：a.txt):",pos=(70,50))
            openFileDlgBtn.Bind(wx.EVT_BUTTON, self.onOpenFile)
            self.readfile=wx.StaticText(parent=panel,label='',pos=(70,90))
            #Step2
            wx.StaticText(parent=panel,label='Step2:',pos=(20,130))
            wx.StaticText(parent=panel,label=u'請輸入點Shapefile檔名(檔名最好是英文，例如：G1-Point2012):',pos=(70,130))
            self.shapefilename=wx.TextCtrl(parent=panel,value='',pos=(70,160))
            #Step3
            wx.StaticText(parent=panel,label='Step3:',pos=(20,200))
            button=wx.Button(parent=panel,label=u'轉換!',pos=(70,200))
            self.msg=wx.StaticText(parent=panel,label='',pos=(70,240))
            self.Bind(wx.EVT_BUTTON,self.shp_generate_point,button)
                                   
                                   
        elif choice==u'線資料':
            # create the buttons and bindings
            #Step1
            wx.StaticText(parent=panel,label='Step1:',pos=(20,50))
            openFileDlgBtn = wx.Button(panel, label=u"載入線資料檔名(檔名最好是英文，例如：a.txt):",pos=(70,50))
            openFileDlgBtn.Bind(wx.EVT_BUTTON, self.onOpenFile)
            self.readfile=wx.StaticText(parent=panel,label='',pos=(70,90))
            #Step2
            wx.StaticText(parent=panel,label='Step2:',pos=(20,130))
            wx.StaticText(parent=panel,label=u'請輸入線Shapefile檔名(檔名最好是英文，例如：G1-Line2012):',pos=(70,130))
            self.shapefilename=wx.TextCtrl(parent=panel,value='',pos=(70,160))
            #Step3
            wx.StaticText(parent=panel,label='Step3:',pos=(20,200))
            button=wx.Button(parent=panel,label=u'轉換!',pos=(70,200))
            self.msg=wx.StaticText(parent=panel,label='',pos=(70,240))
            self.Bind(wx.EVT_BUTTON,self.shp_generate_line,button)
            
        elif choice==u'面資料':
            # create the buttons and bindings
            #Step1
            wx.StaticText(parent=panel,label='Step1:',pos=(20,50))
            openFileDlgBtn = wx.Button(panel, label=u"載入面資料檔名(檔名最好是英文，例如：a.txt):",pos=(70,50))
            openFileDlgBtn.Bind(wx.EVT_BUTTON, self.onOpenFile)
            self.readfile=wx.StaticText(parent=panel,label='',pos=(70,90))
            #Step2
            wx.StaticText(parent=panel,label='Step2:',pos=(20,130))
            wx.StaticText(parent=panel,label=u'請輸入面Shapefile檔名(檔名最好是英文，例如：G1-Polygon2012):',pos=(70,130))
            self.shapefilename=wx.TextCtrl(parent=panel,value='',pos=(70,160))
            #Step3
            wx.StaticText(parent=panel,label='Step3:',pos=(20,200))
            button=wx.Button(parent=panel,label=u'轉換!',pos=(70,200))
            self.msg=wx.StaticText(parent=panel,label='',pos=(70,240))
            self.Bind(wx.EVT_BUTTON,self.shp_generate_polygon,button)
            

 
    #----------------------------------------------------------------------
    def onOpenFile(self, event):
        """
        Create and show the Open FileDialog
        """
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=self.currentDirectory, 
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            try:
                global fin
                fin=open(filename)
                print "資料檔讀取成功"
                self.readfile.SetLabel(u"資料檔讀取成功")
                
            except:
                print "輸入資料檔名錯誤!"
                self.readfile.SetLabel(u"輸入資料檔名錯誤!")
            
        dlg.Destroy()


    #Shapefile_Transform_Point----------------------------------------------------------------------
    def shp_generate_point(self,event):

        shp = shapefile.Writer(shapefile.POINT)
        #新增屬性欄位(點號,橫坐標(X),縱座標(Y),正高(Z),控制點種類,測量方法,使用儀器,測定日期(yyyymmdd),測量員,記錄者,點之記網頁,備註)
        shp.field('ID','C','10')
        shp.field('X','F','15',3)
        shp.field('Y','F','15',3)
        shp.field('Z','F','10',3)
        shp.field('POINT_TYPE','C','10')
        shp.field('METHOD','C','40')
        shp.field('INSTRUMENT','C','40')
        shp.field('DATE','C','8')
        shp.field('OPERATOR','C','20')
        shp.field('RECORDER','C','20')
        shp.field('URL','C','50')
        shp.field('REMARKS','C','50')
        
        # 讀取第一列的檔頭，此為欄位說明，不屬於資料的一部分
        first_line = fin.readline()

        for line in fin:
            line.strip()
            id,x,y,z,pointType,method,inst,dt,operator,recorder,url,remark = line.split(',')
            X=float(x)
            Y=float(y)
            Z=float(z)
            
            #加入點位空間資料(坐標)以及屬性資料
            shp.point(X,Y)      #空間資料
            shp.record(id,x,y,z,pointType,method,inst,dt,operator,recorder,url,remark)    #屬性資料

        fileOut=str(self.shapefilename.GetValue())
        print(type(fileOut))
        try:
            shp.save(fileOut)
            print "Shapefile圖檔 %s 產製成功!" % fileOut
            self.msg.SetLabel(u"Shapefile圖檔 %s 產製成功!")
        except:
            print "Shapefile圖檔 %s 產製失敗!" % fileOut
            self.msg.SetLabel(u"Shapefile圖檔 %s 產製失敗!")


    #Shapefile_Transform_Line----------------------------------------------------------------------
    def shp_generate_line(self,event):

        #產生一個PolyLine的Shapefile檔
        shp = shapefile.Writer(shapefile.POLYLINE)

        #新增屬性欄位(編號,名稱,測量方法,使用儀器,測定日期(yyyymmdd),測量員,記錄者,備註)
        shp.field('ID','C','10')
        shp.field('NAME','C','10')
        shp.field('METHOD','C','40')
        shp.field('INSTRUMENT','C','40')
        shp.field('DATE','C','8')
        shp.field('OPERATOR','C','20')
        shp.field('RECORDER','C','20')
        shp.field('REMARKS','C','50')
        
        # 讀取第一列的檔頭，此為欄位說明，不屬於資料的一部分
        first_line = fin.readline()

        while True:
            line = fin.readline()
            
            if not line:
                break
                
            line.strip()
            s = line.split(',')
            id = s[0]
            name = s[1]
            method = s[2]
            inst = s[3]
            dt = s[4]
            operator = s[5]
            recorder = s[6]
            remark = s[7]
            
            t = ""
            while True:
                l = fin.readline()
                l.strip()
                t = t + l
                if ']' in l:
                    break

            t1 = t.replace('[', ' ')
            t2 = t1.replace(']', ' ')
            segments = t2.split(';')
            
            parts = []
            
            for seg in segments:
                a = seg.split()
                l = len(a)
               
                if l % 2 != 0 or l < 4:
                    print "線段之轉折點必須為(X Y)格式，且至少兩個點對，請檢查資料內容"
                    return
                    
                p = []
                for i in range(0, l, 2):
                    x = float(a[i])
                    y = float(a[i+1])
                    p.append([x,y])
                    
                parts.append(p)
                
            #加入點位空間資料(坐標)以及屬性資料
            shp.line(parts)      #空間資料
            shp.record(id,name,method,inst,dt,operator,recorder,remark)    #屬性資料

            fileOut=str(self.shapefilename.GetValue())
            print(type(fileOut))
            #存成檔名為fileOut的shapefile檔
            try:
                shp.save(fileOut)
                print "Shapefile圖檔 %s 產製成功!" % fileOut
                self.msg.SetLabel(u"Shapefile圖檔 %s 產製成功!")
            except:
                print "Shapefile圖檔 %s 產製失敗!" % fileOut
                self.msg.SetLabel(u"Shapefile圖檔 %s 產製失敗!")


    #Shapefile_Transform_Polygon----------------------------------------------------------------------
    def shp_generate_polygon(self,event):


        #產生一個PolyLine的Shapefile檔
        shp = shapefile.Writer(shapefile.POLYGON)

        #新增屬性欄位(編號,名稱,測量方法,使用儀器,測定日期(yyyymmdd),測量員,記錄者,備註)
        shp.field('ID','C','10')
        shp.field('NAME','C','10')
        shp.field('METHOD','C','40')
        shp.field('INSTRUMENT','C','40')
        shp.field('DATE','C','8')
        shp.field('OPERATOR','C','20')
        shp.field('RECORDER','C','20')
        shp.field('REMARKS','C','50')
        
        # 讀取第一列的檔頭，此為欄位說明，不屬於資料的一部分
        first_line = fin.readline()

        while True:
            line = fin.readline()
            
            if not line:
                break
                
            line.strip()
            s = line.split(',')
            id = s[0]
            name = s[1]
            method = s[2]
            inst = s[3]
            dt = s[4]
            operator = s[5]
            recorder = s[6]
            remark = s[7]
            
            t = ""
            while True:
                l = fin.readline()
                l.strip()
                t = t + l
                if ']' in l:
                    break

            t1 = t.replace('[', ' ')
            t2 = t1.replace(']', ' ')
            segments = t2.split(';')
     
            parts = []
            
            for seg in segments:
                a = seg.split()
                l = len(a)
               
                if l % 2 != 0 or l < 4:
                    print "線段之轉折點必須為(X Y)格式，且至少兩個點對，請檢查資料內容"
                    return
                    
                p = []
                for i in range(0, l, 2):
                    x = float(a[i])
                    y = float(a[i+1])
                    p.append([x,y])
                    
                parts.append(p)
                
            #加入點位空間資料(坐標)以及屬性資料
            shp.poly(parts)      #空間資料
            shp.record(id,name,method,inst,dt,operator,recorder,remark)    #屬性資料

            fileOut=str(self.shapefilename.GetValue())
            print(type(fileOut))
            #存成檔名為fileOut的shapefile檔
            try:
                shp.save(fileOut)
                print "Shapefile圖檔 %s 產製成功!" % fileOut
                self.msg.SetLabel(u"Shapefile圖檔 %s 產製成功!")
            except:
                print "Shapefile圖檔 %s 產製失敗!" % fileOut
                self.msg.SetLabel(u"Shapefile圖檔 %s 產製失敗!")
 
#----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()
