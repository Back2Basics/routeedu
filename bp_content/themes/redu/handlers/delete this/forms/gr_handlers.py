from webapp2_extras.i18n import gettext as _
import requests as req
from models.gr_tag import Tag
from models.gr_translate_tag import Tag_translated

#Tag_translated
import webapp2

import web.handlers.gr_forms as forms
#import gaepdb
#from lib import utils, httpagentparser, captcha, twitter
from boilerplate.lib.basehandler import BaseHandler
from boilerplate.lib.decorators import user_required
#from config.production import config
#from lib import facebook, simplejson
#from lib.linkedin import linkedin
from models.gr_concept import Concept
from models.gr_concept_order import Concept_order
from models.gr_content import Video, Content


#google drive api stuff
#from apiclient.discovery import build
#from google.appengine.ext import webapp
#from oauth2client.appengine import OAuth2Decorator

## this is messing around with drive.google.com
#
#decorator = OAuth2Decorator(
#                            client_id = config['google_drive_client_id'],
#                            client_secret=config['google_drive_client_secret'],
#                            scope=config['scope']
#),
#
#service = build('drive', 'v2')

#from lib.gr_utils import create_concept
#from lib.formvalidate import newConceptFormHandler
#from lib.conceptlist import getTeachersConceptList
class GoalSearchHandler(BaseHandler):
    def get(self):
        return NotImplementedError
    
    def form(self):
        return forms.REDU_Search(self)
    
    def post(self):
        if not self.form.validate():
            message = _("You can look for concept titles and influencers")
            self.add_message(message, "error")
        params = {}
        self.render_template('gr_showConcepts.html',**params)

class MainHandler(BaseHandler):
    def get(self):
        #main is going to return the list of user goals they have left to learn to their goal.  users can choose the first one and which constructs a continuous playlist based on the one they chose.
        #If the fetch the list returns =[] then show them goals to choose from.
        
        params = {}
        return self.render_template('gr_main.html', **params)

    def form(self):
        return forms.GR_Search(self)


class AboutHandler(BaseHandler):
    def get(self):
        params = {}
        return self.render_template('gr_about.html', **params)

#class EnterVidForm(BaseHandler):
#   def form(self):
#      return forms.GR_FileURL(self)

class TeachConceptHandler(BaseHandler):
    @user_required
    def get(self):
        params = {}
        return self.render_template("gr_teach_conceptv1.html",**params)

    @webapp2.cached_property
    def form(self):
        return forms.GR_EnterConceptv1(self)
    
    def post(self):
        params = {}
        params['key'] = Concept.new(title = self.form.title.data , description = self.form.description.data)
        prerequisite_tags = [Tag.get_or_insert(tag) for tag in self.form.prerequisite_tags]
        optional_prerequisite_tags = []
        Concept_order.new(params['key'],prerequisite_tags, optional_prerequisite_tags, how_many_optional = 0)
#            params = {'concept':concept.key()}
#            message = _("It worked") +" "+ str(concept.key())
#            self.add_message(message, "success")
        message = _("the concept posted.")
        self.add_message(message, "success")

        if params['key'] is None:
            message = _("the concept didn't post.  The title is '") + self.form.title.data + _("' and the description is '") + self.form.description.data + _(" the key is ") + str(params['key'])+"'"
            self.add_message(message, "error")
        
        return self.render_template("gr_teach_conceptv1.html",**params)
        
        
class EnterContentHandler(BaseHandler):
    @user_required
    def get(self):
        params = {}
        return self.render_template('gr_EnterContentv1', **params)
    def post(self):
        if not self.form.validate():
            message = _("That url didn't validate or was missing info.")
            self.add_message(message, "error")
            return self.get()
        try:
            Content.new(url = self.form.url.data.lower())
            message = _("Content is submitted.  Add another?")
            self.add_message(message, "success")
        except:
            message = _("Content wasn't submitted")
            self.add_message(message, "error")

    
class EnterVidHandler(BaseHandler):
    @user_required
    def get(self):        
        params = {}
        return self.render_template('gr_EnterVidv1.html', **params)
    
    def post(self):
        if not self.form.validate():
            message = _("That url didn't validate or was missing info.")
            self.add_message(message, "error")
            return self.get()
        
        try: 
            Video.new(url=self.form.url.data.lower())
            message = _("Video is submitted.  Add another?")
            self.add_message(message, "success")

        except:
            message = _("Video wasn't submitted")
            self.add_message(message, "error")
            
