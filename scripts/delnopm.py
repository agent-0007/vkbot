import log
import accounts
import time
import config
import scriptlib
import check_friend

def main(a, args):
    friends = scriptlib.getFriends(a, fields='can_write_private_message')
    to_del = []
    for j in friends:
        if not j['can_write_private_message']:
            to_del.append(str(j['id']))
            log.info('Found id{} ({} {})'.format(j['id'], j['first_name'], j['last_name']))
    check_friend.appendNoadd(to_del)
