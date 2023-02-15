import re
import codecs
import nltk
from collections import Counter

# List of patterns to search for

# Text to parse
text = 'This is a string with term5.'
if re.search("term[0-4]",  text):
        print('Found first term.')
if re.search("term[5-9]",  text):
        print ('Found second term.')
# \d+ is a regular expression that matches one or more digits
# it is not all digits in the string, just match first one
match = re.search("\d+",  "This is the COMP3225 module's 1st lab")

print("The regexp matched '%s' between positions %s and %s" % (match.group(0), match.start(), match.end()))

match = re.search("(\d+).*(\d+)",  "This is the COMP3225 module's 1st lab")

print("The regexp matched '%s' and '%s'" % (match.group(1), match.group(2)))

# search matches only the first occurrence
# findall matches all occurrences
match = re.findall("\d+",  "This is the COMP3225 module's 1st lab")

print("The regexp matched '%s'" % (match))


my_text_name=".\corpus\mytest.txt"

# codecs.open is used to read the file with utf-8 encoding
for line in codecs.open(my_text_name,"r",encoding="utf-8"):
    match=re.findall("\d+", line)
    if match: print(match)
    
misctext=".\corpus\misctext.txt"
hashtag_re="#covid"
postcode_re="SO22 4NR"
phone_re="\+44 \(23\) 8059 5000"
#etc

for line in codecs.open(misctext,"r",encoding="utf-8"):
    match=re.findall(hashtag_re, line)
    if match: print(match)
    match=re.findall(postcode_re, line)
    if match: print(match)
    match=re.findall(phone_re, line)
    if match: print(match)


text='That U.S.A. poster-print costs $12.40...'

# The following pattern is reproduced from the textbook figure 2.12.
# UNFORTUNATELY, the behaviour of NLTK has changed since version 3.1,
# so that capture groups don't work any more and every set
# of grouping parentheses () has now to explicitly declare non-capturing semantics with ?:
pattern = r'''(?x)			# set flag to allow verbose regexps 
	 (?:[A-Z]\.)+			# abbreviations, e.g. U.S.A. 
	 | \w+(?:-\w+)*			# words with optional internal hyphens 
	 | \$?\d+(?:\.\d+)?%?	# currency and percentages, e.g. $12.40, 82% 
	 | \.\.\.				# ellipsis 
	 | [][.,;"'?():-_`]		# these are separate punctuation tokens; includes ], [ 
	 '''
# 这是一个文本分词的正则表达式模式。该模式由多个用“|”符号分隔的交替组成，每个交替都匹配不同类型的令牌：

# (?:[A-Z]\.)+：匹配大写字母后跟一个句点的序列，例如“U.S.A.”

# \w+(?:-\w+)*：匹配由字母数字字符和连字符组成的单词，例如“word-processing”

# \$?\d+(?:\.\d+)?%?：匹配货币金额或百分比，例如“$100”、“0.5%”、“1,000.00”

# \.\.\.：匹配省略号，即“...”

# [][.,;"?():-_]：匹配任何标点符号或符号字符，例如方括号、逗号、句点、分号、引号、问号、感叹号、括号、冒号、连字符和下划线。

# 请注意，模式开头的(?x)是“自由空格模式”选项，允许模式跨越多行并包含可读性空格。

tokens=nltk.regexp_tokenize(text, pattern)
print(tokens)


def extract_topic(text):
    pattern = re.compile(r"How many (.*?) does it take to change a lightbulb\?")
    match = pattern.search(text)
    if match:
        return match.group(1)
    return None

def get_top_topics(filename):
    with codecs.open(filename, 'r', 'utf-8') as f:
        jokes = f.readlines()
    
    topics = [extract_topic(joke) for joke in jokes if extract_topic(joke)]
    topic_counts = Counter(topics)
    return topic_counts.most_common(100)

print("2015:")
print(get_top_topics(".\corpus\lightbulbs-2015.txt"))

print("\n2020:")
print(get_top_topics(".\corpus\lightbulbs-2020.txt"))