import csv
csv.register_dialect("plus",delimiter=",",skipinitialspace=True)
def runner():
	ques=questions()
	ans=answers()
	return ques,ans
def questions():
    datum=[[]]
    num=0
    a=1
    with open("Questions.txt","r") as rf:
        data=csv.reader(rf,dialect="plus")
        for i in data:
            if i[0]=="+":
                datum.append([])
                num+=1
                continue
            datum[num].append(i[0])
    return datum
def answers():
    a=1
    datum=[[]]
    num=0
    last=0
    csv.register_dialect("s",delimiter="+",skipinitialspace=True)
    with open("Answers.txt","r",encoding="utf-8") as rf:
        data=csv.reader(rf,dialect="plus")
        for i in data:
            if i[0]=="+":
                last=0
                datum.append([])
                num+=1
                continue
            datum[num].append("".join([str(x)+" " for x in i]))
            if last==0:
                a+=1
                last=1
    return datum
