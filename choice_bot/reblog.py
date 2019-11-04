from mastodon import Mastodon
import time
import pprint
import time

DOMAIN   = 'thu.closed.social'
THRESHOLD = 5


def POST(msg):
    if(len(msg) > 500):
        msg = msg[:500]
    th.status_post(msg, visibility='public')

pp = pprint.PrettyPrinter(indent=4)

#   Set up Mastodon
token = open('token.secret','r').read().strip('\n')
print(token)
th = Mastodon(
    access_token = token,
    api_base_url = 'https://' + DOMAIN
)

last = th.account_statuses(th.me().id, limit=1)
#pp.pprint(last)
start = last[0].reblog.id

print(start)

while True:
    print('conn')
    r = th.timeline(timeline='local', min_id=start, limit = 40);
    print(len(r))
    if(len(r) == 0):
        break
    start = r[0].id
    ids = [st.id for st in r if st.favourites_count > THRESHOLD ]
    #sts = [st for st in r if st.favourites_count > THRESHOLD ]

    for i in ids[::-1]:
        th.status_reblog(i)
        #print(st.id, st.favourites_count, st.content)
    #pp.pprint(r);
    print('jjj')
    time.sleep(1)
    print('kkk')

