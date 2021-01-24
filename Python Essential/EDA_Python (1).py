#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd


# In[7]:


data = pd.read_csv("Python_Data_File.csv")


# In[8]:


data.head()


# In[12]:


data.tail()


# In[15]:


data.shape
#data.shape[0]


# In[18]:


data.describe()


# In[22]:


col_names =  data.columns


# In[23]:


col_names


# In[24]:


data.shape


# In[27]:


data.nunique()


# In[30]:


data['Category'].unique()


# In[31]:


#cleaning the data


# In[33]:


data.isnull().sum()


# In[38]:


data["Postal Code"].head(10)


# In[39]:


data["Postal Code"].fillna(00000, inplace=True)


# In[41]:


data["Postal Code"].head(10).astype('int32')


# In[45]:


data["Postal Code"] = data["Postal Code"].astype('int32')


# In[46]:


data["Postal Code"]


# In[47]:


pd.set_option('display.max_columns', None)


# In[48]:


data


# In[50]:


# u can drop unnecessary columns


# In[52]:


new_data = data.drop(['Postal Code','Ship Mode'], axis=1)


# In[53]:


new_data


# In[55]:


new_data['Region'].value_counts()


# In[56]:


# Relationshp analysis


# In[57]:


import seaborn as sns


# In[61]:


corr = new_data.corr()
sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns, annot=True)


# In[62]:


sns.pairplot(new_data)


# In[71]:


#relation plot
sns.relplot(x='Shipping Cost', y='Profit', hue = 'Category', data=new_data)


# In[76]:


#distribution plot
sns.distplot(new_data['Quantity'])


# In[83]:


# bar plot 
sns.barplot(x = 'Segment', y= 'Sales', data=new_data)


# In[84]:


# group by and sum, average functions


# In[87]:


new_data.groupby(['Region','Country'])['Sales'].sum()


# In[109]:


new_data.groupby(['Region','Country'])['Sales'].mean()


# In[98]:


type(agg_data)


# In[137]:


nn = new_data.groupby(['Region'])['Sales'].sum().to_frame()
#nn.sort_values(by='Sales', ascending=True)
nn.sort_values(by='Sales', ascending=True)


# In[ ]:




