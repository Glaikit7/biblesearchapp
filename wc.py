import wordcloud
from wordcloud import WordCloud
import json
import matplotlib.pyplot as plt

# load the names and meanings from the json file
with open('biblenames.json', 'r') as infile:
    names_dict = json.load(infile)

text = " ".join(list(names_dict.values()))

wordcloud = WordCloud().generate(text)

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
