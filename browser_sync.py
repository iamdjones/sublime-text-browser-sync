import sublime, sublime_plugin
import subprocess, sys, os
import inspect



def plugin_loaded():
	BrowsersyncListener.loadFiles();


class BrowsersyncState:
	startFileIndex = 0
	startDirIndex = 0
	startFiles = set()
	watchPaths = set()

class BrowsersyncListener(sublime_plugin.EventListener):

	def on_load(self, view):
		BrowsersyncListener.loadFiles()

	def post_window_command(self, window, window_command_name,args):
		BrowsersyncListener.loadFiles()

	def on_new(self, view):
		BrowsersyncListener.loadFiles()

	def loadFiles():
		window = sublime.active_window()

		viewPaths = {view.file_name() for view in window.views()}
		folders = {folder for folder in window.folders()}

		#self.startFiles |= {os.path.join(root,f) for folder in self.window.folders() for root,dirs,files in os.walk(folder) for f in files}
		BrowsersyncState.startFiles = viewPaths

		BrowsersyncState.watchPaths = {folder + "\\**" for folder in folders}
		BrowsersyncState.watchPaths |= viewPaths



class ChangeBrowsersyncIndexCommand(sublime_plugin.ApplicationCommand):
	
	def description(self, index):
		try:
			return sorted(BrowsersyncState.startFiles)[index]
		except IndexError:
			return ""

	def is_visible(self, index):
		try:
			derp = sorted(BrowsersyncState.startFiles)[index]
			return True
		except IndexError:
			return False

	def is_checked(self,index):
		return BrowsersyncState.startFileIndex == index
	
	def run(self,index):
		BrowsersyncState.startFileIndex = index


class StartBrowsersync(sublime_plugin.ApplicationCommand):
	def run(self):

		scriptPath = inspect.getframeinfo(inspect.currentframe()).filename
		scriptDir = os.path.dirname(scriptPath)

		os.chdir(scriptDir)

		files = ",".join(sorted(BrowsersyncState.watchPaths))
		index = sorted(BrowsersyncState.startFiles)[BrowsersyncState.startFileIndex]
		server = os.path.dirname(index)

		index = index.replace(server + "\\", "")

		plat = sublime.platform()

		killMethod = {
			'osx': 'killall -KILL node-osx',
			'linux': 'pkill -x node-linux',
			'windows': 'taskkill /im node-windows.exe /f /t'
		}.get(plat)

		os.system(killMethod)

		cmd = 'node-{0} browser_sync_launch.js "{1}" "{2}" "{3}"'
		cmd = cmd.format(plat, server,files, index)

		sublime.set_timeout_async(self.make_callback(cmd), 0)


	def make_callback(self, cmd):
		def callback():
			proc = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
			print(proc.communicate()[1])
		return callback
