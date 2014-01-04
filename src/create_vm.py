import libvirt
import os
import get
import app1
from random import random
from uuid import uuid4
import subprocess

pmid=0
vmid=0
vm_list=[]
def create_xml(vm_name, hypervisor,uid,path,ram,cpu,emulator_path,emulator1,arch_type):
	xml = r"<domain type='" + hypervisor + 			\
	    "'><name>" + vm_name + "</name>				\
	      <memory>" + ram + "</memory>					\
	      <uuid>" + uid + "</uuid> \
	      <vcpu>" + cpu + "</vcpu>						\
	      <os>							\
	        <type arch='" + arch_type + "' machine='pc'>hvm</type>		\
		<boot dev='hd'/>					\
	      </os>							\
	      <features>						\
	        <acpi/>							\
          	<apic/>							\
	      	<pae/>							\
	      </features>						\
	      <on_poweroff>destroy</on_poweroff>			\
  	      <on_reboot>restart</on_reboot>				\
	      <on_crash>restart</on_crash>				\
	      <devices>							\
	        <emulator>" + emulator_path + "</emulator>	\
	        <disk type='file' device='disk'>			\
		<driver name=" + emulator1 + " type='raw'/>			\
		<source file='" + path + "'/>		\
		<target dev='hda' bus='ide'/>				\
		<address type='drive' controller='0' bus='0' unit='0'/>	\
		</disk>							\
	      </devices>						\
   	      </domain>"

	return xml
def create(attrs):
	name=attrs["name"]
	instance_type = int(attrs["instance_type"])
	image_id=attrs["image_id"]
	num=1
	
	Image_name = image_id + ".img"

	Ram=get.Desc['types'][instance_type-1]['ram']
	Ram = Ram * 1024
	vcpu=int(get.Desc['types'][instance_type-1]['cpu'])
	global pmid,vmid,vm_list

	tot = 1 
	machine = get.machine_list[pmid]
	user = machine[0]
	ip = machine[1]
	avail_cpu=int(subprocess.check_output("ssh " + user + "@" + ip + " nproc" ,shell=True))


	free_space=(subprocess.check_output("ssh " + user + "@" + ip + " free -m" ,shell=True))
	free_space=free_space.split("\n")
	free_space=free_space[1].split()
	avail_ram=int(free_space[3])	
	avail_ram = avail_ram * 1024

	try:
		anystr=(subprocess.check_output("ssh " + user + "@" + ip + " cat /proc/cpuinfo | grep lm " ,shell=True))
		avail_bit = '64'
	except:
		avail_bit = '32'
	
	check_arch = (((get.img_list[int(image_id)-1])[-1]).split('/')[-1]).split('.')[0].split('_')[1]

	while(avail_cpu < vcpu or avail_ram < Ram or int(avail_bit) < int(check_arch)):
		pmid=(pmid+1)%(len(get.machine_list))
		tot=tot+1
		if(tot > len(get.machine_list)):
			return {"Error" : " Specifications could not be satisfied, Virtual Machine cannot be created" }
		machine = get.machine_list[pmid]
		user = machine[0]
		ip = machine[1]
		avail_cpu=int(subprocess.check_output("ssh " + user + "@" + ip + " nproc" ,shell=True))
		free_space=(subprocess.check_output("ssh " + user + "@" + ip + " free -m" ,shell=True))
		free_space=free_space.split("\n")
		free_space=free_space[1].split()
		avail_ram=int(free_space[3])	
		avail_ram = avail_ram * 1024
		check_arch = (((get.img_list[int(image_id)-1])[-1]).split('/')[-1]).split('.')[0].split('_')[1]
	

	
	vmid=vmid+1
	vm_list.append([vmid,name,instance_type,pmid])
	pmid=(pmid+1)%(len(get.machine_list))
	uid = str(uuid4())
#try:
#		os.path.exists("~/"+Image_name+"/")
#	except:
	get.scp_img_path(int(image_id))
#		print Image_name

	Image_path="/home/" + user + "/" + Image_name
	os.system("scp ~/" + Image_name + " " +  user + "@" + ip + ":" + Image_path + " 2> /dev/null")#arpita@10.1.97.143:~/replica11.img")	

	connect = libvirt.open(get.make_path(user, ip))

	system_info = connect.getCapabilities()
	emulator_path = system_info.split("emulator>")
	emulator_path = emulator_path[1].split("<")[0] #location of xen/qemu
#	print emulator_path
	emulator1 = system_info.split("<domain type=")
	emulator1 = emulator1[1].split(">")[0] #type of emulator present on given machine xen/qemu
#	print emulator1
	arch_type = system_info.split("<arch>")
	arch_type = arch_type[1].split("<")[0] #archituctue of machine print arch_type


	req = connect.defineXML(create_xml(name, connect.getType().lower(),uid,Image_path,str(Ram),str(vcpu),emulator_path,emulator1,arch_type))
	try:
		req.create()
		return {"vmid": vmid}
	except:
		return {"vmid" : 0 }

def vm_type():
	return get.Desc

def List_Images():
	print_imglist = []
	for i in get.List_Images:
		mydict = {}
		mydict['id']=i[0]
		mydict['name']=i[1].split('.')[0]
		print_imglist.append(mydict)

	return {"Images" : print_imglist }
	
	 
