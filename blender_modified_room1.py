import bpy
import pickle
import os
import subprocess

print("File blender_scene.py called")





#fin = open("extracted_models.txt", 'r')
fnouns_id = open("nouns_and_IDs.txt", 'r')
fsent = open("Spatial_Relation_test.txt", 'r')
#fout = open("Prep_nouns.txt", 'w') 

data = pickle.load(fp_data)

#fnouns_id = open("nouns_and_IDs.txt", 'r')
models = fnouns_id.read()
models = models.split('\n')
print(models)

fnouns_id.seek(0)
line1 = fnouns_id.readline().split(" ")
nouns = list()
ids = list()
print("out line1",line1)
for j in range(len(models)-1):
	print(line1)
	nouns.append(line1[0])
	ids.append(line1[1])
	line1 = fnouns_id.readline().split(" ")
print("\n\n\n\n")
print("line1",line1)
print(nouns)
print(ids)
print("\n\n\n\n")

placement_prepositions = {'right':['right'], 'up':['above', 'on', 'top'], 'left':['left','near'], 'down':['beneath', 'below', 'under']}
prepositions = ['right', 'left', 'up', 'down', 'above', 'below', 'on', 'beneath', 'top', 'front', 'back','near']

'''
sentence = fsent.read().split(' ')
print(sentence)

prev_noun = ''
pres_noun = ''
last_prep = ''
prep_mapping = dict()
for n in range(len(sentence)):
	if sentence[n] in nouns:
		prev_noun = sentence[n]
		pres_noun = sentence[n]
		break
print(n)
# print(pres_noun)
# for p in range(n+1, len(sentence)):
# 	if sentence[p] in prepositions:
# 		# last_prep = sentence[p]
# 		# prep_mapping[last_prep].append([])
# 		print(prev_noun, sentence[p], end = ' ')
# 		fout.write(prev_noun + ' ' + sentence[p] + ' ')
# 	elif sentence[p] in nouns:
# 		print(sentence[p])
# 		fout.write(sentence[p] + '\n')
# 		prev_noun = sentence[p]
for p in range(n+1, len(sentence)):
	if sentence[p] in prepositions:
		for j in range(p+1, len(sentence)):
			if sentence[j] in nouns:
				# print(sentence[j], sentence[p], prev_noun)
				fout.write(sentence[j] + ' ' + sentence[p] + ' ' + prev_noun + '\n')
				break
	elif sentence[p] in nouns:
		prev_noun = sentence[p]

fout.close()
'''
print(os.system("python modify_sentence_order.py"))

path = "D:/Text_to_scene_generation-master/Text_to_scene_generation-master/models-OBJ/models/"
path2 = "D:/Text_to_scene_generation-master/Text_to_scene_generation-master/Models/"
#x_dims_count_right = 0
#y_dims_count_right = 0
#z_dims_count_right = 0

x_dims_count = 0
y_dims_count = 0
z_dims_count = 0

#x_dims_count_left = 0
#y_dims_count_left = 0
#z_dims_count_left = 0

fnouns_preps = open("Spatial_Relation_test.txt", 'r')  # change
data1 = fnouns_preps.read()
data1 = data1.split('.')

new_models = list()
placed_models = dict()
combined_models = list()
print("\n\n\n\n")
data1.pop()
print("dataq",data1)



on_placed=dict()

