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
from gi.repository import GLib
from gi.repository import Pango
from gi.repository import Vte
from gi.repository import GObject

from gi.repository.Gtk import Notebook
from gi.repository.Gtk import Label
from gi.repository import GtkSource
from gi.repository import Vte
from Handlers import WorkspaceHandler,FileHandler,GCCHandler
from gettext import gettext as _

class TabbedCanvas(Gtk.EventBox):
	basePath=""
	counter=0
	saveAsFilename=""
	fileName=""
	data=""
	currentPageIndex=""
	hbox=""

	#property to hold <filename,notebook page> pair
	pageMap=dict()
	
	def __init__(self):	
		Gtk.EventBox.__init__(self)

	       	#Adding HBox
		self.mainbox=Gtk.HPaned()
		#self.mainbox.orientation(gtk.Orientation.VERTICAL	#gtk.HBox()
		self.elementBox=Gtk.VBox()
		
		scrolled_window = Gtk.VPaned()#gtk.ScrolledWindow()
		scrolled_window.set_border_width(5)	
	 	scrolled_window.set_size_request(300, 300)
		scrolled_window.add(self.elementBox)	
	       
		self.treestore=Gtk.TreeStore(str)
		self.treestore.clear()
		self.exampleNode=self.treestore.append(None,[_("Examples")])
		#self.newitem=self.treestore.append(self.exampleNode,["test1"])
		
		self.programNode=self.treestore.append(None,[_("Your Programs")])

		#adding treeview 
		self.treeview=Gtk.TreeView()
		
		#adding treeviewcolumn
		self.tvcolumn=Gtk.TreeViewColumn(_("Explorer"))
		self.cell=Gtk.CellRendererText()
		self.tvcolumn.pack_start(self.cell,True)
		self.tvcolumn.add_attribute(self.cell,"text",0)

		self.treeview.append_column(self.tvcolumn)
		self.treeview.set_model(self.treestore)

		#add handler for row-activated signal
		self.treeview.connect('row-activated',self.openSelectedFile)
		
		#changed was causing different behavior as when treeview is refreshed, it calls openSelected, thus opening all files under this section
		#self.treeview.get_selection().connect("changed", self.openSelectedFile)
		
		#create a scrolled window for explorer
		self.explorerScrollWindow=Gtk.ScrolledWindow()
		self.explorerScrollWindow.set_policy(Gtk.PolicyType.NEVER,Gtk.PolicyType.AUTOMATIC);
		self.explorerScrollWindow.add(self.treeview)
		self.explorerScrollWindow.set_size_request(100,650)
		self.elementBox.pack_start(self.explorerScrollWindow,False,False,0)
		#self.elementBox.pack_start(self.btn2,False,False,0)

		#Adding Notebook
		self.notebook=Notebook()		
		self.notebook.tab_curvature=100
		self.notebook.set_scrollable(True)
		self.notebook.show()
		
		#Adding Notebook pages
		self.addPage(None,None)		
	
		self.mainbox.add(scrolled_window)
		self.mainbox.add(self.notebook)
		self.add(self.mainbox)

	#method to add a page to Notebook
	def addPage(self,textBuffer,pageTitle):
		print "INSIDE_ADD_PAGE"
		caption=_("Untitled"+str(self.counter))
		#add hbox
		self.hbox=Gtk.HBox();
		self.hbox.show();

		#create text_buffer
		
		self.sourceBuffer= GtkSource.Buffer()
		#add textview
		self.textview=GtkSource.View()
		self.textview.set_buffer(self.sourceBuffer)
		self.textview.set_show_line_numbers(True)
		self.textview.set_show_line_marks(True)
		self.textview.set_size_request(250,400)
		self.setLanguage(self.textview)
	
		#check for textBuffer passed as param
		if textBuffer!=None:			
			#set the textbuffer data to editor	
			start, end = textBuffer.get_bounds()		
			self.sourceBuffer.set_text(textBuffer.get_text(start, end, True))

		#add vpane
		self.vpane=Gtk.VPaned();
		#add scroll to text view
		self.scroll=Gtk.ScrolledWindow();
		self.scroll.set_policy(Gtk.PolicyType.NEVER,Gtk.PolicyType.AUTOMATIC);
		self.scroll.add_with_viewport(self.textview)
		self.scroll.set_size_request(250,400)
		self.scroll.show()
		self.vpane.add(self.scroll)

		
		#add scroll to text view
		self.opScroll= Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		

		#create Vte Terminal
		self.vteObject=Vte.Terminal()
		self.opScroll.pack_start(self.vteObject, True, True, 0)
		self.outsb = Gtk.Scrollbar(orientation=Gtk.Orientation.VERTICAL)
		self.outsb.set_adjustment(self.vteObject.get_vadjustment())
		self.outsb.show()
		self.opScroll.pack_start(self.outsb, False, False, 0)		

		self.vteObject.set_colors(Gdk.color_parse('#000000'),Gdk.color_parse('#E7E7E7'),[])
		self.vteObject.set_size_request(200,200)
		self.vteObject.show()
		#self.opScroll.set_size_request(250,200)
		self.opScroll.show()	
		print "VTE_KARTIK:",self.vteObject.get_vadjustment()
		self.vpane.add(self.opScroll)
		self.vpane.show()

		self.hbox.pack_start(self.vpane,True,True,0)
		self.textview.show()

		#attach text-change listener for buffer
		self.attachTextChangedListener(self.hbox)		

		self.hbox.set_size_request(250, 300)

		#if pageTitle is none then give a Untitled caption
		if pageTitle==None:
			self.newlabel=Label(caption)
		else:
			self.newlabel=Label(pageTitle)

		#self.newlabel.set_size_request(75,30)
		self.resizeLabel(self.newlabel)
		self.newlabel.show()		
		self.notebook.append_page(self.hbox,self.newlabel)

		#assigning notebook page for the filename
		#self.pageMap[self.newlabel.get_text()]=self.hbox
		self.addPageToPageMap(self.newlabel.get_text(),self.hbox)

		self.counter=self.counter+1
	
		print "Curr :",self.pageMap
		self.selectFileNamePage(self.newlabel.get_text())

	#method to add page to pageMap
	def addPageToPageMap(self,fileName,hbox):
		print "BEFORE_CURRENT_PAGE_MAP:",self.pageMap
		print "addPageToPageMap_called_for:",fileName
		try:
			#assigning notebook page for the filename
			self.pageMap[fileName]=hbox
			print "Page:",fileName," added to pageMap"
		except:
			print "Page already exist in pageMap"
		print "AFTER_CURRENT_PAGE_MAP:",self.pageMap
	
	#method to remove page from pageMap
	def removePageFromPageMap(self,fileName):
		try:
			print "looking for page:",fileName, " in pageMap for removal"
			del self.pageMap[fileName]
			print "Page:",fileName," removed from pageMap"
		except:
			print "Unable to remove page from pageMap"
	
	#method to resize the tab label to appropriate dimension
	def resizeLabel(self,label):
		label.set_size_request(label.get_width_chars(),40)

	#method to get label for tab
	def resizeSelectedTabLabel(self):		
		label=self.getSelectedTabLabel()
		self.resizeLabel(label)
	
	#method to get hbox for selected tab
	def getSelectedTabHBox(self):
		currentPageIndex=self.notebook.get_current_page()
		print "current page number:",currentPageIndex
		hbox=self.notebook.get_nth_page(currentPageIndex)
		return hbox

	#method to get tab label for selected tab
	def getSelectedTabLabel(self):
		hbox=self.getSelectedTabHBox()
		label=self.notebook.get_tab_label(hbox)
		return label

	#method to get textview for selected tab( code editor)
	def getSelectedTabTextView(self):
		hbox=self.getSelectedTabHBox()
		children=hbox.get_children()#VPANED
						    #ScrolledWindow   #Viewport		#textview
		textview=children[0].get_children()[0].get_children()[0].get_children()[0]
		return textview

	#method to get outputWindow text view for selected tab( output window)
	def getSelectedTabOutputWindowTextView(self):
		hbox=self.getSelectedTabHBox()
		children=hbox.get_children()       #ScrolledWindow   #Viewport		#textview
		textview=children[0].get_children()[1].get_children()[0].get_children()[0]
		return textview
		
	#method to get text-buffer for selected tab( code editor)
	def getSelectedTabTextBuffer(self):
		hbox=self.getSelectedTabHBox()
		textview=self.getSelectedTabTextView()
		tvbuffer=textview.get_buffer()
		return tvbuffer

	#method to get text-buffer for selected tab( output window)
	def getSelectedTabOutputWindowBuffer(self):
		hbox=self.getSelectedTabHBox()
		textview=self.getSelectedTabOutputWindowTextView()
		tvbuffer=textview.get_buffer()
		return tvbuffer
	
	#method to get text-buffer for selected tab( output window)
	def getSelectedTabVte(self):
		hbox=self.getSelectedTabHBox()
		children=hbox.get_children()       #ScrolledWindow   #Viewport		#vte
		vteObj=children[0].get_children()[1].get_children()[0]#.get_children()[0]
		return vteObj

	#method to remove the selected page
	def removePage(self):
		currentPageIndex=self.notebook.get_current_page()
		print "Removing page number:",currentPageIndex

		#remove page from pageMap first
		fileName_to_be_removed=self.getSelectedTabLabel()
		self.removePageFromPageMap(fileName_to_be_removed.get_text())
	
		self.notebook.remove_page(currentPageIndex)

	#method to delete the selected page and file
	def deletePage(self):
		del_filename=self.getSelectedTabLabel().get_text()
		actualFileName=del_filename.replace('*','')			
		self.showConfirmDeleteDialog(actualFileName,self.basePath)
		
		
	#method to confirm deletion operation
	def showConfirmDeleteDialog(self,fileName,basePath):
		print "show confirm delete dialog called"
		self.deleteDialog=Gtk.Dialog(_("Oopsy Alert on Delete !"),None,0,None)
		self.label = Gtk.Label(_("Are you sure you want to delete '"+fileName+"' ?"))		
		self.deleteDialog.vbox.pack_start(self.label,True,True,0)		
		
		#adding buttons
		btnOk=Gtk.Button(_("Ok"))
		btnOk.connect("clicked",self.hideConfirmDeleteDialogOnOK,fileName,basePath)
	
		btnCancel=Gtk.Button(_("Cancel"))
		btnCancel.connect("clicked",self.hideConfirmDeleteDialogOnCancel,basePath)

		self.deleteDialog.action_area.pack_start(btnCancel,True,True,0)
		self.deleteDialog.action_area.pack_start(btnOk, True, True, 0)
		self.deleteDialog.set_size_request(150,150)
		btnOk.show()
		btnCancel.show()
		self.label.show()		
		self.deleteDialog.show()
	
	#method to hide confirm deletion operation and delete the file as user pressed OK	
	def hideConfirmDeleteDialogOnOK(self,widget,fileName,basePath):
		print "hideConfirmDeleteDialogOnOK called"
		self.deleteDialog.hide()
		
		self.removePage()
		fh=FileHandler()
		fh.basePath=self.basePath
		fh.deleteFile(fileName)

		#refresh the explorer
		self.refreshExplorer(self.basePath)

	#method to hide confirm deletion operation as user pressed CANCEL	
	def hideConfirmDeleteDialogOnCancel(self,widget,basePath):
		print "hideConfirmDeleteDialogOnCancel called"
		self.deleteDialog.hide()
		
	

	#method to apply text-changed callback to textview's text buffer
	def attachTextChangedListener(self,hbox):
			      #HBOX		  #VPANED          #SCROLL_WINDOW     #ViewPort         #TextView	
		textview=self.hbox.get_children()[0].get_children()[0].get_children()[0].get_children()[0]	
	
		print "L1:",self.hbox.get_children()[0]
		print "L2:",self.hbox.get_children()[0].get_children()[0]
		print "L3:",self.hbox.get_children()[0].get_children()[0].get_children()[0]
		print "attached text changed listener to :",textview
		tbuffer=textview.get_buffer()
		tbuffer.connect("changed",self.showUnsavedTab)
		print "\nAttached change listener"

	#method that detects text-change in text buffer and indicates on tab with a * mark
	def showUnsavedTab(self,widget):		
		label=self.getSelectedTabLabel()
		oldTitle=label.get_text()
		oldTitle=oldTitle.replace('*','')
		oldTitle=oldTitle + '*'
		label.set_text(oldTitle)

	#method to set Language of sourceView with Language Manager
	def setLanguage(self,sourceView):
		self.lmgr=GtkSource.LanguageManager.get_default()
		self.language=self.lmgr.get_language('cpp')
		sourceView.get_buffer().set_language(self.language)

	#method to open the selected file from the explorer
	def openSelectedFile(self, widget, row, col):
		model=self.treeview.get_model()
       		value = model[row][0]		
		print "Open Selected File called for :",value
		filename=value

		page_in_pageMap=None
		#get page from pageMap and select already open tab for this file
		try:
			page_in_pageMap=self.pageMap[filename]
			print "PAGE_MAP:",page_in_pageMap," for :",filename
			self.selectFileNamePage(filename)
		except:
			print "NO_PAGE_IN_PAGE_MAP"
		
		#create fileHandler instance
		fh=FileHandler()
		fh.basePath=self.basePath
		fileData=fh.loadFileFromWorkspace(filename)
		print "FILE_DATA:",fileData

		text_buffer=Gtk.TextBuffer()
		text_buffer.set_text(fileData)
		
		if page_in_pageMap==None:
			print "since no page in pageMap thus creating page"
			self.addPage(text_buffer,filename)

	#method to select the tab with a filename
	def selectFileNamePage(self,filename):
		h_box=self.pageMap[filename]
		page_num=self.getPageNumberWithTabHBox(h_box)
		self.notebook.set_current_page(page_num)

	#method to get hbox for a hbox
	def getPageNumberWithTabHBox(self,hbox):		
		page_number=self.notebook.page_num(hbox)
		return page_number

	#method to save the file on selected notebook page
	def saveFile(self,basePath):		
		hbox=self.getSelectedTabHBox()				
		textview_buffer=self.getSelectedTabTextBuffer()
		start, end = textview_buffer.get_bounds()				
		self.data=textview_buffer.get_text(start, end, True)	
		self.fileName=self.notebook.get_tab_label(hbox).get_text()

		#check if file exists on drive
		actualFilename=self.fileName.replace('*','')
		fh=FileHandler()
		fh.basePath=basePath
		
		if fh.checkFileExists(actualFilename):
			self.saveAsFilename=actualFilename			
			self.saveToDisk(basePath)
		else:
			self.showSaveDialog(basePath)
	
		#print "HBOX has elements:",str(len(lst))
		print "Got data:",self.data," with filename:",self.fileName
		
		

	#method to show save dialog on click of save button
	def showSaveDialog(self,basePath):
		print "save dialog called"
		self.dialog=Gtk.Dialog(_("Save Program"),None,0,None)
		self.label = Gtk.Label(_("Save your program as :"))
		self.entry=Gtk.Entry()
		self.dialog.vbox.pack_start(self.label,True,True,0)
		self.dialog.vbox.pack_start(self.entry,True,True,0)
		
		#adding buttons
		btnOk=Gtk.Button(_("Save"))
		btnOk.connect("clicked",self.hideSaveDialogOnSave,basePath)
		self.dialog.action_area.pack_start(btnOk, True, True, 0)
		self.dialog.set_size_request(150,150)
		btnOk.show()
		self.label.show()
		self.entry.show()
		self.dialog.show()
	
	#method to show alert dialog if file is unsaved and compile or executed is selected
	def showAlertDialog(self,basePath,message):
		print "show Alert dialog called"
		self.alertDialog=Gtk.Dialog(_("Oopsy Alert"),None,0,None)
		self.label = Gtk.Label(_(message))		
		self.alertDialog.vbox.pack_start(self.label,True,True,0)		
		
		#adding buttons
		btnOk=Gtk.Button(_("Ok"))
		btnOk.connect("clicked",self.hideAlertDialog,basePath)
		self.alertDialog.action_area.pack_start(btnOk, True, True, 0)
		self.alertDialog.set_size_request(150,150)
		btnOk.show()
		self.label.show()		
		self.alertDialog.show()

	#method to hide alert dialog 
	def hideAlertDialog(self,widget,basePath):
		print "hide Alert Dialog called"
		self.alertDialog.hide()


	#method to hide save-dialog and invoke saveToDisk--for actual saving
	def hideSaveDialogOnSave(self,widget,basePath):
		print "hideSaveDialog called"
		self.saveAsFilename=self.entry.get_text()
		print "got save as filename:",self.saveAsFilename
		self.dialog.hide()
				
		#check if file is saved as .c or .cpp file
		isCFlag=self.saveAsFilename[-2:]
		isCppFlag=self.saveAsFilename[-4:]

		#if file is either of c or cpp file then proceed to save on disk
		if isCFlag=='.c'or isCppFlag=='.cpp':	
			self.saveToDisk(basePath)
		else:
			self.showAlertDialog(basePath,"You must save your program as .c or .cpp file !")

	#method to save data from text-buffer to disk as a file
	def saveToDisk(self,basePath):
		fh=FileHandler()
		fh.basePath=basePath
		fh.saveFile(self.saveAsFilename,self.data)
		self.renameTabOnSave(self.saveAsFilename)
		
		#get selected Tab HBox
		hbox_obj=self.getSelectedTabHBox()
		self.addPageToPageMap(self.saveAsFilename,hbox_obj)

		#refresh the explorer
		self.refreshExplorer(basePath)
		
		#reselect file in explorer after explorer refresh
		self.selectFileInExplorer(self.saveAsFilename)

	#method to rename tab as save is clicked
	def renameTabOnSave(self,fileName):
		hbox=self.getSelectedTabHBox()
		self.notebook.set_tab_label_text(hbox, fileName)		
		self.resizeSelectedTabLabel()
		print "Tab renamed"

	#method to compile selected file
	def compileSelectedFile(self,basePath):
		gc=GCCHandler()
		gc.basePath=basePath
		fn=self.getSelectedTabLabel().get_text()
		actualFilename=fn.replace('*','')
		
		#check if file is saved as .c or .cpp file
		isCFlag=actualFilename[-2:]
		isCppFlag=actualFilename[-4:]

		#if file is either of c or cpp file then proceed otherwise show alert dialog asking user to save the file first.
		if isCFlag=='.c'or isCppFlag=='.cpp':		
			vteObj=self.getSelectedTabVte()
			compilationOutput=gc.compileFile(actualFilename,vteObj)
		else:
			self.showAlertDialog(basePath,"You must save the file before compiling or executing the program.")
		

	#method to run selected file
	def executeSelectedFile(self,basePath):
		gc=GCCHandler()
		gc.basePath=basePath
		fn=self.getSelectedTabLabel().get_text()
		actualFilename=fn.replace('*','')
		
		#check if file is saved as .c or .cpp file
		isCFlag=actualFilename[-2:]
		isCppFlag=actualFilename[-4:]

		#if file is either of c or cpp file then proceed otherwise show alert dialog asking user to save the file first.
		if isCFlag=='.c'or isCppFlag=='.cpp':
			vteObj=self.getSelectedTabVte()
			executionOutput=gc.execute(actualFilename,vteObj)
		else:
			self.showAlertDialog(basePath,"You must save the file before compiling or executing the program.")
		
	#clear the children under examples and your programs
	def clearFilesInTreeView(self):
		for row in self.treestore:
			print "ROW:",row," NAME:",row[0]
			rowIter=row.iterchildren()
			try:
				child=rowIter.next()
			except:
				print "No rows at all"

			try:
				while(child!=None):
					print "Removing CHILD:",child[0]	
					self.treestore.remove(child.iter)				
					child=rowIter.next()
			except:
				print "No more rows !"

	#method to select the row in TreeView
	def selectFileInExplorer(self,fileName):
		for row in self.treestore:
			print "ROW:",row," NAME:",row[0]
			rowIter=row.iterchildren() 
			
			try:
				child=rowIter.next()
			except:
				print "No rows at all"

			try:
				while(child!=None):
					print "Checking CHILD:",child[0], " for selecting:",fileName
					if fileName==child[0]:
						self.treeSel=self.treeview.get_selection()
						self.treeSel.select_iter(child.iter)
						print "TREE_SEL:",self.treeSel
						break			
					child=rowIter.next()
			except:
				print "No more rows !"
			
			
			#self.treeSel.select_path(

	#refresh explorer
	def refreshExplorer(self,basePath):				
		print "flushing treestore"
		self.clearFilesInTreeView()
		self.loadExplorer(basePath)

	#method to load the explorer
	def loadExplorer(self,basePath):
		
		
		#flush all rows first
		#self.refreshExplorer()
		print "INSIDE_LOAD_EXPLORER"

		print "basePath_in_TabControl:",basePath
		ws=WorkspaceHandler(basePath)		
		
		#add child nodes to exampleNode-which shows all examples
		print "ws.exampleList:",len(ws.exampleList)
		for item in ws.exampleList:
			print "adding item:",item," to examples:",self.exampleNode
			self.newitem=self.treestore.append(self.exampleNode,[item])
			
		
		#add child nodes to programNode-which shows your programs
		print "ws.programList:",len(ws.programList)
		for item in ws.programList:
			print "adding item:",item," to programs:",self.programNode
			self.newitem=self.treestore.append(self.programNode,[item])
		
		#now expand all nodes
		self.treeview.expand_all()
		
		

	
	


