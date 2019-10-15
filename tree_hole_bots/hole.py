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

with open("THUOCL_animal.txt",'r') as x:
    names = x.readlines()

while True:
    r = th.conversations(since_id=lid);

    for conv in r[::-1]:
        if conv.unread:
            text = conv.last_status.content
            pt = h2t.handle(text).lstrip()

            rid = random.randint(0,len(names)-1)
            th.status_post(names[rid].split()[0] + ":\n" + pt)
            th.conversations_read(conv.id)
        lid = max(lid,conv.id);
    print(lid)

    time.sleep(10)

#print(len(r))
#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(r)
