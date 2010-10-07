# coding: utf-8

import re
import codecs
import urllib
import urllib2
import simplejson
from bkn_wsf import *

'''
TO EXPERIMENT

Edit bkn_wsf.wsf_test() function or coment out the call below add whatever you want.

I put the tests in a bkn_wsf function so bkn_wsf can be imported without side effects 
but if one prefers they can use just the bkn_wsf file for experiments.

'''
    
def test_data():
    objref1 = {
              'id':'objref1',
              'in':'nested object string',
              'nested_array':['four', 'five']
               }
    objref2 = {
              "id":"objref2",
              "in":"array of objects index one"
              }
    objref3 = {
               "id":"objref3",
               "in":"second object in nested array"
               }
    objref4 = {
                "id":"objref4",
                "key":"object key value in mixed array"
                }

    mixed = {
                   "key": "value",
                    "mixed_array": [
                       "basic string in array",
                        {
                        "ref":"objref4"
                        }
                    ]
            }

    record_id = 'sample1'
    bibjson = {"name": "sample one",
               "id": record_id, 
               "type":"Object", 
               "test": "try overwrite record using update with less data. Old data should not remain",
               "value":"a string",
               "value_array":["one", "two", "three"],
               "object": {
                          "ref":"objref1"
                          },
                "object_array": [{
                                  "ref":"objref2"
                                  },
                                  {
                                   "ref":"objref3"
                                   }]
               }
    
    return bibjson
    
#Test.wsf_test()
response = {}
#instance = 'http://www.bibkn.org/wsf/'
#instance = 'http://people.bibkn.org/wsf/'
instance = 'http://datasets.bibsoup.org/wsf/'
Logger.set(0,'level')
#Test.autotest(instance)

BKNWSF.set(instance,'root')
Service.set(BKNWSF.get()+'ws/','root')    
Dataset.set(BKNWSF.get()+'datasets/','root')

Dataset.set('dod')
#response = Dataset.set(Dataset.get(), 'public_access')
#response = Dataset.list('access')
#response = BKNWSF.browse()
#print simplejson.dumps(response, indent=2)

if 1:
    
#    Dataset.set('dod')
    Dataset.set('id_test')
#    datasource = 'dod.bib.json' 
#    datasource = 'test.json'
    testlimit = 0
    import_interval = 5
    print Dataset.get()

    response = Dataset.delete(Dataset.get())
        
#        response = Dataset.set(Dataset.get(), 'default_access')    
#        response = Dataset.set(Dataset.get(), 'public_access')
#        instance_ip = '184.73.164.129'
#        instance_ip = '0.0.0.0'
#        response = Dataset.auth_registrar_access(Dataset.get(), 'update', instance_ip, 'read_update', access_uri)        

    response = Dataset.list('ids')
#    response = Dataset.list('description')    
#    response = Dataset.list('access_detail')    
#    response = Dataset.read('all') #THIS GIVE BAD JSON ERROR
#    response = Dataset.access()

# UPDATE ACCESS FOR PUBLIC READ_ONLY
#    instance_ip = '0.0.0.0'
#    access_uri = 'http://datasets.bibsoup.org/wsf/access/c252265a5b60d426d8e4ac3a0d6e4d66'
#    response = Dataset.auth_registrar_access(Dataset.get(), 'update', instance_ip, 'read_only', access_uri)        
#    print simplejson.dumps(response, indent=2)
#    print 'access list'
#    response = Dataset.list('access')    
    
#    response = BKNWSF.browse()
#    response = Dataset.list('access')
    print simplejson.dumps(response, indent=2)
    print '\n'       
    response = {}
    if (('recordList' in response) and response['recordList']):
        # you can get total results by calling
        facets = get_result_facets(response)
        if (facets):
            print 'facets'
            print simplejson.dumps(facets, indent=2)
            print '\nNOTE: not all things are people. See facets[\"type\"]'
            print 'for  counts: (there are a few things to check)'
            print '\t owl_Thing - \t should represent everything if it exists'
            print '\t Object - \t not sure why this does not represent everything'
            print '\t Person - \t just people'




    