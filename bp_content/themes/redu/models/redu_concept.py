from google.appengine.ext import ndb
from models.gr_tag import Tag
from models.gr_translate_tag import Tag_translated

class Concept(ndb.Model):
    """ prerequisites: you need to get_or_insert a Title and description from TagTranslated
    optional prerequisites: make a tag for the institution, make the prequisite
    an email is sent to the co-teachers, teachers aids so they can confirm they have a part in this class.  So that part of the concept isn't going to be available right away.
    """
    
    associated_tag_for_title = ndb.KeyProperty(kind="TagTranslated")
    tag_translated_from_whence_the_title_comes = ndb.KeyProperty(kind="Tag_translated")
    language_codes = ndb.StringProperty(repeated=True) #if a spanish class is taught for the english speaking world then you have 2 possible languages.
    title = ndb.StringProperty()
    description = ndb.StringProperty()
#    title = ndb.ComputedProperty(self.get_title())
#    title, description = ndb.ComputedProperty(get_or_insert(tag_from_whence_the_title_comes, language_codes[0]))  #formerly string property now it references a tag.
    teacher = ndb.UserProperty(auto_current_user_add=True)
    other_teachers = ndb.UserProperty(repeated = True)
    content_list = ndb.KeyProperty(repeated=True) #don't put kind= * in there ... it's left vague for a reason.
    
    created_date = ndb.DateProperty(auto_now_add=True)
    last_modified_date = ndb.DateTimeProperty(auto_now=True)
    
    concept_order = ndb.KeyProperty(repeated=True, kind = "Concept_order")

    #______________optional information____________________
    group = ndb.KeyProperty() #school name /institution name /company name /or just "individual" in a tag.
    teachers_aid_list = ndb.KeyProperty(repeated=True)

    #badges = ndb.KeyProperty(repeated=True) # of the Badge
    #student could be here but I assume that if a person is interested they will take the class then it will show up in their student record

    #I'm not sure if content should have a default order or not

    @classmethod
    def new(cls, title, description):
        cls.concept = Concept()
        cls.concept.tag_translated_from_whence_the_title_comes = Tag_translated.new(title, description) 
        cls.concept.title = title
        cls.concept.description = description
        
        try:
            cls.concept.put()
            return cls.concept.key
        except:
            return "error_in_classmethod"
        #return cls.concept.key


    def get_title(self, tag, language_code):
        title = Tag.query(Tag.languages == Tag_translated(language_code=language_code)).title.get()
        description = Tag.query(Tag.languages == Tag_translated(language_code=language_code)).description.get()
        return (title, description)
    
#    def _pre_put_hook(self):
#        if self.title != NoneType and self.description != NoneType :
#            pass
#        else:
#            if self.associated_tag_for_title:
#                translated_tag_entity = self.associated_tag_for_title.get()
#                self.title = translated_tag_entity.title
#                self.description = translated_tag_entity.description



    
