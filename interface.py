import webbrowser
import tkinter
from tkinter.ttk import *
from tkinter import messagebox
import xml.etree.ElementTree as ET
import re
from fuzzywuzzy import fuzz
import ast
from tkinter import tix

class course():
	def __init__(self,courseobject):
		self.title = courseobject.find("coursetitle").text
		self.url=courseobject.find("coourselink").text
		self.creators=courseobject.find("creators").text
		self.instructors=courseobject.find("instructordetails").text
		self.string=0
		self.percentage=0
		self.matchwords=0
		self.matchvalues=0
		self.sourcetopics=0
		self.level=courseobject.find("level").text
		z=courseobject.find("startdate").text
		zz=z.split("N/A")
		z="".join(zz)
		self.startdate=z
		self.duration=courseobject.find("duration").text
		l=courseobject.find("review").text.split("See")
		if len(l)==2 :
			self.review=courseobject.find("review").text.split("See")[0]
		else :
			self.review=" user rating unavailable"
		mx=courseobject.find("syl")
		x=mx.find("topics").text
		xx = ast.literal_eval(x)
		xxx = [i.strip() for i in xx]
		self.topics=xxx

def comparepage(mm) :
	window=tkinter.Tk()
	lbl1 = tkinter.Label(window, text="                ",font=("Arial Black bold",20,"bold"))
	lbl1.grid(column=0,row=0)
	lbl1 = tkinter.Label(window, text=" Source Topics ",font=("Arial Black bold",20,"bold"))
	lbl1.grid(column=1,row=0)
	s1=mm.sourcetopics
	kl12 = ast.literal_eval(str(s1))
	s = [i.strip() for i in kl12]
	t1=mm.topics
	kl12 = ast.literal_eval(str(t1))
	t = [i.strip() for i in kl12]
	r1=mm.matchwords
	kl12 = ast.literal_eval(str(r1))
	r = [i.strip() for i in kl12]

	i=0
	while i < len(s) :


		sourcetopic=s[i]
		
		if sourcetopic in r :
			lbl1 = tkinter.Label(window, text=" *"+sourcetopic+"* ",font=("Arial Black",20),bg="yellow")
			lbl1.grid(column=2-i%3,row=1+int(i/3))
		else :
			lbl1 = tkinter.Label(window, text=" *"+sourcetopic+"* ",font=("Arial Black",20))
			lbl1.grid(column=2-i%3,row=1+int(i/3))
		
		i=i+1


	i=0
	l=len(s)/3 +3
	l=int(l)
	lbl1 = tkinter.Label(window, text=" MOOC Topics ",font=("Arial Black bold",20,"bold"))
	lbl1.grid(column=1,row=l-2)
	while i < len(t) :


		sourcetopic=t[i]
		
		if sourcetopic in r :
			lbl1 = tkinter.Label(window, text=" *"+sourcetopic+"* ",font=("Arial Black",20),bg="yellow")
			lbl1.grid(column=2-i%3,row=1+l+int(i/3))
		else :
			lbl1 = tkinter.Label(window, text=" *"+sourcetopic+"* ",font=("Arial Black",20))
			lbl1.grid(column=2-i%3,row=1+l+int(i/3))
		
		i=i+1
	l=l+len(t)+3
	lbl1 = tkinter.Label(window, text=" Mapping Topics ",font=("Arial Black bold",20,"bold"))
	lbl1.grid(column=1,row=l-2)
	i=0
	z=l
	while i <len(mm.matchwords):
		info=mm.matchwords[i]+" : "+mm.matchwords[i+1]+" : "+str(mm.matchvalues[i])
		lbl1 = tkinter.Label(window, text=info,font=("Arial Black",20))
		lbl1.grid(column=1,row=z)
		i=i+2
		z=z+1

	
	window.mainloop()

