from datetime import date
def differ_days(p,q):
    #p,q are parameters passed into differdays function
    #p,q represent the dates input as strings
    d_first=date(int(p[0:4]),int(p[5:7]),int(p[8:10]))
    d_next=date(int(q[0:4]),int(q[5:7]),int(q[8:10]))
    print('Today is:',int(p[0:4]),'-',int(p[5:7]),'-',int(p[8:10]))
    print('Day of return is:',int(q[0:4]),'-',int(q[5:7]),'-',int(q[8:10]))
    delta=d_first-d_next      
    print('Difference in expected date and actual date of return:',delta.days)
    return delta.days
