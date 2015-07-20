import os
import gensim
from gensim.models import word2vec
import logging
from semantics import *
import glob
import requests
from lxml import etree
from text_normalization import TextNormalization
from unidecode import unidecode
import urllib
import json
import operator



text_norm_obj=TextNormalization()
semantics_obj=WordsSemantics()
model=semantics_obj.loading_model("/media/Elements/Skillate/Modified_Codes/Data/Trained_Data/Skills")
def get_solr_response(query):
	params={}
	params['q']="skills:"+query.encode ('utf8')
	params ['rows'] = '50000'
	params ['wt'] = 'json'
	list_of_docs = []
	try:
		paramstr = urllib.urlencode (params)
		solrquery = "http://localhost:8983/solr/Resume_skills/select?" + paramstr
		r = requests.get (solrquery)
		decoded = json.loads (r.content)
		list_of_docs = decoded ['response']['docs']
	except Exception, e:
		print>>sys.stderr, repr (e)

	return list_of_docs

def skill_list_norm(skills_list):
	a=[]
	for skill in skills_list:
		skill_norm=text_norm_obj.Canonical(skill)
		if skill_norm:
			skill_norm=skill_norm.split(" ")
			if len(skill_norm)>1:
				final_skill="_".join(skill_norm)
			else:
				final_skill=skill_norm[0]

			if final_skill in skills_vocab_dic:
				a.append(final_skill)
			else:
				continue
	return a

def skill_present_vocab(skill_list):
	a=[]
	for skill in skill_list:
		if skill in skills_vocab_dic:
			a.append(skill)
	return a


fr=open(r"/media/Elements/Skillate/Modified_Codes/Data/Vocab/Skills/Skills_list.txt","r")
readlines=fr.readlines()
skills_vocab_dic={};
for skills in readlines:
	skills=skills.strip("\n")
	skills_vocab_dic[skills]=1

query_doc_path=r"/media/Elements/Skillate/Modified_Codes/Data/Query_Data/Jobs"

# def list_norm(skills_list):
# 	for skill in skills_list:
# 		skill=





for files in glob.glob(query_doc_path+"/*.html"):
	matching_score={}
	file_name=files.split("/")[-1]
	fp=open(files,"r")
	root=etree.HTML(fp.read())
	skills_list=root.xpath('//div[@class="ksTags"]//text()')
	normalized_skills_list=skill_list_norm(skills_list)
	if len(normalized_skills_list)>1:
		list_of_docs=get_solr_response('('+' '.join(normalized_skills_list)+')')
		print len(list_of_docs)
		dic={};idx=1
		for doc in list_of_docs:
			#print idx;idx+=1
			skills_present=skill_present_vocab(doc["skills"])
			if skills_present:
				match_score=semantics_obj.similarity_between_sets(model,skills_present,normalized_skills_list)
				#print doc["id"],match_score,skills_present
				dic[doc["id"]]=round(match_score*100.0,4)
			else:
				continue
		sorted_dic = sorted(dic.items(), key=operator.itemgetter(1))
		top_10=list(reversed(sorted_dic))[0:10]
		least_10=list(reversed(sorted_dic))[-10:]
		matching_score[file_name]={}
		matching_score[file_name]["top_10"]=top_10
		matching_score[file_name]["least_10"]=least_10
		print json.dumps(matching_score)

	else:
		print "Skills present in the file %s are not present in database :("%(file_name)

		





		

	





	





