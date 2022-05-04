import pubchempy as pcp
from lib import FileAction, JsonAction

c = pcp.Compound.from_cid(2244)

FileAction("./__output__/compound.json").write(JsonAction(c.to_dict()).toStr())

