class Node!1:
    pass


class Container!1:
    pass


container = Container!1()
container.item = Node!1()
print(type(container.item))
