#!/usr/bin/env python
# coding: utf-8

# 
# 
# # Project: TMDb Movie Dataset Data Analysis
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# In this dataset, I will be analysing the TMDb Movie Dataset which has over 5000 movies, and I will be looking at the budget and revenue columns in the dataset.
# 
# ### Dataset Description 
# 
# > **Tip**: This data set contains information about 10,000 movies collected from The Movie Database (TMDb), including user ratings and revenue.
# Certain columns, like ‘cast’ and ‘genres’, contain multiple values separated by pipe (|) characters.
# There are some odd characters in the ‘cast’ column.
# The final two columns ending with “_adj” show the budget and revenue of the associated movie in terms of 2010 dollars, accounting for inflation over time. 
# 
# 
# ### Question(s) for Analysis
# >What is the lowest and highest profit earned in the movies released?
# 
# > What years had the highest revenue?

# In[1]:


# import packages 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


# Upgrade pandas to use dataframe.explode() function. 
get_ipython().system('pip install --upgrade pandas==0.25.0')


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# After observing the dataset and the questions for the analysis, I will be keeping only relevent data and deleting the unused ones to makes the analysis process simple.

# In[3]:


# Load data and inspect for instances of missing or possibly errant data

df = pd.read_csv('tmdb_5000_movies.csv')
df.head()


# In[4]:


#This descriptive statistics is a summary of the central tendency, dispersion and 
#shape of a dataset’s distribution, excluding NaN values.

df.describe()


# 
# ### Data Cleaning
#  

# In[5]:


#Removing unused information from the dataset to make the analysis efficient and simple

# 1. Dropping columns from the dataset 
# 2. Changing format of release date into datetime format
# 3. Remove the movies which are having zero value of budget and revenue.


# In[6]:


# This method prints information about a DataFrame including the index dtype and 
#columns, non-null values and memory usage. Information for this dataset shows that there are 4803 entries
# of datatypes integer, string and float.

df.info()


# In[7]:


#The following columns were dropped because they were not used in the data analysis process
#'homepage', 'keywords', 'overview', 'tagline', 'status', 'spoken_languages','runtime', 'production_companies', 
#'original_language', 'popularity', 'title', 'vote_average' and 'vote_count'


df.drop(['homepage', 'keywords', 'overview', 'tagline', 'status', 'spoken_languages', 
         'runtime', 'production_companies', 'original_language', 'popularity', 'title', 'vote_average', 
         'vote_count'], axis=1, inplace=True)
df.head()


# In[8]:


# This calculates the number of rows that were duplicated. Since no duplicates were in this dataset, 
#there was no need to drop any duplicates


sum(df.duplicated())


# In[9]:


df.info()


# In[10]:


#the date given in the dataset was in string format so I changed it to a datetime format

df['release_date'] = pd.to_datetime(df['release_date'])
df['release_date'].head()


# In[11]:


print("Rows With Zero Values In The Budget Column:",df[(df['budget']==0)].shape[0])
print("Rows With Zero Values In The Revenue Column:",df[(df['revenue']==0)].shape[0])


# In[12]:


#the histograms show that majority of the movies did not have high budgets and also did not make a lot of revenue

df.hist()


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# 
# ### Research Question 1 - What was the lowest and highest profit made for the movies in this dataset?

# In[13]:


#calculating profit made for each of the movies in the dataset
#addition of a new column in the dataframe called 'Profit'

df['profit'] = df['revenue'] - df['budget']

#use the function 'idmin' to find the index of lowest and highest profit made

def find_minmax(a):
    highind = df[a].idxmax()
    minind = df[a].idxmin()
    top = pd.DataFrame(df.loc[highind,:])
    bottom = pd.DataFrame(df.loc[minind,:])
    
# Given list
    print("The Given list : ",df['profit'])

# use max
    res1 = max(df['profit'], key=lambda i: (isinstance(i, int), i))
    res2 = min(df['profit'], key=lambda i: (isinstance(i, int), i))
    return pd.concat([top,bottom],axis = 1)

# Result - print the movie with high and low profit
    print("The movie with the highest profit is : ",res1)
    print("The movie with the lowest profit is : ",res2)
find_minmax('profit')


# In[14]:


#These lines of code show the top 5 profitable movies for this dataset 


news = pd.DataFrame(df['profit'].sort_values(ascending = False))
news['original_title'] = df['original_title']
data = list(map(str,(news['original_title'])))
x = list(data[:5])
y = list(news['profit'][:5])

#plot using pointplot for top 5 profitable movies
mapplot = sns.pointplot(x=y,y=x)

#figure size
sns.set(rc={'figure.figsize':(10,5)})

#title and labels of the plot
mapplot.set_title("Top 5 Movies With The Highest Profit",fontsize = 20)
mapplot.set_xlabel("Profit Index",fontsize = 15)


# In[15]:


#These lines of code show the top 5 least profitable movies for this dataset 


news = pd.DataFrame(df['profit'].sort_values(ascending = True))
news['original_title'] = df['original_title']
data = list(map(str,(news['original_title'])))
x = list(data[:5])
y = list(news['profit'][:5])

#plot using pointplot for top 5 profitable movies
mapplot = sns.pointplot(x=y,y=x)

#figure size
sns.set(rc={'figure.figsize':(10,5)})

#title and labels of the plot
mapplot.set_title("Top 5 Movies With The Highest Profit",fontsize = 20)
mapplot.set_xlabel("Profit Index",fontsize = 15)


# This analysis reveals that the lowest profit earned was '-165710090' for The Lone Ranger movie, which was a loss and the highest profit earned was '2550965087' for the Avatar movie. From the first graph, the top 5 profit earning movies are 'The Avengers', 'Furious 7', 'Jurassic World', 'Titanic' and 'Avatar'. The second graph shows that the 5 least profitable movies were 'The Lone Ranger', 'The Wolfman', 'The Alamo', 'Mars Needs Moms', and 'Drangonball Evolution'. 

# ### Research Question 2 - Which years had the highest revenue?

# In[16]:


#Finding the years which had the highest revenue was done by grouping dates and revenues earned

df.groupby('release_date')['revenue'].mean().plot()

#setup the title and labels of the figure.
plt.title("Year Vs Revenue",fontsize = 15)
plt.xlabel('Release year',fontsize = 13)
plt.ylabel('Average revenue',fontsize = 13)

#setup the figure size.
sns.set(rc={'figure.figsize':(10,5)})
sns.set_style("whitegrid")


# The above graph shows that from the year 2000 were the most profitable years.The profit was very low between the years 1920 and 1976.
# 

# <a id='conclusions'></a>
# ## Conclusions
# 
# I examined the TMDb movies dataset since 1960 based on revenue generated and budget allocated for each movie in the dataset. My analysis revealed that the lowest profit earned was '-165710090' for The Lone Ranger movie, which was a loss and the highest profit earned was '2550965087' for the Avatar movie.
# 
# Also, my analysis revealed that, from year 2000 were the most profitable years.The profit was very low between the years 1920 and 1976.
# 
# ## Limitations
# 
# The analysis did not reveal why Avatar and The Lone Ranger performed that way thus, it would be good to know more about why it happened that way. It would be good to know what makes these movies good or bad to watch to generate such revenue, or make such a loss. 
# 
# Also, the literature for the dataset does not provide any information on why movie released after 2000 made higher revenue. It would also be good to explore that as well.

# In[17]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])


# In[ ]:




