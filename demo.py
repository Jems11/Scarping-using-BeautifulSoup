import re
string = "(This) i's? what?!"
print(re.sub('\W+',' ',string))