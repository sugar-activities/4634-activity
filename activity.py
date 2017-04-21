# -*- coding: utf-8 -*-
#!/usr/bin/python
#
# Oopsy: an IDE for developing, compiling and executing C, C++ programs for children.
#	http://tinyurl.com/oopsyActivity
# Written by Kartik Perisetla <kartik.peri@gmail.com>
# Copyright (C) 2013, Kartik Perisetla
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU General Public License
# along with this library; if not, write to the Free Software
# Foundation, 51 Franklin Street, Suite 500 Boston, MA 02110-1335 USA

from gi.repository import Gtk
from gi.repository import Gdk
from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.graphics.toolbarbox import ToolbarButton
from sugar3.graphics.toolbutton import ToolButton
from sugar3.activity.widgets import ActivityToolbarButton
from gi.repository import Pango
from sugar3.activity.widgets import ActivityButton
from sugar3.graphics.toolbutton import ToolButton
from sugar3.activity.widgets import StopButton
from gettext import gettext as _
import os

from TabControl import TabbedCanvas

class Oopsy(activity.Activity):
	

	def __init__(self,handle):
		activity.Activity.__init__(self,handle,True)
		self.basePath=activity.get_bundle_path()
	
		scroll=Gtk.ScrolledWindow();
		scroll.set_policy(Gtk.PolicyType.NEVER,Gtk.PolicyType.NEVER);
		
		#get container
		self.canvasHolder=TabbedCanvas()
		self.canvasHolder.basePath=self.basePath
	
		#add tabControl to scrolled window
		scroll.add_with_viewport(self.canvasHolder)
		self.set_canvas(scroll)

		#add toolbox
		toolbox= ToolbarBox(self)
		activity_button=ActivityButton(self);
		toolbox.toolbar.insert(activity_button,0)
		activity_button.show()
		
		separator = Gtk.SeparatorToolItem()
		separator.show()
		toolbox.toolbar.insert(separator, 1)

		#new file button
		new_file = ToolButton('list-add')
		new_file.set_tooltip(_('New File'))
		new_file.props.accelerator=('<ctrl><shift>n')
		new_file.connect('clicked', self.newFile)
		toolbox.toolbar.insert(new_file,2)
		new_file.show()		
		
		#close file button
		close_file=ToolButton('list-remove')
		close_file.set_tooltip(_('Close File'))
		close_file.props.accelerator=('<ctrl><shift>x')
		close_file.connect('clicked',self.closeFile)
		toolbox.toolbar.insert(close_file,3)
		
		#delete button						
		delete_file=ToolButton('dialog-cancel')
		delete_file.set_tooltip('Delete File')
		delete_file.props.accelerator=('del')		
		delete_file.connect('clicked',self.deleteFile)
		toolbox.toolbar.insert(delete_file,4)
	
		separator = Gtk.SeparatorToolItem()
		separator.show()
		toolbox.toolbar.insert(separator, 5)

		#save file button
		saveBtnImage = Gtk.Image()
	        saveBtnImage.set_from_file("%s/icons/oopsy_save_as.svg" % os.getcwd())		
		save_file=ToolButton('gtk-save')
		save_file.set_icon_widget(saveBtnImage)
		save_file.set_tooltip(_('Save File'))
		save_file.props.accelerator=('<ctrl>s')
		save_file.connect('clicked',self.saveFile,self.basePath)
		toolbox.toolbar.insert(save_file,6)		
		
		#compile button
		compile_button=ToolButton('view-source')		
		compile_button.set_tooltip(_('Compile'))
		compile_button.props.accelerator=('<ctrl>F6')
		compile_button.connect('clicked',self.compileFile,self.basePath)
		toolbox.toolbar.insert(compile_button,7)
			
		#run button		
		gobutton = ToolButton('media-playback-start')
		gobutton.props.accelerator = ('<ctrl>F5')
		#gobutton.set_icon_widget(goicon_bw)
		gobutton.set_tooltip(_("Run!"))
		gobutton.connect('clicked',self.executeFile,self.basePath)
		toolbox.toolbar.insert(gobutton,8)

			
	
		separator = Gtk.SeparatorToolItem()
		separator.props.draw = False
	        separator.set_expand(True)
		separator.show()
		toolbox.toolbar.insert(separator, 9)

		#stop button
		stop_button=StopButton(self)
		toolbox.toolbar.insert(stop_button,10)
		stop_button.show()
	
		self.set_toolbar_box(toolbox)

		act_path = activity.get_bundle_path()	
		print "BUNDLE_PAth:",act_path

		self.loadExplorer(self.basePath)
		self.show_all()

	#method to open new tab for a file
	def newFile(self,widget):
		print "newFile called for widget:",widget
		self.canvasHolder.addPage(None,None)

	#method to close current tab
	def closeFile(self,widget):
		print "closeFile called for widget:",widget
		self.canvasHolder.removePage()

	#method to delete current tab 
	def deleteFile(self,widget):
		print "deleteFile called for widget:",widget
		self.canvasHolder.deletePage()

	#method to save file
	def saveFile(self,widget,basePath):
		print "saveFile called for widget:",widget
		self.canvasHolder.saveFile(basePath)
		
		
	#method to compile selected file
	def compileFile(self,widget,basePath):
		print "CompileFile called"
		self.canvasHolder.compileSelectedFile(basePath)
	
	#method to execute selected file
	def executeFile(self,widget,basePath):
		print "ExecuteFile called"
		self.canvasHolder.executeSelectedFile(basePath)

	#method to load explorer
	def loadExplorer(self,basePath):
		self.canvasHolder.loadExplorer(basePath)

	#method to refresh explorer
	def refreshExplorer(self,basePath):
		self.canvasHolder.refreshExplorer(basePath)

