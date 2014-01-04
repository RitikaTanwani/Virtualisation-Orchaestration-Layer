import json
import os

from uuid import uuid4
machine_list = []
Desc = {}
def create_machines(filename):
	mf = open(filename)
	for line in mf.readlines():
		line = line[:-1]
		if line:
			machines = line.split("@")
			machine_list.append(machines + [str(uuid4())])

#[[user,ip,path][user,ip,path][user,ip,path]]
img_list = []
List_Images = []
def create_images(filename):	
	imgf = open(filename)
	cnt=1
	for line in imgf.readlines():
		line = line[:-1]
		if line:
			img1 = line.split("@")
			img2 = img1[1].split(":")
			img = []
			img.append(img1[0])
			img.append(img2[0])
			img.append(img2[1])
			img_list.append(img)
			img = []
			img.append(cnt)
			img.append(img2[1].split('/')[-1])
			List_Images.append(img)
			cnt=cnt+1
			
#	print img_list
def CreateTypes(Filename):
	global Desc
        vMDescFile=open(Filename)
        vMLines=vMDescFile.readlines()
	vMDesc=unicode(''.join(  map(lambda lin: lin.strip(),vMLines) )  )
	Desc=json.loads(vMDesc)
#	print Desc['types']			

def make_path(user,ip):
	path = 'remote+ssh://' + user + '@' + ip + '/'
	return path

def scp_img_path(img_id):
	user = img_list[img_id-1][0]
	ip = img_list[img_id-1][1]
	path = img_list[img_id-1][2]
	os.system("scp "+user+"@"+ip+":"+path+" ~/" + str(img_id) + ".img 2> /dev/null")