class resultspage():
	def __init__(self,visualize,visualizescore,visualizeindex):
		self.window=tix.Tk()
		self.window.title("Results Page")
		scr_win = tix.ScrolledWindow(self.window,width=1500, height=786)
		
		scr_win.grid(row=0,column=0)
		sframe = scr_win.window

		n=len(visualize)
		p=int(n/5)
		pp=n%5
		print("total pages : "+str(p+1),"last page entries : "+str(pp))
		
		# sorting visualize		
		courseobjects=[]
		percentagematch1=[]
		stringmatches=[]
		for i in visualizescore :
			percentagematch1.append(i)
		visualizescore.sort(reverse=True)

		i=0
		percentagematch=[]
		while i<len(visualizeindex) :
			p=percentagematch1.index(visualizescore[i])
			courseobjects.append(visualizeindex[p])
			stringmatches.append(visualize[p])
			percentagematch.append(visualizescore[i])
			i=i+1

		# print(courseobjects)
		# print(stringmatches)
		# print(percentagematch)

		# i=0
		# # while i<len(courseobjects) :
		# # 	print(courseobjects[i])
		# # 	print(stringmatches[i])
		# # 	print(percentagematch[i])
		# # 	print("\n\n")
		# # 	i=i+1
		def visualizebutton(mm):
			# print("________________match words ________")
			# print(mm.matchwords)
			
			# print("__________________source topics________________")
			# print(mm.sourcetopics)
			# print("__________________target topics________________")
			# print(mm.topics)
			# print("__________________topic matching_______________________")
			i=0
			while i <len(mm.matchwords):
				print(mm.matchwords[i]+" : "+mm.matchwords[i+1]+" : "+str(mm.matchvalues[i]))
				i=i+2
			print("-------------")
			print(mm.matchwords)
			c=comparepage(mm)

		def visitbutton(mm):
			print(mm.url)
			webbrowser.open(mm.url)

		i=0
		coursefuncobjects=[]
		while i<len(courseobjects):
			m=courseobjects[i]
			mm=course(m)
			mm.percentage=percentagematch[i]
			mm.string=stringmatches[i]
			zx=[]
			zxv=[]
			zxc=[]
			k=stringmatches[i]
			for kk in k :
				kkk=kk.split(" :")
				v=kkk[1]
				j=kkk[0]
				jj=j.split("==")
				zxc.append(jj[0])
				if int(v)>0 :

					j=kkk[0]
					jj=j.split("==")
					zx.append(jj[0])
					
					zx.append(jj[1])
					zxv.append(int(v))
					zxv.append(int(v))

			mm.matchwords=zx
			mm.matchvalues=zxv
			mm.sourcetopics=zxc
			coursefuncobjects.append(mm)
			i=i+1
			# print(str(mm.title)+"\n"+"percentage matched :"+str(mm.percentage)+"\n"+str(mm.creators)+"\n"+str(mm.level)+" "+str(mm.startdate)+"; "+str(mm.duration)+"\n"+str(mm.review)+"pricing : "+"N/A")
			# m=visualizeindex[0]
			# mm=m.find("coursetitle").text
			# lbl1 = tkinter.Label(self.window, text="Title : "+str(mm),font=("Arial Black",35))
			# lbl1.pack()
		# info=str(mm.title)+"\n"+str(mm.url)+"\n"+"percentage matched :"+str(mm.percentage)+"\n"+"Created By :"+str(mm.creators)+"\n"+"level :"+str(mm.level)+" ; "+str(mm.startdate)+"; "+str(mm.duration)+"\n"+str(mm.review)+"pricing : "+"N/A"
			# print("\n\n\n\n")
			# print(mm.topics)
			# print(mm.string)
			# print(mm.matchwords)
			# print(mm.matchvalues)
			# print("\n\n\n\n")
		
		
		# mm0=courseobjects[0]
		# info0=str(mm.title)+"\n"+str(mm.url)+"\n"+"percentage matched :"+str(mm.percentage)+"\n"+"Created By :"+str(mm.creators)+"\n"+"level :"+str(mm.level)+" ; "+str(mm.startdate)+"; "+str(mm.duration)+"\n"+str(mm.review)+"pricing : "+"N/A"
		# lbl0 = tix.Label(sframe, text=info,font=("Arial Black",20))
		# lbl1.grid(row=2*i,column=0)
		# nextbutton=tix.Button(sframe,text="Visit",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visitbutton(mm))
		# nextbutton.grid(row=2*i,column=1)
		# nextbutton=tix.Button(sframe,text="Compare",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visualizebutton(mm))
		# nextbutton.grid(row=2*i,column=2)
		# lbl1 = tix.Label(sframe, text="______________________________________________________________",font=("Arial Black",20))
		# lbl1.grid(row=2*i+1,column=0)

		def roundstring22(str):
			l=len(str)
			i=18-l
			str=str+" "
			return str

		def roundstring85(str):
			l=len(str)
			# print(l)
			i=20-l
			str="  "+str
			return str

		def infofunc(mm):
				
			info=""
			title=mm.title
			title=roundstring85(title)
			l="Course Name"
			l=roundstring22(l)
			info=info+l+":"+title+"\n"

			provider="Coursera"
			provider=roundstring85(provider)
			l="MOOC Provider"
			l=roundstring22(l)
			info = info+l+":"+provider+"\n"

			link=mm.url
			link=roundstring85(link)
			l="Course Link"
			l=roundstring22(l)
			info=info+l+" : "+link+"\n"

			offeredby=mm.creators
			offeredby=roundstring85(offeredby)
			l="Offered By"
			l=roundstring22(l)
			info=info+l+":"+offeredby+"\n"

			z=mm.startdate
			x="no start date "
			# print(z,k)
			if z==x :
				zx="Self Paced"
				zx=roundstring85(zx)
				zxs="Course Type"
				zxs=roundstring22(zxs)
				duration=mm.duration
				duration=roundstring85(duration)
				d="Estimated Duration"
				d=roundstring22(d)
				info = info+zxs+":"+zx+"\n"+d+":"+duration+"\n"

				z1="Avg User Rating"
				z=roundstring22(z1)
				x=mm.review
				x=roundstring85(x)
				info=info+z+":"+x+"\n"

				p="Percentage Match"
				p=roundstring22(p)
				pp=mm.percentage
				pp=str(round(pp, 2))
				pp=roundstring85(pp)
				info=info+p+":"+pp+"\n"
	    	
				p="Price"
				p=roundstring22(p)
				pp="Not Available"
				pp=roundstring85(pp)
				info=info+p+":"+pp

				
				return info

			else :
				zx="Scheduled"
				zx=roundstring85(zx)
				zxs="Course Type"
				zxs=roundstring22(zxs)
				startdate=mm.startdate
				startdate=roundstring85(startdate)
				d="Start Date"
				d=roundstring22(d)
				info = info+zxs+":"+zx+"\n"+d+":"+startdate+"\n"
				z="Avg User Rating"
				z=roundstring22(z)
				x=mm.review
				x=roundstring85(x)
				info=info+z+":"+x+"\n"

				p="Percentage Match"
				p=roundstring22(p)
				pp=mm.percentage
				pp=str(round(pp, 2))
				pp=roundstring85(pp)
				info=info+p+":"+pp+"\n"
	    		
				p="Price"
				p=roundstring22(p)
				pp="Not Available"
				pp=roundstring85(pp)
				info=info+p+":"+pp

				
				return info

			
			


		i=0
		try:
			# print("0")
			mm0=coursefuncobjects[i]
			# print("1")
			info=infofunc(mm0)
			# print("2")
			lbl0 = tix.Label(sframe, text=info,font=("Arial Black",20))
			lbl0.grid(row=2*i,column=0)
			nextbutton0=tix.Button(sframe,text="Visit",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visitbutton(mm0))
			nextbutton0.grid(row=2*i,column=1)
			nextbutton00=tix.Button(sframe,text="Compare",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visualizebutton(mm0))
			nextbutton00.grid(row=2*i,column=2)
			lbl0 = tix.Label(sframe, text="______________________________________________________________",font=("Arial Black",20))
			lbl0.grid(row=2*i+1,column=0)
		except :
			pass

		i=1
		try:
			mm1=coursefuncobjects[i]
			info=infofunc(mm1)
			lbl = tix.Label(sframe, text=info,font=("Arial Black",20))
			lbl.grid(row=2*i,column=0)
			nextbutton1=tix.Button(sframe,text="Visit",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visitbutton(mm1))
			nextbutton1.grid(row=2*i,column=1)
			nextbutton11=tix.Button(sframe,text="Compare",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visualizebutton(mm1))
			nextbutton11.grid(row=2*i,column=2)
			lbl = tix.Label(sframe, text="______________________________________________________________",font=("Arial Black",20))
			lbl.grid(row=2*i+1,column=0)
		except :
			pass
		
		i=2
		try:
			mm2=coursefuncobjects[i]
			info=infofunc(mm2)
			lbl1 = tix.Label(sframe, text=info,font=("Arial Black",20))
			lbl1.grid(row=2*i,column=0)
			nextbutton2=tix.Button(sframe,text="Visit",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visitbutton(mm2))
			nextbutton2.grid(row=2*i,column=1)
			nextbutton22=tix.Button(sframe,text="Compare",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visualizebutton(mm2))
			nextbutton22.grid(row=2*i,column=2)
			lbl1 = tix.Label(sframe, text="______________________________________________________________",font=("Arial Black",20))
			lbl1.grid(row=2*i+1,column=0)
		except :
			pass

		i=3
		try:
			mm3=coursefuncobjects[i]
			info=infofunc(mm3)
			lbl1 = tix.Label(sframe, text=info,font=("Arial Black",20))
			lbl1.grid(row=2*i,column=0)
			nextbutton3=tix.Button(sframe,text="Visit",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visitbutton(mm3))
			nextbutton3.grid(row=2*i,column=1)
			nextbutton33=tix.Button(sframe,text="Compare",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visualizebutton(mm3))
			nextbutton33.grid(row=2*i,column=2)
			lbl1 = tix.Label(sframe, text="______________________________________________________________",font=("Arial Black",20))
			lbl1.grid(row=2*i+1,column=0)
		except :
			pass

		i=4
		try:
			mm4=coursefuncobjects[i]
			info=infofunc(mm4)
			lbl1 = tix.Label(sframe, text=info,font=("Arial Black",20))
			lbl1.grid(row=2*i,column=0)
			nextbutton4=tix.Button(sframe,text="Visit",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visitbutton(mm4))
			nextbutton4.grid(row=2*i,column=1)
			nextbutton44=tix.Button(sframe,text="Compare",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visualizebutton(mm4))
			nextbutton44.grid(row=2*i,column=2)
			lbl1 = tix.Label(sframe, text="______________________________________________________________",font=("Arial Black",20))
			lbl1.grid(row=2*i+1,column=0)
		except :
			pass

		i=5
		try:
			mm5=coursefuncobjects[i]
			info=infofunc(mm5)
			lbl1 = tix.Label(sframe, text=info,font=("Arial Black",20))
			lbl1.grid(row=2*i,column=0)
			nextbutton5=tix.Button(sframe,text="Visit",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visitbutton(mm5))
			nextbutton5.grid(row=2*i,column=1)
			nextbutton55=tix.Button(sframe,text="Compare",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visualizebutton(mm5))
			nextbutton55.grid(row=2*i,column=2)
			lbl1 = tix.Label(sframe, text="______________________________________________________________",font=("Arial Black",20))
			lbl1.grid(row=2*i+1,column=0)
		except :
			pass

		i=6
		try:
			mm6=coursefuncobjects[i]
			info=infofunc(mm6)
			lbl1 = tix.Label(sframe, text=info,font=("Arial Black",20))
			lbl1.grid(row=2*i,column=0)
			nextbutton6=tix.Button(sframe,text="Visit",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visitbutton(mm6))
			nextbutton6.grid(row=2*i,column=1)
			nextbutton66=tix.Button(sframe,text="Compare",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visualizebutton(mm6))
			nextbutton66.grid(row=2*i,column=2)
			lbl1 = tix.Label(sframe, text="______________________________________________________________",font=("Arial Black",20))
			lbl1.grid(row=2*i+1,column=0)
		except :
			pass

		i=7
		try:
			mm7=coursefuncobjects[i]
			info=infofunc(mm7)
			lbl1 = tix.Label(sframe, text=info,font=("Arial Black",20))
			lbl1.grid(row=2*i,column=0)
			nextbutton7=tix.Button(sframe,text="Visit",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visitbutton(mm7))
			nextbutton7.grid(row=2*i,column=1)
			nextbutton77=tix.Button(sframe,text="Compare",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visualizebutton(mm7))
			nextbutton77.grid(row=2*i,column=2)
			lbl1 = tix.Label(sframe, text="______________________________________________________________",font=("Arial Black",20))
			lbl1.grid(row=2*i+1,column=0)
		except :
			pass

		i=8
		try:
			mm8=coursefuncobjects[i]
			info=infofunc(mm8)
			lbl1 = tix.Label(sframe, text=info,font=("Arial Black",20))
			lbl1.grid(row=2*i,column=0)
			nextbutton8=tix.Button(sframe,text="Visit",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visitbutton(mm8))
			nextbutton8.grid(row=2*i,column=1)
			nextbutton88=tix.Button(sframe,text="Compare",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visualizebutton(mm8))
			nextbutton88.grid(row=2*i,column=2)
			lbl1 = tix.Label(sframe, text="______________________________________________________________",font=("Arial Black",20))
			lbl1.grid(row=2*i+1,column=0)
		except :
			pass

		i=9
		try:
			mm9=coursefuncobjects[i]
			info=infofunc(mm9)
			lbl1 = tix.Label(sframe, text=info,font=("Arial Black",20))
			lbl1.grid(row=2*i,column=0)
			nextbutton9=tix.Button(sframe,text="Visit",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visitbutton(mm9))
			nextbutton9.grid(row=2*i,column=1)
			nextbutton99=tix.Button(sframe,text="Compare",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visualizebutton(mm9))
			nextbutton99.grid(row=2*i,column=2)
			lbl1 = tix.Label(sframe, text="______________________________________________________________",font=("Arial Black",20))
			lbl1.grid(row=2*i+1,column=0)
		except :
			pass

		
		i=10
		try:
			mm10=coursefuncobjects[i]
			info=infofunc(mm10)
			lbl0 = tix.Label(sframe, text=info,font=("Arial Black",20))
			lbl0.grid(row=2*i,column=0)
			nextbutton10=tix.Button(sframe,text="Visit",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visitbutton(mm10))
			nextbutton10.grid(row=2*i,column=1)
			nextbutton1010=tix.Button(sframe,text="Compare",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visualizebutton(mm10))
			nextbutton1010.grid(row=2*i,column=2)
			lbl0 = tix.Label(sframe, text="______________________________________________________________",font=("Arial Black",20))
			lbl0.grid(row=2*i+1,column=0)
		except :
			pass

		i=11
		try:
			mm11=coursefuncobjects[i]
			info=infofunc(mm11)
			lbl = tix.Label(sframe, text=info,font=("Arial Black",20))
			lbl.grid(row=2*i,column=0)
			nextbutton11=tix.Button(sframe,text="Visit",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visitbutton(mm11))
			nextbutton11.grid(row=2*i,column=1)
			nextbutton1111=tix.Button(sframe,text="Compare",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visualizebutton(mm11))
			nextbutton1111.grid(row=2*i,column=2)
			lbl = tix.Label(sframe, text="______________________________________________________________",font=("Arial Black",20))
			lbl.grid(row=2*i+1,column=0)
		except :
			pass
		
		i=12
		try:
			mm12=coursefuncobjects[i]
			info=infofunc(mm12)
			lbl1 = tix.Label(sframe, text=info,font=("Arial Black",20))
			lbl1.grid(row=2*i,column=0)
			nextbutton12=tix.Button(sframe,text="Visit",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visitbutton(mm12))
			nextbutton12.grid(row=2*i,column=1)
			nextbutton1212=tix.Button(sframe,text="Compare",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visualizebutton(mm12))
			nextbutton1212.grid(row=2*i,column=2)
			lbl1 = tix.Label(sframe, text="______________________________________________________________",font=("Arial Black",20))
			lbl1.grid(row=2*i+1,column=0)
		except :
			pass

		i=13
		try:
			mm13=coursefuncobjects[i]
			info=infofunc(mm13)
			lbl1 = tix.Label(sframe, text=info,font=("Arial Black",20))
			lbl1.grid(row=2*i,column=0)
			nextbutton13=tix.Button(sframe,text="Visit",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visitbutton(mm13))
			nextbutton13.grid(row=2*i,column=1)
			nextbutton1313=tix.Button(sframe,text="Compare",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visualizebutton(mm13))
			nextbutton1313.grid(row=2*i,column=2)
			lbl1 = tix.Label(sframe, text="______________________________________________________________",font=("Arial Black",20))
			lbl1.grid(row=2*i+1,column=0)
		except :
			pass

		i=14
		try:
			mm14=coursefuncobjects[i]
			info=infofunc(mm14)
			lbl1 = tix.Label(sframe, text=info,font=("Arial Black",20))
			lbl1.grid(row=2*i,column=0)
			nextbutton14=tix.Button(sframe,text="Visit",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visitbutton(mm14))
			nextbutton14.grid(row=2*i,column=1)
			nextbutton1414=tix.Button(sframe,text="Compare",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visualizebutton(mm14))
			nextbutton1414.grid(row=2*i,column=2)
			lbl1 = tix.Label(sframe, text="______________________________________________________________",font=("Arial Black",20))
			lbl1.grid(row=2*i+1,column=0)
		except :
			pass

		i=15
		try:
			mm15=coursefuncobjects[i]
			info=infofunc(mm15)
			lbl1 = tix.Label(sframe, text=info,font=("Arial Black",20))
			lbl1.grid(row=2*i,column=0)
			nextbutton15=tix.Button(sframe,text="Visit",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visitbutton(mm15))
			nextbutton15.grid(row=2*i,column=1)
			nextbutton1515=tix.Button(sframe,text="Compare",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visualizebutton(mm15))
			nextbutton1515.grid(row=2*i,column=2)
			lbl1 = tix.Label(sframe, text="______________________________________________________________",font=("Arial Black",20))
			lbl1.grid(row=2*i+1,column=0)
		except :
			pass

		i=16
		try:
			mm16=coursefuncobjects[i]
			info=infofunc(mm16)
			lbl1 = tix.Label(sframe, text=info,font=("Arial Black",20))
			lbl1.grid(row=2*i,column=0)
			nextbutton16=tix.Button(sframe,text="Visit",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visitbutton(mm16))
			nextbutton16.grid(row=2*i,column=1)
			nextbutton1616=tix.Button(sframe,text="Compare",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visualizebutton(mm16))
			nextbutton1616.grid(row=2*i,column=2)
			lbl1 = tix.Label(sframe, text="______________________________________________________________",font=("Arial Black",20))
			lbl1.grid(row=2*i+1,column=0)
		except :
			pass

		i=17
		try:
			mm17=coursefuncobjects[i]
			info=infofunc(mm17)
			lbl1 = tix.Label(sframe, text=info,font=("Arial Black",20))
			lbl1.grid(row=2*i,column=0)
			nextbutton17=tix.Button(sframe,text="Visit",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visitbutton(mm17))
			nextbutton17.grid(row=2*i,column=1)
			nextbutton1717=tix.Button(sframe,text="Compare",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visualizebutton(mm17))
			nextbutton1717.grid(row=2*i,column=2)
			lbl1 = tix.Label(sframe, text="______________________________________________________________",font=("Arial Black",20))
			lbl1.grid(row=2*i+1,column=0)
		except :
			pass

		i=18
		try:
			mm18=coursefuncobjects[i]
			info=infofunc(mm18)
			lbl1 = tix.Label(sframe, text=info,font=("Arial Black",20))
			lbl1.grid(row=2*i,column=0)
			nextbutton18=tix.Button(sframe,text="Visit",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visitbutton(mm18))
			nextbutton18.grid(row=2*i,column=1)
			nextbutton1818=tix.Button(sframe,text="Compare",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visualizebutton(mm18))
			nextbutton1818.grid(row=2*i,column=2)
			lbl1 = tix.Label(sframe, text="______________________________________________________________",font=("Arial Black",20))
			lbl1.grid(row=2*i+1,column=0)
		except :
			pass

		i=19
		try:
			mm19=coursefuncobjects[i]
			info=infofunc(mm19)
			lbl1 = tix.Label(sframe, text=info,font=("Arial Black",20))
			lbl1.grid(row=2*i,column=0)
			nextbutton19=tix.Button(sframe,text="Visit",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visitbutton(mm19))
			nextbutton19.grid(row=2*i,column=1)
			nextbutton1919=tix.Button(sframe,text="Compare",bd=2,bg='blue',fg='white',font=("Arial Black",15),command=lambda:visualizebutton(mm19))
			nextbutton1919.grid(row=2*i,column=2)
			lbl1 = tix.Label(sframe, text="______________________________________________________________",font=("Arial Black",20))
			lbl1.grid(row=2*i+1,column=0)
		except :
			pass


	
		# self.window.eval('tk::PlaceWindow %s center' % self.window.winfo_pathname(self.window.winfo_id()))		
		self.window.mainloop()

