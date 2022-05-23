import django.contrib.sessions.backends.db as db


class SessionStore(db.SessionStore):
	"""SessionStore implements database session store.
	With SessionStore this application bypasses the session key generation from django's middleware.
	Generated session key follows the example from the course exercise 2.13-session hijack.
	"""

	session_counter = -1

	def _get_new_session_key(self):
		while True:
			session_key = 'session' + str(SessionStore.session_counter)
			SessionStore.session_counter -= 1
			if not self.exists(session_key):
				return session_key
