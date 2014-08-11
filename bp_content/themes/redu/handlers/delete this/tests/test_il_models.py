"""
just testing the models/models.py models

"""
import unittest
from google.appengine.ext import ndb
from bp_content.themes.il.handlers.models.tag import Tag
from bp_content.themes.il.handlers.models.concept import Concept
from google.appengine.ext import testbed
from google.appengine.datastore import datastore_stub_util



class MakeConceptTest(unittest.TestCase):
    """
        Test to see if Concepts can be written
    """
    def setUp(self):
        """
            set up the env and data
        """
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(probability=.01)
    # Initialize the datastore stub with this policy.
        self.testbed.init_datastore_v3_stub(consistency_policy=self.policy)
        self.testbed.init_memcache_stub()
        self.InsertConcept()
        self.InsertTag()
        
    def tearDown(self):
        self.testbed.deactivate()

    @ndb.transactional(retries=1, xg=True)        
    def InsertConcept(self):
        ''' think about this:
        Tags can have multiple english translations
        should there be a generic definitive tag for multiple same language tagtranslated's
        "Teachers on Drugs", "winning", "recorded after 4:20"
        '''
        t =  Tag()
        t.languages =  Tag_translated()
        t.languages.title = "something"
        t.languages.description="something"
        t.languages.languageCode='en-us'
        tkey = t.put()
        nc= Concept()
        nc.associatedTagforTitle = tkey
        nc.put()
        
    def test_InsertConcept(self):
        self.assertEqual(1,len( Tag_translated.query().fetch(1)),"TagTranslated wasn't created")
        self.assertEqual(1,len(Tag.query().fetch(1)),"Tag wasn't created")
        self.assertEqual(1,len(Concept.query().fetch(1)),"Concept wasn't created")

    @ndb.transactional(retries=1, xg=True)        
    def InsertTag(self):
        tt = Tag_translated()
        tt.languageCode = 'en-us'
        tt.description = 'something'
        tt.title = 'something'
        tt.isRefinedTranslation = False
        nt = Tag()
        nt.languages.append(tt)
        nt.tagType="gr-teacher"
        nt.put()
        
    def TestInsertTag(self):
        self.assertEqual(1, len(Tag.query().fetch(1)), "tag wasn't created")
        
        
if __name__ == '__main__':
    unittest.main()