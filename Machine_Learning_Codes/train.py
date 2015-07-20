import os
import gensim
from gensim.models import word2vec
import logging


from semantics import *

semantics_obj=WordsSemantics()
semantics_obj.building_vocab('/media/Elements/Skillate/Modified_Codes/Data/Input_Data/Skills')


print "Training going on.."
model=semantics_obj.training(100, 0.03, 5, 8, 3, 1, 1, 1)

print "saving the trained model..."
semantics_obj.saving_model(model,'/media/Elements/Skillate/Modified_Codes/Data/Trained_Data/Skills')
