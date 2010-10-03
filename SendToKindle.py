from google.appengine.api import mail
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import login_required
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch


class SendToKindle(webapp.RequestHandler):
    @login_required
    def get(self):
        """1.Check Parameters
        2. Scrape HTML page
        3. Send Email!"""     
        self.response.headers['Content-Type'] = 'text/plain'
   
        to_addr = self.request.get("kindleEmail")
        url = self.request.get("url")
        
        if not mail.is_email_valid(to_addr):
            # Return an error message...
            self.response.out.write ("ERROR! Kindle Email address seems Invalid!")

        message = mail.EmailMessage()
        message.sender = users.get_current_user().email()
        message.to = to_addr
        message.subject = "Convert"
        message.body = "Sent from web2kindle.appspot.com"
        attachment = self.getData(url)
        message.attachments = [(r"web2kindle.html",attachment)]      
        message.send()
        
        self.response.out.write('Alright buddy, this should reach your kindle in a while...')
       
    def getData(self,url):
        """Scrape the html data from the given url and return a string containing
        the html data"""
        self.response.out.write(url+"\n")
        result = urlfetch.fetch(url)
        return result.content



application = webapp.WSGIApplication([('/Send', SendToKindle)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
