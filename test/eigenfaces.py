#OpenCV module
import cv2.cv2
#os module for reading training data directories and paths
import os
#numpy to convert python lists to numpy arrays as it is needed by OpenCV face recognizers
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import sklearn as sk
from sklearn.svm import SVC  #esto para importar el clasificador vectorial
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
from sklearn.decomposition import PCA
from sklearn.datasets.base import Bunch



#there is no label 0 in our training data so subject name for index/label 0 is empty
subjects = ["", "Max Pizarro", "Mateo Decu"]
svc_3 = SVC(kernel='linear')  #esto es clasificador o Classifier cuyo modelos es un hiperplano que separa instancias (puntos) de una clase del resto
clf = SVC(gamma=0.001, C=100.)

def train_and_evaluate(clf, X_train, X_test, y_train, y_test):
    
    clf.fit(X_train, y_train)
    
    print("Exactitud training set:")
    print(clf.score(X_train, y_train))
    print("Exactitud testing set:")
    print(clf.score(X_test, y_test))
    
    y_pred = clf.predict(X_test)
    
    print("Reporte de Classificador:")
    print(metrics.classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(metrics.confusion_matrix(y_test, y_pred))

def print_faces(images, target, top_n):
    # configuramos el tamanio de las imagenes por pulgadas
    fig = plt.figure(figsize=(12, 12))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=0.05, wspace=0.05)
    for i in range(top_n):
        # graficamos las imagenes en una matriz de 20x20
        p = fig.add_subplot(20, 20, i + 1, xticks=[], yticks=[])
        p.imshow(images[i], cmap=plt.cm)
        # etiquetamos las imagenes con el valor objetivo (target value)
        p.text(0, 14, str(target[i]))
        p.text(0, 60, str(i))    
#function to detect face using OpenCV
def detect_face(img):
    #convert the test image to gray scale as opencv face detector expects gray images
    gray = cv2.cv2.cvtColor(img, cv2.cv2.COLOR_BGR2GRAY)

    #load OpenCV face detector, I am using LBP which is fast
    #there is also a more accurate but slow: Haar classifier
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    #let's detect multiscale images(some images may be closer to camera than others)
    #result is a list of faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);

    #if no faces are detected then return original img
    if (len(faces) == 0):
        return None, None

    #under the assumption that there will be only one face,
    #extract the face area    
    x, y, w, h = faces[0]
    #return only the face part of the image
    return gray[y:y+w, x:x+h], faces[0]


#and will return two lists of exactly same size, one list 
#of faces and another list of labels for each face
def prepare_training_data(data_folder_path):
         
        #------STEP-1--------
        #get the directories (one directory for each subject) in data folder
        dirs = os.listdir(data_folder_path)
        #print(dirs)
         
        #list to hold all subject faces
        faces = []
        #list to hold labels for all subjects
        labels = []
         
        #let's go through each directory and read images within it
        for dir_name in dirs:
             
            #our subject directories start with letter 's' so
            #ignore any non-relevant directories if any
            if not dir_name.startswith("s"):
                continue;
              
            #------STEP-2--------
            #extract label number of subject from dir_name
            #format of dir name = slabel
            #, so removing letter 's' from dir_name will give us label
            label = int(dir_name.replace("s", ""))
             
            #build path of directory containing images for current subject subject
            #sample subject_dir_path = "training-data/s1"
            subject_dir_path = data_folder_path + "/" + dir_name
             
            #get the images names that are inside the given subject directory
            subject_images_names = os.listdir(subject_dir_path) 
            #------STEP-3--------
            #go through each image name, read image, 
            #detect face and add face to list of faces
            for image_name in subject_images_names:
             
                #ignore system files like .DS_Store
                if image_name.startswith("."):
                    continue;
                 
                #build image path
                #sample image path = training-data/s1/1.pgm
                image_path = subject_dir_path + "/" + image_name
                
                #read image
                image = cv2.imread(image_path)
                 
                #display an image window to show the image 
                cv2.imshow("Training on image...", image)
                cv2.waitKey(100)
                #detect face
                face, rect = detect_face(image)
         
                #------STEP-4--------
                #for the purpose of this tutorial
                #we will ignore faces that are not detected
                if face is not None:
                    #add face to list of faces
                    faces.append(face)
                    #add label for this face
                    labels.append(label)
                     
                    cv2.destroyAllWindows()
                    cv2.waitKey(1)
                    cv2.destroyAllWindows()
         
        return faces, labels
    
	
