from flask import Flask, jsonify
from flask import request
import json
from uuid import uuid4
import sys
from flask import make_response
import CreateVM
import re,os,xml
import simplejson as json
import libvirt
machine_list=[]
image_list=[]
remote_ip=[]
info=[]
remoteconns=[]
types={}
def pout(x):
    sys.stdout.write(str(x))
def perr(x):
    sys.stderr.write(str(x))
app = Flask(__name__)

@app.route("/image/list",methods=['GET'])
def getImageList():
    retv={'images':[]}
    i=0
    for imname in image_list:
        retv['images'].append({"id":1+i,"name":imname})
        i=i+1
    return json.dumps(retv)
   
@app.route("/vm/types",methods=['GET'])
def gettypeList1(): 
	return json.dumps(types)   

@app.route("/vm/create", methods=['GET'])
def getParams():
	 
	      args = request.args
# print (args)
	      name1 = args['name']
	      instance_type1 = args['instance_type']
	      image_id1=args['image_id']
	      
	      #print name1
	      #print instance_type1
              #print image_id1
              #return ("<h2> name is "+ name1+" instance is "+instance_type1 + " image id is " + image_id1+ " </h2>")
	      ans= CreateVM.create_domain(name1,instance_type1,image_id1,machine_list,image_list,Vdesc,info)
	      m={'tr':'+','fl':'0'}
	      ans=str(ans)
	      n = json.dumps(m)
	      o=json.loads(n)
	      if ans=="0":
			return (o['fl'])
	      else:
			return (o['tr'])	    
 
         
         
#return ("ERROR : Maybe some problem with the parameters")

@app.route("/vm/query", methods=['GET'])
def getQuery():
	 
	      answer_list=[]
              args = request.args
	      vm_id=args['vmid']
	      vm_id1=int (vm_id)
	      ans=CreateVM.domain_query(vm_id1)
              #print answer_list
              
              if(len(ans)>0):
                        	 m={'vmid':(ans[0]),'name':(ans[1]),'instance_type':(ans[2]),'pmid':(ans[3])}
				 n=json.dumps(m)
				 o=json.loads(n)
			         return jsonify(o)
              
			 
              else: 
                     return ("ERROR : Maybe some problem with the parameters")
@app.route("/vm/destroy", methods=['GET'])
def Destroy_Domain():
	args = request.args
        vm_id=args['vmid']
        vm_id1=int (vm_id)
        ans= CreateVM.destroy_domain(vm_id1,machine_list)
       
        if ans=="1":
	   st={"status":1}
	   n=json.dumps(st)
	   m=json.loads(n)
	   return jsonify(m)
	else:
	   st={"status":0}
	   n=json.dumps(st)
	   m=json.loads(n)
	   return jsonify(m)        

def CreateMachines(FileName):
	
        MachineList = []
        fPtr = open(FileName)
	for line in fPtr.readlines():
		line = line[:-1]
		if line:
			remote_ip.append(line)
			Machines = line.split("@")
			MachineList.append(Machines + [str(uuid4())])
        return MachineList

def CreateImages(Filename):	
	iPtr = open(Filename)
        ImageList = []
	for line in iPtr.readlines():
		line = line[:-1]
		if line:
			img1 = line.split("@")
			img2 = img1[1].split(":")
			img3 = img2[1].split("/")
			ImageList.append(img3[len(img3)-1])
			
        return ImageList 
def CreateTypes(Filename):
        vMDescFile=open(Filename)
        vMLines=vMDescFile.readlines()
	vMDesc=unicode(''.join(  map(lambda lin: lin.strip(),vMLines) )  )
		
	Desc=json.loads(vMDesc)
	global types
	types = Desc        
	return Desc
def Make_Path(user,ip):
	path='remote+ssh://'+user+'@' + ip +'/'
	return path

def specs():
	for i in xrange(0,len(remote_ip),1):
    		remoteconns.append(libvirt.open("qemu+ssh://"+remote_ip[i]+'/system'));
	for i in xrange(0,len(remoteconns),1):
    		info.append(remoteconns[i].getInfo())
	print info         
if __name__ == '__main__':
	if len(sys.argv) < 4:
		print "Format: ./script pm_file image_file"
		exit(1)

	machine_list=CreateMachines(sys.argv[1])
	image_list=CreateImages(sys.argv[2])
        Vdesc=CreateTypes(sys.argv[3])
	specs() 
	#copy images to local directory, imageNames[] contains ith image name (zero-based)
	remoteImgFile=open(sys.argv[2],"r")
	remoteImgLines=remoteImgFile.readlines()
	remoteImgLines=map(lambda x: x.strip(),remoteImgLines)
	remoteImg=[]
	imageNames=[]
	for i in remoteImgLines:
   		if(i):
        		remoteImg.append(i)
	os.system("mkdir vishalxyz")
	os.system("rm -rf vishalxyz/*")
	for i in range(len(remoteImg)):
    		imageNames.append(re.findall("[^\\\]/[^/]*$",remoteImg[i])[-1][2:])
    		#perr("scp %s %s"%(remoteImg[i],"vishalxyz/"+ imageNames[-1] ))
    		os.system("scp %s %s"%(remoteImg[i],"vishalxyz/"+ imageNames[-1] ));       
	#print machine_list
        #print image_list
        #print Vdesc
        app.run(debug = True)

