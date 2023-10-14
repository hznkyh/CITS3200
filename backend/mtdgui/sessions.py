import time
import threading
import uuid

# sessions = {
#     'da017b12-8470-47f4-a4e9-58182b6f3ee3': {
#         "uuid": "da017b12-8470-47f4-a4e9-58182b6f3ee3"
#     }
# }

import threading
import time
import uuid

# class SessionManager:
#     """
#     A class for managing user sessions.

#     Parameters
#     ----------
#     purge_interval : int, optional
#         The interval (in seconds) at which to purge old sessions. Default is 3600.
#     session_timeout : int, optional
#         The amount of time (in seconds) after which a session is considered expired. Default is 3600.

#     Attributes
#     ----------
#     sessions : dict
#         A dictionary containing information about each active session.
#     purge_interval : int
#         The interval (in seconds) at which to purge old sessions.
#     session_timeout : int
#         The amount of time (in seconds) after which a session is considered expired.
#     lock : threading.Lock
#         A lock to ensure thread safety when accessing the `sessions` dictionary.

#     Methods
#     -------
#     create_session()
#         Creates a new session and returns its UUID.
#     """

#     def __init__(self, purge_interval=3600, session_timeout=3600):
#         self.sessions = {
#             "da017b12-8470-47f4-a4e9-58182b6f3ee3": {
#                 "uuid": "da017b12-8470-47f4-a4e9-58182b6f3ee3",
#                 "timestamp": time.time()
#             }
#         }
#         self.purge_interval = purge_interval
#         self.session_timeout = session_timeout
#         self.lock = threading.Lock()
#         # self._start_purge_thread()

#     def __getitem__(self, key):
#         with self.lock:
#             return self.sessions[key]

#     def __setitem__(self, key, value):
#         with self.lock:
#             if key in sessions:
#               self.sessions[key] = value
#             else :
#              self.sessions[key] = value | {"timestamp": time.time()}

#     def __delitem__(self, key):
#         with self.lock:
#             del self.sessions[key]

#     def __contains__(self, key):
#         with self.lock:
#             return key in self.sessions

#     def create_session(self):
#         """
#         Creates a new session and returns its UUID.

#         Returns
#         -------
#         str
#             The UUID of the newly created session.
#         """
#         new_uuid = str(uuid.uuid4())
#         current_time = time.time()
#         with self.lock:
#             self.sessions[new_uuid] = {"uuid": new_uuid, "timestamp": current_time}
#         return new_uuid

#     def _purge_old_sessions(self):
#         """
#         A private method that periodically purges old sessions from the `sessions` dictionary.
#         """
#         while True:
#             current_time = time.time()
#             keys_to_remove = []

#             with self.lock:
#                 for session_uuid, session in self.sessions.items():
#                     if current_time - session["timestamp"] > self.session_timeout:
#                         keys_to_remove.append(session_uuid)

#                 for key in keys_to_remove:
#                     del self.sessions[key]

#             time.sleep(self.purge_interval)

#     def _start_purge_thread(self):
#         """
#         A private method that starts a daemon thread to periodically purge old sessions.
#         """
#         purge_thread = threading.Thread(target=self._purge_old_sessions)
#         purge_thread.daemon = (
#             True  # daemon thread will be killed when main program exits
#         )
#         purge_thread.start()


class SessionManager(dict):
    """
    A class for managing user sessions.
    ...
    """

    def __init__(self, purge_interval=3600, session_timeout=3600):
        self.purge_interval = purge_interval
        self.session_timeout = session_timeout
        self.lock = threading.Lock()
        # self._start_purge_thread()

    def __setitem__(self, key, value):
        with self.lock:
            # If value is a dict and does not contain "timestamp", add it
            if isinstance(value, dict) and "timestamp" not in value:
                value["timestamp"] = time.time()
            # Directly manipulate the dictionary using self
            dict.__setitem__(self, key, value)

    def create_session(self):
        new_uuid = str(uuid.uuid4())
        with self.lock:
            self[new_uuid] = {"uuid": new_uuid}
        return new_uuid

    def _purge_old_sessions(self):
        while True:
            current_time = time.time()
            keys_to_remove = []

            with self.lock:
                for session_uuid, session in self.items():
                    if current_time - session["timestamp"] > self.session_timeout:
                        keys_to_remove.append(session_uuid)

                for key in keys_to_remove:
                    dict.__delitem__(self, key)

            time.sleep(self.purge_interval)

    def _start_purge_thread(self):
        purge_thread = threading.Thread(target=self._purge_old_sessions)
        purge_thread.daemon = (
            True  # daemon thread will be killed when the main program exits
        )
        purge_thread.start()


# Instantiate SessionManager globally so it can purge sessions in the background
sessions = SessionManager(purge_interval=3600, session_timeout=3600)
sessions["da017b12-8470-47f4-a4e9-58182b6f3ee3"] = {
    "uuid": "da017b12-8470-47f4-a4e9-58182b6f3ee3",
    "timestamp": time.time(),
}
