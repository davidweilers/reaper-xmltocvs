# REAPER -> XML to CVS - v0.2

import wx
import xml.etree.ElementTree as el

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade

class MyFrame(wx.Frame):
	def __init__(self, *args, **kwds):
		# begin wxGlade: MyFrame.__init__
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
		wx.Frame.__init__(self, *args, **kwds)
		self.SetSize((456, 325))
		self.SetTitle("REAPER -> XML to CVS - v0.2")

		self.frame_statusbar = self.CreateStatusBar(1)
		self.frame_statusbar.SetStatusWidths([-1])

		self.panel_1 = wx.Panel(self, wx.ID_ANY)

		sizer_1 = wx.BoxSizer(wx.VERTICAL)

		self.text_ctrl_1 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "", style=wx.TE_MULTILINE)
		sizer_1.Add(self.text_ctrl_1, 1, wx.EXPAND, 0)

		self.panel_1.SetSizer(sizer_1)

		self.fload = wx.Button(self.panel_1,-1,'load')
		sizer_1.Add(self.fload, 1, wx.EXPAND, 0)
		self.fload.Bind(wx.EVT_BUTTON,self.load)

		self.fsave = wx.Button(self.panel_1,-1,'save')
		sizer_1.Add(self.fsave, 1, wx.EXPAND, 0)
		self.fsave.Bind(wx.EVT_BUTTON,self.save)
		
		self.Layout()
		# end wxGlade
	
	def load(self, event):
		with wx.FileDialog(self, "Open XML file", wildcard="XML Files|*.xml", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return
			pathname = fileDialog.GetPath()
			print(pathname)
			tree = el.parse(pathname)
			text = '#,Name,Start,End,Length\n'
			i=1

			for element in tree.findall('./element'):
				_in = element.find('./timeRange/in').text.strip()
				for content in element.findall('./comments/element'):
					_displayName = content.find('./author/displayName').text.strip()
					_content = '['+_displayName+'] '+content.find('./content').text.strip().replace('"','""').replace(',','.')
					
					time = float(_in)
					result = str(round(time,2))

					text = text + 'M'+str(i)+',"'+_content+'",'+result+str(i)+',,\n'
					i=i+1
					
			self.text_ctrl_1.Clear()
			self.text_ctrl_1.WriteText(text)
			return
		return

	def save(self, event):
		with wx.FileDialog(self, "Save CSV file", wildcard="CSV Files|*.csv", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return
			pathname = fileDialog.GetPath()
			with open(pathname, mode="w", encoding="utf-8") as output_file:
				text = self.text_ctrl_1.GetValue()
				output_file.write(text)
		return

# end of class MyFrame

class MyApp(wx.App):
	def OnInit(self):
		self.frame = MyFrame(None, wx.ID_ANY, "")
		self.SetTopWindow(self.frame)
		self.frame.Show()
		return True

# end of class MyApp

if __name__ == "__main__":
	app = MyApp(0)
	app.MainLoop()
