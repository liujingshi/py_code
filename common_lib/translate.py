from lib import NiuTrans, FileAction
from json import loads

niuTrans = NiuTrans(api=NiuTrans.TextApi)

rst = niuTrans.start({
    "src_text": FileAction(filename="./__input__/trans").read()
})

result = loads(rst)

FileAction(filename="./__output__/trans").write(result["tgt_text"])
