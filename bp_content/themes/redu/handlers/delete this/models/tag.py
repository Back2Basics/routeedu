import ndb    
import datetime as dt

class Tag():
    author= ndb.UserProperty()
    is_appropriate=ndb.BooleanProperty()
    date_authored=ndb.DateProperty()
    translations = {'en-us': {'title':'example',
                              'author':'id',
                              'human_checked':'UserID'}
                    }
    
    def __new__(self,language='en-us',title="example",author="self"):
        self.translations[language]={'title':title,'author':author}
        self.date_authored=dt.date.day

