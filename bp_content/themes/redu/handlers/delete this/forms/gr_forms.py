from wtforms import fields
from wtforms import validators
from boilerplate.lib import utils
from webapp2_extras.i18n import lazy_gettext as _
#from webapp2_extras.i18n import ngettext, gettext
from boilerplate.forms import BaseForm

FIELD_MAXLENGTH = 100 # intended to stop maliciously long input

class REDU_Search(BaseForm):
    goal_search = fields.TextField('',[validators.Length(max=FIELD_MAXLENGTH)])

class REDU_Title(BaseForm): #title of the concept
    title = fields.TextField(_('Title'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH)])

class REDU_Description(BaseForm):
    description = fields.TextAreaField(_('Description'), [validators.Required()])

class REDU_FileURL(BaseForm):
    url = fields.StringField(_('Full URL'), [validators.url(require_tld=True, message=_('Invalid URL.'))])
    #pass    

class REDU_Prerequisite(BaseForm): #title of the concept
    Prerequisite_title = fields.TextField(_('Prerequisite'))
    experience_level = fields.SelectField(
                                          _('Experience Level'), 
                                          choices=[
                                                   ('Useful', _('Get the Gist')),
                                                   ('passive', _('Watch Videos/Read About it')),
                                                   ('active', _('Passed Quizes, Exams')),
                                                   ('expert', _('Demonstrated ability using specific concepts in broader context'))
                                                   ]
                                                )
    #yes even I have limits on how long I'll tolerate line length (but it's not 80 char)

class REDU_Optional_Prerequisite(BaseForm): #title of the concept
    Prerequisite_title_optional = fields.TextField(_('Optional Prerequisite'))

class REDU_Languages(BaseForm): # used when tagging multiple languages to a concept
    language = fields.TextField(_('Languages'),[validators.Length(max=FIELD_MAXLENGTH)])
    
#class REDU_EnterConceptv1(REDU_Title, REDU_Prerequisite, REDU_Description, REDU_Optional_Prerequisite, REDU_Languages, REDU_FileURL):
class REDU_Goals(BaseForm):
    goals = fields.TextField(_('Goals'),[validators.Required()])
    
class REDU_Mentor(BaseForm):
    mentor = fields.TextField(_('Email address of a parent, or learning coach'), [validators.regexp(utils.EMAIL_REGEXP, message=_('Invalid email address.'))])

class REDU_EnterConceptv1(REDU_Search,REDU_Title,REDU_Description,REDU_Prerequisite, REDU_Optional_Prerequisite, REDU_Languages): # this is a test to see how 2 work
    pass

