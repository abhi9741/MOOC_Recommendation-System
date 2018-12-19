import xml.etree.ElementTree as ET
import re
from fuzzywuzzy import fuzz
import ast

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
			print(cid+cname)
	course=int(input("enter the course id : "))
	semid1=list(str(course))
	semid=int(semid1[0])
	print("selected course falls in semester : "+str(semid))
	
	currentsem=sem[semid-1]
	c=currentsem
	
	# print(c)
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
			print("course found")
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
			print(targetmooc)
			# print(m)

			# mm=m[0]
			# mn=mm.find("coursetitle").text
			# print(mn)
			print(coursetopics)
			print("-------------------------------")
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
					if score2>=40 :
						score1=score1+score2
						lll.append(i+"=="+item+" : "+str(score2))
					else :
						score1=score1+0
						lll.append(i+"=="+"nomatchfound"+" : "+str(0))
				print(lll)
				visualize.append(lll)
				visualizeindex.append(mm)
				print("\n\n\n")
				# print(score1)
				l=len(coursetopics)
				maxm=l*100
				p=(score1/maxm)*100
				visualizescore.append(p)
				mp.append(p)
			i=0
			while i < len(targetmooc) :
				print(targetmooc[i]+" : "+ str(mp[i]))
				i=i+1
			i=0
			while i < len(visualizescore) :
				print(visualizescore[i])
				i=i+1
