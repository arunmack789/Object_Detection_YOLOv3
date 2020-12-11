import numpy as np
import cv2
#print(cv2.__version__)
def objectDectector(img):
    yolo = cv2.dnn.readNet("yolov3.weights","yolov3.cfg")
    classes = []

    with open("coco.names","r") as file:
        classes = [line.strip() for line in file.readlines()]
    layer_names = yolo.getLayerNames()
    output_layer = [layer_names[i[0] -1] for i in yolo.getUnconnectedOutLayers()]   
    color_red = (0, 0, 255)
    color_green = (0, 255, 0)
    
    #name = "img3.jpg"
    #img = cv2.imread(name)
    height, width, channel =  img.shape

    #detect
    blob = cv2.dnn.blobFromImage(img,0.00392,(416,416),(0,0,0),True,crop=True)
    yolo.setInput(blob)
    output = yolo.forward(output_layer)

    class_ids=[]
    confidences = []
    boxes = []

    for outputs in output:
        for detection in outputs:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - (w/2))
                y = int(center_y - (h/2))

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    indexes = cv2.dnn.NMSBoxes(boxes,confidences,0.5,0.4)
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            cv2.rectangle(img,(x, y),(x+w, y+h),color_green,3)
            cv2.putText(img, label,(x,y+30),cv2.FONT_HERSHEY_PLAIN,8,color_red,8)  

    #cv2.imshow("image",img)
    #cv2.imwrite("output.jpg",img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return img