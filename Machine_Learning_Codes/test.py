import os
import gensim
from gensim.models import word2vec
import logging


from semantics import *

semantics_obj=WordsSemantics()


model=semantics_obj.loading_model("/media/Elements/Skillate/Modified_Codes/Data/Trained_Data/Skills")
#print model.syn1
print len(model.vocab)

print semantics_obj.most_similar(model,'html',100)

print semantics_obj.similarity_between_sets(model,['c','c++','java'],['javascript','java','mysql','c++','angular_js','ajax','css'])
print semantics_obj.similarity_between_sets(model,['c','c++','java'],['r','pattern_recognition','data_mining'])
print semantics_obj.similarity_between_sets(model,['c','c++','java'],['business_development','business_strategy','sales_and_marketing'])
