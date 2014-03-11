"""
Scrape NYTimes API for members of Congress from 102-on
(note that House is not currently available prior to 102nd, Senate
goes back to 98th)
"""

import nyt, time, sys, urllib2

def bioscrape(sessions, chamber, newdict=True, olddict=None):

    "define dictionary for all members of a Congressional House"
    if newdict is True:
        cong_dict = {}
    else:
        cong_dict = olddict

    "check that sessions is a list"
    if not type(sessions) is list:
        print("Sessions must be list")
        sys.exit()
    
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


def artscrape(congdict):
    """
    scrape bi-yearly Times article counts for MoCs
    serves as wrapper for nyt.search()

    only gets counts, doesn't get individual article info
    """

    "instantiate new dictionary"
    newdict = congdict.copy()

    "bring in term-date dict"
    d = congdates()

    for i in newdict:

        "check that term indicators exist"
        if newdict[i].has_key('terms'):

            "create internal dict for article counts"
            newdict[i]['art_counts'] = {}

            "encode full name"
            fullname = newdict[i]['first'] + ' ' + newdict[i]['last']
            fullname = urllib2.quote(fullname).decode('utf-8')

            "pull full name from MoC"
            fullname = "%22" + fullname + "%22%7E1"

            "print status to screen"
            print "Retrieving articles for", i

            "loop over terms"
            for j in newdict[i]['terms']:

                "construct search query"
                
                "begin/end dates"
                bdate = d[j]['begin']
                edate = d[j]['end']

                searchterms = fullname + "&begin_date=" + bdate + "&end_date=" + edate

                "hit NYT article search API"
                try:
                    resp = nyt.search(searchterms)['response']['meta']['hits']
                    newdict[i]['art_counts'][j] = resp                    
                except:
                    newdict[i]['art_counts'][j] = -99
                    continue

                "wait"
                time.sleep(0.3)

            newdict[i]['artcount_status'] = True

    return(newdict)



def addterms(congdict, termdict):
    "add terms of service to MoCs' dict entries"

    newdict = congdict.copy()

    "loop over congressional bio dict, add terms"
    for i in newdict:
        try:
            newdict[i]['terms'] = termdict[newdict[i]['icpsr_id']]
        except:
            continue
            
    return(newdict)






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



















                                   



