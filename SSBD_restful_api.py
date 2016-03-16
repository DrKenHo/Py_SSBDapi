
# coding: utf-8

# ## Examples to access SSBD using REST API
# 
# The following are some examples of accessing SSBD via REST API directly using Python.

# In[1]:

get_ipython().magic(u"config InlineBackend.figure_formats=['png']")


# In[2]:

from IPython.display import display


# In[3]:

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# In[4]:

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d


# In[5]:

get_ipython().magic(u'matplotlib inline')


# In[6]:

from math import sqrt


# ## Loading ivisual library allows iPython to use VPython to display 3D graphics
# 
# * Installing ivisual can be found here https://github.com/mwcraig/ivisual-notebook-info

# In[7]:

from ivisual import *


# ## Loading json library allows iPython to deal with JSON formatted data

# In[8]:

import json


# ## Loading requests to access REST API

# In[9]:

import requests


# In[10]:

resp = requests.get('http://ssbd.qbic.riken.jp/SSBD/api/v1/data/?format=json;bdmlUUID__icontains=d15115')
if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /tasks/ {}'.format(resp.status_code))
#for todo_item in resp.json():
#    print('{} {}'.format(todo_item['id'], todo_item['summary']))
bdmldata = resp.json()
#print type(bdmldata)
#print "bdmldata=", bdmldata
print "meta=", bdmldata['meta']
print "total_count=", bdmldata['meta']['total_count']
#print "limit=", bdmldata['meta']['limit']
#print "objects=", bdmldata['objects']
for i in bdmldata['objects']:
#    print "i=", i
#   print "i[meta_data]=", i['meta_data']
    print "bdmlUUID=", i['bdmlUUID']
    print "E_mail=", i['meta_data']['E_mail']
    print "name=", i['meta_data']['name']


# In[11]:

resp = requests.get('http://ssbd.qbic.riken.jp/SSBD/api/v1/scale/?format=json;bdml__bdml_ID__icontains=d15115')
if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /tasks/ {}'.format(resp.status_code))
scaledata = resp.json()
#print type(bdmldata)
#print "bdmldata=", bdmldata
#print "meta=", bdmldata['meta']
print "total_count=", scaledata['meta']['total_count']
#print "objects=", bdmldata['objects']
for j in scaledata['objects']:
#    print "i=", i    
    print "Scale: ", j['xScale'], j['yScale'], j['zScale']


# ## Example of using REST API to get numerical data

# In[12]:

urlbase = 'http://ssbd.qbic.riken.jp/SSBD/api/v1/'
#urlbase = 'http://172.21.20.198:8000/SSBD/api/v1/'

apifunc = 'coordsXYZ/?'
fmt = 'format=json;'
resp = requests.get(urlbase+apifunc+fmt+'limit=50000;bdml__bdml_ID__icontains=d15115;t=2')
if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /tasks/ {}'.format(resp.status_code))
#for todo_item in resp.json():
#    print('{} {}'.format(todo_item['id'], todo_item['summary']))
bdmldata = resp.json()
print type(bdmldata)
#print "bdmldata=", bdmldata
#print "meta=", bdmldata['meta']
#print "limit=", bdmldata['meta']['limit']
#print "objects=", bdmldata['objects']
for i in bdmldata['objects']:
#    print "i=", i
#    print "bdmlUUID", i['bdmlUUID']
#    print "i[bdml]=", i['bdml']
    print "i[x]=", i['x']
    print "i[y]=", i['y']
    print "i[z]=", i['z']
    print "i[t]=", i['t']


# ## Display 3D positions

# In[13]:

canvas(title="Displaying 3D graphics", background=(0.8,0.8,0.8) )
c = color.red
r = 0.1
x = 0
y = 0
Z = 0


# In[14]:

for j in scaledata['objects']:
    print j['xScale'], j['yScale'], j['zScale']
    sx = j['xScale']
    sy = j['yScale']
    sz = j['zScale']
    sr = j['xScale']

for i in bdmldata['objects']:
#        print "i[x]=", i['x']," i[y]=", i['y'], "i[z]=", i['z'], "i[t]=", i['t']
        sphere(pos=(i['x']*sx, i['y']*sy, i['z']*sz), color=c, radius=i['radius'])


# In[ ]:



