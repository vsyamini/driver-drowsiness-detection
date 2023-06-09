# importing the necessary packages
from scipy.spatial import distance as dist
from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2
import matplotlib.animation as animation
import time
import matplotlib.pyplot as plt
import os
from datetime import date
import statistics
import serial
flag_alert=0
arduino = serial.Serial(port='COM4', baudrate=9600, timeout=.1)
def write_read(x):
    arduino.write(x)
    time.sleep(0.05)
    data = arduino.readline()
    return data
#calculating eye aspect ratio
def eye_aspect_ratio(eye):
	# compute the euclidean distances between the vertical
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])

	# compute the euclidean distance between the horizontal
	C = dist.euclidean(eye[0], eye[3])
	# compute the eye aspect ratio
	ear = (A + B) / (2.0 * C)
	return ear

#calculating mouth aspect ratio
def mouth_aspect_ratio(mou):
	# compute the euclidean distances between the horizontal
	X   = dist.euclidean(mou[0], mou[6])
	# compute the euclidean distances between the vertical
	Y1  = dist.euclidean(mou[2], mou[10])
	Y2  = dist.euclidean(mou[4], mou[8])
	# taking average
	Y   = (Y1+Y2)/2.0
	# compute mouth aspect ratio
	mar = Y/X
	return mar

camera = cv2.VideoCapture(0)
predictor_path = 'shape_predictor_68_face_landmarks.dat'


file1 = open("PreProcessed.txt","r+")#append mode
file1.truncate(0) # need '0' when using r+
file1.close()
file1 = open("PreProcessed.txt","a")#append mode
file1.write(str(0)+','+str(0)+','+str(0)+"\n")
file1.close()

file2 = open("class2.txt","r+")#append mode
file2.truncate(0) # need '0' when using r+
file3 = open("class3.txt","r+")#append mode
file3.truncate(0) # need '0' when using r+
file4 = open("class5.txt","r+")#append mode
file4.truncate(0) # need '0' when using r+

file5 = open("features.txt","r+")#append mode
file5.truncate(0) # need '0' when using r+

def f(t):
    return np.exp(-t) * np.cos(2*np.pi*t)

t1 = np.arange(0.0, 5.0, 0.1)
t2 = np.arange(0.0, 5.0, 0.02)

# define constants for aspect ratios
EYE_AR_THRESH = 0.25
EYE_AR_CONSEC_FRAMES = 48
MOU_AR_THRESH = 0.55

COUNTER = 0
yawnStatus = False
yawns = 0
Total_yawns=0
# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

# grab the indexes of the facial landmarks for the left and right eye
# also for the mouth
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]
#execfile('ex2.py')
No_of_Frame=0
a=[]
eye_flag=0
CS_data=[]
rOS_data=[]
BD_data=[]
PERCLOS_data=[]
B_count=0
# loop over captuing video
while True:
	# grab the frame from the camera, resize
	# it, and convert it to grayscale
	# channels)
	ret, frame = camera.read()
	frame = imutils.resize(frame, width=640)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	prev_yawn_status = yawnStatus
	# detect faces in the grayscale frame
	rects = detector(gray, 0)
        
	# loop over the face detections
	for rect in rects:
                No_of_Frame=No_of_Frame+1
		# determine the facial landmarks for the face region, then
		# convert the facial landmark (x, y)-coordinates to a NumPy
		# array
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)

		# extract the left and right eye coordinates, then use the
		# coordinates to compute the eye aspect ratio for both eyes
		leftEye = shape[lStart:lEnd]
		rightEye = shape[rStart:rEnd]
		mouth = shape[mStart:mEnd]
		leftEAR = eye_aspect_ratio(leftEye)
		rightEAR = eye_aspect_ratio(rightEye)
		mouEAR = mouth_aspect_ratio(mouth)
		# average the eye aspect ratio together for both eyes
		ear = (leftEAR + rightEAR) / 2.0
                a.append(ear)
                print np.mean(a)
		# compute the convex hull for the left and right eye, then
		# visualize each of the eyes
		leftEyeHull = cv2.convexHull(leftEye)
		rightEyeHull = cv2.convexHull(rightEye)
		mouthHull = cv2.convexHull(mouth)
		cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 255), 1)
		cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 255), 1)
		cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)

		# check to see if the eye aspect ratio is below the blink
		# threshold, and if so, increment the blink frame counter
		if ear < EYE_AR_THRESH:
                        
                        if eye_flag==0:
                                CS=a[No_of_Frame-2]-a[No_of_Frame-1]
                                CS_data.append(CS)
                                print("Closing Speed Per Frame % s" %CS)
                                eye_flag=1
                        #ear_var_b_theta.append(ear)
                        #print("Variance of Below Theta EAR is % s" %(statistics.variance(ear_var_b_theta))) 
			COUNTER += 1
			cv2.putText(frame, "Eyes Closed ", (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                        BD=COUNTER/30.0
                        BD_data.append(float("{0:.2f}".format(BD)))
                        cv2.putText(frame, "BLink Duration {:.2f}" .format(BD)+"s", (10,60),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        PERCLOS=(COUNTER/30.0)*100
                        PERCLOS_data.append(float("{0:.2f}".format(PERCLOS)))
                        cv2.putText(frame, "PERCLOS : {:.2f}" .format(PERCLOS)+"%", (10,90),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
			
			# if the eyes were closed for a sufficient number of
			if COUNTER >= EYE_AR_CONSEC_FRAMES:

				write_read("*b") #v2.putText(frame, "DROWSINESS ALERT!", (10, 50),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                #write_read("*b")
                # write_read("")otherwise, the eye aspect ratio is not below the blink
		# threshold, so reset the counter and alarm
		else:
                        if eye_flag==1:
                                B_count+=1
                                rOS=a[No_of_Frame-1]-a[No_of_Frame-2]
                                rOS_data.append(rOS)
                                print("Reopening Speed Per Frame % s" %rOS)
                                eye_flag=0
                        if No_of_Frame % 30==0:
                                #BD_data=np.array(BD_data)
                                g = float("{0:.2f}".format(np.mean(PERCLOS_data)))
                                h = float("{0:.2f}".format(np.max(CS_data)))
                                h_mean = float("{0:.2f}".format(np.mean(CS_data)))
                                h_25= float("{0:.2f}".format(np.percentile(CS_data,0.25)))
                                h_50 = float("{0:.2f}".format(np.percentile(CS_data,0.50)))
                                m = float("{0:.2f}".format(np.max(rOS_data)))
                                m_mean = float("{0:.2f}".format(np.mean(rOS_data)))
                                m_50=float("{0:.2f}".format(np.percentile(rOS_data,0.50)))
                                m_75=float("{0:.2f}".format(np.percentile(rOS_data,0.75)))
                         

                                BR=B_count/30.0
                                print("Blink Rate % s" %BR)
                                br_v=float("{0:.2f}".format(BR))
                                cv2.putText(frame, "Blink Rate : {:.2f}" .format(BR)+"s", (10,120),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                                bd_75=float("{0:.2f}".format(np.percentile(BD_data, 0.75)))
         
                                m1=(g+bd_75+h+m+h_mean+m_75+m_mean)/7.0
                                m2=(g+h_25+br_v+m_50+m_75+h+h_50)/7.0
                                m3=(g+m_50+m_mean+h_25+h+m_75+h_mean)/7.0
                                lbl1=0
                                lbl2=0
                                lbl3=0
                                if m1>1.0:
                                        lbl1=1
                                else:
                                        lbl1=0
                                if m2<1.0:
                                        lbl2=0
                                elif m2>1.0 and m2<1.5:
                                        lbl2=1
                                else:
                                        lbl2=2
                                        
                                if m3<0.75:
                                        lbl3=0
                                elif m3>0.75 and m3<1.0:
                                        lbl3=1
                                elif m3>1 and m3<1.25:
                                        lbl3=2
                                elif m3>1.25 and m3<1.75:
                                        lbl3=3
                                else:
                                        lbl3=4                                
                                file2 = open("class2.txt","a")#append mode
                                file2.write(str(g)+','+str(bd_75)+','+str(h)+','+str(m)+','+str(h_mean)+','+str(m_75)+','+str(m_mean)+','+str(lbl1)+"\n") 
                                file2.close()
                                                                                       #time.sleep(2)
                                file3 = open("class3.txt","a")#append mode
                                file3.write(str(g)+','+str(h_25)+','+str(br_v)+','+str(m_50)+','+str(m_75)+','+str(h)+','+str(h_50)+','+str(lbl2)+"\n") 
                                file3.close()
                                file4 = open("class5.txt","a")#append mode
                                file4.write(str(g)+','+str(m_50)+','+str(m_mean)+','+str(h_25)+','+str(h)+','+str(m_75)+','+str(h_mean)+','+str(lbl3)+"\n") 
                                file4.close()
                                B_count=0
                                PERCLOS_data=[0]
                                CS_data=[0]
                                rOS_data=[0]
                                BD_data=[0]
                                #file5= open("features.txt","a")#append mode
                                #file5.write(str(g)+','+str(br_v)+','+str(bd_75)+','+str(h)+','+str(h_mean)+','+str(h_25)+','+str(h_50)+','+str(m)+','+str(m_mean)+','+str(m_50)+','+str(m_75)+','+str(2)+"\n")
                                #file5.write(str(g)+','+str(br_v)+','+str(bd_75)+','+str(h)+','+str(h_mean)+','+str(h_25)+','+str(h_50)+','+str(m)+','+str(m_mean)+','+str(m_50)+','+str(m_75)+','+str(3)+"\n")
                                #file5.write(str(g)+','+str(br_v)+','+str(bd_75)+','+str(h)+','+str(h_mean)+','+str(h_25)+','+str(h_50)+','+str(m)+','+str(m_mean)+','+str(m_50)+','+str(m_75)+','+str(5)+"\n")
                                #file5.close()


                                
                        #ear_var_a_theta.append(ear)
                        #print("Variance of Above Theta EAR  is % s" %(statistics.variance(ear_var_a_theta)))
                        BD=COUNTER/30.0
                        #cv2.putText(frame, "BLink Duration {:.2f}" .format(BD)+"s", (10,50),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
			
			write_read("*a") #v2.putText(frame, "Eyes Open ", (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
			COUNTER = 0

		cv2.putText(frame, "EAR: {:.2f}".format(ear), (480, 30),
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

		# yawning detections

		if mouEAR > MOU_AR_THRESH:
			cv2.putText(frame, "Yawning ", (5, 10),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
			yawnStatus = True
			output_text = "Yawn Count: " + str(yawns + 1)
			cv2.putText(frame, output_text, (10,100),cv2.FONT_HERSHEY_SIMPLEX, 0.7,(255,0,0),2)
			#cv2.putText(frame, output_text, (10,100),cv2.FONT_HERSHEY_SIMPLEX, 0.7,(255,0,0),2)
		else:
			yawnStatus = False

		if prev_yawn_status == True and yawnStatus == False:
			yawns+=1

		cv2.putText(frame, "MAR: {:.2f}".format(mouEAR), (480, 60),
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		cv2.putText(frame,"Driver Fatigue Detection System",(270,470),cv2.FONT_HERSHEY_COMPLEX,0.6,(153,51,102),1)
                print("Frame No %d,EAR %0.2f,MAR %0.2f"%(No_of_Frame,ear,mouEAR))
                g = float("{0:.2f}".format(ear))
                h = float("{0:.2f}".format(mouEAR))
                file1 = open("PreProcessed.txt","a")#append mode
                file1.write(str(No_of_Frame)+','+str(g)+','+str(h)+"\n") 
                file1.close() 
	# show the frame
	
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
        
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
                break
	#plt.plot(t1, f(t1), 'bo', t2, f(t2), 'k')
        #plt.show()

# do a bit of cleanup
cv2.destroyAllWindows()
camera.release()
