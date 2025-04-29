import sqlite3
import random
import csv
from Parse import runner

DB=sqlite3.connect("Covid.db",check_same_thread=False)
cur=DB.cursor()

def train():
    cur.execute("DROP TABLE Responses")
    cmd="""CREATE TABLE Responses(
KW1 varCHAR(100),
KW2 varCHAR(100),
KW3 varCHAR(100),
RS varCHAR(9000)
)"""
    cur.execute(cmd)
    keys,ans=training()
    for i in range(len(keys)-1):
        print(i,keys[i])
        if i==70:
            break
        cmd="Select * from Responses"
        if len(keys[i])==1:
            cur.execute("Insert into Responses(KW1,KW2,KW3,RS) Values (?,?,?,?)",(keys[i][0],keys[i][0],keys[i][0],ans[i][0]))        
        elif len(keys[i])==2:
            cur.execute("Insert into Responses(KW1,KW2,KW3,RS) Values (?,?,?,?)",(keys[i][0],keys[i][1],keys[i][0],ans[i][0]))
        elif len(keys[i])>=3:
            cur.execute("Insert into Responses(KW1,KW2,KW3,RS) Values (?,?,?,?)",(keys[i][0],keys[i][1],keys[i][2],ans[i][0]))
    DB.commit()

def training():
    question=runner()[0]
    answer=runner()[1]
    num="break"
    word=[]
    words=[]
    for i in question:
        if type(i)==list:
            for j in i:
                h=j.rstrip("?") 
                words.append(h)
        else:
            h=i.rstrip("?") 
            words.append(h)
        words.append(num)
    for i in words:
        w=i.split(" ")
        word.extend(w)
    sentence=[[]]
    hit=False
    cov=False
    a=0
    ignore=["the","it","is","can","about","are","for","from","does","did","i","was","were","am","be","has","have","had","do","will","shall","could","would","may","might","must","you","to","your","a","on","my","if","get","in","as","takes","take","like","with"]
    covids=["covid","covid-19","covid-","19","covid19","corona","coronavirus","virus"]
    questions=["what","where","when","why","how","who","which"]
    for i in word:
        hit=False
        if i=="break":
            sentence.append([])
            a+=1
            continue
        elif i=="":
            hit=True
        elif(i.lower() in ignore):
            hit=True
        elif(i.lower() in questions):
            hit=True
        elif(i.lower() in covids):
            hit=True
        elif i.lower() in sentence[a]:
            hit=True
        if hit==True:
            if cov==False:
                sentence[a].append("covid")
                cov=True
            continue
        else:
            sentence[a].append(i.lower())
            pass   
        pass
    for i in range(len(answer)):
        print(i,"Keyword:",sentence[i])
        pass
    return sentence,answer

def keyword(query):
    check=query.split(" ")
    word=[]
    words=[]
    for i in check:
        h=i.rstrip("?") 
        words.append(h)
    print(*words,sep="\n      ")
    for i in words:
        w=i.split(" ")
        word.extend(w)
    sentence=[[]]
    hit=False
    cov=False
    a=0
    ignore=["it","is","can","about","are","for","from","does","did","i","was","were","am","be","has","have","had","do","will","shall","could","would","may","might","must","you","to","your","a","on","my","if","get","in","as","takes","take","like","with"]
    covids=["covid","covid-19","covid-","19","covid19","corona","coronavirus","virus"]
    questions=[]#["what","where","when","why","how","who","which"]
    for i in word:
        hit=False
        if i=="break":
            sentence.append([])
            a+=1
            continue
        elif i=="":
            hit=True
        elif( i.lower() in ignore):
            hit=True
        elif(i.lower() in questions):
            hit=True
            cov=False
        elif(i.lower() in covids):
            hit=True
        elif i.lower() in sentence[a]:
            hit=True
        if hit==True:
            if cov==False:
                sentence[a].append("covid")
                cov=True
            continue
        else:
            sentence[a].append(i.lower())
    return sentence                 

def respond(query):
    keywords=keyword(query)
    user=query
    if query[len(query)-1]=="?":
        user=query.rstrip("?")
    word=user.split(" ")
    words=[i.lower() for i in word]
    responses={"all":"sorry"}
    toadd=0
    for i in range(len(keywords[0])):    
            current=keywords[0][i]
            cur.execute(f"select RS from Responses where KW1='{current.lower()}'")
            toadd=cur.fetchall()
            if (len(toadd)>0):
                responses[current]=toadd[0][0]
            cur.execute(f"select RS from Responses where KW2='{current.lower()}'")
            toadd=cur.fetchall()
            if (len(toadd)>0):
                responses[current]=toadd[0][0]
            cur.execute(f"select RS from Responses where KW3='{current.lower()}'")
            toadd=cur.fetchall()
            if (len(toadd)>0):
                responses[current]=(toadd)[0][0]
    dict_keys=list(responses.keys())
    answer=list(responses.values())
    if len(answer)>2:
        while ("covid" in dict_keys):
            index=dict_keys.index("covid")
            dict_keys.pop(index)
            answer.pop(index)
    else:
        pass
    best={}
    bestans=[]
    if len(answer)>1:
        answer.remove("sorry")
    for i in answer:
        if i not in best.keys():
            best[i]=answer.count(i)
    highcount=0
    high_key=[]
    for i in best.keys():
        if best[i]>highcount:
            highcount=best[i]
            high_key=i
    bestans=high_key
    print(bestans)
    return bestans
