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

from gi.repository import Gtk,Vte,GLib
import os
import time

class FileHandler:
	basePath=""
	def __init__(self):
		print "FileHandler intantiated"
		
	#method to check if file exist on workspace
	def checkFileExists(self,filename):
		filepath=self.basePath+"/workspace/"+filename		
		if os.path.exists(filepath):
			return True
		else:
			return False
	
	#method to save file to disk
	def saveFile(self,filename,data):
		dirpath=self.basePath+"/workspace"
		
		#if workspace directory does not exists, create one
		if not os.path.exists(dirpath):
			os.makedirs(dirpath)
		
		
		savepath=dirpath+"/"+filename
		print "checking savePath:",savepath		
		f=open(savepath,"w")
		f.write(data)
		f.close()
		
		
      		print "Save complete"
		#print "ERROR while saving file:",savepath
		
	#method to delete the file
	def deleteFile(self,filename):
		dirpath=self.basePath+"/workspace"
		os.chdir(dirpath)
		filepath=self.basePath+"/workspace/"+filename	
		os.system("rm "+filepath)
		
	#method to load a file using filename
	def loadFileFromWorkspace(self,filename):
		print "loadFileFromWorkspace:BasePath:",self.basePath
		os.chdir(self.basePath+"/workspace")
		f=open(filename,"r")
		data=f.read()
		f.close()
		return data

class GCCHandler:
	basePath=""
	command=""
	def __init__(self):
		print "GCCHandler instantiated"

	def clearVte(self,vteObj):		
		vteObj.grab_focus()
		vteObj.feed("\x1B[H\x1B[J\x1B[0;39m")
	
	#method to compile a file
	def compileFile(self,filename,vteObj):
		os.chdir(self.basePath+"/workspace")
		print "compileFile got filename:",filename

		compilerName=""
		isCFlag=filename[-2:]
		print "isCFlag=",isCFlag

		isCppFlag=filename[-4:]
		print "isCppFlag=",isCppFlag

		if isCFlag=='.c':
			print "\nusing gcc"
			compilerName="gcc "
		if isCppFlag=='.cpp':
			print "\nusing g++"
			compilerName="g++ "

		command=compilerName+filename+" 3>&1 1>&2 2>&3 | tee output_dump.dump" 
		
		self.clearVte(vteObj)
		
		#delete the a.out file		
		#os.system("rm ./a.out")		 
	        #vteObj.connect ("child-exited", lambda term: Gtk.main_quit())
		vteObj.fork_command_full(Vte.PtyFlags.DEFAULT,".",["/bin/sh", "-c",command],None,GLib.SpawnFlags.DO_NOT_REAP_CHILD,None,None)
		
		return "done"
		

	#method to run the compiled file
	def execute(self,filename,vteObj):		
		data=self.compileFile(filename,vteObj)
		
		time.sleep(2)
		execPath=self.basePath+"/workspace/./a.out"
		print "looking for ./a.out in :",self.basePath
		
		f=open(self.basePath+"/workspace/output_dump.dump","r")
		errData=f.read()
		f.close()
		
		print "ERR_DATA:",errData
		if(errData.find("error")==-1):
			print "Successfully Compiled"			
			self.clearVte(vteObj)		
			vteObj.fork_command_full(Vte.PtyFlags.DEFAULT,".",["/bin/sh", "-c",execPath],None,GLib.SpawnFlags.DO_NOT_REAP_CHILD,None,None)
		
			
		
		return "done"
		

class WorkspaceHandler:
	basePath=""
	exampleList=[]
	programList=[]
	
	#constructor
	def __init__(self,basePath):
		print "workspaceHanlder called"
		self.basePath=basePath		
		self.loadExamples()
		self.loadFiles()
	
	#method to load examples
	def loadExamples(self):
		print "loadExamples:BasePath:",self.basePath
		os.chdir(self.basePath+"/workspace")
		self.exampleList=[]
		for dirname, dirnames, filenames in os.walk('.'):			
			for filename in filenames:
				lowerCaseFileName=filename.lower()
				#print "LOWER_CASE_FILENAME:",lowerCaseFileName
				if lowerCaseFileName.find("example.c")!=-1:
					self.exampleList.append(filename)
	#method to load files
	def loadFiles(self):
		print "loadFiles:BasePath:",self.basePath
		os.chdir(self.basePath+"/workspace")
		self.programList=[]
		for dirname, dirnames, filenames in os.walk('.'):			
			for filename in filenames:
				lowerCaseFileName=filename.lower()
				#print "LOWER_CASE_FILENAME:",lowerCaseFileName
				if lowerCaseFileName.find(".c")!=-1 and lowerCaseFileName.find("example.c")==-1:
					self.programList.append(filename)
			#print filename		#os.path.join(dirname, filename)

	
	
		
