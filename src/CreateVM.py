import libvirt
import os,sys,re
from uuid import uuid4
import parse
vmid=0
query_list=[]
machine_id=0
def pout(x):
    sys.stdout.write(str(x))
def perr(x):
    sys.stderr.write(str(x))
def create_xml(hyper,vm_name,vm_mem,vm_uid,vm_cpu,ari,user,vm_image):
	xml="<domain type='%s'> \
  	      <name>%s</name> \
	      <memory>%s</memory>					\
	      <uuid>%s</uuid> \
	      <vcpu>%s</vcpu>						\
	      <os>							\
	        <type arch='%s' machine='pc'>hvm</type>		\
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
	        <emulator>/usr/bin/qemu-system-x86_64</emulator>	\
	        <disk type='file' device='disk'>			\
  	        <driver name='qemu' type='raw'/>			\
		<source file='/home/%s/%s'/>		\
		<target dev='hda' bus='ide'/>				\
		<address type='drive' controller='0' bus='0' unit='0'/>	\
		</disk>							\
	      </devices>						\
   	      </domain>"%(hyper,vm_name,vm_mem,vm_uid,vm_cpu,ari,user,vm_image)
 	return xml
def create_domain(name1,instance_type1,image_id1,machine_list,image_list,Vdesc,info):
	global machine_id,vmid,query_list
	#machine_id = (machine_id+1)%len(machine_list)
	#print machine_id
	#machine=machine_list[0]
	#user= machine[0]
	#ip= machine[1]
        uid = str(uuid4())
        #print user
        #print ip
        print uid
        # to index the image        
	wimage=str(image_list[int(image_id1)])
	print wimage	
	temp =int (instance_type1)
	#print temp
	temp=temp-1	
	Ram= Vdesc['types'][temp]['ram']
	Ram=Ram*1024
        Ram1=str(Ram)
        #print Ram1
	VCPU = Vdesc['types'][temp]['cpu']
	VCPU1=str(VCPU)
        cpu = int(VCPU1)
        print cpu
	#print VCPU1
        n_mac=len(info)
        ntries=0        
	flag=-1
	while ntries!=n_mac:
		match=info[ntries]
		if(match[1]*1024>=Ram and match[2]>=cpu):
			flag=ntries
			break
		ntries=ntries+1
	user=-1
	ip=-1
	arch=-1
        if flag!=-1:
		machine = machine_list[flag]
		#vmid=vmid+1
		user = machine[0]
		ip = machine[1]
		arch=info[flag][0]
		vmid=vmid+1
        	temp_list=[]
        	temp_list.append(vmid)
         	temp_list.append(name1)
        	temp_list.append(instance_type1)
        	temp_list.append(machine_id)
        #print temp_list
        	query_list.append(temp_list)
		os.system("scp %s %s"%("vishalxyz/"+ wimage,user + "@" + ip+ ":~/" ));
        #print query_list
	else:
		perr("could not fine suitable machine")
		return 0        
        try:  	
		conn=libvirt.open(parse.Make_Path(user,ip))
      		request = conn.defineXML(create_xml(conn.getType().lower(),name1,Ram1,uid,VCPU1,arch,user,wimage))        	
		request.create()
                return str(vmid)
        except:
        	return "0"
mid=0
domain_name=""
def destroy_domain(vmid,machine_list):
	temp_list=[]
        global mid,domain_name
	for li in query_list:
		if li[0]==(int)(vmid):
			mid=li[3]
			temp_list=li
                        domain_name=str(li[1])
			break
	print mid
	print domain_name
	machine = machine_list[mid]
	user = machine[0]
	ip = machine[1]
	#temp1=Make_Path(user,ip)
        #print temp
        try:
		conn = libvirt.open(parse.Make_Path(user, ip))
		req = conn.lookupByName(domain_name)
		if req.isActive():
			req.destroy()
		req.undefine()
		query_list.remove(temp_list)
                return "1"
	except:
		return "0"


def domain_query(vm_id):
	answer=[] 
	print vm_id
	for li in query_list:
		if(li[0]== vm_id):
			answer.append(li[0])
	                answer.append(li[1])
			answer.append(li[2])
                        answer.append(li[3])
                        #print answer
                        return answer
        return answer

	