for i in data1:
	print(i)
	if len(i) < 2:
		break
	line2 = i.split(' ')
	print(line2)

	if line2[1] == 'right':
		print("here1")
		print("\n\n\n\nRIGHT PLACEMENT\n\n\n\n")
		id1 = ids[nouns.index(line2[0])]
		id1 = id1.strip()
		print("\n\nRecieved ID1 is", id1)
		id2 = ids[nouns.index(line2[2])]
		id2 = id2.strip()
		print("\n\nRecieved ID2 is", id2)
		full_id =id1
		id1=id1[4:]
		dims = data[full_id]['dims']
		try:
			rotation_info = data[full_id]['up']
			unit = float(data[full_id]['unit'][0])
		except:
			rotation_info = (0,0,0)
			unit = 1.0
		x_rot = 0
		y_rot = 0
		z_rot = 0
		model_id = id1 + '.obj'
		mtl_id = id1 + '.mtl'
		model_path = path + model_id
		print('\n\n\n\n\n\n\n')
		path1 = "D:/Text_to_scene_generation-master/Text_to_scene_generation-master/models-OBJ/models/"
		if id1 not in combined_models:
			print(os.system("cd " + path1 + '\n' + 'copy ' + model_id + ' D:/Text_to_scene_generation-master/Text_to_scene_generation-master/Models'))
			print(os.system("cd " + path1 + '\n' + 'copy ' + mtl_id + ' D:/Text_to_scene_generation-master/Text_to_scene_generation-master/Models'))
			# os.system("cd " + path1 + '\n' + 'open ' + model_id + '.obj')
		else:
			model_path = path2 + model_id
			print("\n\n\n\nPATH CHANGED\n\n\n\n")
		if id1 not in placed_models:
			print("not placed ",line2[0])
			imported_object = bpy.ops.import_scene.obj(filepath=model_path)
			print("Object", model_id, "imported")
			object1 = bpy.context.selected_objects[0]
			object1.delta_scale = (unit, unit, unit)
			object1.rotation_euler = (x_rot, y_rot, z_rot)
			bpy.ops.object.origin_set(type = 'GEOMETRY_ORIGIN')
			object1.location = (z_dims_count, x_dims_count , 0)
			placed_models[id1] = (x_dims_count, 0, z_dims_count)
			print("dims",dims)
			x_dims_count += (float(dims[0]))/200
			x_dims_count=x_dims_count*2.0
			z_dims_count+=0.3
		else:
			x_dims_count = placed_models[id1][0] + (float(dims[0])/200)
			x_dims_count=x_dims_count*2.0
			z_dims_count+=placed_models[id1][2] + (float(dims[2])/200)
		full_id =id2
		id2=id2[4:]
		dims2 = data[full_id]['dims']
		try:
			rotation_info = data[full_id]['up']
			unit = float(data[full_id]['unit'][0])
		except:
			rotation_info = (0,0,0)
			unit = 1.0
		x_rot = 0
		y_rot = 0
		z_rot = 0
		model_id = id2 + '.obj'
		model_path = path + model_id
		if id2 in combined_models:
			print("\n\n\n\nCOMMAND WENT HERE\n\n\n")
			model_path = path2 + model_id

		if id2 not in placed_models:
			print("not placed ",line2[2])
			imported_object = bpy.ops.import_scene.obj(filepath=model_path)
			print("Object", model_id, "imported")
			obj_object = bpy.context.selected_objects[0] 
			obj_object.delta_scale = (unit, unit, unit)
			obj_object.rotation_euler = (x_rot, y_rot, z_rot)
			bpy.ops.object.origin_set(type = 'GEOMETRY_ORIGIN')
			x = x_dims_count + (float(dims[0])/200)
			x_dims_count=x_dims_count*2.0
			#y_dims_count += (float(dims[1]))/200
			z = z_dims_count + placed_models[id1][2] 

			obj_object.location = ( z,x, 0)
			placed_models[id2] = (x,0,z)
			
			x_dims_count += (float(dims2[0]))/200
			x_dims_count=x_dims_count*2.0
			z_dims_count += (float(dims2[2]))/200	
		else:
			print("placed ",line2[2])
			x_dims_count += (float(dims2[0]))/200
			x_dims_count=x_dims_count*2.0
			z_dims_count += (float(dims2[2]))/200	
		print("after right",placed_models)


	elif line2[1] == 'left' or line2[1] == 'near':
		print("\n\n\n\nLEFT PLACEMENT\n\n\n\n")
		id1 = ids[nouns.index(line2[0])]
		id1 = id1.strip()
		print("\n\nReceived ID1 is", id1, "\n\n")
		# print("\n\n\n\n\n\n", nouns.index(line2[2]), "\n\n\n\n")
		id2 = ids[nouns.index(line2[2])]
		id2 = id2.strip()
		print("\n\nRecieved ID2 is", id2, "\n\n")
		full_id =id1
		id1=id1[4:]
		dims = data[full_id]['dims']
		rotation_info = data[full_id]['up']
		#unit=data[full_id]['unit'][0]
		
		unit = float(data[full_id]['unit'][0])
		x_rot = 0
		y_rot = 0
		z_rot = 0
		model_id = id1 + '.obj'
		mtl_id = id1 + '.mtl'
		model_path = path + model_id
		print("\n\nID1 is ", id1)
		print("\n\nCombined_models: ", combined_models, "\n\n")
		path1 = "D:/Text_to_scene_generation-master/Text_to_scene_generation-master/models-OBJ/models/"
		if id1 not in combined_models:
			print(os.system("cd " + path1 + '\n' + 'copy ' + model_id + ' D:/Text_to_scene_generation-master/Text_to_scene_generation-master/models-OBJ/models'))
			print(os.system("cd " + path1 + '\n' + 'copy ' + mtl_id + ' D:/Text_to_scene_generation-master/Text_to_scene_generation-master/models-OBJ/models'))
			# os.system("cd " + path1 + '\n' + 'open ' + model_id + '.obj')
		else:
			print("\n\n\n\nPATH CHANGED\n\n\n\n")
			model_path = path2 + model_id

		if id1 not in placed_models:
			imported_object = bpy.ops.import_scene.obj(filepath=model_path)
			print("Object", model_id, "imported")
			obj_object = bpy.context.selected_objects[0]
			obj_object.delta_scale = (unit, unit, unit)
			obj_object.rotation_euler = (x_rot, y_rot, z_rot)
			bpy.ops.object.origin_set(type = 'GEOMETRY_ORIGIN')

			obj_object.location = (z_dims_count, x_dims_count , 0)
			placed_models[id1] = (x_dims_count, 0, z_dims_count)
			x_dims_count += (float(dims[0]))/80
			x_dims_count=x_dims_count*2.0
			z_dims_count+=0.3
			print("dims",dims)
			
			
			
		else:
			
			print("\n\nMODEL", id1, "ALREADY IMPORTED\n\n")
			print("dims",dims)
			x_dims_count = placed_models[id1][0] + (float(dims[0]))/80
			z_dims_count+=placed_models[id1][2] + (float(dims[2]))/80
			

			
		if id2 not in placed_models:
			full_id =id2
			id2=id2[4:]
			dims2 = data[full_id]['dims']
			try:
				rotation_info = data[full_id]['up']
				unit = float(data[full_id]['unit'][0])
			except:
				rotation_info = (0,0,0)
				unit = 1.0
			# data['wss.'+filename]['dims'] = data['wss'+id1]['dims']
			x_rot = 0
			y_rot = 0
			z_rot = 0
			model_id = id2 + '.obj'
			model_path = path + model_id
			if id2 in combined_models:
				print("\n\n\n\nCOMMAND WENT HERE\n\n\n")
				model_path = path2 + model_id
			imported_object = bpy.ops.import_scene.obj(filepath=model_path)
			print("Object", model_id, "imported")
			obj_object = bpy.context.selected_objects[0] 
			obj_object.delta_scale = (unit, unit, unit)
			obj_object.rotation_euler = (x_rot, y_rot, z_rot)
			bpy.ops.object.origin_set(type = 'GEOMETRY_ORIGIN')
			
			#y = placed_models[id1][1]
			x = x_dims_count + (float(dims[0]))/80
			x_dims_count=x_dims_count*2.0
			#y_dims_count += (float(dims[1]))/200
			z = z_dims_count + placed_models[id1][2] 
			'''if x in placed_models:
				print("in here")
				z=z+0.4
				obj_object.location = ( z,-x, 0)
			else:

				obj_object.location = ( z,-x, 0)'''
			obj_object.location = ( z,-x, 0)
			placed_models[id2] = (x,0,z)
			
			x_dims_count += (float(dims2[0]))/80
			x_dims_count=x_dims_count*2.0
			z_dims_count += (float(dims2[2]))/80
			
		else:
			x_dims_count += (float(dims2[0]))/80 
			x_dims_count=x_dims_count*2.0
			#y_dims_count += (float(dims[1]))/200 
			z_dims_count += (float(dims2[2]))/80
		print("aftr left",placed_models)

	elif (line2[1] == 'above') or (line2[1] == 'on'):
		print("\n\n\n\nLEFT PLACEMENT\n\n\n\n")
		id1 = ids[nouns.index(line2[0])]
		id1 = id1.strip()
		print("\n\nReceived ID1 is", id1, "\n\n")
		# print("\n\n\n\n\n\n", nouns.index(line2[2]), "\n\n\n\n")
		id2 = ids[nouns.index(line2[2])]
		id2 = id2.strip()
		print("\n\nRecieved ID2 is", id2, "\n\n")
		
		full_id =id1
		id1=id1[4:]

		dims = data[full_id]['dims']
		print(line2[0],dims)
		rotation_info = data[full_id]['up']
		unit = float(data[full_id]['unit'][0])
		x_rot = 0
		y_rot = 0
		z_rot = 0
		
		
		
		model_id = id1 + '.obj'
		mtl_id = id1 + '.mtl'
		model_path = path + model_id
		print("\n\nID1 is ", id1)
		print("\n\nCombined_models: ", combined_models, "\n\n")
		path1 = "D:/Text_to_scene_generation-master/Text_to_scene_generation-master/models-OBJ/models/"
		if id1 not in combined_models:
			print(os.system("cd " + path1 + '\n' + 'copy ' + model_id + ' D:/Text_to_scene_generation-master/Text_to_scene_generation-master/models-OBJ/models'))
			print(os.system("cd " + path1 + '\n' + 'copy ' + mtl_id + ' D:/Text_to_scene_generation-master/Text_to_scene_generation-master/models-OBJ/models'))
			# os.system("cd " + path1 + '\n' + 'open ' + model_id + '.obj')
		else:
			print("\n\n\n\nPATH CHANGED\n\n\n\n")
			model_path = path2 + model_id

		if id1 not in placed_models:
			imported_object = bpy.ops.import_scene.obj(filepath=model_path)
			print("Object", model_id, "imported")
			object1 = bpy.context.selected_objects[0]
			object1.delta_scale = (unit, unit, unit)
			object1.rotation_euler = (x_rot, y_rot, z_rot)
			bpy.ops.object.origin_set(type = 'GEOMETRY_ORIGIN')
			
			object1.location = (z_dims_count, x_dims_count, 0)
			placed_models[id1] = (x_dims_count, 0, z_dims_count)
			print("x_dims_count in id1 in on",x_dims_count)
			
			x_dims_count += (float(dims[0]))/80
			x_dims_count=x_dims_count*2.0 
			y_dims_count += (float(dims[1]))/80 
			z_dims_count += (float(dims[2]))/80
			#height=bpy.data.objects[id1].dimensions[2]
			
		else:
			#height=bpy.data.objects[id1].dimensions[2]
			print("\n\nMODEL", id1, "ALREADY IMPORTED\n\n")
			print("dims",dims)
			x_dims_count = placed_models[id1][0] + (float(dims[0]))/80
			x_dims_count=x_dims_count*2.0
			#y_dims_count = placed_models[id1][1] + (float(dims[1]))/200
			z_dims_count = placed_models[id1][2] + (float(dims[2]))/80
			
		

		full_id =id2
		id2=id2[4:]
		dims2 = data[full_id]['dims']


		try:
			rotation_info = data[full_id]['up']
			unit = float(data[full_id]['unit'][0])
		except:
			rotation_info = (0,0,0)
			unit = 1.0
		# data['wss.'+filename]['dims'] = data['wss'+id1]['dims']
		x_rot = 0
		y_rot = 0
		z_rot = 0
		model_id = id2 + '.obj'
		model_path = path + model_id
		print("placed",placed_models)
		if id2 not in placed_models:
			imported_object = bpy.ops.import_scene.obj(filepath=model_path)
			print("Object", model_id, "imported")
			object2 = bpy.context.selected_objects[0] 
			object2.delta_scale = (unit, unit, unit)
			object2.rotation_euler = (x_rot, y_rot, z_rot)
			bpy.ops.object.origin_set(type = 'GEOMETRY_ORIGIN')
			#x = x_dims_count + (float(dims[0]))/200
			if id1 in on_placed:
				print("placed_models[id1][0]",placed_models[id1][0])
				x=placed_models[id1][0]+on_placed[id1]  #x=width
				on_placed[id1]+=float(dims2[0])/100+0.3
				
			else:
				x=placed_models[id1][0]
				print("x",x)
				on_placed[id1]=float(dims2[0])/100
			#x=placed_models[id1][0]+on_placed[id1]
			y=(float(dims[1]))/200
			z=placed_models[id1][2]

			print("go",x,y,z)
			object2.location = (z,x,y)
			#x_dims_count += (float(dims[0]))/100
			placed_models[id2] = (x,y,z)
			print("ab toh sahi hoooio",placed_models[id2])

		else:
			print("id2 in placed models")
	

	elif line2[1] == 'front':
		print("\n\n\nFRONT PLACEMENT\n\n\n\n")
		id1 = ids[nouns.index(line2[0])]
		id1 = id1.strip()
		print("\n\nRecieved ID1 is", id1)
		id2 = ids[nouns.index(line2[2])]
		id2 = id2.strip()
		print("\n\nRecieved ID2 is", id2)
		full_id =id1
		id1=id1[4:]
		dims = data[full_id]['dims']
		# rotation_info = data[full_id]['up']
		# unit = float(data[full_id]['unit'][0])
		try:
			rotation_info = data[full_id]['up']
			unit = float(data[full_id]['unit'][0])
		except:
			rotation_info = (0,0,0)
			unit = 1.0
		x_rot = 0
		y_rot = 0
		z_rot = 0
		model_id = id1 + '.obj'
		mtl_id = id1 + '.mtl'
		model_path = path + model_id
		print('\n\n\n\n\n\n\n')
		path1 = "D:/Text_to_scene_generation-master/Text_to_scene_generation-master/models-OBJ/models/"
		#path2 = "/Volumes/My Passport/SHAPE/Models/Volumes/My Passport/SHAPE/Models/"
		if id1 not in combined_models:
			print(os.system("cd " + path1 + '\n' + 'copy ' + model_id + ' D:/Text_to_scene_generation-master/Text_to_scene_generation-master/Models/'))
			print(os.system("cd " + path1 + '\n' + 'copy ' + mtl_id + ' D:/Text_to_scene_generation-master/Text_to_scene_generation-master/Models/'))
			# os.system("cd " + path1 + '\n' + 'open ' + model_id + '.obj')
		else:
			model_path = path1 + model_id
			print("\n\n\n\nPATH CHANGED\n\n\n\n")

		if id1 not in placed_models:
			imported_object = bpy.ops.import_scene.obj(filepath=model_path)
			print("Object", model_id, "imported")
			obj_object = bpy.context.selected_objects[0]
			obj_object.delta_scale = (unit, unit, unit)
			obj_object.rotation_euler = (x_rot, y_rot, z_rot)
			bpy.ops.object.origin_set(type = 'GEOMETRY_ORIGIN')
			obj_object.location = (0, 0, 0)
			x_dims_count += (float(dims[0]))/200 
			y_dims_count += (float(dims[1]))/200 
			z_dims_count += (float(dims[2]))/200
			placed_models[id1] = (0, 0, 0)
		else:
			print("\n\nMODEL", id1, "ALREADY IMPORTED\n\n")
			# x_dims_count = placed_models[id1][0] + (float(dims[0]))/200
			x_dims_count = placed_models[id1][0]
			y_dims_count = placed_models[id1][1] + (float(dims[1]))/200
			z_dims_count = placed_models[id1][2] + (float(dims[2]))/200

		full_id =id2
		id2=id2[4:]
		dims2 = data[full_id]['dims']
		# rotation_info = data[full_id]['up']
		try:
			unit = float(data[full_id]['unit'][0])
		except:
			unit = 1
		x_rot = 0
		y_rot = 0
		z_rot = 0
		model_id = id2 + '.obj'
		model_path = path + model_id
		if id2 not in placed_models:
			
			#dims2 = data[full_id]['dims']
			try:
				rotation_info = data[full_id]['up']
				unit = float(data[full_id]['unit'][0])
			except:
				rotation_info = (0,0,0)
				unit = 1.0
			# data['wss.'+filename]['dims'] = data['wss'+id1]['dims']
			x_rot = 0
			y_rot = 0
			z_rot = 0
			model_id = id2 + '.obj'
			model_path = path + model_id
			if id2 in combined_models:
				print("\n\n\n\nCOMMAND WENT HERE\n\n\n")
				model_path = path2 + model_id
			imported_object = bpy.ops.import_scene.obj(filepath=model_path)
			print("Object", model_id, "imported")
			obj_object = bpy.context.selected_objects[0] 
			obj_object.delta_scale = (unit, unit, unit)
			obj_object.rotation_euler = (x_rot, y_rot, z_rot)
			bpy.ops.object.origin_set(type = 'GEOMETRY_ORIGIN')
			x_dims_count += (float(dims2[0]))/200 
			y_dims_count += (float(dims2[1]))/200 
			z_dims_count += (float(dims2[2]))/200
			x = x_dims_count + (float(dims2[0]))/100
			z = z_dims_count + (float(dims2[2]))/100


			obj_object.location = ( z,placed_models[id1][1],placed_models[id1][2])
			#x_dims_count += (float(dims[0]))/100
			placed_models[id2] = (placed_models[id1][1],placed_models[id1][2],z)
		else:
			#x_dims_count += (float(dims[0]))/200 
			#y_dims_count += (float(dims[1]))/200 
			z_dims_count += (float(dims2[2]))/200
			#x = x_dims_count + (float(dims[0]))/100
			#z = z_dims_count + (float(dims[2]))/100

			#obj_object = bpy.data.objects[id2]
			#obj_object.location=(z,placed_models[id1][1],placed_models[id1][2])
			#placed_models[id2] = (placed_models[id1][1],placed_models[id1][2],z)
	elif line2[1] == 'behind':
			print("\n\n\nbehind PLACEMENT\n\n\n\n")
			id1 = ids[nouns.index(line2[0])]
			id1 = id1.strip()
			print("\n\nRecieved ID1 is", id1)
			id2 = ids[nouns.index(line2[2])]
			id2 = id2.strip()
			print("\n\nRecieved ID2 is", id2)
			full_id =id1
			id1=id1[4:]
			dims = data[full_id]['dims']
			# rotation_info = data[full_id]['up']
			# unit = float(data[full_id]['unit'][0])
			try:
				rotation_info = data[full_id]['up']
				unit = float(data[full_id]['unit'][0])
			except:
				rotation_info = (0,0,0)
				unit = 1.0
			x_rot = 0
			y_rot = 0
			z_rot = 0
			model_id = id1 + '.obj'
			mtl_id = id1 + '.mtl'
			model_path = path + model_id
			print('\n\n\n\n\n\n\n')
			path1 = "D:/Text_to_scene_generation-master/Text_to_scene_generation-master/models-OBJ/models/"
			#path2 = "/Volumes/My Passport/SHAPE/Models/Volumes/My Passport/SHAPE/Models/"
			if id1 not in combined_models:
				print(os.system("cd " + path1 + '\n' + 'copy ' + model_id + ' D:/Text_to_scene_generation-master/Text_to_scene_generation-master/Models/'))
				print(os.system("cd " + path1 + '\n' + 'copy ' + mtl_id + ' D:/Text_to_scene_generation-master/Text_to_scene_generation-master/Models/'))
				# os.system("cd " + path1 + '\n' + 'open ' + model_id + '.obj')
			else:
				model_path = path1 + model_id
				print("\n\n\n\nPATH CHANGED\n\n\n\n")

			if id1 not in placed_models:
				imported_object = bpy.ops.import_scene.obj(filepath=model_path)
				print("Object", model_id, "imported")
				obj_object = bpy.context.selected_objects[0]
				obj_object.delta_scale = (unit, unit, unit)
				obj_object.rotation_euler = (x_rot, y_rot, z_rot)
				bpy.ops.object.origin_set(type = 'GEOMETRY_ORIGIN')
				obj_object.location = (0, 0, 0)
				x_dims_count += (float(dims[0]))/200 
				y_dims_count += (float(dims[1]))/200 
				z_dims_count += (float(dims[2]))/200
				placed_models[id1] = (0, 0, 0)
			else:
				print("\n\nMODEL", id1, "ALREADY IMPORTED\n\n")
				# x_dims_count = placed_models[id1][0] + (float(dims[0]))/200
				x_dims_count = placed_models[id1][0]
				y_dims_count = placed_models[id1][1] + (float(dims[1]))/200
				z_dims_count = placed_models[id1][2] + (float(dims[2]))/200

			full_id =id2
			id2=id2[4:]
			dims = data[full_id]['dims']
			# rotation_info = data[full_id]['up']
			try:
				unit = float(data[full_id]['unit'][0])
			except:
				unit = 1
			x_rot = 0
			y_rot = 0
			z_rot = 0
			model_id = id2 + '.obj'
			model_path = path + model_id
			if id2 not in placed_models:
				full_id =id2
				id2=id2[4:]
				dims2 = data[full_id]['dims']
				try:
					rotation_info = data[full_id]['up']
					unit = float(data[full_id]['unit'][0])
				except:
					rotation_info = (0,0,0)
					unit = 1.0
				# data['wss.'+filename]['dims'] = data['wss'+id1]['dims']
				x_rot = 0
				y_rot = 0
				z_rot = 0
				model_id = id2 + '.obj'
				model_path = path + model_id
				if id2 in combined_models:
					print("\n\n\n\nCOMMAND WENT HERE\n\n\n")
					model_path = path2 + model_id
				imported_object = bpy.ops.import_scene.obj(filepath=model_path)
				print("Object", model_id, "imported")
				obj_object = bpy.context.selected_objects[0] 
				obj_object.delta_scale = (unit, unit, unit)
				obj_object.rotation_euler = (x_rot, y_rot, z_rot)
				bpy.ops.object.origin_set(type = 'GEOMETRY_ORIGIN')
				#x_dims_count += (float(dims[0]))/200 
				#y_dims_count += (float(dims[1]))/200 
				z_dims_count += (float(dims[2]))/200
				#x = x_dims_count + (float(dims[0]))/100
				z = z_dims_count + (float(dims[2]))/100


				obj_object.location = ( z,placed_models[id1][1],placed_models[id1][2])
				#x_dims_count += (float(dims[0]))/100
				placed_models[id2] = (placed_models[id1][1],placed_models[id1][2],z)
			else:
				#x_dims_count += (float(dims[0]))/200 
				#y_dims_count += (float(dims[1]))/200 
				z_dims_count += (float(dims[2]))/200
				#x = x_dims_count + (float(dims[0]))/100
				#z = z_dims_count + (float(dims[2]))/100

				#obj_object = bpy.data.objects[id2]
				#obj_object.location=(z,placed_models[id1][1],placed_models[id1][2])
				#placed_models[id2] = (placed_models[id1][1],placed_models[id1][2],z)

	# bpy.ops.object.select_all(action = 'DESELECT')
	# bpy.context.space_data.show_textured_solid = True
	# bpy.types.SpaceView3D('show_textured_solid')``
print(placed_models)

#fin.close()
fp_data.close()

for i in placed_models:
	print(i, "placed at position", placed_models[i])
print("PROGRAM RAN SUCCESSFULLY")
