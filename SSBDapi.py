
# coding: utf-8

# ## Reference implementation of Python SSBD API using SSBD REST_API
# 
# This is a reference implementation. It can be used as it is for visualization and analysis.
# Contributors are welcome to fork and extend this API or to implement a separate Python API differently based on this implementation.

# In[1]:

import requests


# In[ ]:

class ssbd(object):
    apifunc="data"
    field='organism'# default search field
    search_cond='__icontains='
    bdml_field=field+search_cond # default to use case-insensitive containment search
    search='elegans' #default search for C.elegans
    fmt = '?format=json;'
    urlbase = 'http://ssbd.qbic.riken.jp/SSBD/api/v1/'
    parameters=urlbase+apifunc+'/'+fmt+bdml_field+search+';'
    allowed_fields=['data', 'meta_data', 'coordsXYZ']
    display=True
    
    def set_display(self, status):
        if status == 'off':
            self.display=False
            #print "display="+str(self.display)
        if status == 'on':
            self.display=True
            print "display="+str(self.display)
            
    def check_field(self, test):
        for i in self.allowed_fields:
            if i == test:
                return True
        # if not matching any fields, raise RuntimeError
        mesg=", ".join(self.allowed_fields)
        raise RuntimeError('wrong field. Available fields are: '+mesg)
        
    def display_items(self, bdmldata):
        if self.display : 
            # meta contains meta information: total count, offset, limit, etc.
            print "meta=", bdmldata['meta']
            print "found=", bdmldata['meta']['total_count']
            print "limit=", bdmldata['meta']['limit']
        #print "objects=", bdmldata['objects']
            count=1
            for i in bdmldata['objects']:
                #print "i=", i
                print "No.:",count
                for j in i:
                    print "   ", j, ":", i[j]
                count=count+1 

    def ssbd_get(self, field, search):
        self.check_field(field)
        self.field=field
        self.search= search
        self.bdml_field= self.field+self.search_cond
        self.parameters=self.urlbase+self.apifunc+'/'+self.fmt+self.bdml_field+search+';'
        if self.display :
            print 'display=', self.display
            print 'parameter=', self.parameters
        resp = requests.get(self.parameters)
        if resp.status_code != 200:
            # This means something went wrong.
            raise ApiError('GET /tasks/ {}'.format(resp.status_code))
        bdmldata = resp.json()
        return bdmldata
    
    def ssbd_get_t(self, field, search, t, offset=0, limit=20):
        self.check_field(field)
        self.field=field
        self.search= search
        self.bdml_field= self.field+self.search_cond
        self.parameters=self.urlbase+self.apifunc+'/'+self.fmt+self.bdml_field+search+';t='+str(t)+';offset='+str(offset)       
        if self.display :
            print 'display=', self.display
            print 'parameter=', self.parameters
        resp = requests.get(self.parameters)
        if resp.status_code != 200:
            # This means something went wrong.
            raise ApiError('GET /tasks/ {}'.format(resp.status_code))
        bdmldata = resp.json()
        return bdmldata
    
    def data(self, field, search):
        self.apifunc='data'
        self.allowed_fields=['bdmlUUID', 
                        'localid', 
                        'meta_data__address',
                        'meta_data__basedon',
                        'meta_data__contributors',
                        'meta_data__datatype',
                        'meta_data__department',
                        'meta_data__description',
                        'meta_data__laboratory',
                        'meta_data__name',
                        'meta_data__organism',
                        'meta_data__organization']
        bdmldata=self.ssbd_get(field, search)
        self.display_items(bdmldata)
        return(bdmldata)
        
    def meta_data(self, field, search):
        self.apifunc='meta_data'
        self.allowed_fields=['address', 
                        'basedon', 
                        'contributors', 
                        'datatype', 
                        'department', 
                        'description', 
                        'laboratory', 
                        'name',
                        'localid',
                        'organism', 
                        'organization']
        bdmldata=self.ssbd_get(field, search)
        self.display_items(bdmldata)
        return(bdmldata)
    
    def scale(self, field, search):
        self.apifunc='scale'
        self.allowed_fields=['bdml__bdml_ID', 
                            'tUnit', 
                            'xyzUnit']
        bdmldata=self.ssbd_get(field, search)
        self.display_items(bdmldata)
        return(bdmldata)
    
    def coordXYZ(self, bdmlID, timept, offset=0, limit=100):
        self.apifunc='coordsXYZ'
        self.allowed_fields=['bdml__bdml_ID']
        bdmldata=self.ssbd_get_t('bdml__bdml_ID', str(bdmlID), str(timept), str(offset), str(limit))
        self.display_items(bdmldata)
        return(bdmldata)

