from webbrowser import get
from mysqlx import Column
import requests
from bs4 import BeautifulSoup
import pandas as pd

# url = "https://github.com/topics"

# response = requests.get(url)

# print(response.status_code)
# # print(len(response.text))
# page_content = response.text
# # Parsing html content using beautifulsoup
# soup = BeautifulSoup(page_content,'html.parser')
# # print(type(soup))

# # with open('webpage.html','w') as f:
# #     f.write(page_content[:100])

# # p_tags = soup.find_all('p')
# # print(len(p_tags))
# # print(p_tags[:10])

# # Extract title tags
# selection_class = 'f3 lh-condensed mb-0 mt-1 Link--primary'
# topic_title_tags = soup.find_all('p',{'class':selection_class})
# # print(topic_title_tags[:5])

# # Extract description
# dec_selector = 'f5 color-fg-muted mb-0 mt-1'
# topic_desc_tags = soup.find_all('p',{'class':dec_selector})
# # print(topic_desc_tags[:5])

# topic_title_tags0 = topic_title_tags[0]
# topic_url0 = "https://github.com" + topic_title_tags0.parent['href']
# # print(topic_url0)

# # Here we get list of all topic title
# # Here we get list of description
# # Here we get topic url
# topic_titles = [i.text for i in topic_title_tags]
# # print(topic_titles)
# topic_desc = [i.text.strip() for i in topic_desc_tags]
# # print(topic_desc)
# topic_url = ["https://github.com"+i.parent['href'] for i in topic_title_tags]
# # print(topic_url)

# topics_dict = {'Title':topic_titles,
#                 'Description':topic_desc,
#                 'URL':topic_url}
# topic_df = pd.DataFrame(topics_dict)
# # print(topic_df)
# # topic_df.to_csv('Data.csv')

# ### Getting information out of a page 

# topic_page_url = topic_url[0]
# page_response = requests.get(topic_page_url)
# print(page_response.status_code)
# topic_doc = BeautifulSoup(page_response.text,'html.parser')
# repo_tags = topic_doc.find_all('h3',{'class':'f3 color-fg-muted text-normal lh-condensed'})
# a_tags = repo_tags[0].find_all('a')
# # print(a_tags[0].text.strip())
# # print(a_tags[1].text.strip())
base_url = "https://github.com"
# repo_url = base_url + a_tags[1]['href']
# # print(repo_url)

# star_tags = topic_doc.find_all('span',{'class':'Counter js-social-count'})
# # print(len(star_tags))
# # print(star_tags[0].text)

# # Make function for converting star count from stg to number
def parse_star_count(star_str):
    star_str = star_str.strip()
    if star_str[-1] == 'k':
        return int(float(star_str[:-1]) * 1000)
    return int(star_str)

# # print(parse_star_count(star_tags[0].text))

# # Get all repo information
def get_repo_info(h1_tag,star_tag):
    # retunrs all the required info about a repository
    a_tags = h1_tag.find_all('a')
    username = a_tags[0].text.strip()
    repo_name = a_tags[1].text.strip()
    repo_url = base_url + a_tags[1]['href']
    stars = parse_star_count(star_tag.text.strip())
    return username,repo_name,stars,repo_url
# print(get_repo_info(repo_tags[2],star_tags[2]))

# topic_repos_dict = {
#     'Username': [],
#     'Repo_Name':[],
#     'Stars':[],
#     'Repo_Url':[]
# }

# for i in range(len(repo_tags)):
#     repo_info = get_repo_info(repo_tags[i],star_tags[i])
#     topic_repos_dict['Username'].append(repo_info[0])
#     topic_repos_dict['Repo_Name'].append(repo_info[1])
#     topic_repos_dict['Stars'].append(repo_info[2])
#     topic_repos_dict['Repo_Url'].append(repo_info[3])
# # print(topic_repos_dict)

# # topic_repos_df = pd.DataFrame(topic_repos_dict)
# # print(topic_repos_df)

