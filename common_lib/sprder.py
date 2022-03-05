from fileinput import filename
from lib import Request, FileAction
from json import loads

rq = Request(url="http://www.pangubpm.com/pagedoc1.html", method="POST", data={
    "page": 1,
    "length": 400
})

res = rq.start()
rst = loads(res)
s1 = []
s2 = []
for i in range(len(rst["list"])):
    ss = rst["list"][i]
    name = ss["name"]
    s1.append(" -> ".join([str(i+1), name]))
    if "CMMN" in name or "cmmn" in name or "案例" in name:
        s2.append(" -> ".join([str(i+1), name]))

    ss1 = "\n".join(s1)
    ss2 = "\n".join(s2)

    sss = ss1 + "\n\n" + ss2

    FileAction(filename="./__output__/rst").write(sss)
    
# for page in range(1, 40):
#     rq.data = {
#         "page": page,
#         "length": 10
#     }
