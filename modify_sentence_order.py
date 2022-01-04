fin = open("Spatial_Relation_test.txt", 'r')
fout = open("new_sentences.txt", 'w')

data = fin.read().split('.')
data.pop()
for i in data:
	sentence = i.split(' ')
	if sentence[1] not in ['on', 'above']:
		print(i)
		fout.write(i+'\n')
fin.close()
fin = open("Spatial_Relation_test.txt", 'r')
data = fin.read().split('\n')
data.pop()
for i in data:
	sentence = i.split(' ')
	if sentence[1] in ['on', 'above']:
		print(i)
		fout.write(i+'\n')

fout.close()
