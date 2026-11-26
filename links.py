"""Trusted navigation links. Configuration must be administrator-controlled."""
import re
from urllib.parse import urlsplit

DEFAULT_HOSTS = frozenset({'github.com','codephrex.slack.com','api.slack.com'})
GITHUB_SECTIONS = {'repository':'','builds':'/actions','prs':'/pulls','issues':'/issues','commits':'/commits','releases':'/releases','security':'/security','docs':'#readme'}

def validate_url(url, hosts=DEFAULT_HOSTS):
    if not isinstance(url,str) or len(url)>2000 or any(ord(c)<=32 or ord(c)==127 for c in url) or '\\' in url:
        raise ValueError('Invalid URL')
    parts = urlsplit(url)
    if parts.scheme != 'https' or parts.username is not None or parts.password is not None or parts.hostname not in hosts or parts.port not in (None,443):
        raise ValueError('Untrusted destination')
    return url

def github_link(repo, section='repository'):
    if not re.fullmatch(r'[A-Za-z0-9_.-]+',repo) or repo in ('.','..') or section not in GITHUB_SECTIONS:
        raise ValueError('Invalid repository or section')
    return validate_url('https://github.com/CodePhrex/'+repo+GITHUB_SECTIONS[section])

def slack_channel_link(channel):
    if not re.fullmatch(r'[CG][A-Z0-9]{8,20}',channel):
        raise ValueError('Invalid channel')
    return validate_url('https://codephrex.slack.com/archives/'+channel)

def link_button(label,url,hosts=DEFAULT_HOSTS):
    if not isinstance(label,str) or not label.strip() or len(label)>75:
        raise ValueError('Invalid button label')
    return {'type':'button','text':{'type':'plain_text','text':label},'url':validate_url(url,hosts)}

def registered_app_link(alias, registry, hosts=DEFAULT_HOSTS):
    if alias not in registry:
        raise ValueError('Unknown application')
    return validate_url(registry[alias],hosts)
