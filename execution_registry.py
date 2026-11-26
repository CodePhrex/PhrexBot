"""In-memory request metadata; no prompts, credentials or answers retained."""
from threading import Lock
from time import monotonic

class ExecutionRegistry:
    def __init__(self, capacity=128):
        if not 1 <= capacity <= 1024:
            raise ValueError("Invalid capacity")
        self.capacity = capacity
        self.records = {}
        self.lock = Lock()

    def register(self, request_id, team, user, deadline_seconds=240):
        if not all(isinstance(x,str) and x and x != "*" for x in (request_id,team,user)):
            raise ValueError("Explicit ownership required")
        if not 1 <= deadline_seconds <= 900:
            raise ValueError("Invalid deadline")
        with self.lock:
            if request_id in self.records or len(self.records) >= self.capacity:
                raise RuntimeError("Registry unavailable")
            now = monotonic()
            self.records[request_id] = dict(team=team,user=user,state="queued",created=now,deadline=now+deadline_seconds,cancel_requested=False)

    def inspect(self, request_id, team, user):
        with self.lock:
            record = self.records.get(request_id)
            if not record or (record["team"],record["user"]) != (team,user):
                raise PermissionError("Request unavailable")
            return dict(record)

    def cancel(self, request_id, team, user):
        with self.lock:
            record = self.records.get(request_id)
            if not record or (record["team"],record["user"]) != (team,user):
                raise PermissionError("Request unavailable")
            if record["state"] not in ("queued","executing","generating"):
                return False
            record["cancel_requested"] = True
            return True

    def transition(self, request_id, state):
        allowed = {"queued":{"executing","cancelled","failed"},"executing":{"generating","completed","cancelled","failed"},"generating":{"completed","cancelled","failed"}}
        with self.lock:
            record = self.records[request_id]
            if state not in allowed.get(record["state"],set()):
                raise ValueError("Invalid transition")
            record["state"] = state

    def remove_finished(self):
        with self.lock:
            for key in list(self.records):
                if self.records[key]["state"] in ("completed","failed","cancelled"):
                    del self.records[key]

    def owned(self, team, user):
        with self.lock:
            return [(key, dict(value)) for key,value in self.records.items() if (value["team"],value["user"]) == (team,user)]
