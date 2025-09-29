import http.client
import json
import time
import sys

API_Token = sys.argv[1]
zone_ID = sys.argv[2]
domain = sys.argv[3]
sleepTime = int(sys.argv[4])
IPv4 = sys.argv[5].lower() == 'true'
IPv6 = sys.argv[6].lower() == 'true'

if not IPv4 and not IPv6:
    print("ERROR: No IP version selected (IPv4 or IPv6) - exiting")
    exit()

connCloudflare = http.client.HTTPSConnection("api.cloudflare.com")
headers = {
    'authorization': f"Bearer {API_Token}",
    'content-type': "application/json"
}

def get_Public_IP(IPv6Mode=False):
    if IPv6Mode:
        conn = http.client.HTTPSConnection("api6.ipify.org")
    else:
        conn = http.client.HTTPSConnection("api.ipify.org")
    try:
        conn.request("GET","/")
        res = conn.getresponse()
        return res.read().decode("utf-8")
    except Exception as e:
        print(f"ERROR: Failed to get public IP - Are you sure you are on IPv6? {e}")
        print(f"Exiting - error: {e}")
        exit()
    
def get_DNS_Record_IP(IPv6Mode=False):
    print("INFO: Retrieving DNS records from Cloudlare")
    connCloudflare.request("GET", f"/client/v4/zones/{zone_ID}/dns_records", headers=headers)
    res = connCloudflare.getresponse()
    response = json.load(res)
    print(response)
    #find the DNS record
    for res in response["result"]:
        if res["name"] == domain:
            if IPv6Mode and res["type"] == "AAAA":
                return res["id"], res["content"]
            if (not IPv6Mode) and res["type"] == "A":
                return res["id"], res["content"]
    return None, None

def update_DNS_Record_IP(DNS_record_ID, public_IP,IPv6Mode=False):
    print("INFO: Updating DNS record")
    if IPv6Mode:
        payload = f"{{\"content\":\"{public_IP}\",\"type\":\"AAAA\"}}"
    else:
        payload = f"{{\"content\":\"{public_IP}\",\"type\":\"A\"}}"
    connCloudflare.request("PATCH", f"/client/v4/zones/{zone_ID}/dns_records/{DNS_record_ID}", payload, headers)
    res = connCloudflare.getresponse()
    response = json.load(res)
    print(response)

old_Public_IPv4 = None
old_Public_IPv6 = None
while True:
    if IPv4:
        public_IPv4 =  get_Public_IP(IPv6Mode=False)
        if old_Public_IPv4 == public_IPv4:
            print("INFO: Publc IPv4 address has not changed!")
        else:
            #Get list of DNS records, to find the DNS record ID
            DNS_record_ID, DNS_Content = get_DNS_Record_IP(IPv6Mode=False)
            if not DNS_record_ID or not DNS_Content:
                print("ERROR: DNS A ecord not found! Check config file and/or Cloudlare domain configuration")
                exit()
            #Update the DNS Record?
            if DNS_Content == public_IPv4:
                print("INFO: DNS A Record matches already your public IPv4 - No update needed")
            else:
                update_DNS_Record_IP(DNS_record_ID, public_IPv4,IPv6Mode=False)
            old_Public_IPv4 = public_IPv4
    if IPv6:
        public_IPv6 =  get_Public_IP(IPv6Mode=True)
        if old_Public_IPv6 == public_IPv6:
            print("INFO: Publc IPv6 address has not changed!")
        else:
            #Get list of DNS records, to find the DNS record ID
            DNS_record_ID, DNS_Content = get_DNS_Record_IP(IPv6Mode=True)
            if not DNS_record_ID or not DNS_Content:
                print("ERROR: DNS AAAA Record not found! Check config file and/or Cloudlare domain configuration")
                exit()
            #Update the DNS Record?
            if DNS_Content == public_IPv6:
                print("INFO: DNS AAAA Record matches already your public IPv6 - No update needed")
            else:
                update_DNS_Record_IP(DNS_record_ID, public_IPv6,IPv6Mode=True)
            old_Public_IPv6 = public_IPv6
    time.sleep(sleepTime)
    
