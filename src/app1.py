#!/usr/bin/env python
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
import sys
import create_vm
import get
import Destroy
import Query

app = Flask(__name__)

@app.route('/server/vm/create/' , methods = ['GET'])
def get_create():
	vm={}
	vm['name']=request.args.get('name')
	vm['instance_type']=request.args.get('instance_type')
	vm['image_id']=request.args.get('image_id')
	return jsonify(create_vm.create(vm))
#return jsonify(vm)

@app.route('/server/vm/destroy/' , methods = ['GET'])
def get_destroy():
	vmid=request.args.get('vmid')
	return jsonify(Destroy.destroy(int(vmid)))

@app.route('/server/vm/query/' , methods = ['GET'])
def get_query():
	vmid=request.args.get('vmid')
	return jsonify(Query.query(int(vmid)))

@app.route('/server/vm/types/')
def get_types():
	return jsonify(create_vm.vm_type())

@app.route('/server/vm/image/list')
def get_imagelist():
	return jsonify(create_vm.List_Images())
	

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

if __name__ == '__main__':
	if len(sys.argv) < 4:
		print "Format: ./script pm_file image_file"
		exit(1)

	get.create_machines(sys.argv[1])
	get.create_images(sys.argv[2])
	get.CreateTypes(sys.argv[3])
    	app.run(debug = True)
#get.create_vmtypes(sys.argv[3])
	