#let's first prepare our training data
#data will be in two lists of same size
#one list will contain all the faces
#and the other list will contain respective labels for each face
print("Preparing data...")
faces, labels = prepare_training_data("../resources")
print("Data prepared")
 
#print total faces and labels
print("Total faces: ", len(faces))
print("Total labels: ", len(labels))    



#eval_faces = [np.reshape(a, (64, 64)) for a in faces]


rostros=Bunch(DESCR="descripcion dataset", keys=['target', 'DESCR', 'data', 'images'],
            images=faces,data=len(faces),target=np.asarray(faces))

#imprimimos propiedades del dataset faces.data contiene el puntero de la lista y faces.target la lista de imagenes en cuestion
print(rostros.DESCR)
print(rostros.keys())
print(rostros.images)
print(rostros.data)
print(rostros.target.shape)
	
#create our LBPH face recognizer 
#face_recognizer = cv2.face.createLBPHFaceRecognizer()
 
#or use EigenFaceRecognizer by replacing above line with 
#face_recognizer = cv2.face.createEigenFaceRecognizer()
 
#or use FisherFaceRecognizer by replacing above line with 
#face_recognizer = cv2.face.createFisherFaceRecognizer()

#train our face recognizer of our training faces
#train_and_evaluate(svc_3, X_train, X_test, y_train, y_test)	
#function to draw rectangle on image 
#according to given (x, y) coordinates and 
#given width and heigh
def draw_rectangle(img, rect):
     (x, y, w, h) = rect
     cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
 
#function to draw text on give image starting from
#passed (x, y) coordinates. 
def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

	
#this function recognizes the person in image passed
#and draws a rectangle around detected face with name of the 
#subject
def predict(test_img):
    #make a copy of the image as we don't want to change original image
    img = test_img.copy()
    #detect face from the image
   # face, rect = detect_face(img)
    #predict the image using our face recognizer 
    
    label= svc_3.predict(img)
    #get name of respective label returned by face recognizer
    label_text = subjects[label]

    #draw a rectangle around face detected
   # draw_rectangle(img, rect)
    #draw name of predicted person
    #draw_text(img, label_text, rect[0], rect[1]-5)
     
    return img 

	
print("Predicting images...")
 
#load test images
test_img1 = cv2.imread("../resources/s1/maxi.png")
#plt.imshow(test_img1)
#plt.show()
test_img2 = cv2.imread("../resources/s2/mateo.png")
#predicted_img1 = predict(test_img1)

X_train, X_test, y_train, y_test=train_test_split(faces, labels, random_state=0)
 
#perform a prediction

svc_3.fit(X_train,y_train)
#y_pred = svc_3.predict(X_train)
#train_and_evaluate(svc_3, X_train, X_test, y_train, y_test)
#y_pred = svc_3.predict(X_test)

#train_and_evaluate(svc_3, X_train, X_test, test_img2, y_test)
##predicted_img1 = predict(test_img1)
##predicted_img2 = predict(test_img2)
print("Prediction complete")

 #esto es para abrir un frame donde se pegan las imagenes



#plt.imshow(pca.mean_.reshape(faces.images[0].shape),
 #          cmap=plt.cm.bone)



#fig = plt.figure(figsize=(16, 6))
#for i in range(30):
 #   ax = fig.add_subplot(3, 10, i + 1, xticks=[], yticks=[])
  #  ax.imshow(pca.components_[i].reshape(faces.images[0].shape),
   #           cmap=plt.cm.bone)
    
#display both images
##cv2.imshow(subjects[1], predicted_img1)
##cv2.imshow(subjects[2], predicted_img2)
##cv2.waitKey(0)
cv2.destroyAllWindows()
 