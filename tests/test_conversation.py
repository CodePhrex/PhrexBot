import unittest
from conversation import conversation_request

class ConversationTests(unittest.TestCase):
    def test_mention(self):
        body = {'team_id':'T1','event':{'type':'app_mention','user':'U1','text':'<@BOT> status'}}
        self.assertEqual(conversation_request(body,'T1',{'U1'}),('U1','status'))
        self.assertIsNone(conversation_request(body,'T1',{'*'}))
        self.assertIsNone(conversation_request(body,'T2',{'U1'}))
    def test_dm_only(self):
        body = {'team_id':'T1','event':{'type':'message','user':'U1','text':'hello','channel_type':'im'}}
        self.assertEqual(conversation_request(body,'T1',{'U1'}),('U1','hello'))
        body['event']['channel_type']='channel'
        self.assertIsNone(conversation_request(body,'T1',{'U1'}))
        body['event']['channel_type']='im'
        body['event']['bot_id']='B1'
        self.assertIsNone(conversation_request(body,'T1',{'U1'}))
