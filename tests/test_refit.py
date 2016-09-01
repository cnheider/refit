import os
import tempfile
import unittest

import flaskr


class FlaskrTestCase(unittest.TestCase):

  def setUp(self):
    self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    flaskr.app.config['TESTING'] = True
    self.app = flaskr.app.test_client()
    with flaskr.app.app_context():
      flaskr.init_db()

  def tearDown(self):
    os.close(self.db_fd)
    os.unlink(flaskr.app.config['DATABASE'])

  def login(self, username, password):
  return self.app.post('/login', data=dict(
      username=username,
      password=password
  ), follow_redirects=True)

  def logout(self):
  return self.app.get('/logout', follow_redirects=True)


if __name__ == '__main__':
  unittest.main()
