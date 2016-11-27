import os
import urllib
import MySQLdb
#import jinja2
import webapp2
from google.appengine.ext.webapp import template
from twilio import twiml
from twilio.rest import TwilioRestClient

# These environment variables are configured in app.yaml.
CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')
#JINJA_ENVIRONMENT = jinja2.Environment(
#  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
#  extensions=['jinja2.ext.autoescape'],
#  autoescape=True)

def connect_to_cloudsql():
  # When deployed to App Engine, the 'SERVER_SOFTWARE' environment variable
  # will be set to 'Google App Engine/version'.
  if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
    # Connect using the unix socket located at
    # /cloudsql/cloudsql-connection-name.
    cloudsql_unix_socket = os.path.join('/cloudsql/', CLOUDSQL_CONNECTION_NAME)
    db = MySQLdb.connect(
      unix_socket=cloudsql_unix_socket, 
      user=CLOUDSQL_USER, 
      passwd=CLOUDSQL_PASSWORD)
  # If the unix socket is unavailable, then try to connect using TCP. This
  # will work if you're running a local MySQL server or using the Cloud SQL
  # proxy, for example:
  #
  #  $ cloud_sql_proxy -instances=your-connection-name=tcp:3306
  #
  else:
    db = MySQL.connect(
      host='127.0.0.1', user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD)
  return db 


class MainPage(webapp2.RequestHandler):
  def get(self):
    """Simple request handler that shows all of the MySQL variables."""
    db = connect_to_cloudsql()
    cursor = db.cursor()
    cursor.execute('USE questionlog')
    cursor.execute("""SELECT * FROM entries""")
    results = cursor.fetchall()
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, {}))
#    for result in results:
#      self.response.write('{}\n'.format(result))

class HelloTeam(webapp2.RequestHandler):
  def post(self):
    r = twiml.Response()
    r.say("Hello Team!")
    self.response.headers['Content-Type'] = 'text/xml'
    self.response.write(str(r))


class SendSMS(webapp2.RequestHandler):
  def get(self):
    # replace with your credentials from: https://www.twilio.com/user/account
    account_sid = "ACfd55b03ff3ad50bb37608b6145adff21"
    auth_token = "85f755c8111d0fb42aa0582d26a89005"
    client = TwilioRestClient(account_sid, auth_token)
    # replace "to" and "from_" with real numbers
    rv = client.messages.create(to="+14168546186",
                                from_="+16475601629",
                                body="Hello Team!")
    self.response.write(str(rv))

app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/twiml', HelloTeam),
  ('/send_sms', SendSMS)
], debug=True)
