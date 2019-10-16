from mastodon import Mastodon
import random
import html2text
import time
#import pprint

MAX_SEND = 4
REC_TIME = 600

def POST(msg):
    th.status_post(msg)

def PM(msg):
    th.status_post(msg, visibility='direct')


#   Set up Mastodon
token = open('token.secret','r').read().strip('\n')
print(token)
th = Mastodon(
    access_token = token,
    api_base_url = 'https://thu.closed.social/'
)

lid = 102970936686565234
recs = {}

h2t = html2text.HTML2Text()
h2t.ignore_links = True

#pp = pprint.PrettyPrinter(indent=4)

with open("THUOCL_animal.txt",'r') as x:
    names = x.readlines()

while True:
    r = th.conversations(min_id=lid);
    
    for conv in r[::-1]:
        print(conv.last_status.id,conv.unread, conv.last_status.account.acct)
        if conv.unread:
            
            #pp.pprint(conv);
            name = conv.last_status.account.acct
            if '@' in name:
                PM('树洞只允许在本站使用 @'+name)
            else:
                rec = recs.get(name,[])
                cur_time = time.time()
                print('rec',rec)
                rec = [mes for mes in rec if cur_time - mes[0] < REC_TIME]
                if(len(rec) >= MAX_SEND):
                    PM('次数已满, %d 秒后可继续使用 @%s' % (int(REC_TIME + rec[0][0] - cur_time),name))
                else:
                    if(len(rec)):
                        ani = rec[0][1]
                    else:
                        ani = random.choice(names).split()[0]
                    rec.append((cur_time,ani))

                    text = conv.last_status.content
                    pt = h2t.handle(text).lstrip()

                    POST(ani + ":\n" + pt)
                    recs[name] = rec

            th.conversations_read(conv.id)
        lid = max(lid,conv.last_status.id);
    #print(lid)
    time.sleep(5)

