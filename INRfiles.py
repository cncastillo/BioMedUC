from numpy import gradient, array, amin, amax, mgrid, sin, cos, column_stack, fromstring, zeros
#################
### INR IMAGE ###
#################

def writeINR(inrfile, field, dx, dy, dz, Type="float32", CPU="decm"):
	s = len(field.shape)/4  # 1 vfield 0 sfield 
	if s==1:
		vdim=3
	elif s==0:
		vdim=1  
	header = "#INRIMAGE-4#{\n" 
	header +="XDIM="+str(field.shape[0+s])+"\n"  # x dimension 
	header +="YDIM="+str(field.shape[1+s])+"\n"  # y dimension 
	header +="ZDIM="+str(field.shape[2+s])+"\n"  # z dimension 
	header +="VDIM="+str(vdim)+"\n"  
	header +="VX="+str(dx)+"\n"  # voxel size in x 
	header +="VY="+str(dy)+"\n"  # voxel size in y 
	header +="VZ="+str(dz)+"\n"  # voxel size in z 
	Scale = -1
	Type_np = Type.lower()
	if(Type_np in ['float32','single','float','float_vec']):
		Type = "float"
		Pixsize = "32 bits"
	elif(Type_np in ['float64','double','double_vec']):
		Type = "float"
		Pixsize = "64 bits"
	elif(Type_np in ['uint8']):
		Type = "unsigned fixed"
		Pixsize = "8 bits"
		Scale = "2**0"
	elif(Type_np in ['int16']):
		Type = "signed fixed"
		Pixsize = "16 bits"
		Scale = "2**0"
	elif(Type_np in ['uint16']):
		Type = "unsigned fixed"
		Pixsize = "16 bits"
		Scale = "2**0"
	else:
		print "Incorrect Data Type."		

	header +="TYPE="+Type+"\n"  #float, signed fixed, or unsigned fixed 
	header +="PIXSIZE="+Pixsize+"\n"  #8, 16, 32, or 64 
	if Scale!=-1: header +="SCALE="+Scale+"\n"  #not used in my program 
	header +="CPU="+CPU+"\n"  
	# decm, alpha, pc, sun, sgi ; ittle endianness : decm, alpha,
	# pc; big endianness :sun, sgi
	for i in range(256-(len(header)+4)):
		header +="\n"
	header +="##}\n"
	######################################
	raw_data = field.transpose().astype(Type_np).tostring()

	file = open(inrfile, 'w')
	file.write(header)
	file.write(raw_data)
	file.close()
	print "##############################"
	print "## INR Created Successfully ##"
	print "##############################"

def readINR(inrfile, Type="float32"):
	"""
	For Gray Level Images Only (Scalar fields)
	"""
	file = open(inrfile, 'r')
	inp = file.readlines()
	n=0
	raw_data = ""
	for line in inp:
		n+= len(line)
		if(n>256):
			raw_data += line
		else:
			if line.find("XDIM")!=-1: xdim = int(line.split("=")[1])
			if line.find("YDIM")!=-1: ydim = int(line.split("=")[1])
			if line.find("ZDIM")!=-1: zdim = int(line.split("=")[1])
			# if line.find("PIXSIZE")!=-1: 
			# 	pixsize = int(line.split("=")[1].split(" ")[0])
			if line.find("VX")!=-1: vx = float(line.split("=")[1])
			if line.find("VY")!=-1: vy = float(line.split("=")[1])
			if line.find("VZ")!=-1: vz = float(line.split("=")[1])

	data = fromstring(raw_data, dtype=Type)
	#size=XDIM*YDIM*ZDIM*VDIM*PIXSIZE/8 
	if(len(data)==xdim*ydim*zdim):
		#read Transposed file          ##IMPORTANT##
		return data.reshape((zdim,ydim,xdim)).transpose(),[vx,vy,vz]
	else:
		print "Error Reading the file make sure the data type its correct."
		print "[data saved in \"data\"]"
		return data
