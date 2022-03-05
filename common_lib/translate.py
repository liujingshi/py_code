from lib import NiuTrans, FileAction
from json import loads

niuTrans = NiuTrans(api=NiuTrans.TextApi)

rst = niuTrans.start({
    "src_text": FileAction(filename="./input/trans").read()
})

result = loads(rst)

FileAction(filename="./output/trans").write(result["tgt_text"])
