import json


class Node:
    def __init__(self, name, dir='data', next=None):
        file = open(dir + '/' + name + '.json', 'r')
        self.name = name
        self.next = next
        self.data = json.load(file)
        file.close()
        pass
    pass


class LRU:
    def __init__(self, nmax=20):
        self.head = None
        self.foot = None
        self.nmax = nmax
        self.nums = 0
        pass

    def find(self, name):
        if self.head()
        while(self.foot.next):
            self

    def append(self, node):
        # 队列已满
        if self.nmax == self.nums:



        return node

    pass



if __name__ == '__main__':

