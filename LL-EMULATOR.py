from tkinter import *
import re
from LL import *
top = Tk()
top.title("LL-EMULATOR")
top.geometry('900x830')
label = Label(top, text='LL-EMULATOR',font='Algerian -48 bold', fg="brown")
label.pack()

def read():
    gr={}
    try:
        term=t.get(1.0,END).strip().split(",")
        print(term)
        nterm=n.get(1.0,END).strip().split(",")
        print(nterm)
        G=g.get(1.0,END).strip().split("\n")
        for i in range(len(G)):
            t1=re.search("\s*(\w)\s*-->\s*([\^]|[^|^\s]+)\s*",G[i])
            l=[]
            l.append(t1.group(2))
            gr[t1.group(1)]=l
            m=re.findall("\|\s*([\^]|[^|^\s]+)\s*",G[i])
            gr[t1.group(1)].extend(m)
        print(gr)
        return gr,term,nterm
    except:
        print("INVALID INPUT")

def read1(event):
    try:
        rd=read()
        f=first(rd[0],rd[1],rd[2])
        fst=Tk()
        fst.title("FIRST SET")
        sz=str((len(rd[1])+2)*70)+"x"+str((len(rd[2])+1)*70)
        fst.geometry(sz)
        ys=Scrollbar(fst)
        opt=Text(fst, wrap=NONE, fg="blue")
        ys.pack(side=RIGHT, fill=Y)
        opt.config(yscrollcommand=ys.set)
        opt.pack(side=LEFT, fill=Y)
        ys.config(command=opt.yview)
        opt.config(state=NORMAL, font='Arial -24')
        opt.delete(0.0,END)
        opt.insert(END,"\n\n")
        for i in rd[2]:
            opt.insert(END,"      FIRST("+i+")   =   ")
            f1=" , ".join(f[i])
            opt.insert(END,"{  "+f1+"  }")
            opt.insert(END,"\n\n")
        opt.config(state=DISABLED)
    except:
        print("INVALID INPUT")

def read2(event):
    try:
        rd=read()
        f=follow(rd[0],rd[1],rd[2])
        flw=Tk()
        flw.title("FOLLOW SET")
        sz=str((len(rd[1])+2)*70)+"x"+str((len(rd[2])+1)*70)
        flw.geometry(sz)
        ys=Scrollbar(flw)
        opt=Text(flw, wrap=NONE, fg="blue")
        ys.pack(side=RIGHT, fill=Y)
        opt.config(yscrollcommand=ys.set)
        opt.pack(side=LEFT, fill=Y)
        ys.config(command=opt.yview)
        opt.config(state=NORMAL, font='Arial -24')
        opt.delete(0.0,END)
        opt.insert(END,"\n\n")
        for i in rd[2]:
            opt.insert(END,"      FOLLOW("+i+")   =   ")
            f1=" , ".join(f[i])
            opt.insert(END,"{  "+f1+"  }")
            opt.insert(END,"\n\n")
        opt.config(state=DISABLED)
    except:
        print("INVALID INPUT")

def display_table(PPT,con,inpt,non_ter,ter):
        lltab=Tk()
        lltab.title("LL(1)-TABLE")
        sz=str((len(inpt)+1)*230)+"x"+str((len(non_ter)+1)*88)
        lltab.geometry(sz)
        ys=Scrollbar(lltab)
        xs=Scrollbar(lltab, orient=HORIZONTAL)
        opt=Text(lltab, wrap=NONE, width=str((len(inpt)+1)*20), height=str((len(non_ter)+1)*2+2), fg="blue")
        ys.pack(side=RIGHT, fill=Y)
        xs.pack(side=BOTTOM, fill=X)
        opt.config(yscrollcommand=ys.set, xscrollcommand=xs.set)
        opt.pack(side=LEFT, fill=Y)
        ys.config(command=opt.yview)
        xs.config(command=opt.xview)
        opt.config(state=NORMAL, font='Arial -24')
        opt.delete(0.0,END)
        opt.insert(END,"="*16*(len(inpt)+1)+"\n")
        opt.insert(END,"   NON_TERMINAL\t\t\t"+inpt[0])
        for i in inpt[1:]:
            opt.insert(END,"\t\t"+i)
        opt.insert(END,"\n")
        opt.insert(END,"="*16*(len(inpt)+1)+"\n")
        k=0
        for i in non_ter:
            opt.insert(END,"\t"+i+"\t\t")
            k=non_ter.index(i)
            for j in PPT[k]:
                if j=="error" or j=="conflict":
                    opt.insert(END,j+"    \t\t")
                else:
                    if j[1]=="^":
                        opt.insert(END,j[0]+"-->lambda"+"    \t\t")
                    else:
                        opt.insert(END,j[0]+"-->"+j[1]+"    \t\t")
            opt.insert(END,"\n")
            k+=1
            if k<len(non_ter):
                opt.insert(END,"-"*28*(len(inpt)+1)+"\n")
        opt.insert(END,"="*16*(len(inpt)+1)+"\n")
        if con:
            opt.config(fg="red")
            opt.insert(END,"\n     "+"="*7*(len(ter)+1)+"<:: TABLE HAS CONFLICT ::>"+"="*7*(len(ter)+1)+"\n")
        opt.config(state=DISABLED)

def read3(event):
    try:
        rd=read()
        PPT,con,inpt=table(rd[0],rd[1],rd[2])
        display_table(PPT,con,inpt,rd[2],rd[1])
    except:
        print("INVALID INPUT")
    
