import logging
import accounts
import itertools

def _getPeople(fun, fields):
    friends = []
    for i in itertools.count():
        logging.info('page ' + str(i+1))
        if fields:
            fr = fun(count=1000, offset=i*1000, fields=fields)
        else:
            fr = fun(count=1000, offset=i*1000)
        friends.extend(fr['items'])
        if len(fr['items']) < 1000:
            break
    return friends



def getFriends(a, fields=None):
    logging.info('Fetching friends')
    return _getPeople(a.friends.get, fields)

def getFollowers(a, fields=None):
    logging.info('Fetching followers')
    return _getPeople(a.users.getFollowers, fields)

def getDialogs(a):
    dialogs = []
    logging.info('Fetching dialogs')
    for i in itertools.count():
        logging.info('page ' + str(i+1))
        fr = a.messages.getDialogs(count=200, offset=i*200)
        for t in fr['items']:
            t = t['message']
            if 'chat_id' in t:
                dialogs.append(t['chat_id'] + 2000000000)
            else:
                dialogs.append(t['user_id'])
        if len(fr['items']) < 200:
            break
    return dialogs

def resolvePid(a, pid, conf_allowed=True):
    if conf_allowed:
        if pid.isdigit():
            return int(pid)
        if pid.startswith('c') and pid[1:].isdigit():
            return 2000000000 + int(pid[1:])
    if '/' in pid:
        pid = pid.split('/')[-1]
    try:
        return a.users.get(user_ids=pid)[0]['id']
    except Exception:
        return None
