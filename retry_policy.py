"""Temporary owner-scoped retry storage; never persist or log prompts."""
from threading import Lock
from time import monotonic
from access_policy import contains_known_secret

class RetryPolicy:
    def __init__(self):
        self.lock = Lock()
        self.records = {}

    def remember_failure(self, root_id, team, user, question):
        if not all(isinstance(x,str) and x for x in (root_id,team,user,question)) or len(question)>8000:
            return False
        if team == '*' or user == '*' or contains_known_secret(question):
            return False
        with self.lock:
            now = monotonic()
            self._prune(now)
            if root_id in self.records:
                return False
            if len(self.records)>=128:
                return False
            self.records[root_id] = dict(team=team,user=user,question=question,expires=now+900,count=0,busy=False)
            return True

    def _prune(self, now):
        for key in list(self.records):
            if self.records[key]["expires"] <= now:
                del self.records[key]

    def prune_expired(self):
        with self.lock:
            self._prune(monotonic())

    def reserve(self, root_id, team, user):
        with self.lock:
            self._prune(monotonic())
            r=self.records.get(root_id)
            if not r or (r["team"],r["user"]) != (team,user):
                raise PermissionError("Retry unavailable")
            if r["busy"] or r["count"]>=2:
                raise RuntimeError("Retry unavailable")
            r["busy"]=True
            r["count"]+=1
            return r["question"]

    def finish(self, root_id, success):
        with self.lock:
            r=self.records.get(root_id)
            if r:
                if success or r["count"]>=2:
                    del self.records[root_id]
                else:
                    r["busy"]=False

    def rollback(self, root_id):
        with self.lock:
            r=self.records.get(root_id)
            if r and r["busy"]:
                r["busy"]=False
                r["count"]-=1
