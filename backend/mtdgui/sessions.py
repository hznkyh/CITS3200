import time
import threading
import uuid

class SessionManager(dict):
    """
    A class for managing user sessions.
    ...
    """

    def __init__(self, purge_interval=3600, session_timeout=3600):
        self.purge_interval = purge_interval
        self.session_timeout = session_timeout
        self.lock = threading.Lock()

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
