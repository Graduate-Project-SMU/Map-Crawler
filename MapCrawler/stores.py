class storeInfoClass:
    def __init__(self):
        self.name = 0
        self.branch = 0
        self.phoneNum = 0
        self.address = 0

    def setName(self, name):
        self.name = name

    def setBranch(self, branch):
        self.branch = branch

    def setPhoneNum(self, phoneNum):
        self.phoneNum = phoneNum

    def setAddress(self, address):
        self.address = address

    def getName(self):
        return self.name

    def getBranch(self):
        return self.branch

    def getPhoneNum(self):
        return self.phoneNum

    def getAddress(self):
        return self.address