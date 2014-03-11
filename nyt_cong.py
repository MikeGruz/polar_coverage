"""
Scrape NYTimes API for members of Congress from 102-on
(note that House is not currently available prior to 102nd, Senate
goes back to 98th)
"""

import nyt, time

def bioscrape(sessions, chamber, newdict=True, olddict=None):

    "define dictionary for all members of a Congressional House"
    if newdict is True:
        cong_dict = {}
    else:
        cong_dict = olddict

    
    "loop over sessions"
    for session in sessions:

        "pull chamber membership for that session"
        session = str(session)

        print "Pulling data for Congress #" + session

        membs = nyt.cong_membership(session, chamber)

        "wait for a sec"
        time.sleep(1)

        "loop over individual members, check if already in dict"
        for mem in membs['results'][0]['members']:

            if not cong_dict.has_key(mem['id']):

                "pull individual bio"
                bio = nyt.cong_meminfo(mem['id'])['results'][0]

                cong_dict[mem['id']] = {'first': mem['first_name'],
                                       'middle': mem['middle_name'],
                                       'last': mem['last_name'],
                                       'party': mem['party'],
                                       'state': mem['state'],
                                       'icpsr_id': bio['icpsr_id'],
                                       'govtrack_id': bio['govtrack_id'],
                                       'nyt_id': bio['member_id'],
                                       'thomas_id': bio['thomas_id'],
                                       'gender': bio['gender'],
                                       'roles': bio['roles']}

                "avoid rate limiting"
                time.sleep(0.5)

    return(cong_dict)


def dw_import(dwfile):
    "pulls dw-nominate data into a dict to insert sessions"

    "pull csv in as a list"
    dwlist = open(dwfile, 'r').read()
    dwlist = [i.split() for i in dwlist.split('\n')]

    "create dictionary"
    dwdict = {}

    for i in dwlist:

        "remove sessions prior to 102nd"
        try:
            if int(i[0]) >= 102:

                "check if icpsr key has been encountered"
                if not dwdict.has_key(i[1]):
                    dwdict[i[1]] = []

                dwdict[i[1]].append(int(i[0]))
        except IndexError:
            continue

    return(dwdict)


def congdates():
    "create dict of Congress dates"

    cdates = {102: {'begin': '19910101', 'end': '19921231'},
              103: {'begin': '19930101', 'end': '19941231'},
              104: {'begin': '19950101', 'end': '19961231'},
              105: {'begin': '19970101', 'end': '19981231'},
              106: {'begin': '19990101', 'end': '20001231'},
              107: {'begin': '20010101', 'end': '20021231'},
              108: {'begin': '20030101', 'end': '20041231'},
              109: {'begin': '20050101', 'end': '20061231'},
              110: {'begin': '20070101', 'end': '20081231'},
              111: {'begin': '20090101', 'end': '20101231'},
              112: {'begin': '20110101', 'end': '20121231'}}

    return(cdates)



















                                   



