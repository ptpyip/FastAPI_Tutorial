
class SuperClass:
    def __init__(self) -> None:
        print("init SuperClass")
        self.sub = SubClass(id=1)
        pass
    
class SubClass(SuperClass):
    def __init__(self, id) -> None:
        print("init SubClass")
        self.id = id
        pass
    
# super_class = SuperClass()
# print(super_class.sub.id)


if __name__ == "__main__":
    a = {"a": "a"}
    b = {'b': "b"}
    print(a|b)
        