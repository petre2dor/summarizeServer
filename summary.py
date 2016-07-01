import falcon
import json
from pyteaser import Summarize
from pyteaser import grab_link

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class SummaryResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        try:
            article = grab_link(req.get_param('url'))
        except IOError:
            print 'IOError'
            return None

        if not (article and article.cleaned_text and article.title):
            return None

        summaries = Summarize(unicode(article.title),
                              unicode(article.cleaned_text))
        body = "";
        for summary in summaries:
            body = body + " " + summary;

        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = json.dumps({'title':article.title, 'body':body}, encoding='utf-8')

# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
summary = SummaryResource()

# summary will handle all requests to the '/summary' URL path
app.add_route('/summary', summary)
