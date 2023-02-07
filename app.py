import requests
import streamlit as st
import openai
import re
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image


# opening the image

image = Image.open('350e1136-340b-c410-9f94-a0336d1bfadc.png')

openai.api_key = "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"

st.title("Advanced Web Scrapping App..😁")
st.image(image, caption="Header Image")


def is_valid_url(url):
    pattern = re.compile(r"^https://.+")
    match = pattern.match(url)
    return bool(match)


def scrape_website(url):

    relevant_urls = []

    # Scrap All teh Urls contains in a website
    try:
        page = requests.get(url)
    except:
        page = urlopen(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    # Extract the Sentences from the url
    visible_text = soup.getText()
    sentences = visible_text.splitlines()
    sen_cnt = len(sentences)
    # print(sen_cnt)

    # Fetching All the Links
    urls = [link.get('href') for link in soup.find_all('a')]

    # Filter out the links which have https in its string
    for url_ in urls:
        try:
            if url_.startswith('https://'):
                relevant_urls.append(url_)
                # print(url)
        except:
            pass

    # Generate a Word Cloud based on the Word Frequency
    words = ' '.join(soup.stripped_strings)
    wordcloud = WordCloud(collocations=False,
                          background_color='white').generate(words)

    # Top 10 Keywords
    top_words = [word for word in wordcloud.words_]

    # Extract every image url
    images = [img.get('src') for img in soup.find_all('img')]
    # print(len(images))

    return pd.DataFrame({'Website URL': [url],
                        'Total Sentence Count': [sen_cnt],
                         'Top 10 frequent words': [top_words[:10]],
                         'First 10 urls': [relevant_urls[:10]]}), wordcloud


input_url = st.text_input("Please enter a Valid Url")
col1, col2 = st.columns(2)
if st.button("Submit"):
    if(len(input_url) != 0):
        if is_valid_url(input_url):
            with st.spinner():
                df, wordcloud = scrape_website(input_url)

            df = df.transpose()
            df.columns = ['Value']
            with col1:
                st.dataframe(df)
            #fig = plt.imshow(wordcloud, interpolation='bilinear')
            with col2:
                fig, ax = plt.subplots(figsize=(12, 8))
                ax.imshow(wordcloud, interpolation='bilinear')
                plt.axis('off')
                st.pyplot(fig)

            st.success("Url has been succesfully scraped...😀")
        else:
            st.warning("Please enter a valid URL.🤨")
    else:
        st.warning("Why are you pressing teh button...Enter a link first😣")
