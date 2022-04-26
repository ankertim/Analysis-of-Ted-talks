#!/usr/bin/env python
# coding: utf-8

# In[1]:
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
from scipy.ndimage import gaussian_gradient_magnitude
import imageio
import pandas as pd
import random
import nltk
#nltk.download('punkt')
from nltk.corpus import stopwords
#nltk.download('stopwords')

# In[5]:
def collect_stopword():
    Stopword = nltk.corpus.stopwords.words('english')
    newStopword = ['!',',','.','?','-s','-ly','</s>','s', '\'s', '(',')','I','He','They','’','n\'t','We','usually','Some','used']
    Stopword.extend(newStopword)
    return Stopword

# In[6]:
def cut_text(text, Stopword):
    with open(text,'r',encoding="utf-8") as f:
        text = f.readlines()
    f.close()
    text_list = nltk.word_tokenize(text[0])
    filtered_words = [word for word in text_list if word not in Stopword]
    return filtered_words

# In[7]:
def count_seq(list):
    count_df = pd.DataFrame(list,columns=['text'])
    count_df['count']=1
    set_freq = count_df.groupby('text')['count'].sum().sort_values(ascending=False)
    set_freq = pd.DataFrame(set_freq)
    set_freq = set_freq[~set_freq['count'].isin([1])]
    set_freq.reset_index(inplace = True)
    return set_freq

# In[9]:
def generate_wordcloud(word_list,mask_pic):
    wc_list=' '.join(word_list)

    #背景色隨機
    color=['#D0D0D0','white','#D9FFFF','#FFD2D2','#E6CAFF','#E8FFC4','#C4E1E1','#EBD6D6','#EBD3E8','#FFF0AC','black']
    a = random.randint(0,len(color)-1)
    ran = random.randint(10,50)
    if mask_pic == 'preset':
        wc = WordCloud(max_words=500,
                       max_font_size=50,
                       min_font_size=10,
                       scale=20,
                       background_color=color[a],
                       prefer_horizontal=0.9,
                       random_state=ran,
                       relative_scaling=1)
    else:
        mask_img = imageio.imread('WordCloud_proj/mask/'+mask_pic+'.png')
        wc = WordCloud(max_words=500,
                       max_font_size=50,
                       min_font_size=10,
                       scale=20,
                       background_color=color[a],
                       mask=mask_img,
                       prefer_horizontal=0.9,
                       random_state=ran,
                       relative_scaling=1)
    wc.generate(wc_list)
    # Plot 顯示在網頁上面
    #plt.axis('off')
    #plt.imshow(wc)
    #plt.show()
    return wc

# In[12]:
def main(video_name, Text_path, Img_path, freq_path):  
    text = Text_path + video_name + '.txt'
    stopword = collect_stopword()
    cut = cut_text(text, stopword)
    mask = ['circle', 'pentagon', 'star']
    for i in mask:
        wc = generate_wordcloud(cut, i)
        wc.to_file(Img_path + video_name + '_' + i + '.jpg')
    print('analysis finish')
    count = count_seq(cut)
    count.to_csv(freq_path + video_name + '.csv', index=False)
    print('download csv finish')


# In[13]:
def generate_csv(video_name, Text_path, freq_path):
    text = Text_path + video_name + '.txt'
    stopword = collect_stopword()
    cut = cut_text(text, stopword)
    count = count_seq(cut)
    count.to_csv(freq_path + video_name + '.csv', index=False)
    print('download csv finish')