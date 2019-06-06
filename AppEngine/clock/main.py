import datetime
import webapp2
import jinja2
import os
import models

from google.appengine.api import users

template_env = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.getcwd()))

class MainPage(webapp2.RequestHandler):
	def get(self):
		host = self.request.headers['Host']
		self.response.out.write('Host: %s' % host)
		current_time = datetime.datetime.now()
		user = users.get_current_user()
		login_url = users.create_login_url(self.request.path)
		logout_url = users.create_logout_url(self.request.path)
		userprefs = models.get_userprefs()
		if userprefs:
			current_time += datetime.timedelta(
				0, 0, 0, 0, 0, userprefs.tz_offset)
		template = template_env.get_template('home.html')
		context = {
			'current_time': current_time,
			'user': user,
			'login_url': login_url,
			'logout_url': logout_url,
			'userprefs': userprefs,
		}

		self.response.out.write(template.render(context))

application = webapp2.WSGIApplication([('/', MainPage)], debug=True)