#todo fix the video title with data using the youtube dev key to get actual titles.
        params = {}
        self.render_template('gr_EnterVidv1.html', **params)
        
    
    @webapp2.cached_property
    def form(self):        
        return forms.GR_FileURL(self)



#class TeachHandler(BaseHandler):
#    def get(self):
#        params = {}
#        params['conceptTable'] = getTeachersConceptList(self)
#        return self.render_template('gr_teach.html', **params)
class EnterDocHandler(BaseHandler):
    #@oauth_required
    @user_required
    def post(self):
#        data = {
#                'Content-Type':'text/txt'
#                }
        req.post()
        #POST https://www.googleapis.com/upload/drive/v2/files?uploadType=media

class PracticeHandler(BaseHandler):
    def get(self):
        params = {}
        return self.render_template('gr_practice.html', **params)

class UseHandler(BaseHandler):
    def get(self):
        params = {}
        return self.render_template('gr_use.html', **params)

    
#class NewConceptHandler(BaseHandler):
#    '''
#    Create a New Concept form handler
#    ''' 
#    def get(self):
#        params = {}
#        return self.render_template('register.html', **params)
#    
#    def post(self):
#        if not self.form.validate():
#            return self.get()
#        gr_title = self.form.GR_Title.data.lower()
#        gr_description = self.form.GR_Description.data.strip()
#        gr_required_prerequisite = self.form.GR_Prerequisite.data.lower() # this should be a comma separated list
#        gr_optional_prerequisite = self.form.GR_Optional_Prerequisite.data.lower() #this should be a comma separated list
#        
#        conceptTagTranslated = Tag_translated.all.filter(title=gr_title).get()
#        if conceptTagTranslated == None:
#            conceptTagTranslated = Tag_translated.new_tag_translated(title = gr_title, description = gr_description)
#
#        concept = Concept.new_concept(gr_title,gr_description)
#        
#        
        #new_concept.language_codes = language_codes
        
        

#class NewConceptHandler(BaseHandler):
#    def get(self):
#        params = {
#                  "action": self.request.url,
#                  }
#        return self.render_template('gr_newconcept.html', **params)
#    def post(self):
#        """ 
#        parse the form info and send to the next page in the form
#        the name attr on the send button has the form page number
#        """
#        try: 
#            obj= json.decoder(self.request.POST)
#            newConcept = newConceptFormHandler(obj)
#            #this from here toill the end of the try statement is going to be a function outside of this and put somewhere in lib.
#            # this will be a transaction.
#            newConcept.put(obj)
#            
#        
#        except:
#            return repr(self.request.POST)
#    
##        objs = json.loads(self.request.POST)
#        for languages in objs:
            
#        return objs

#        #if (True if self.request.POST.get('page1') else False):
#        tags = str(self.request.POST.get('tags')).lower().strip()
#        coteachers = str(self.request.POST.get('coteach')).lower().strip()
#        teach_aids = str(self.request.POST.get('teachaid')).lower().strip()
#        title_tag = str(self.request.POST.get('title')).lower().strip()
#        desc = str(self.request.POST.get('desc')).strip()
#        if title_tag == "" or desc == "":
#            message = 'Sorry, title and description fields are required.'
#            self.add_message(message, 'error')
#            return self.redirect_to('GR-newconcept')
#
#        concept = Concept()
#        teachersaid_list=teach_aids.split(,)
#        concept.tea,coteachers_list = coteachers)
#        
#        for teacher in coteachers.split(,):
#            pass
#        for teacher in teach_aids:
#            pass
#        for tag in tags:
#            pass
#
#        if (True if self.request.POST.get('page2') == 'on' else False):
#            pass
#
#        
#        
        
        
        
#class EnterTagHandler(BaseHandler): #temporary while I work out bugs in Tag handling
#    #TODO: get rid of this
#    @user_required
#    def get(self):        
#        params = {}
#        return self.render_template('gr_waste_of_a_tag_form.html', **params)
#    
#    def post(self):
#        if not self.form.validate():
#            message = _("That tag didn't validate or was missing info.")
#            self.add_message(message, "error")
#            return self.get()
#        
#        try: 
#            key = Tag_translated.new(title=self.form.title.data.lower(), description = self.form.description.data)
#            message = _(" Tag is submitted.  Add another?")
#            self.add_message(message, "success")
#
#        except:
#            message = _("Tag wasn't submitted")
#            self.add_message(message, "error")
#            
#        params = {}
#        self.render_template('gr_waste_of_a_tag_form.html', **params)
#        
#    
#    @webapp2.cached_property
#    def form(self):        
#        return forms.GR_EnterConceptv1(self)
