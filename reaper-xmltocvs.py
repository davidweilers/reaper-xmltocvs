# REAPER -> XML to CVS - v0.3

import wx
import xml.etree.ElementTree as el
import os
import re

class MyFrame(wx.Frame):
	filename = ''

	def __init__(self, *args, **kwds):
		# begin wxGlade: MyFrame.__init__
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
		wx.Frame.__init__(self, *args, **kwds)
		self.SetSize((456, 325))
		self.SetTitle("REAPER -> XML to CVS - v0.3")

		self.frame_statusbar = self.CreateStatusBar(1)
		self.frame_statusbar.SetStatusWidths([-1])

		self.panel = wx.Panel(self)
		self.text_ctrl_1 = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE)

		self.button_load = wx.Button(self.panel, label="Load")
		self.button_load.Bind(wx.EVT_BUTTON, self.load)
		self.button_save = wx.Button(self.panel, label="Save")
		self.button_save.Bind(wx.EVT_BUTTON, self.save)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.text_ctrl_1, 1, wx.EXPAND | wx.ALL, 5)
		sizer.Add(self.button_load, 0, wx.EXPAND | wx.ALL, 5)
		sizer.Add(self.button_save, 0, wx.EXPAND | wx.ALL, 5)
		self.panel.SetSizer(sizer)

		self.Show()
		
		# self.Layout()
	
	def load(self, event):
		with wx.FileDialog(self, "Open XML file", wildcard="XML Files|*.xml", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return
			pathname = fileDialog.GetPath()
			print(pathname)

			self.filename = fileDialog.GetFilename().lower()
			self.filename = self.filename[0:self.filename.rindex('.')-1:]
			print(self.filename)
			
			tree = el.parse(pathname)
			text = '#,Name,Start,End,Length\n'
			i=1

			for element in tree.findall('./element'):
				_in = element.find('./timeRange/in').text.strip()
				for content in element.findall('./comments/element'):
					_displayName = content.find('./author/displayName').text.strip()

					value = content.find('./content').text.strip() #.replace('"','""').replace(',','.')
					value = re.sub('[^a-zA-Z0-9 .?!]','',value)
					_content = '['+_displayName+'] '+value
					
					time = float(_in)
					result = str(round(time,2))

					text = text + 'M'+str(i)+',"'+_content+'",'+result+str(i)+',,\n'
					i=i+1
					
			self.text_ctrl_1.Clear()
			self.text_ctrl_1.WriteText(text)
			return
		return

	def save(self, event):
		with wx.FileDialog(self, "Save CSV file", wildcard="CSV Files|*.csv", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT, defaultFile=self.filename) as fileDialog:
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
