#!/usr/bin/python3 -OO
from zlib import compressobj,decompressobj
from json import loads,dumps
from ast import literal_eval
from base64 import encodebytes
from sys import argv,stdout
try:
	import readline
except:
	stdout.write("warning: failed to import readline, moving cursor with arrow keys won't work\n")
def jinput(p):
	p=input(p)
	return literal_eval(p) if p[:1]=="\"" else p
def chelp():
	stdout.write("""usage: python3 pbptricks.py [FILE]
do stuff with pbp (proboards plugin) file

commands:
help, ?  print this help
exit, q  exit
o        open file
ro       reopen current file
c        current file info
sp       save pbp
sj       save json
s        save to current file
+e       make plugin editable
-e       make plugin not editable
aif      add image from file
ail      add image from link (url)

if input starts with `"` it's python3 string literal (`"\\x2Be"` is same as `+e`)
""")
def askyn(p):
	while True:
		inp=jinput(p)
		if inp in ("Y","y"):
			return True
		if inp in ("N","n"):
			return False
		stdout.write("bad input\n")
def cexit():
	if objunchanged or askyn("unsaved changes, exit? [y/n] "):
		stdout.write("exiting\n")
		raise SystemExit
	stdout.write("not exiting\n")
def openw(path):
	try:
		return open(path,"xb")
	except FileExistsError:
		if askyn("file exists, overwrite? [y/n] "):
			return open(path,"wb")
def setfile(newpath):
	global obj,currpath,currispbp,objunchanged
	with open(newpath,"rb") as f:
		f=f.read()
	ispbp=f[:6]==b"PBP1>>"
	if ispbp:
		stdout.write("loading file as pbp\n")
		d=decompressobj(31)
		obj=loads(str(d.decompress(f[6:])+d.flush(),"utf-8"))
		del d
	else:
		stdout.write("loading file as json\n")
		obj=loads(str(f,"utf-8"))
	currpath=newpath
	currispbp=ispbp
	objunchanged=True
def co():
	if objunchanged or askyn("unsaved changes, open? [y/n] "):
		newpath=jinput("file: ")
		setfile(newpath)
		stdout.write("current file changed\n")
def cro():
	if objunchanged or askyn("unsaved changes, reopen? [y/n] "):
		setfile(currpath)
def cc():
	stdout.write("current file: %s\ncurrent type: %s\n"%(
		currpath,
		"pbp" if currispbp else "json"
	))
def savepbp(f):
	with f:
		c=compressobj(9,8,31,9,0)
		f.write(b"PBP1>>%b%b"%(
			c.compress(bytes(dumps(obj,ensure_ascii=False,separators=",:"),"utf-8")),
			c.flush()
		))
	stdout.write("saved as pbp\n")
def savejson(f):
	with f:
		f.write(bytes(dumps(obj,ensure_ascii=False,indent="\t",separators=",:"),"utf-8"))
	stdout.write("saved as json\n")
def askset(path,ispbp):
	global currpath,currispbp,objunchanged
	if askyn("set current file? [y/n] "):
		currpath=path
		currispbp=ispbp
		objunchanged=True
		stdout.write("current file changed\n")
def csp():
	path=jinput("file: ")
	f=openw(path)
	if f:
		savepbp(f)
		askset(path,True)
def csj():
	path=jinput("file: ")
	f=openw(path)
	if f:
		savejson(f)
		askset(path,False)
def cs():
	global objunchanged
	(savepbp if currispbp else savejson)(open(currpath,"wb"))
	objunchanged=True
def cpe():
	global objunchanged
	obj["editable"]=1
	objunchanged=False
	stdout.write("set plugin editable\n")
def cme():
	global objunchanged
	obj["editable"]=0
	objunchanged=False
	stdout.write("set plugin not editable\n")
isvalidnamechar=frozenset("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz").__contains__
def caif():
	global objunchanged
	name=jinput("name: ")
	if not name:
		stdout.write("name is empty, image not added\n")
		return
	if False in map(isvalidnamechar,name):
		stdout.write("name contains char that isn't [0-9A-Z_a-z], image not added\n")
		return
	url=jinput("file name (not path): ")
	with open(jinput("file: "),"rb") as f:
		f=f.read()
	if not f:
		stdout.write("empty file, image not added\n")
		return
	obj["images"].append({
		"name":name,
		"storage_file":str(encodebytes(f),"ascii"),
		"url":url
	})
	objunchanged=False
	stdout.write("image added\n")
def cail():
	global objunchanged
	name=jinput("name: ")
	if not name:
		stdout.write("name is empty, image not added\n")
		return
	if False in map(isvalidnamechar,name):
		stdout.write("name contains char that isn't [0-9A-Z_a-z], image not added\n")
		return
	url=jinput("url: ")
	obj["images"].append({
		"name":name,
		"storage_file":"",
		"url":url
	})
	objunchanged=False
	stdout.write("image added\n")
cmds={
	"help":chelp,
	"?":chelp,
	"exit":cexit,
	"q":cexit,
	"o":co,
	"ro":cro,
	"c":cc,
	"sp":csp,
	"sj":csj,
	"s":cs,
	"+e":cpe,
	"-e":cme,
	"aif":caif,
	"ail":cail
}
stdout.write("pbptricks v1\n")
if len(argv)==2:
	setfile(argv[1])
elif len(argv)<2:
	setfile(jinput("file can be pbp or json\nfile: "))
else:
	stdout.write("only 0 or 1 arguments supported, got %d\n"%(len(argv)-1))
	exit(1)
stdout.write("try `help` or `?` command\n")
while True:
	try:
		cmd=jinput("cmd: ")
	except KeyboardInterrupt:
		stdout.write("\nuse `exit` or `q` command to exit\n")
		continue
	except EOFError:
		stdout.write("\nEOFError, exiting\n")
		raise SystemExit
	if not cmd:
		continue
	try:
		cmd=cmds[cmd]
	except KeyError:
		stdout.write("bad command: %s\n"%cmd)
		continue
	try:
		cmd()
	except (Exception,KeyboardInterrupt) as exc:
		stdout.write("\n%r\n"%exc)