"""GitHub inventory adapter; callers must enforce user entitlement."""
import re
import requests

class GitHubIntelligence:
    def __init__(self, token, owner='CodePhrex', session=None):
        if not re.fullmatch(r'[A-Za-z0-9-]+', owner):
            raise ValueError('Invalid owner')
        self.owner = owner
        self.session = session or requests.Session()
        self.headers = {'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28'}

    def _get(self, path, params=None):
        response = self.session.get('https://api.github.com' + path, headers=self.headers, params=params, timeout=15, allow_redirects=False)
        if response.status_code != 200:
            raise RuntimeError('GitHub data unavailable (HTTP %d)' % response.status_code)
        return response.json()

    def repositories(self, max_pages=10):
        if not 1 <= max_pages <= 20:
            raise ValueError('Invalid page limit')
        rows = []
        for page in range(1, max_pages+1):
            batch = self._get('/user/repos', {'affiliation':'owner,collaborator,organization_member','per_page':100,'page':page})
            rows.extend(r for r in batch if r.get('owner',{}).get('login','').lower() == self.owner.lower())
            if len(batch) < 100:
                return {'repositories':rows,'truncated':False}
        return {'repositories':rows,'truncated':True}

    def activity(self, repo, kind):
        if not re.fullmatch(r'[A-Za-z0-9_.-]+', repo) or repo in ('.','..'):
            raise ValueError('Invalid repository')
        endpoints = {'commits':'commits','branches':'branches','issues':'issues','prs':'pulls','releases':'releases','builds':'actions/runs'}
        if kind not in endpoints:
            raise ValueError('Unsupported activity')
        data = self._get('/repos/' + self.owner + '/' + repo + '/' + endpoints[kind], {'per_page':20})
        if kind == 'issues':
            data = [item for item in data if 'pull_request' not in item]
        return {'data':data,'scope':'First page; up to 20 API records'}
