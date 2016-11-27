import os
import urllib
import MySQLdb
#import jinja2
import webapp2
from google.appengine.ext.webapp import template

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
    for result in results:
      self.response.write('{}\n'.format(result))
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, {}))

app = webapp2.WSGIApplication([
  ('/', MainPage),
], debug=True)
