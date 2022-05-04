from threading import Thread
from lib import Request, JsonAction, FileAction

heads = []
reqs = [0, 0]

def reqt(i):
    req = Request(url="https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{0}/JSON/".format(i))
    rst = req.start()
    rstObj = JsonAction(rst).toObj()
    for hot in rstObj["Record"]["Section"]:
        h = hot["TOCHeading"]
        if not h in heads:
            heads.append(h)
    reqs[0] += 1

for i in range(1, 10001):
    print(reqs[1], "/10000")
    for j in range(5):
        reqs[1] += 1
        Thread(target=reqt, args=(reqs[1], )).start()

    if reqs[1] > 10000:
        break

    while reqs[0] < 5:
        pass

    reqs[0] = 0

    FileAction("./__output__/TOCHeading.json").write(JsonAction(heads).toStr())

