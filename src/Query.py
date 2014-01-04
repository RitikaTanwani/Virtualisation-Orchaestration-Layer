import libvirt
import create_vm
import get
import app1


def query(vid):
	mydict={}
	try:
		for i in create_vm.vm_list:
			if i[0]==vid:
				mydict['vmid']=i[0]
				mydict['name']=i[1]
				mydict['instance_type']=i[2]
				mydict['pmid']=i[3]+1
				break
		return mydict
	except:
		return mydict
