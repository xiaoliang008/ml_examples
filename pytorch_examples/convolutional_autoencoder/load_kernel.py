#!/usr/bin/env python

import sys
sys.path.append('../pytorch_load_image/')
import pickle
import torch
import numpy as np
from img_load import *
from cnn_kernel_net import *
from torch.autograd import Variable
import torch.nn.functional as F
from pickle_dataset import *

db = {}
db['img_height'] = 29
db['img_width'] = 29
db['batch_size'] = 5
db['data_file_name'] = 'mnist_20.pk'
db['label_file_name'] = 'mnist_20_label.pk'
#dtype = torch.cuda.FloatTensor
dtype = torch.FloatTensor

def load_data():
	face_data = image_datasets('../../dataset/faces/', 'face_img')
	data_loader = DataLoader(face_data, batch_size=db['batch_size'], shuffle=True, drop_last=True)
	result = pickle.load( open( "face.p", "rb" ) )
	return [face_data, data_loader, result]


def get_loss(ckernel_net, data_loader):
	#	Compute final average loss
	loss_sum = 0
	for idx, (data, label, indx) in enumerate(data_loader):
		data = Variable(data.type(dtype), requires_grad=False)
		try:
			loss = ckernel_net.CAE_compute_loss(data)
		except:
			import pdb; pdb.set_trace()
		loss_sum += loss
	
	avgL = loss_sum/idx
	return avgL.cpu().data.numpy()[0]


def update_mnist_kernel_to_lates():
	#result = pickle.load( open( "kernel_mnist.p", "rb" ) )
	result = pickle.load( open( "mnist.p", "rb" ) )
	dset = pickle_dataset(db)
	data_loader = DataLoader(dataset=dset, batch_size=db['batch_size'], shuffle=True)

#	avgLoss = get_loss(result['kernel_net'], data_loader)
#	print('avgLoss : %.3f'%avgLoss)
#	import pdb; pdb.set_trace()

	if dtype == torch.cuda.FloatTensor:
		ckernel_net = cnn_kernel_net(db).cuda()
		batch = zip(ckernel_net.children(), result['kernel_net'].children())
		
		for a, b in batch:
			if hasattr(a, 'weight'):
				a.weight = b.weight
				a.bias = b.bias
	else:	
		ckernel_net = cnn_kernel_net(db)
		batch = zip(ckernel_net.children(), result['kernel_net'].children())
		
		for a, b in batch:
			if hasattr(a, 'weight'):

				a.weight.data = b.weight.data.cpu()
				a.bias.data = b.bias.data.cpu()
	

#	xin = Variable(dset.x.type(dtype), requires_grad=False)
#	img = xin[0,0,:,:].data.numpy()
#	plt.imshow(img, cmap='gray')
#	plt.show()
#
#
#
#	xout = ckernel_net.CAE_forward(xin)
#	img = xout[0,0,:,:].data.numpy()
#	plt.imshow(img, cmap='gray')
#	plt.show()
#	import pdb; pdb.set_trace()



	avgLoss = get_loss(ckernel_net, data_loader)
	print('avgLoss : %.3f'%avgLoss)

	new_result = {}
	new_result['avgLoss'] = avgLoss
	new_result['kernel_net'] = ckernel_net
	pickle.dump( new_result, open( "kernel_mnist.p", "wb" ) )
	import pdb; pdb.set_trace()	

def update_kernel_to_lates():
	[face_data, data_loader, result] = load_data()

	if dtype == torch.cuda.FloatTensor:
		ckernel_net = cnn_kernel_net(db).cuda()
		batch = zip(ckernel_net.children(), result['kernel_net'].children())
		
		for a, b in batch:
			if hasattr(a, 'weight'):
				a.weight = b.weight
				a.bias = b.bias
	else:	
		ckernel_net = cnn_kernel_net(db)
		batch = zip(ckernel_net.children(), result['kernel_net'].children())
		
		for a, b in batch:
			if hasattr(a, 'weight'):

				a.weight.data = b.weight.data.cpu()
				a.bias.data = b.bias.data.cpu()
	
	avgLoss = get_loss(ckernel_net, data_loader)
	print('avgLoss : %.3f'%avgLoss)

	new_result = {}
	new_result['avgLoss'] = avgLoss
	new_result['kernel_net'] = ckernel_net
	pickle.dump( new_result, open( "face.p", "wb" ) )
	


def view_xout():
	[face_data, data_loader, result] = load_data()
	ckernel_net = result['kernel_net']
	
	for idx, data in enumerate(data_loader):
		data = Variable(data.type(dtype), requires_grad=False)
		xout = ckernel_net.CAE_forward(data)

		#xout = ckernel_net(data[1,:,:,:])
		#print(data[1,:,:,:].unsqueeze(dim=0))
		#single_data = data[1,:,:,:].unsqueeze(dim=0)
		#xout = ckernel_net(single_data)
		#import pdb; pdb.set_trace()
		#face_data.display_image(xout[1,0,:,:].cpu().data.numpy())
		import pdb; pdb.set_trace()

	#avgLoss = get_loss(ckernel_net, data_loader)
	#print('avgLoss : %.3f'%avgLoss)

update_mnist_kernel_to_lates()
#update_kernel_to_lates()
#view_xout()


#for idx, data in enumerate(data_loader):
#	print data.shape
#	data = Variable(data.type(dtype), requires_grad=False)
#
#
#	for m in result['kernel_net'].children():
#		print m.weight.shape
#
#	import pdb; pdb.set_trace()
#
#	xout = result['kernel_net'](data)
#
#result['avgLoss']
#result['kernel_net']
#
