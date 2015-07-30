import sublime, sublime_plugin
import subprocess, sys, os
import inspect
import re


class BrowsersyncCommandBase(sublime_plugin.WindowCommand):

	startFileIndex = 0
	startDirIndex = 0
	startFiles = set()
	watchPaths = set()


	def __init__(self, window):
		super().__init__(window)

		viewPaths = {view.file_name() for view in window.views()}
		folders = {folder for folder in window.folders()}

		self.startFiles |= {os.path.join(root,f) for folder in self.window.folders() for root,dirs,files in os.walk(folder) for f in files}
		self.startFiles |= viewPaths

		self.watchPaths |= {folder + "\\**" for folder in folders}
		self.watchPaths |= viewPaths

	def run(self, index):
		None



class ChangeBrowsersyncIndexCommand(BrowsersyncCommandBase):
	
	def description(self, index):
		try:
			return sorted(self.startFiles)[index]
		except IndexError:
			return ""

	def is_visible(self, index):
		try:
			derp = sorted(self.startFiles)[index]
			return True
		except IndexError:
			return False

	def is_checked(self,index):
		return BrowsersyncCommandBase.startFileIndex == index
	
	def run(self,index):
		BrowsersyncCommandBase.startFileIndex = index


class StartBrowsersync(BrowsersyncCommandBase):
	def run(self):

		scriptPath = inspect.getfile(inspect.currentframe())
		scriptDir = os.path.dirname(scriptPath)

		os.chdir(scriptDir)

		files = ",".join(sorted(self.watchPaths))
		index = sorted(self.startFiles)[BrowsersyncCommandBase.startFileIndex]
		server = os.path.dirname(index)
		


		startPath = index.replace(server + "\\", "")
		index = startPath

		res = os.system('taskkill /im node.exe /f /t')

		cmd = 'node browser_sync_launch.js --server "{0}" --files "{1}" --index "{2}" --startPath "{3}"'
		cmd = cmd.format(server,files, index, startPath)
		proc = subprocess.Popen(cmd, shell=True)