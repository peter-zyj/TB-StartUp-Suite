#!/usr/bin/env python
import sys,os,re
import optparse
import time


def execute(vSeID, vFile):
    s1 = "SETUP rtsp://"

    s2 = "PLAY rtsp://"

    s3 = "TEARDOWN * RTSP/1.0"

    s4 = "PAUSE * RTSP/1.0"

    s5 = "GET_PARAMETER * RTSP/1.0"

    s6 = "RTSP/1.0 200 OK"



    cmd = "awk '/Session: %s/{getline ti;if(ti~/OnDemandSessionId/){print ti;exit}}' %s" % (vSeID,vFile)
    oDSID = os.popen(cmd).read().split(": ")[1].strip()
    print "OnDemandSessionId is ",oDSID
        
    keyWord1 = 'OnDemandSessionId: ?%s' % (oDSID)
    keyWord2 = '[s|S]ession: ?%s' % (vSeID.strip())

    # print "keyword is: ",keyWord2

    # T1 = "\d{4}-\d{2}-\d{2}.*?UTC|(?s)SETUP(?:[^S]|<(?!ETUP))*?RTSP/1.0(?:[^S]|<(?!ETUP))*?"+keyWord1+".*?(?=20\d\d-)"
    # T2 = "\d{4}-\d{2}-\d{2}.*?UTC|(?s)PLAY(?:[^P]|<(?!LAY))*?RTSP/1.0(?:[^P]|<(?!LAY))*?"+keyWord2+".*?(?=20\d\d-)"
    # T3 = "\d{4}-\d{2}-\d{2}.*?UTC|(?s)TEARDOWN(?:[^T]|<(?!EARDOWN))*?RTSP/1.0(?:[^T]|<(?!EARDOWN))*?"+keyWord2+".*?(?=20\d\d-)"
    # T4 = "\d{4}-\d{2}-\d{2}.*?UTC|(?s)PLAY(?:[^P]|<(?!AUSE))*?RTSP/1.0(?:[^P]|<(?!AUSE))*?"+keyWord2+".*?(?=20\d\d-)"
    # T5 = "\d{4}-\d{2}-\d{2}.*?UTC|(?s)GET_PARAMETER(?:[^G]|<(?!ET_PARAMETER))*?RTSP/1.0(?:[^G]|<(?!ET_PARAMETER))*?"+keyWord2+".*?(?=20\d\d-)"
    # T6 = "\d{4}-\d{2}-\d{2}.*?UTC|(?s)RTSP/1.0(?:[^R]|<(?!TSP))*?"+keyWord2+".*?(?=20\d\d-)"
 
   
    # T1 = "(?s)\\n(?:[^\\n])*?..SETUP(?:[^S]|S(?!ETUP))*?RTSP/1.0(?:[^S]|<(?!ETUP))*?"+keyWord1+".*?(?=\\n20\d\d-)"
    # T2 = "(?s)\\n(?:[^\\n])*?..PLAY(?:[^P]|P(?!LAY))*?RTSP/1.0(?:[^P]|<(?!LAY))*?"+keyWord2+".*?(?=\\n20\d\d-)"
    # T3 = "(?s)\\n(?:[^\\n])*?..TEARDOWN(?:[^T]|T(?!EARDOWN))*?RTSP/1.0(?:[^T]|<(?!EARDOWN))*?"+keyWord2+".*?(?=\\n20\d\d-)"
    # T4 = "(?s)\\n(?:[^\\n])*?..PAUSE(?:[^P]|P(?!AUSE))*?RTSP/1.0(?:[^P]|<(?!AUSE))*?"+keyWord2+".*?(?=\\n20\d\d-)"
    # T5 = "(?s)\\n(?:[^\\n])*?..GET_PARAMETER(?:[^G]|G(?!ET_PARAMETER))*?RTSP/1.0(?:[^G]|<(?!ET_PARAMETER))*?"+keyWord2+".*?(?=\\n20\d\d-)"
    # T6 = "(?s)\\n(?:[^\\n])*?..RTSP/1.0(?:[^R]|R(?!TSP))*?"+keyWord2+".*?(?=\\n20\d\d-)"
    # T7 = "(?s)\\n(?:[^\\n])*?..ANNOUNCE(?:[^A]|A(?!NNOUNCE))*?RTSP/1.0(?:[^A]|<(?!NNOUNCE))*?"+keyWord2+".*?(?=\\n20\d\d-)"
 
    # T11 = "(?s)\n(?:[^\n])*?..SETUP(?:[^S]|S(?!ETUP))*?RTSP/1.0(?:[^S]|<(?!ETUP))*?CSeq(?:[^S]|<(?!ETUP))*?"+keyWord1+".*?(?=\\n20\d\d-)"
    
    T1 = "(?s)\\n(?:[^\\n])*?..SETUP(?:[^S]|S(?!ETUP))*?"+keyWord1+".*?(?=\\n20\d\d-)"
    T2 = "(?s)\\n(?:[^\\n])*?..PLAY(?:[^P]|P(?!LAY))*?"+keyWord2+".*?(?=\\n20\d\d-)"
    T3 = "(?s)\\n(?:[^\\n])*?..TEARDOWN(?:[^T]|T(?!EARDOWN))*?"+keyWord2+".*?(?=\\n20\d\d-)"
    T4 = "(?s)\\n(?:[^\\n])*?..PAUSE(?:[^P]|P(?!AUSE))*?"+keyWord2+".*?(?=\\n20\d\d-)"
    T5 = "(?s)\\n(?:[^\\n])*?..GET_PARAMETER(?:[^G]|G(?!ET_PARAMETER))*?"+keyWord2+".*?(?=\\n20\d\d-)"
    T6 = "(?s)\\n(?:[^\\n])*?..RTSP/1.0(?:[^R]|R(?!TSP))*?"+keyWord2+".*?(?=\\n20\d\d-)"
    T7 = "(?s)\\n(?:[^\\n])*?..ANNOUNCE(?:[^A]|A(?!NNOUNCE))*?"+keyWord2+".*?(?=\\n20\d\d-)"
 
    T11 = "(?s)\\n(?:[^\\n])*?..SETUP(?:[^S]|S(?!ETUP))*?"+keyWord1+".*?(?=\\n20\d\d-)"

    # r1 = '.{400}%s.*?(?:%s|%s|%s|%s|%s|%s)' % (keyWord2,s1,s2,s3,s4,s5,s6)
    # r1 = '(%s|%s|%s|%s|%s|%s|%s|%s)' % (T1,T11,T2,T3,T4,T5,T6,T7)
    r1 = "\\n2013(?:[^\\n]|\\n(?!2013))*?"+keyWord1+".*?(?=\n20\d\d-)"
    r2 = "\\n2013(?:[^\\n]|\\n(?!2013))*?"+keyWord2+".*?(?=\n20\d\d-)"
    # r1 = '.{200}(%s|%s|%s|%s|%s|%s|%s)' % (T1,T2,T3,T4,T5,T6,T7)
    
    f = open(vFile, 'r')    
    
    recsvr = None
    dict = {}
    recsvr = f.read()
    reobj = re.compile(r'(?s)%s' % (r1))
    ll1 = reobj.findall(recsvr)
    print ll1[0]

    reobj2 = re.compile(r'(?s)%s' % (r2))
    ll2 = reobj2.findall(recsvr)
 

    for i in ll2:
        reobj_2 = re.compile(r'(?m)^20\d\d-\d\d.*$') 
        ll_2 = reobj_2.findall(i)

        if ll_2[0] != i.strip():
            print i
    # timeList = dict.keys()
    # timeList.sort()


    # for i in range(len(dict)):
    #     print timeList[i]
    #     print dict[timeList[i]]
    #     print "#######################"
            
    f.close()
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

