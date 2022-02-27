import sqlite3
fname = 'statement.txt'
dbname = 'bankrec.sqlite'
conn=sqlite3.connect('bankrec.sqlite')
cur = conn.cursor()
cur.executescript('''
DROP TABLE IF EXISTS Record;
CREATE TABLE IF NOT EXISTS Record(
    DATE TEXT,
    PARTICULARS TEXT,
    CHEQUE_NO INTEGER,
    AMOUNT REAL,
    TYPE TEXT,
    BALANCE REAL )'''
)
handle = open(fname)
prevbal = None
for line in handle:
    line = line.strip()
    ch = line[2:4]
    if ch == '-0':
        lst = line.split()
        l = len(lst)
        i=0
        fl = 0
        try:
            chqno = lst[l-3]
            chqno = int(chqno)
            fl=1
        except:
            fl=0
            chqno = None
        for items in lst:
            if i==0:
                date = lst[0]
            elif i==1:
                part = lst[1]
            elif i == l-1:
                ba = lst[l-1]
            elif i == l-2:
                amts = lst[l-2]
            elif i == l-3:
                if fl==0:
                    part = part + ' ' + lst[l-3]
            else:
                part = part + ' ' + lst[i]
            i= i+1
        ba = ba[:-2]
        a = ba
        lst1 = a.split(',')
        b = None
        for v in lst1:
            if b==None:
                b=v
            else:
                b = b + v
        bal = float(b)
        b = None
        a = amts
        lst1 = a.split(',')
        for v in lst1:
            if b==None:
                b=v
            else:
                b = b + v
        amt = float(b)
        typ = 'Credit'
        if prevbal==None:
            prevbal = bal
        else:
            if prevbal>bal:
                typ = 'Debit'
            else:
                typ = 'Credit'
        prevbal = bal
        print(date, part, chqno, amt, typ, bal)
        if chqno == None:
            cur.execute('''INSERT INTO Record(DATE, PARTICULARS, AMOUNT, TYPE, BALANCE)
            VALUES (?, ?, ?, ?, ?)''', (date, part, amt, typ, bal))
        else:
            cur.execute('''INSERT INTO Record(DATE, PARTICULARS, CHEQUE_NO, AMOUNT, TYPE, BALANCE)
            VALUES (?, ?, ?, ?, ?, ?)''', (date, part, chqno, amt, typ, bal))
        conn.commit()