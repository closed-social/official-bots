from mastodon import Mastodon
import random
import html2text
import time

#   Set up Mastodon
token = open('token.secret','r').read().strip('\n')
print(token)
th = Mastodon(
    access_token = token,
    api_base_url = 'https://thu.closed.social/'
)

lid = 0

h2t = html2text.HTML2Text()
h2t.ignore_links = True

while True:
    r = th.conversations(since_id=lid);

    for conv in r:
        if conv.unread:
            text = conv.last_status.content
            pt = h2t.handle(text)

            rid = random.randint(10000000,99999999)
            th.status_post(hex(rid) + ":\n" + pt)
            th.conversations_read(conv.id)
        lid = max(lid,conv.id);
    print(lid)

    time.sleep(10)

#print(len(r))
#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(r)
