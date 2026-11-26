"""In-process replay suppression and rate limiting."""
from collections import OrderedDict
from threading import Lock
from time import monotonic

class EventGate:
    def __init__(self, interval=15, ttl=600, capacity=4096, clock=monotonic):
        self.interval, self.ttl, self.capacity, self.clock = interval, ttl, capacity, clock
        self.events, self.users = OrderedDict(), OrderedDict()
        self.lock = Lock()

    def admit(self, event_id, user):
        if not isinstance(event_id,str) or not event_id or len(event_id)>128 or not user:
            return False
        with self.lock:
            now = self.clock()
            for cache, lifetime in ((self.events,self.ttl),(self.users,self.interval)):
                while cache and now-next(iter(cache.values())) >= lifetime:
                    cache.popitem(last=False)
            if event_id in self.events or user in self.users:
                return False
            if len(self.events)>=self.capacity or len(self.users)>=self.capacity:
                return False
            self.events[event_id]=now
            self.users[user]=now
            return True
