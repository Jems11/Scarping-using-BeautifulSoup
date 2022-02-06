from datetime import datetime
from operator import index
from webbrowser import get
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re

# url = "https://blog.privacyengine.io/"

# response = requests.get(url)
# print(response.status_code)
# page_content = response.text

# doc = BeautifulSoup(page_content,'html.parser')

# a.next-posts-link
# a.previous-posts-link
# next_tag = doc.find('a',class_='next-posts-link')
# print(next_tag)
# print(prev_tag)
# h2_title_tags = doc.find_all('h2')
# links_of_blog = []
# h20 = h2_title_tags[0]
# for i in range(len(h2_title_tags)):
#     for c in h2_title_tags[i].children:
#         links_of_blog.append(c['href'])

# b_url = doc.find_all('a',class_="more-link")
# url_blog = [b['href'] for b in b_url]
# print( url_blog)

# topic_desc = doc.find_all('div',{'class':'full-width post-listing-summary-wrap'})

# listof_topic_desc = [i.text.strip() for i in topic_desc]

# titles = [i.text.strip() for i in h2_title_tags]

# dates = doc.find_all('span',{'class':'post-listing-publish-date'})
# # date_1 = dates[0].text
# # converted_date = datetime.strptime(date_1,'%d %B %Y').date()
# # converted_date1 = converted_date.strftime('%d/%m/%Y')
# topic_date = []
# for dats in dates:
#     l = datetime.strptime(dats.text,'%d %B %Y').date()
#     l1 = l.strftime('%d/%m/%Y')
#     topic_date.append(l1)
# # print(topic_date)
# data_dict = {'Title':titles,
#                 'Description':listof_topic_desc,
#                 'URL':links_of_blog,
#                 'Date':topic_date}
# data_df = pd.DataFrame(data_dict)
# # data_df.to_csv('privacy_data.csv')

# resposnse1 = requests.get(links_of_blog[0])
# print(resposnse1.status_code)
# page_doc = BeautifulSoup(resposnse1.text,'html.parser')

# single_page_title=page_doc.find('h1',{'class':"full-width"})
# # print(single_page_title.text)
# single_page_content = page_doc.find('div',class_="full-width section post-body")
# # print(single_page_content.text)
# topic_author=single_page_title.find_next('a').text
# print(topic_author)


# First of all we started to make scarper.
# first we parse the page and get blog title,blog date and blog url.
# then we parse the single url and get the blog details and blog author.
# then we make one csv file using blog title.

def blog_title(doc):
    b_title = doc.find_all('h2')
    title_blog = [i.text.strip() for i in b_title]
    return title_blog

def blog_url(doc):
    b_url = doc.find_all('a',class_="more-link")
    url_blog = [b['href'] for b in b_url]
    return url_blog

def blog_date(doc):
    b_date = doc.find_all('span',{'class':'post-listing-publish-date'})
    topic_date = []
    for dats in b_date:
        l = datetime.strptime(dats.text,'%d %B %Y').date()
        l1 = l.strftime('%d/%m/%Y')
        topic_date.append(l1)
    return topic_date

def scrape_blog_content(page_url,path):
    if os.path.exists(path):
        print("The {} already exists. Slipping...".format(path))
        return
    content = scrape_content(page_url)
    content.to_csv(path)

def scrape_content(page_url):
    response = requests.get(page_url)
    if response.status_code != 200:
        raise Exception("Failed to load Page {}".format(page_url))
    topic_doc = BeautifulSoup(response.text,'html.parser')

    single_page_title = topic_doc.find('h1',class_="full-width")
    s_page_title = single_page_title.text
    single_page_content = topic_doc.find('div',class_="full-width section post-body").text
    topic_author = single_page_title.find_next('a').text

    page_details = {'Title':[s_page_title],
                    'Details':[single_page_content],
                    'Author':[topic_author]}
    return pd.DataFrame(page_details)

def scrape_page(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to load page")
    doc = BeautifulSoup(response.text,'html.parser')
    next_page_tag = doc.find('a',class_='next-posts-link')
    page_dict = {'Title':blog_title(doc),
                'Date':blog_date(doc),
                'URL':blog_url(doc)}
    blog_df = pd.DataFrame(page_dict)
    return blog_df,next_page_tag

def scrape_page_content(url):
    s_page = scrape_page(url)
    b_df = s_page[0]
    next_tag = s_page[1]
    os.makedirs('Privacy Data',exist_ok=True)

    for index,row in b_df.iterrows():
        print("Scarping data for::::-  {}".format(row['Title']))
        row['Title'] = re.sub('\W+',' ',row['Title'])
        scrape_blog_content(row['URL'],'Privacy Data/{}.csv'.format(row['Title']))
    
    if next_tag == None:
        return
    scrape_page_content(next_tag['href'])
# print(scrape_page_content())

url = "https://blog.privacyengine.io/"
print(scrape_page_content(url))


# def scrape_website():
#     url = "https://blog.privacyengine.io/"
#     scrape_page_content(scrape_page(url))

# def scrape_next_page(doc):
#     next_tag = doc.find('a',class_='next-posts-link')
#     if (next_tag == None):
#         return
#     else:
#         next_tag_link = next_tag['href']
#         scrape_page_content(scrape_page(next_tag_link))      