def parse(PPT,G,ter,non_ter,Input,start=0):
    First=first(G,ter,non_ter)
    Follow=follow(G,ter,non_ter,start)
    inpt=ter[:]
    inpt.append('$')
    if start==0:
        start=non_ter[0]
    stack=start+"$"
    Input=Input+"$"
    matched=""
    action=""
    ip=0
    error=False
    x=stack[0]
    prse=Tk()
    prse.geometry("1050x850")
    prse.title("STRING PARSING")
    ys=Scrollbar(prse)
    xs=Scrollbar(prse, orient=HORIZONTAL)
    opt=Text(prse, wrap=NONE,fg="blue")
    ys.pack(side=RIGHT, fill=Y)
    xs.pack(side=BOTTOM, fill=X)
    opt.config(yscrollcommand=ys.set, xscrollcommand=xs.set)
    opt.pack(side=LEFT, fill=Y)
    ys.config(command=opt.yview)
    xs.config(command=opt.xview)
    opt.config(state=NORMAL, font='Arial -24')
    opt.delete(0.0,END)
    opt.insert(END,"\n    ","="*70+"\n")
    opt.insert(END,"\tMATCHED\t\tSTACK\t\tINPUT\t\tACTION\n")
    opt.insert(END,"    "+"="*70+"\n")
    opt.insert(END,"\t\t\t"+stack+"\t\t"+Input+"\n")
    while x!='$':
        opt.insert(END,"    "+"-"*122+"\n")
        a=Input[ip]
        if a not in inpt:
            action="Error: Input symbol doesn't belongs to Grammar symbol"
            error=True
            break
        if x==Input[ip]:
            stack=stack[1:]
            matched=matched+Input[ip]
            ip=ip+1
            action="match "+x
        elif x in ter:
            error=True
            action="Error"
        elif PPT[non_ter.index(x)][inpt.index(a)]=="error" or PPT[non_ter.index(x)][inpt.index(a)]=="conflict":
            error=True
            action="Error"
        else:
            prod=PPT[non_ter.index(x)][inpt.index(a)]
            l,r=prod
            stack=stack[1:]
            if r!="^":
                stack=r+stack
            if r=="^":
                action="output "+l+"-->"+"lambda"
            else:
                action="output "+l+"-->"+r
        x=stack[0]
        opt.insert(END,"\t"+matched+"\t\t"+stack+"\t\t"+Input[ip:]+"\t\t"+action+"\n")
        if error:
            break
    opt.insert(END,"    "+"="*70+"\n")
    if error:
        opt.config(fg="red")
        opt.insert(END,"\n\t         \"THE  GIVEN  STRING  DOES  NOT  BELONGS  TO  LANGUAGE\"\n")
    else:
        opt.insert(END,"\n\t\t\t\"STRING  PARSED  SUCCESSFULLY\"\n")
    opt.config(state=DISABLED)
    return (not error)

def readstr(event):
    try:
        rd=read()
        PPT,con,inpt=table(rd[0],rd[1],rd[2])
        strng=s.get(1.0,END).strip()
        parse(PPT,rd[0],rd[1],rd[2],strng)
    except:
        print("INVALID INPUT")


label1 = Label(top, text='GRAMMAR:',font='Arial -15 bold', fg="brown")
label1.place(relx = 0.08, rely = 0.15)
label2 = Label(top, text='TERMINALS:',font='Arial -15 bold', fg="brown")
label2.place(relx = 0.08, rely = 0.53)
label3 = Label(top, text='NON-TERMINALS:',font='Arial -15 bold', fg="brown")
label3.place(relx = 0.08, rely = 0.652)
label4 = Label(top, text='STRING:',font='Arial -15 bold', fg="brown")
label4.place(relx = 0.08, rely = 0.88)

g = Text(width="40", height="10",font='Arial -24')
g.place(relx = 0.23, rely = 0.15)
t = Text(width="40", height="2",font='Arial -24')
t.place(relx = 0.23, rely = 0.53)
n = Text(width="40", height="2",font='Arial -24')
n.place(relx = 0.23, rely = 0.65)
s = Text(width="29", height="2",font='Arial -24')
s.place(relx = 0.23, rely = 0.85)



button1 = Button(top, text='  FIRST SET  ',font='Arial -17 bold', fg="brown")
button1.bind('<Button-1>',read1)
button2 = Button(top, text='FOLLOW SET',font='Arial -17 bold', fg="brown")
button2.bind('<Button-1>',read2)
button3 = Button(top, text='PARSING TABLE',font='Arial -17 bold', fg="brown")
button3.bind('<Button-1>',read3)
button4 = Button(top, text='PARSE STRING',font='Arial -17 bold', fg="brown")
button4.bind('<Button-1>',readstr)

button1.place(relx = 0.23, rely = 0.76)
button2.place(relx = 0.46, rely = 0.76)
button3.place(relx = 0.68, rely = 0.76)
button4.place(relx = 0.69, rely = 0.86)

g.insert(END,"E-->TA\n")
g.insert(END,"A-->+TA|^\n")
g.insert(END,"T-->FB\n")
g.insert(END,"B-->*FB|^\n")
g.insert(END,"F-->(E)|a")

t.insert(END,"a,+,*,(,)")

n.insert(END,"E,A,T,B,F")

s.insert(END,"a+a*a")

mainloop()

