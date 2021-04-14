with open("../needCrawl/careerbuilder.txt", 'r') as f:
    data = f.read()

data = data.split("\n")[:-1]
print(len(data))
data = set(data)
print(len(data))