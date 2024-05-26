counter = 10
def loop(c, f):
    if(c > 0):
        f(c)
        loop(c-1,f)
    else:
        return

class Printer!1():
    def print(self, n):
        print(n)
        return

printer = Printer!1()
print_func = printer.print
loop(counter, print_func)
