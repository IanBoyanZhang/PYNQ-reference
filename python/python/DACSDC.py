import os
import matplotlib.pylab as plt
import cv2
import time
import xml.dom.minidom

count = 0
batchsize = 500


##default work directory for each team
DAC = '/home/xilinx/jupyter_notebooks/DAC'

imgdir = '/home/xilinx/jupyter_notebooks/DAC/images'
overlaydir = '/home/xilinx/jupyter_notebooks/DAC/overlay'
result = '/home/xilinx/jupyter_notebooks/DAC/result'

timedir = '/home/xilinx/jupyter_notebooks/DAC/result/time'
coordir = '/home/xilinx/jupyter_notebooks/DAC/result/coordinate'
xmlpath = '/home/xilinx/jupyter_notebooks/DAC/result/xml'

alltime = '/home/xilinx/jupyter_notebooks/DAC/result/time/alltime.txt'
##must be called to creat default directory
def startup(teamname):
    mycoord = coordir + '/' + teamname
    myxml = xmlpath +'/' + teamname
    
    if os.path.isdir(DAC):
        pass
    else:
        os.mkdir(DAC)
        
    if os.path.isdir(imgdir):
        pass
    else:
        os.mkdir(imgdir)
        
    if os.path.isdir(overlaydir):
        pass
    else:    
        os.mkdir(overlaydir)
        
    if os.path.isdir(result):
        pass
    else:
        os.mkdir(result)
        
    if os.path.isdir(timedir):
        pass
    else:    
        os.mkdir(timedir)
        
    if os.path.isdir(coordir):
        pass
    else:    
        os.mkdir(coordir)
        
    if os.path.isdir(xmlpath):
        pass
    else:
        os.mkdir(xmlpath)
        
    if os.path.isdir(mycoord):
        pass
    else:
        os.mkdir(mycoord)
            
    if os.path.isdir(myxml):
        pass
    else:
        os.mkdir(myxml)
##create timefile file
    ftime = open(alltime,'a+')
    ftime.close()
    return [DAC,imgdir,overlaydir,result,timedir,coordir,xmlpath,mycoord,myxml]
    
    
##get image name list
def getnames():
    nameset1 = []
    namefiles= os.listdir(imgdir)
    for f in namefiles:
        if 'jpg' in f:
            imgname = f.split('.')[0]
            nameset1.append(imgname)
    nameset1.sort(key = int)
    for f in range(len(nameset1)):
        nameset1[f] = nameset1[f]  + ".jpg"
    return nameset1

##batch the images, may help when write to XML
def getnamesbatch():
    nameset1 = []
    nameset3 = []
    nameset4 = []
    namefiles= os.listdir(imgdir)
    for f in namefiles:
        if 'jpg' in f:
            imgname = f.split('.')[0]
            nameset1.append(imgname)
    nameset1.sort(key = int)
    for f in range(len(nameset1)):
        nameset1[f] = nameset1[f]  + ".jpg"
    for i in range (0, len(nameset1), batchsize):
        nameset3 = nameset1[i:i+batchsize]
        nameset4.append(nameset3)
    return nameset4

##get imagepath list
def getpath():
    set1 = []
    files= os.listdir(imgdir)
    for f in files:
        if 'jpg' in f:
            imgname = f.split('.')[0]
            set1.append(imgname)
    set1.sort(key = int)
    for f in range(len(set1)):
        set1[f] = imgdir +"/" + set1[f] + ".jpg"
    return set1

##batch the images dir
def getpathbatch():
    set1 = []
    set3 = []
    set4=  []
    files= os.listdir(imgdir)
    for f in files:
        if 'jpg' in f:
            imgname = f.split('.')[0]
            set1.append(imgname)
    set1.sort(key = int)
    for f in range(len(set1)):
        set1[f] = imgdir +"/" + set1[f] + ".jpg"
    for i in range (0, len(set1), batchsize):
        set3 = set1[i:i+batchsize]
        set4.append(set3)
    return set4
    
##when "send" is called, it will return a batch of image dir   
def send(interval_time, sendlist):
    global count
    time.sleep(interval_time)
    set3 = sendlist
    tmp = set3 [count] 
    # im_array = cv2.imread(tmp)
    count = count + 1
    return tmp

##reset the global count
def reset():
    global count
    count = 0
    return

##write time result to alltime.txt
def write(tbatch,totalimg,teamname):
    # tt = tbatch / int((totalimg/batchsize))
    FPS = totalimg / tbatch
    ftime = open(alltime, 'a+')
    ftime.write( "\n" + teamname + " Frames per second:" + str((FPS)) + '\n') 
    ftime.close()
    return


def storeResultsToXML(resultRectangle, allImageName, myxml):
    for i in range(len(allImageName)):
        doc = xml.dom.minidom.Document()
        root = doc.createElement('annotation')

        doc.appendChild(root)
        nameE = doc.createElement('filename')
        nameT = doc.createTextNode(allImageName[i])
        nameE.appendChild(nameT)
        root.appendChild(nameE)

        sizeE = doc.createElement('size')
        nodeWidth = doc.createElement('width')
        nodeWidth.appendChild(doc.createTextNode("640"))
        nodelength = doc.createElement('length')
        nodelength.appendChild(doc.createTextNode("360"))
        sizeE.appendChild(nodeWidth)
        sizeE.appendChild(nodelength)
        root.appendChild(sizeE)

        object = doc.createElement('object')
        nodeName = doc.createElement('name')
        nodeName.appendChild(doc.createTextNode("NotCare"))
        nodebndbox = doc.createElement('bndbox')
        nodebndbox_xmin = doc.createElement('xmin')
        nodebndbox_xmin.appendChild(doc.createTextNode(str(resultRectangle[i][0])))
        nodebndbox_xmax = doc.createElement('xmax')
        nodebndbox_xmax.appendChild(doc.createTextNode(str(resultRectangle[i][1])))
        nodebndbox_ymin = doc.createElement('ymin')
        nodebndbox_ymin.appendChild(doc.createTextNode(str(resultRectangle[i][2])))
        nodebndbox_ymax = doc.createElement('ymax')
        nodebndbox_ymax.appendChild(doc.createTextNode(str(resultRectangle[i][3])))
        nodebndbox.appendChild(nodebndbox_xmin)
        nodebndbox.appendChild(nodebndbox_xmax)
        nodebndbox.appendChild(nodebndbox_ymin)
        nodebndbox.appendChild(nodebndbox_ymax)

        #nodebndbox.appendChild(doc.createTextNode("360"))
        object.appendChild(nodeName)
        object.appendChild(nodebndbox)
        root.appendChild(object)

        fileName = allImageName[i].replace('jpg', 'xml')
        # print (fileName)
        fp = open(myxml + "/" + fileName + ".xml", 'w')
        doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")
    return