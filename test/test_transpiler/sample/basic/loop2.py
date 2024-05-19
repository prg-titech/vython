def loop(c, f):
    if(c > 0):
        f(c)
        loop(c-1,f)
    else:
        return

class A!1:
    def __init__(this):
        this.value = 1
    def fact(this,n):
        this.value = this.value * n

a = A!1()
fact_func = a.fact
loop(10,fact_func)
print(a.value)       
