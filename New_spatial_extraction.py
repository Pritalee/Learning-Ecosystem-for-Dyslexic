import spacy
import neuralcoref
import csv
import json
import os,sys
import nltk
from spacy import displacy
nlp = spacy.load("en_core_web_sm")
nlp = spacy.load('en')
neuralcoref.add_to_pipe(nlp)

nouns= []
visited = []
landmark = []
prep = []
trajector = []

with open('Spatial_Relation_test.txt','w'): pass
with open('nouns_and_IDs.txt','w'): pass

def dfs(visited, graph, node):

    global landmark, prep, trajector

    if node not in visited:
        if node.dep_ is "prep" :
            prep.append(node.text)

        if node.dep_ is "pobj" or node.dep_ is "pcomp":
            landmark.append(node.text)

        if node.dep_ is "nsubj" or node.dep_ is "acomp" :
            trajector.append(node.text)

        if node.dep_ is "attr":
            trajector.append(node.text)

        if  node.dep_ is "nsubjpass" :
            trajector.append(node.text)

        visited.append(node)

        for neighbour in node.children:
            dfs(visited, graph, neighbour)

def specialcase1(string):
    global landmark, prep, trajector
    print("Special case")

    for t in nlp(string):
        print("text",t.text)
        print("t.dep_",t.dep_)
        if t.dep_ is "nsubj" or t.dep_ is "attr" or t.dep_ is "nsubjpass" or t.dep_ is "csubj":
            trajector.append(t.text)
            
        if t.dep_ is "pobj" or t.dep_ is "pcomp":
            landmark.append(t.text)
            
    print("check",landmark[0])
    prep = landmark[0]
    landmark = landmark[-1]
    if landmark[0]:
            nouns.append(landmark)
    if trajector[0]:
            nouns.append(trajector[0])
    with open('Spatial_Relation_test.txt', 'a', newline='') as file:
            S=landmark+" "+prep+" "+trajector[0]+"."
            file.write(S)

    print("Trajector",trajector)
    print("Prep",prep)
    print("Landmark",landmark)


def first_call(string):
    # print("1")
    global prep, landmark, trajector
    trajector =[]
    prep= []
    landmark =[]

    if "left" in string or "right" in string or "front" in string or "behind" in string:
        specialcase1(string)
    else:
        print("HERE")
        graph = nlp(string)
        for t in range(len(graph)):
            if graph[t].dep_ ==  "ROOT" :
                root = graph[t]
                print("ROOT",root)
                break
        dfs(visited, graph, root)
        print("trajector",trajector[0])
        if landmark[0]:
            nouns.append(landmark[0])
        if trajector[0]:
            nouns.append(trajector[0])
        with open('Spatial_Relation_test.txt', 'a', newline='') as file:
            S=landmark[0]+" "+prep[0]+" "+trajector[0]+"."
            file.write(S)
        print("Trajector",trajector)
        print("Prep",prep)
        print("Landmark",landmark)

def start(doc):
   
    print("Original Sentence",doc)
    if doc._.has_coref:
        # print(type(doc._.coref_resolved))
        print("Reference Resolution ",doc._.coref_resolved)
        doc = doc._.coref_resolved

    sentences = str(doc).split(".")
    sentences=[s for s in sentences if s]

    print("Sentences",sentences)
    for string in sentences:
        # print("HERE",string)
        if "and" in string:
            parts = string.split(" and")
            print(len(parts))
            print("P",parts)

            for p in range(len(parts)):
                if "is" in parts[p] or "are" in parts[p]:
                    print("Yes",parts[p].replace("are", "is"))
                    first_call(parts[p].replace("are", "is"))
                else:
                    print("No",parts[p])
                    if "is" in parts[p+1] :
                        sentence = parts[p]+" is "+str(parts[p+1].split("is")[1])
                        print("S",sentence)
                        first_call(sentence)
                    elif "are" in parts[p+1]:
                        sentence = parts[p]+" is "+str(parts[p+1].split("are")[1])
                        print("S",sentence)
                        first_call(sentence)
                    else:
                        print("some other verb detected")


           

        else:
            first_call(string)
inp=sys.argv[1:]
sent=' '.join(str(elem) for elem in inp)



print("sent",sent)
start(nlp(sent))

#nouns=landmark+trajector
print(nouns)
nouns=list(dict.fromkeys(nouns))
print(nouns)

#noun_extracted=list(set(nouns))
with open("new_nouns_ids.txt", 'r') as f:
    d = json.load(f)


ids=[]
sim={}
for i in nouns:
    try:
        ids.append(d[i])
        ni=i+" "+d[i]
        
    except:
        for j in d:
            cos=nltk.edit_distance(i,j)
            sim[cos]=j

        simi=sorted(sim)
        sid=sim[simi[0]]
        ids.append(d[sid])
        ni=j+" "+d[sid]
    with open('nouns_and_IDs.txt', 'a', newline='') as noun_id:
            noun_id.write(ni)
            print("ni",ni)
            noun_id.write("\n")
            
    
print(ids)
os.system('blender blank.blend --python blender_modified_room1.py')

