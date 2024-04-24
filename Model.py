class Model:
    """ 
    Model class that holds literal assignments in levels, just implemented as a list for now
    """
    def __init__(self):
        self.data = []
        self.decides = []
        
    def add(self, lit):
        self.data.append(lit)

    def add_decide(self,lit):
        self.data.append([lit])
        self.decides.append(len(self.data) - 1)
        
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
        if not self.has_decide():
            return 0

        decision = self.decides.pop()
        val = self.data[decision][0]
        self.data = self.data[:decision]
        return val

    def has_decide(self):
        return len(self.decides) > 0

    def print(self):
        return str(self.data)