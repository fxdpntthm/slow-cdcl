class Model:
    """ 
    Model class that holds literal assignments in levels, just implemented as a list for now
    """
    def __init__(self):
        self.data = []
        
    def add(self, lit):
        self.data.append(lit)

    def add_decide(self,lit):
        self.data.append([lit])
        
    def flat(self):
        return list(map(lambda x: x[0] if type(x) == list else x, self.data))
    
    def set(self):
        return set(self.flat())

    def has(self, lit):
        for literal in self.data:
            if literal == lit or (type(literal) == list and literal[0] == lit):
                return True
        return False
    
    def pop_decide(self):
        cut = -1
        for i in range(len(self.data) - 1, -1):
            if type(self.data[i]) == list:
                cut = i
                break
        
        if cut < 0:
            return 0
        else:
            val = self.data[cut][0]
            self.data = self.data[:cut]
            return val

    def print(self):
        return str(self.data)