class curajpage():
	def __init__(self):
		self.window=tkinter.Tk()
		self.window.title("Central University of Rajasthan")
		self.window.geometry("1000x768")

		dummy1 = tkinter.Label(self.window, text=" ")
		dummy1.pack()
		dummy1 = tkinter.Label(self.window, text=" ")
		dummy1.pack()
		dummy1 = tkinter.Label(self.window, text=" ")
		dummy1.pack()

		img = tkinter.PhotoImage(file="curaj.png")		
		lbl=tkinter.Label(self.window,image=img)
		lbl.pack()

		

		lbl1 = tkinter.Label(self.window, text=" MOOC Recommendation ",font=("Arial Black",40))
		lbl1.pack()

		course1=Combobox(self.window,font=("Arial Black",25),width=30)
		coursecontent=[]
		with open("curajsyllabus.txt","r") as syl :
			s=syl.read()
			sem=s.split("SEMESTER")
			del(sem[0])
			# print("Number of  semesters : "+str(len(sem)))
			# semid=int(input("select a semester : "))
	

			for currentsem in sem :
				c=currentsem
				# print(c)
				cc=c.split("\n\n")
				del(cc[0])
				c="\n\n".join(cc)
				# print(c)
				cc=c.split("MBD")
				for i in cc :
					ii=i.split("\n\n")
					l=ii[0]
					ll=l.split(" ")
					cid=ll[0]
					del(ll[0])
					cname=" ".join(ll)
					# print(cid+cname)
					coursecontent.append(cid+cname)

		course1['values']=coursecontent
		course1.current(1)

		lbl1 = tkinter.Label(self.window, text="Select a course :  ",font=("Arial Black",35))
		
		def proceed():
			totalcourse=course1.get()
			print(totalcourse)
			self.window.destroy()

			syl=open("curajsyllabus.txt","r") 
			s=syl.read()
			sem=s.split("SEMESTER")
			del(sem[0])

			c=totalcourse.split(" ")
			course=c[0]
			print(course)
			semid1=list(str(course))
			semid=int(semid1[0])
			print("selected course falls in semester : "+str(semid))
			currentsem=sem[semid-1]
			c=currentsem

			cc=c.split("MBD")
			del(cc[0])
			for i in cc :
				ii=i.split("\n")
				# print(ii[0])
				l=ii[0]
				ll=l.split(" ")
				cid=ll[1]
				# print("abhi",cid,course,"abhi")
				if str(cid) == str(course) :
					# print("course found")
					# print(ll)
					del(ll[0])
					del(ll[0])
					cname=" ".join(ll)
					
					coursesyl = i
					# print(coursesyl)
					coursetopics=[]
					ct=coursesyl.split("\n\n")
					del(ct[0])
					del(ct[-1])
					# print(ct)
					for ctt in ct :
						ctt1=ctt.split(":")
						# print(ctt1[0])
						coursetopics.append(ctt1[0])
						ctt2=ctt1[1].split(",")
						for p in ctt2 :
							coursetopics.append(p)
					# print(coursetopics)
					# print(cname)
					targetmooc=[]
					m=[]
					cn=cname.split(" ")
					cnl=[]
					for i in cn :
						cnl.append(i.lower())
					# print(cnl)
					cn=" ".join(cnl)
					cn=cn.title()
					# print(cn)
					tree=ET.parse("coursedatabase.xml")
					root=tree.getroot()
					for  elem in root :
						t=elem.find("coursetitle").text
						k=re.search(cn,t)
						if k :
							targetmooc.append(t)
							m.append(elem)
					# print("list")
					# print(targetmooc)
					# print(m)

					# mm=m[0]
					# mn=mm.find("coursetitle").text
					# print(mn)
					# print(coursetopics)
					# print("-------------------------------")
					mp=[]
					visualize=[]
					visualizeindex=[]
					visualizescore=[]
					for mm in m:
						kl=mm.find("syl")
						kl1=str(kl.find("topics").text)
						# print(kl1)
						kl12 = ast.literal_eval(kl1)
						kl2 = [i.strip() for i in kl12]
						
						score1=0
						lll=[]
						for i in coursetopics :
							score2=0
							item=""
							for z in kl2 :
								sc=fuzz.ratio(i,z)
								if  sc>score2 :
									score2=sc
									item=z
							if score2>44 :
								score1=score1+score2
								lll.append(i+"=="+item+" : "+str(score2))
							else :
								score1=score1+0
								lll.append(i+"=="+"nomatchfound"+" : "+str(0))
						# print(lll)
						visualize.append(lll)
						visualizeindex.append(mm)
						# print("\n\n\n")
						# print(score1)
						l=len(coursetopics)
						maxm=l*100
						p=(score1/maxm)*100
						visualizescore.append(p)
						mp.append(p)
					i=0
					while i < len(targetmooc) :
						# print(targetmooc[i]+" : "+ str(mp[i]))
						i=i+1
					i=0
					while i < len(visualizescore) :
						# print(visualizescore[i])
						i=i+1
			syl.close()
			r=resultspage(visualize,visualizescore,visualizeindex)

		def back() :
			self.window.destroy()
			i=initialpage()

		nextbutton1=tkinter.Button(self.window,text="back",bd=7,bg='blue',fg='white',command=back,font=("Arial Black",20))
		nextbutton1.pack(side=tkinter.BOTTOM)
		nextbutton0=tkinter.Button(self.window,text="proceed",bd=7,bg='blue',fg='white',command=proceed,font=("Arial Black",20))
		nextbutton0.pack(side=tkinter.BOTTOM)

		

		
		lbl1.pack(side=tkinter.LEFT)
		course1.pack(side=tkinter.LEFT)

		

		

		self.window.eval('tk::PlaceWindow %s center' % self.window.winfo_pathname(self.window.winfo_id()))
		self.window.mainloop()

