class Node!1:
    def __init__(self,value,next,end):
        self.value = value
        self.next = next
        self.end = end

    def is_end(self):
        return self.end
    
    def get_end_node(self):
        if self.is_end():
            return self
        
        if self.next.is_end():
            return self
        else:
            return self.next.get_end_node()
    
    def print_list(self):
        if self.is_end():
            return
        print(self.value)
        self.next.print_list()
        return

def under_pivot_list(head,pivot):
    if(head.is_end()):
        return Node!1(-1,1,True)
    
    next = under_pivot_list(head.next,pivot)
    if(head.value < pivot):
        return Node!1(head.value,next,False)
    else:
        return next

def upper_pivot_list(head,pivot):
    if(head.is_end()):
        return Node!1(-1,1,True)
    
    next = upper_pivot_list(head.next,pivot)
    if(head.value > pivot):
        return Node!1(head.value,next,False)
    else:
        return next

def merge(under,head,upper):
    head.next = upper

    if under.is_end():
        return head
    else:
        under.get_end_node().next = head
        return under

def sort(head):
    if(head.is_end()):
        return head
    
    pivot = head.value
    under = under_pivot_list(head.next,pivot)
    upper = upper_pivot_list(head.next,pivot)

    sorted_under = sort(under)
    sorted_upper = sort(upper)

    result = merge(sorted_under,head,sorted_upper)

    return result

end = Node!1(100,1,True)
a1 = Node!1(1,end,False)
a2 = Node!1(3,a1,False)
a3 = Node!1(5,a2,False)
a4 = Node!1(0,a3,False)
a5 = Node!1(4,a4,False)

head = a5
a = sort(head)
a.print_list()
