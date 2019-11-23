import videoto3d
import os
import os.path
from os import path
import numpy as np
import send2trash
import csv

def convertToNumpy(pasta):
    caminho = os.path.dirname(os.path.abspath(__file__))
    pwd = caminho + pasta
    img_rows, img_cols, frames = 32, 32, 10
    color= False
    skip = True
    if color:
        channel=3
    else:
        channel=1
    vid3d = videoto3d.Videoto3D(img_rows, img_cols, frames)
    X = []
    labels = []
    labellist = []
    count=[]
    files = os.listdir(pwd)
    for filename in files:
        print(filename)
        labellist.append(filename)
    for filename in labellist:
        path=pwd+filename
        x=[]
        count.append(len(os.listdir(path)))
        for video in os.listdir(path):
            try:
                pic=vid3d.video3d(path+'/'+video, color=color, skip=skip)
                pic=pic.transpose((1,2,0))
                pic=pic.reshape((img_rows,img_cols,frames,channel))
                x.append(pic)
            except:
                print(path+'/'+video)
        X.append(x)
    for ix in range(len(count)):
        for ij in range(count[ix]):
            labels.append(labellist[ix])
    labels=np.asarray(labels)
    # cria a pasta output
    pathOut = caminho + '/output'
    #print(pathOut)
    if os.path.exists(pathOut):
        send2trash.send2trash('output')
    pathOut = pathOut + '/'   
    os.mkdir(pathOut)
    
    #Cria o CSV
    with open('output/test.csv', 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        csvData = ["filename","nome"]
        writer.writerow(csvData)
    csvFile.close()
    
    for ix in range(len(X)):
        newpath = os.path.join(pathOut,labellist[ix])
        os.mkdir(newpath)
        for ij in range(len(X[ix])):
            image=X[ix][ij]
            csvData = ['/'+labellist[ix]+'/'+str(ij)+'.npz',str(ij)]
            with open('output/test.csv', 'a', newline='') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(csvData)
            csvFile.close()
            np.savez('output/'+labellist[ix]+'/'+str(ij)+'.npz',image)
        
    
if __name__ == '__main__':
    convertToNumpy()
 

