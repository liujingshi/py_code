from asyncore import read
from lib import FileAction, JsonAction
import re

text = FileAction("./__input__/re.svg").read()
text = re.sub(r't="[0-9a-zA-Z]+" ', "", text)
text = re.sub(r'class="[0-9a-zA-Z]+" ', "", text)
text = re.sub(r'fill="[0-9a-zA-Z#]+" ', "", text)
text = re.sub(r'p-id="[0-9a-zA-Z]+"', "fill=\"#000000\"", text)

FileAction("./__output__/reok.svg").write(text)
