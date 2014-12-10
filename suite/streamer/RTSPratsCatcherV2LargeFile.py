#!/usr/bin/env python
import sys,os,re
import optparse
import time


def execute(vSeID, vFile):
    cmd01 = "mkdir temp"
    cmd02 = "split -b 1000k %s temp/log" % (vFile)
    # cmd04 = "rm -rf ./temp/%s" % (vFile)
    os.popen(cmd01)
    os.popen(cmd02)
    # os.popen(cmd03)
    # os.popen(cmd04)





    cmd = "awk '/Session: %s/{getline ti;if(ti~/OnDemandSessionId/){print ti;exit}}' %s" % (vSeID,vFile)
    oDSID = os.popen(cmd).read().split(": ")[1].strip()
    print "OnDemandSessionId is ",oDSID

    keyWord1 = 'OnDemandSessionId: ?%s' % (oDSID)
    keyWord2 = 'Session: ?%s' % (vSeID.strip())



    T1 = "(?s)\n(?:[^\n])*?..SETUP(?:[^S]|<(?!ETUP))*?RTSP/1.0(?:[^S]|<(?!ETUP))*?"+keyWord1+".*?(?=20\d\d-)"
    T2 = "(?s)\n(?:[^\n])*?..PLAY(?:[^P]|<(?!LAY))*?RTSP/1.0(?:[^P]|<(?!LAY))*?"+keyWord2+".*?(?=20\d\d-)"
    T3 = "(?s)\n(?:[^\n])*?..TEARDOWN(?:[^T]|<(?!EARDOWN))*?RTSP/1.0(?:[^T]|<(?!EARDOWN))*?"+keyWord2+".*?(?=20\d\d-)"
    T4 = "(?s)\n(?:[^\n])*?..PAUSE(?:[^P]|<(?!AUSE))*?RTSP/1.0(?:[^P]|<(?!AUSE))*?"+keyWord2+".*?(?=20\d\d-)"
    T5 = "(?s)\n(?:[^\n])*?..GET_PARAMETER(?:[^G]|<(?!ET_PARAMETER))*?RTSP/1.0(?:[^G]|<(?!ET_PARAMETER))*?"+keyWord2+".*?(?=20\d\d-)"
    T6 = "(?s)\n(?:[^\n])*?..RTSP/1.0(?:[^R]|<(?!TSP))*?"+keyWord2+".*?(?=20\d\d-)"
    T7 = "(?s)\n(?:[^\n])*?..ANNOUNCE(?:[^A]|<(?!NNOUNCE))*?RTSP/1.0(?:[^A]|<(?!NNOUNCE))*?"+keyWord2+".*?(?=20\d\d-)"

    T11 = "(?s)\n(?:[^\n])*?..SETUP(?:[^S]|<(?!ETUP))*?RTSP/1.0(?:[^S]|<(?!ETUP))*?CSeq(?:[^S]|<(?!ETUP))*?"+keyWord1+".*?(?=20\d\d-)"
    os.chdir("temp")
    logList = os.listdir(os.getcwd())


    for i in logList:
    #    print "sub-file:",i
        r1 = '(%s|%s|%s|%s|%s|%s|%s|%s)' % (T1,T11,T2,T3,T4,T5,T6,T7)

        f = open(i, 'r')

        recsvr = None
        dict = {}
        recsvr = f.read()
        if (oDSID in recsvr) or (vSeID in recsvr):
            reobj = re.compile(r'(?s)%s' % (r1))
            ll = reobj.findall(recsvr)

            for i in ll:
                print i

            f.close()
        else:
            f.close()
            continue
    print "*************************** DONE *******************************************"
    os.chdir('..')
    cmd03 = "rm -rf temp"
    os.popen(cmd03)
    return



if __name__ == '__main__':
    usage ="""
example: %prog -i "12345" -f "rtsp.log"
"""
    parser = optparse.OptionParser(usage)

    parser.add_option("-i", "--Sid", dest="vSeID",
                      default='Null',action="store",
                      help="the sessionID need to search!")
    parser.add_option("-f", "--FileName", dest="vFile",
                      default='Null',action="store",
                      help="the File where do the search!")




    (options, args) = parser.parse_args()

    argc = len(args)
    if argc != 0:
        parser.error("incorrect number of arguments")
        print usage
    else:
        if options.vSeID != "Null" and options.vFile != "Null":
            result = execute(options.vSeID, options.vFile)
        else:
            print usage
