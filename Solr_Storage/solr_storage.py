import pysolr

solr_target = "http://localhost:8983/solr/Resume_skills"

solr = pysolr.Solr(solr_target)

fo=open(r"/media/Elements/Skillate/Modified_Codes/Text_Normalization/resume_skills_term_document_2.txt","r")

readlines=fo.readlines()
print len(readlines)

dic={};
for j in xrange(len(readlines)):
	print j
	readlines[j]=readlines[j].strip("\n")
	split=readlines[j].split(r"~")
	[doc_no,skill]=split[0],"~".join(split[1:])
	skill_split=skill.split(" ")
	if len(skill_split)>1:
		merge_skill="_".join(skill_split)
	else:
		merge_skill=skill_split[0]

	if doc_no in dic:
		if merge_skill:
			if merge_skill not in dic[doc_no]:
				dic[doc_no].append(merge_skill)
			else:
				continue
		else:
			continue
				

	else:
		if merge_skill:
			dic[doc_no]=[]
			dic[doc_no].append(merge_skill)


idx=0;out=[]
for x,y in dic.iteritems():
	print idx;idx+=1
	doc={}
	doc["id"]=x
	doc["skills"]=y
	#out.append(doc)
	out.append(doc)

del dic


for i in xrange(0,len(out),5000):
	print i
	solr.add(out[i:i+5000],'json')
	solr.commit()




	