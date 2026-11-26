"""Process-local admission observations; not a utilization estimate."""
from collections import deque
from threading import Lock
from time import monotonic

class AdmissionWindow:
    def __init__(self):
        self.events=deque(maxlen=10000)
        self.lock=Lock()
    def record(self,team,owner,accepted):
        if not all(isinstance(x,str) and x and x!="*" for x in (team,owner)):
            return
        with self.lock:
            self.events.append((monotonic(),team,owner,bool(accepted)))
    def summary(self,team,owner):
        if not all(isinstance(x,str) and x and x!="*" for x in (team,owner)):
            raise ValueError("Explicit owner scope required")
        with self.lock:
            now=monotonic()
            while self.events and self.events[0][0]<now-3600:
                self.events.popleft()
            events=[e for e in self.events if e[1:3]==(team,owner)]
            accepted=sum(e[3] for e in events)
            return {"window_seconds":3600,"observed":len(events),"admitted":accepted,
                    "queue_full":len(events)-accepted,"rejection_rate":(len(events)-accepted)/len(events) if events else None,
                    "capacity":3,"sample_cap":10000,"persistent":False}

admissions=AdmissionWindow()
