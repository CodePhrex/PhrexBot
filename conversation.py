"""Slack event routing. Never reply to a channel mention with sensitive data."""
import re

def conversation_request(body, expected_team, administrators):
    event = body.get('event', {})
    user = event.get('user')
    if not expected_team or body.get('team_id') != expected_team or not user or user == '*' or user not in administrators:
        return None
    if event.get('bot_id') or event.get('subtype'):
        return None
    if event.get('type') == 'app_mention':
        pass
    elif event.get('type') != 'message' or event.get('channel_type') != 'im':
        return None
    question = re.sub(r'^<@[A-Z0-9]+>\s*', '', event.get('text','')).strip()
    if not question or len(question)>4000:
        return None
    return user, question

def register_conversation(app, team, administrators, model):
    from intelligence import LocalIntelligence
    ai = LocalIntelligence(model)
    def handle(body, client, logger):
        request = conversation_request(body, team, administrators)
        if request is None:
            return
        user, question = request
        try:
            answer = ai.answer(question, {'availability':'No project or host evidence connected to conversational routing yet.'},
                user_id=user, team_id=body.get('team_id'), expected_team=team, administrators=administrators)
        except Exception:
            logger.warning('Phrex inference unavailable')
            answer = 'Local intelligence unavailable. Check the configured Ollama model and host.'
        try:
            channel = client.conversations_open(users=user)['channel']['id']
            client.chat_postMessage(channel=channel, text=answer, mrkdwn=False, parse='none',
                link_names=False, unfurl_links=False, unfurl_media=False,
                blocks=[{'type':'section','text':{'type':'plain_text','text':answer[:2900]}}])
        except Exception:
            logger.warning('Phrex private delivery unavailable')
    app.event('app_mention')(handle)
    app.event('message')(handle)
