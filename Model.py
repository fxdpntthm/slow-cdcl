class Model:
    """ 
    Model class that holds literal assignments in levels, just implemented as a list for now
    """
    def __init__(self):
        self.__data = []
        self.__decides = []
        
    def add(self, lit):
        self.__data.append(lit)
    
    def add_all(self, lits):
        self.__data.extend(lits)

    def add_decide(self,lit):
        self.__data.append(lit)
        self.__decides.append(len(self.__data) - 1)
        
    def get_data(self):
        return self.__data

    def get_decides(self):
        return self.__decides
    
    def set(self):
        return set(self.__data)

    def has(self, lit):
        for literal in self.__data:
            if literal == lit:
                return True
        return False
    
    def pop_decide(self):
        if not self.has_decide():
            return 0

        decision = self.__decides.pop()
        val = self.__data[decision]
        self.__data = self.__data[:decision]
        return val

    def has_decide(self):
        return len(self.__decides) > 0

    def print(self):
        return str(self.__data)