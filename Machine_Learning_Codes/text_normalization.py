import re


class TextNormalization():
	def __init__(self):
		
		self.punctuations = '''!-;:'"\,./?@#$%^*_~'''
		self.brackets='''[]{}<>()'''
		self.stop_words=["in","the","and","on","by","from","at"]
	def punctuation_removal(self,string):
		""""Removing all the punctuations/delimeter that are found in the string with a free space. """
		if string==".net":
			return string
		string=string.replace("&","and")
		clear_str=""
		for char in string:
			if char not in self.punctuations:
				clear_str=clear_str+char
			else:
				clear_str=clear_str+" "
				continue
		before_bracket=re.findall("[\w\s]+(?=[{\[<\(])",clear_str);after_bracket=re.findall("(?<=[\]\}\)\>])[\w\s]+",clear_str)
		if before_bracket  or after_bracket:
			complete_string_list=before_bracket+after_bracket
			clear_str=" ".join(complete_string_list)
		

		##Again checking the brackets for those cases like <deep learning>.
		if clear_str[0].strip() in self.brackets and clear_str[-1].strip() in self.brackets:
			return clear_str[1:-1].strip()
		elif clear_str[0].strip() in self.brackets and clear_str[-1].strip() not in self.brackets:
			return clear_str[1:].strip()
		elif clear_str[0].strip() not in self.brackets and clear_str[-1].strip() in self.brackets:
			return clear_str[:-1].strip()
		else:
			return clear_str.strip()

	def Canonical(self,string):
		"""The strings are canoncalized in a standard form by using this function.
			All the strings containing string enclosed inside the bracket are removed. """
		digit_check=re.search(r"(\d)+",string)
		clean_string=self.punctuation_removal(string)
		final_string=''
		if digit_check:
			digit_sep=re.split("\d+",clean_string)
			clean_string_list=[string.strip() for string in digit_sep if string!=""]
			final_string=" ".join(clean_string_list).strip()
			

		else:
			final_string=clean_string.strip()

		canonical_string=''
		final_string_list=final_string.split(" ")
		try:
			if final_string[0].strip() in self.stop_words and final_string[-1].strip() in self.stop_words:
				canonical_string=" ".join(final_string_list[1:-1])

			elif final_string_list[0].strip() in self.stop_words and final_string[-1].strip() not in self.stop_words:
				canonical_string=" ".join(final_string_list[1:])

			elif final_string_list[-1].strip() in self.stop_words and final_string[0].strip() not in self.stop_words:
				canonical_string=" ".join(final_string_list[:-1])

			else:
				canonical_string=" ".join(final_string_list)
			if canonical_string.lower().find(r"c++")!=-1:
				canonical_string = ' '.join(re.sub(r'(?u)([^\s\w\+]|_)+', ' ', canonical_string).split()).lower ()
			elif canonical_string.lower().find(r".net")!=-1:
				canonical_string = ' '.join(re.sub(r'(?u)([^\s\w\.]|_)+', ' ', canonical_string).split()).lower ()
			else:
				canonical_string = ' '.join(re.sub(r'(?u)([^\s\w]|_)+', ' ', canonical_string).split()).lower ()
			return canonical_string.strip()
		except:
			return ''


a=TextNormalization()
print a.Canonical("deep learning(dnn)")