class jntupage():
	def __init__(self):
		self.window=tkinter.Tk()
		self.window.title("Jawaharlal Nehru University")
		self.window.geometry("1000x768")

		self.window.eval('tk::PlaceWindow %s center' % self.window.winfo_pathname(self.window.winfo_id()))
		self.window.mainloop()

class hcupage():
	def __init__(self):
		self.window=tkinter.Tk()
		self.window.title("Hyderabad Central University")
		self.window.geometry("1000x768")

		self.window.eval('tk::PlaceWindow %s center' % self.window.winfo_pathname(self.window.winfo_id()))
		self.window.mainloop()		

class initialpage():
	def __init__(self):
		self.window=tkinter.Tk()
		self.window.title("MOOC Recomendation")
		self.window.geometry("1000x768")

		dummy1 = tkinter.Label(self.window, text=" ")
		dummy1.pack()
		dummy1 = tkinter.Label(self.window, text=" ")
		dummy1.pack()
		dummy1 = tkinter.Label(self.window, text=" ")
		dummy1.pack()
		dummy1 = tkinter.Label(self.window, text=" ")
		dummy1.pack()
		dummy1 = tkinter.Label(self.window, text=" ")
		dummy1.pack()
		dummy1 = tkinter.Label(self.window, text=" ")
		dummy1.pack()
		dummy1 = tkinter.Label(self.window, text=" ")
		dummy1.pack()
		dummy1 = tkinter.Label(self.window, text=" ")
		dummy1.pack()
		dummy1 = tkinter.Label(self.window, text=" ")
		

		lbl1 = tkinter.Label(self.window, text=" MOOC Recommendation ",font=("Arial Black",40))
		lbl1.pack()

		dummy1 = tkinter.Label(self.window, text=" ")
		dummy1.pack()
		dummy1 = tkinter.Label(self.window, text=" ")
		dummy1.pack()
		dummy1 = tkinter.Label(self.window, text=" ")
		dummy1.pack()

		def curaj():
			self.window.destroy()
			c=curajpage()

		def jntu():
			self.window.destroy()
			j=jntupage()

		def hcu():
			self.window.destroy()
			h=hcupage()

		dummy1 = tkinter.Label(self.window, text=" ")
		dummy1.pack()
		dummy1 = tkinter.Label(self.window, text=" ")
		dummy1.pack()

		university1=tkinter.Button(self.window,text="Central University of Rajasthan",bd=7,bg='blue',fg='white',command=curaj,font=("Arial Black",25))
		university1.pack()

		dummy1 = tkinter.Label(self.window, text=" ")
		dummy1.pack()
		dummy1 = tkinter.Label(self.window, text=" ")
		dummy1.pack()

		university2=tkinter.Button(self.window,text="Jawaharlal Nehru University",bd=7,bg='blue',fg='white',command=jntu,font=("Arial Black",25))
		university2.pack()

		dummy1 = tkinter.Label(self.window, text=" ")
		dummy1.pack()
		dummy1 = tkinter.Label(self.window, text=" ")
		dummy1.pack()

		university3=tkinter.Button(self.window,text="Hyderabad Central University",bd=7,bg='blue',fg='white',command=hcu,font=("Arial Black",25))
		university3.pack()

		dummy1 = tkinter.Label(self.window, text=" ")
		dummy1.pack()
		dummy1 = tkinter.Label(self.window, text=" ")
		dummy1.pack()

		self.window.eval('tk::PlaceWindow %s center' % self.window.winfo_pathname(self.window.winfo_id()))
		self.window.mainloop()

if __name__ == "__main__" :
	c=initialpage()