# # Here we get repos of only 1st url (3D)
# # topic_repos_df.to_csv('github_topics.csv')




# # We want all urls repo name and url
def get_topic_page(topic_url):
    # Download the page
    response = requests.get(topic_url)
    # Check successful response
    if response.status_code != 200:
        raise Exception('Failed to load Page {}'.format(topic_url))
    # Parse using beautifulsoup
    topic_doc = BeautifulSoup(response.text,'html.parser')
    return topic_doc


def get_topic_repos(topic_doc):
    # Get all h3 tags conataining repo title,repo URL, and Username
    repo_tags = topic_doc.find_all('h3',{'class':'f3 color-fg-muted text-normal lh-condensed'})
    # Get all star counts
    star_tags = topic_doc.find_all('span',{'class':'Counter js-social-count'})

    topic_repos_dict = {
    'Username': [],
    'Repo_Name':[],
    'Stars':[],
    'Repo_Url':[]
    }
    #  Get repo info
    for i in range(len(repo_tags)):
        repo_info = get_repo_info(repo_tags[i],star_tags[i])
        topic_repos_dict['Username'].append(repo_info[0])
        topic_repos_dict['Repo_Name'].append(repo_info[1])
        topic_repos_dict['Stars'].append(repo_info[2])
        topic_repos_dict['Repo_Url'].append(repo_info[3])

    return pd.DataFrame(topic_repos_dict)



# url4 = topic_url[4]
# topic_doc =  get_topic_page(url4)
# # print(topic_doc)
# topic4_repos = get_topic_repos(topic_doc)
# # print(topic4_repos)
# topic4_repos.to_csv('topic4.csv')

# We can also do it only in 1 line of code
# topic4_info = get_topic_repos(get_topic_page(topic_url[4]))
# print(topic4_info)



# Now we write one single page for scraping topics page
#  1. Get the list of topics from topic page
#  2. Get the list of top repos from the individual topic pages
#  3. For each topic, Create a CSV of the top repos for the topic
import os
def scrap_topic(topic_url,path):
    if os.path.exists(path):
        print("The {} already exists. Skipping..".format(path))
        return
    topic_df = get_topic_repos(get_topic_page(topic_url))
    topic_df.to_csv(path,index=None)

def scrape_topic_titles(doc):
    selection_class = 'f3 lh-condensed mb-0 mt-1 Link--primary'
    topic_title_tags = doc.find_all('p',{'class':selection_class})
    topic_titles = [i.text for i in topic_title_tags]
    return topic_titles

def get_topic_url(doc):
    selection_class = 'f3 lh-condensed mb-0 mt-1 Link--primary'
    topic_title_tags = doc.find_all('p',{'class':selection_class})
    topic_url = ["https://github.com"+i.parent['href'] for i in topic_title_tags]
    return topic_url

def get_topic_desc(doc):
    dec_selector = 'f5 color-fg-muted mb-0 mt-1'
    topic_desc_tags = doc.find_all('p',{'class':dec_selector})
    topic_desc = [i.text.strip() for i in topic_desc_tags]
    return topic_desc

def scrape_topics():
    topics_url = "https://github.com/topics"
    response = requests.get(topics_url)
    if response.status_code != 200:
        raise Exception('Failed to load Page {}'.format(topics_url))
    doc = BeautifulSoup(response.text,'html.parser')
    topics_dict = {'Title':scrape_topic_titles(doc),
                'Description':get_topic_desc(doc),
                'URL': get_topic_url(doc)}
    return pd.DataFrame(topics_dict)

def scrape_topics_repos():
    topics_df = scrape_topics()

    os.makedirs('Scrape Data',exist_ok=True)

    for index,row in topics_df.iterrows():
        print("Scraping top repository for {}".format(row['Title']))
        scrap_topic(row['URL'],'Scrape Data/{}.csv'.format(row['Title']))
print(scrape_topics_repos())
