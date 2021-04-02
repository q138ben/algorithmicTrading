"""
Demonstrates streaming feature in OANDA open api
To execute, run the following command:
python streaming.py [options]
To show heartbeat, replace [options] by -b or --displayHeartBeat
"""

import requests
import json

from optparse import OptionParser

def connect_to_stream():

    """
    Environment                 Description 
    fxTrade (Live)              The live (real money) environment 
    fxTrade Practice (Demo)     The demo (simulated money) environment 
    """
    domainDict = { 'live' : 'stream-fxtrade.oanda.com','demo' : 'stream-fxpractice.oanda.com' }

    #domainDict = { 'live' : 'stream-fxtrade.oanda.com','demo' : "api-fxpractice.oanda.com" }
    # Replace the following variables with your personal values 
    environment = "demo" # Replace this 'live' if you wish to connect to the live environment 
    domain = domainDict[environment] 
    access_token = 'bea99ed5c60be2fe88c5b1bc399bef68-6c95453aab4550bae269d49e2d6c7246'
    #account_id = "14446518001"
    account_id = '101-004-14446518-001'
    instruments = "AUD_USD" 

    try:
        s = requests.Session()
        url = "https://" + domain + "/v1/prices"
        headers = {'Authorization' : 'Bearer ' + access_token,
                   # 'X-Accept-Datetime-Format' : 'unix'
                  }
        params = {'instruments' : instruments, 'accountId' : account_id}
        req = requests.Request('GET', url, headers = headers, params = params)
        pre = req.prepare()
        resp = s.send(pre, stream = True, verify = True)
        return resp
    except Exception as e:
        s.close()
        print("Caught exception when connecting to stream\n" + str(e)) 

#def demo(displayHeartbeat):
#    response = connect_to_stream()
#    if response.status_code != 200:
#        print(response.text)
#        return
#    for line in response.iter_lines(1):
#        if line:
#            try:
#                line = line.decode('utf-8')
#                msg = json.loads(line)
#            except Exception as e:
#                print("Caught exception when converting message into json\n" + str(e))
#                return
#
#            if "instrument" in msg or "tick" in msg or displayHeartbeat:
#                print(line)
                

#This actually turned out to be pretty easy, I fixed it by replacing the "demo" function with this:

def demo(displayHeartbeat):
    response = connect_to_stream()
    if response.status_code != 200:
        print (response.text)
        return
    for line in response.iter_lines(1):
        if line:
            try:
                msg = json.loads(line)
            except Exception as e:
                print ("Caught exception when converting message into json\n" + str(e))
                return

            if displayHeartbeat:
                print (line)
            else:
                if msg.has_key("instrument") or msg.has_key("tick"):
                    print (msg["tick"]["ask"] - .001)
                    instrument = msg["tick"]["instrument"]
                    time = msg["tick"]["time"]
                    bid = msg["tick"]["bid"]
                    ask = msg["tick"]["ask"]

def main():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-b", "--displayHeartBeat", dest = "verbose", action = "store_true", 
                        help = "Display HeartBeat in streaming data")
    displayHeartbeat = False

    (options, args) = parser.parse_args()
    if len(args) > 1:
        parser.error("incorrect number of arguments")
    if options.verbose:
        displayHeartbeat = True
    demo(displayHeartbeat)


if __name__ == "__main__":
    main()