#    parser.add_option("-C", "--Content", dest="contentList",
#                      default=[],action="append",type="string",metavar="ContentList",
#                      help="the ContentList, default is empty")
#    parser.add_option("-a", "--action", dest="vAction",
#                      default='search',action="store",type="string",metavar="optional param",
#                      help="search|match are 2 optional choice, match is the default value")
#    parser.add_option("-i", "--CaseSensitive", dest="vCSdata",
#                      default="False",action="store_true",
#                      help="The option switcher for the case sensitivity,default is false")
#    parser.add_option("-i", "--IP", dest="URL",
#                      default='None',action="store",type="string",metavar="REC/ACVurl",
#                      help="the IP address of REC/ACVurl, default is empty")
#    parser.add_option("-o", "--OptionalAttribute", dest="optionalAttribute",
#                      default='None',action="store_true",metavar="Opt_switcher",
#                      help="the swicther on/off of optional Attr in A9, default is empty")


    (options, args) = parser.parse_args()

    argc = len(args)
    if argc != 0:
        parser.error("incorrect number of arguments")
        print usage
    else:
        if options.vSeID != "Null" and options.vFile != "Null":
            # try:
            result = execute(options.vSeID, options.vFile)

            # except Exception,ex:
            #     print Exception,':',ex

        # elif options.vSeID == "Null":
        #     cmd = """awk '{for(i=1;i<NF+1;i++){if($i~/contentObjectId="/){if(NF>1){print $1$2"::"$i}else{print $1}}}}' %s""" % (options.vFile)
        #     printout = os.popen(cmd).read()
        #     print printout
        else:
            print usage
