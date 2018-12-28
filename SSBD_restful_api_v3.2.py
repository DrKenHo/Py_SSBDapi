#%% [markdown]
# ## Examples to access SSBD using REST API version 3.2
# 
# The following are some examples of accessing SSBD via REST API directly using Python.

#%%
get_ipython().run_line_magic('config', "InlineBackend.figure_formats=['png']")


#%%
from IPython.display import display


#%%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


#%%
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d


#%%
get_ipython().run_line_magic('matplotlib', 'inline')


#%%
from math import sqrt

#%% [markdown]
# ## Loading ivisual library allows iPython to use VPython to display 3D graphics
# 
# * Installing ivisual can be found here https://github.com/mwcraig/ivisual-notebook-info

#%%
from ivisual import *

#%% [markdown]
# ## Loading json library allows iPython to deal with JSON formatted data

#%%
import json

#%% [markdown]
# ## Loading requests to access REST API

#%%
import requests

#%% [markdown]
# # Requesting SSBD_REST API
# * Using data
# * finding localID that contains the phrase wt (i.e. wild type)

#%%
resp = requests.get('http://ssbd.qbic.riken.jp/SSBD/api/v3/data/?format=json;localID__icontains=wt')
#resp = requests.get('http://172.21.20.193:8000/SSBD/api/v3/data/?format=json;localID__icontains=wt')
#resp = requests.get('http://host.docker.internal:8000/SSBD/api/v3/data/?format=json;localID__icontains=wt')



print("resp:", resp)
if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /tasks/ {}'.format(resp.status_code))

#print resp.text
bdmldata = resp.json()
#for todo_item in bdmldata:
#    print('{} {}'.format(todo_item['id'], todo_item['summary']))


#%%
print(type(bdmldata))
#print "bdmldata=", bdmldata
print("meta=", bdmldata['meta'])
print("total_count=", bdmldata['meta']['total_count'])
#print "limit=", bdmldata['meta']['limit']
#print "objects=", bdmldata['objects']
for i in bdmldata['objects']:
#    print "i=", i
    print("description=", i['description'])
    print("basedon=", i['basedon'])
    print("bdmlID=", i['bdmlID'])
    print("datatype=", i['datatype'])
    print("dblink=", i['dblink'])
    print("gene=", i['gene'])
    print("license=", i['license'])
    print("method_summary=", i['method_summary'])
    print("organism=", i['organism'])
    print("localID=", i['localID'])
    print("orf=", i['orf'])
    print("release=", i['release'])
    print("schema_ver=", i['schema_ver'])
    print("------------------------")
    

#%% [markdown]
# ## Example of using REST API to get numerical data
# 
# Display a time point in 3D
# Using data set from Bao et al. (2006) Automated cell lineage tracing in Caenorhabditis elegans. Proc. Natl. Acad. Sci. U.S.A., 103(8), 2707-2712  http://www.ncbi.nlm.nih.gov/pubmed/16477039
# 
# http://ssbd.qbic.riken.jp/search3/800faa21-c28c-4b72-bd12-d41f2eed02e8/

#%%
# version 3.2
#urlbase = 'http://ssbd1.qbic.riken.jp:8000/SSBD/api/v3/'
#urlbase = 'http://host.docker.internal:8000/SSBD/api/v3/'

urlbase = 'http://ssbd.qbic.riken.jp/SSBD/api/v3/'


apifunc = 'bd5coords/?'
# version 1.0
#urlbase = 'http://ssbd.qbic.riken.jp/SSBD/api/v1/'
#apifunc = 'coordsXYZ/?'
fmt = 'format=json;'
#lmt = 5000
#offst = 0
start = 0
stop = 100
timestep = 100
#resp = requests.get(urlbase+apifunc+fmt+'limit=50000;bdml__bdml_ID__icontains=d15115;t=2')
mainurl = urlbase+apifunc+fmt+'offset='+str(start)+';limit='+str(stop)+';bdmlID=800faa21-c28c-4b72-bd12-d41f2eed02e8'+';ts='+str(timestep)
print("mainurl=", mainurl)
resp = requests.get(mainurl)
print(resp)

if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /tasks/ {}'.format(resp.status_code))

bdmldata = resp.json()
for i in bdmldata['objects']:
    print("i[x]=", i['x'])
    print("i[y]=", i['y'])
    print("i[z]=", i['z'])
    print("i[t]=", i['t'])
    print("i[radius]=", i['radius'])
    print("--------------")


#%%
# getting scaleUnit information
# version 3.2
#urlbase = 'http://ssbd1.qbic.riken.jp:8000/SSBD/api/v3/'
#urlbase = 'http://host.docker.internal:8000/SSBD/api/v3/'

urlbase = 'http://ssbd.qbic.riken.jp/SSBD/api/v3/'


apifunc = 'bd5scaleunit/?'
fmt = 'format=json;'

mainurl = urlbase+apifunc+fmt+';bdmlID=800faa21-c28c-4b72-bd12-d41f2eed02e8'+';'
print("mainurl=", mainurl)
resp = requests.get(mainurl)
print(resp)

if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /tasks/ {}'.format(resp.status_code))

bdmlscaledata = resp.json()
bdmlscaledata


#%%
xscale = float(bdmlscaledata['objects'][0]['xScale'])
yscale = float(bdmlscaledata['objects'][0]['yScale'])
zscale = float(bdmlscaledata['objects'][0]['zScale'])
print("xscale:", xscale, "yscale:", yscale, "zscale:", zscale)

#%% [markdown]
# ## Display 3D positions

#%%
canvas(title="Displaying 3D graphics", background=(0.8,0.8,0.8) )
c = color.red
r = 0.1
x = 0
y = 0
Z = 0


#%%
#count =1
for i in bdmldata['objects']:
        print("is[x]=", float(i['x'])*xscale," is[y]=", float(i['y'])*yscale, "is[z]=", float(i['z'])*zscale, "i[t]=", i['t'], "i[radius]=", float(i['radius']))
        nucleus = sphere()
        nucleus.pos = vector(float(i['x'])*xscale, float(i['y'])*yscale, float(i['z'])*zscale)
        nucleus.size = float(i['radius'])*vector(1,1,1)
#        nucleus.size = count*2*vector(1,1,1)
        nucleus.color = c
        count = count+1


#%%
bdmldata


#%%
len(bdmldata['objects'])


#%%
i0 = bdmldata['objects'][0]
i0


#%%
i1 = bdmldata['objects'][2]
i1


