#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
列表控件学习
"""



sys.exit();





import os
import wx
import wx.lib.mixins.listctrl as listmix
import wx.lib.masked          as masked

import sqlite3


data = {1 : ("1", "明天干什么", "2010-05-03 19:30", u'频率1'),
        2 : ("2", "后天干什么", "2010-05-03 17:30", u"表格控件"),
        3 : ("3", "大后天干什么", "2010-07-03 17:30", u"树控件"),
        4 : ("4", "下周干什么", "2010-05-03 17:30", u"定时器控件")
       }


class MyListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)      
        listmix.ListCtrlAutoWidthMixin.__init__(self)     # 使列的宽度与ListCtrl的宽度自动对齐
        
        self.setColumns()
        
        # 提示清除成功

        
    def setColumns(self):
        # 定义列头
        self.InsertColumn(0, u"ID")
        self.InsertColumn(1, u"提醒名")
        self.InsertColumn(2, u"下次提醒时间")
        self.InsertColumn(3, u"频率")
        # 设置各列中的值
        items = data.items()
        
    
        for key, values in items:            
            #    InsertStringItem(self, long index, String label, int imageIndex=-1) -> long
            index = self.InsertStringItem(sys.maxint, str(values[0]))
            for i in range(len(values)):
                self.SetStringItem(index, i, str(values[i]))
                self.SetItemData(index, key)               # 设置列表控件的每行数据    
        # 设置列的宽度
        self.SetColumnWidth(0, 30)
        self.SetColumnWidth(1, 200)
        # 第3列的宽度自动对齐
        self.SetColumnWidth(2, 90)
        self.SetColumnWidth(2, 130)
        
        # 列表事件
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        
        ### 调试需要起个别名
        self.list = self
        
       
    def OnDoubleClick(self, event):
        # curr_item 为行索引，从 0 开始的
        curr_item = self.list.GetFocusedItem()  # 获得聚焦的行索引
        curr_item = self.list.GetFirstSelected() # 获得被选择的第一行的索引(可能被选择多行)
        # CurrItem 实际上是单元个 cell, 第二个参数为列数
        # 如果当前没有选择任何行，则输出专门提示信息
        if curr_item < 0:
            # 添加提醒
            self.AlarmItem = AlarmEdit(self)
        else:
            # 获得该行第二列的单元格
            self.AlarmItem = AlarmEdit(self, self.list.GetItem(curr_item).GetText())
            Cell2 = self.list.GetItem(curr_item, 1)
            Cell3 = self.list.GetItem(curr_item, 2)
            #print u"当前行 %d, 第二列 %s, 第三列 %s" % (curr_item, Cell2.GetText(), Cell3.GetText())
            
        self.AlarmItem.ShowModal()

class AlarmView(wx.Dialog):
    """
    查看项
    """
    _aid = None
    
    def __init__(self, parent, aid=None):
        
        wx.Dialog.__init__(self, parent, -1, '提醒项', size=(700,300))
        
        panel = wx.Panel(self) 
        self._aid = aid

        
    

class AlarmEdit(wx.Dialog):
    """
    添加和编辑提醒项(aid 为 None 表示添加)
    """
    _aid = None     # 如果是编辑。该值保存提醒 id, 否则为 None
    def __init__(self, parent, aid=None):
        wx.Dialog.__init__(self, parent, -1, '提醒项', size=(700,300))
        
        panel = wx.Panel(self) 
        self._aid = aid
        
        ### 先确定数据值(添加和编辑不一样)
        if aid == None:
            title = u'默认值'
            content = u'默认内容'
            ### 默认时间和日期目前没有用
            alarm_date = '2010-05-12'
            alarm_time = '19:20'
        else:
            title = u'获取值 %s' % aid
            content = u'默认内容 %s' % aid
            alarm_date = u'获取值 %s' % aid
            alarm_time = u'获取值 %s' % aid
            
        
        ### 首先创建各个显示控件
        # 行: 标题
        LabelTitle = wx.StaticText(panel, -1, u"提醒名称: ")
        InputTitle = wx.TextCtrl(panel, -1, title, size=(400, 20))

        # 行: 内容
        LabelContent = wx.StaticText(panel, -1, u"提醒内容: ")
        InputContent = wx.TextCtrl(panel, -1, content, size=(400, 200), style=wx.TE_MULTILINE)
        # 行: 时间
        LabelDatetime = wx.StaticText(panel, -1, u"提醒时间: ")
        InputDate = wx.DatePickerCtrl(panel, size=(90,-1), style = wx.DP_DROPDOWN|wx.DP_SHOWCENTURY)
        InputTimeSpin = wx.SpinButton(panel, -1, wx.DefaultPosition, (-1,23), wx.SP_VERTICAL)
        InputTime = masked.TimeCtrl(
                        panel, -1, name="24 hour control", fmt24hr=True,
                        spinButton = InputTimeSpin,
                        display_seconds = False
                        )
        # 设置值
        InputTime.SetValue(wx.DateTime_Now())
        
        # 按钮
        ButtonSave = wx.Button(panel, -1, u"保存") 
        ButtonCancel = wx.Button(panel, -1, u"取消") 
        
        # 对象寄存 
        self.InputTitle = InputTitle
        self.InputContent = InputContent
        self.InputDate = InputDate
        self.InputTime = InputTime
        
        ### 事件绑定
        self.Bind(wx.EVT_DATE_CHANGED, self.onDateChanged, InputDate)   # 日期变化
        self.Bind(masked.EVT_TIMEUPDATE, self.onTimeChanged, InputTime)   # 时间变化
        self.Bind(wx.EVT_BUTTON, self.onSave, ButtonSave)
        self.Bind(wx.EVT_BUTTON, self.onCloseDlg, ButtonCancel)
        

        ### 布局的基本结构: 一个垂直 boxsizer组织全局, 
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        
        # 注意 sizer 命名规范更方便和位置对应起来(subSizer 表示一级 size 的子 sizer)
        subSizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        # 行: 标题
        subSizer.Add(LabelTitle, 0,  wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        subSizer.Add(InputTitle, 1,  wx.ALIGN_CENTER_VERTICAL)
        # 行: 内容
        subSizer.Add(LabelContent, 0,  wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        subSizer.Add(InputContent, 1)
        # 行: 日期和时间(再套一个水平 sizer)
        subSizer.Add(LabelDatetime, 0,  wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        subDatetimeSizer = wx.BoxSizer(wx.HORIZONTAL)
        subDatetimeSizer.Add(InputDate, 0)
        subDatetimeSizer.Add(InputTime, 0)
        subDatetimeSizer.Add(InputTimeSpin, 0)
        subSizer.Add(subDatetimeSizer, 0)
        
        mainSizer.Add(subSizer, 0, wx.EXPAND|wx.ALL, 10)
        
        # 按钮放在水平sizer
        subBtnSizer = wx.BoxSizer(wx.HORIZONTAL)
        subBtnSizer.Add(ButtonSave, 0)
        subBtnSizer.Add((20,20), 1) # 按钮之间增加间隙
        subBtnSizer.Add(ButtonCancel, 0)
        mainSizer.Add(subBtnSizer, 1, wx.ALIGN_CENTER|wx.BOTTOM, 10)

        panel.SetSizer(mainSizer) 

        mainSizer.Fit(self)                                      
        mainSizer.SetSizeHints(self) 
        self.Center()

    def onCloseDlg(self, event):
        self.Close()
        
    def onDateChanged(self, event):
        print "OnDateChanged: %s\n" % event.GetDate()
        
    def onSave(self, event):
        title = self.InputTitle.GetValue()
        content = self.InputContent.GetValue()
        plan_date = self.InputDate.GetValue().Format('%Y-%m-%d')
        plan_time = self.InputTime.GetValue()
        print plan_time
        
        ### 插入数据库
        
    def onTimeChanged(self, event):
        timectrl = self.FindWindowById(event.GetId())
        ib_str = [ "  (out of bounds)", "" ]
        print '%s time = %s%s\n' % ( timectrl.GetName(), timectrl.GetValue(), ib_str[ timectrl.IsInBounds() ] ) 
        

class MyFrame(wx.Frame, listmix.ColumnSorterMixin):
    def __init__(self):
        wx.Frame.__init__(self, None, title=u"列表控件", size=(600, 200), style=wx.MINIMIZE_BOX|wx.MAXIMIZE_BOX|wx.RESIZE_BORDER|wx.SYSTEM_MENU|wx.CAPTION|wx.STAY_ON_TOP)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.list = MyListCtrl(self, -1, style=wx.LC_REPORT | wx.BORDER_NONE | wx.LC_SORT_ASCENDING)
        sizer.Add(self.list, 1, wx.EXPAND)
        self.itemDataMap = data                             # 用于排序的字典数据
        listmix.ColumnSorterMixin.__init__(self, len(data))
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        
        # 主菜单
        menubar = wx.MenuBar()

        # 子菜单: 文件
        fileMenu = wx.Menu()
        self.Bind(wx.EVT_MENU, self.onNew, fileMenu.Append(wx.ID_ANY, u"新建编辑器\tCtrl+N", u"新建标签"))

        # 关联主、子菜单
        menubar.Append(fileMenu, u"文件")
        
        
        # 设置主 frame 的菜单栏
        self.SetMenuBar(menubar)
        
        FrameMenu = self.GetMenuBar()
        FrameMenu.Show(False)
        
        self.Center()
        
        
    def onNew(self, event):
        pass

    def GetListCtrl(self):
        return self.list

if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = MyFrame()
    frame.Show()
#    frame = AlarmEdit(None, 1)
#    frame.Show()
    
    app.MainLoop()
