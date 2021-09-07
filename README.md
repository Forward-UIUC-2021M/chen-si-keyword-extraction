
# Keyword Extraction
Given string input, this algorithm could use embeddings and calculation to output a list of keywords appeared in the string.

## Components
 - keyword_extraction.py
 - Trie.py
 - Aho_Corasick.py
 - database.py (for connecting to local database)
 - print_helper.py (for printing results and useful tools in the terminal)
## Usage
###  Initialization
	extractor = KeywordExtractor()
### Function Call
 - Single text extraction

		extractor.extract_from_single_text(string)
	Input: 
		- string: string for keyword extraction
	Output: 9 most related keywords in string

 - Multi text extraction

		extractor.extract_from_multi_text(string_list, weight_list)
	Input:
		- string_list: python list of string
		- weight_list: weighting for string_list (same length as string_list)
	Output: Normalized keywords output (all keyword score sum up to 1)

## Code Example
#### extract_from_single_text()
```python
def extract_from_single_text(self, string):
	# Sentence Transformer embedding for entire given string
	embeddings = model.encode([string])[0]
	
	# Extracting glossaries appeared in the given string and calculate cosine similarity score into score_list
	glossary_list = self.get_glossary_in_string(string)  
	score_list = []  
	for word in glossary_list:  
	    temp_embedding = model.encode([word])[0]  
	    score = cosine(temp_embedding, embeddings)  
	    score_list.append(score)  
	  
	if len(glossary_list) == 0 or len(glossary_list) == 1:  
	    return glossary_list  
	  
	# Process for eliminating similar keywords  
	similar_keyword_index_list = []  
	for index in range(len(glossary_list) - 1):  
	    word = glossary_list[index]  
	    score = score_list[index]  
	  
	    for i in range(index + 1, len(glossary_list)):  
	        temp_word = glossary_list[i]  
	        temp_score = score_list[i]  
	  
	        # using sequence matcher for similarity score  
	  str_sim = string_similarity(word, temp_word)  
	        if str_sim > 0.5 and abs(score - temp_score) < 0.05:  
	            if i not in similar_keyword_index_list:  
	                similar_keyword_index_list.append(i)  
	  
	for index in sorted(similar_keyword_index_list, reverse=True):  
	    del glossary_list[index]  
	    del score_list[index]  
	  
	return get_top_keywords(glossary_list, score_list, n=10)
```