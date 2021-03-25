# importing modules required
import cv2                                                       #open cv 
import face_recognition                                          #face recognition
import time                                                      #time
import numpy as np                                               #for converting face landmarks in numpy array form
from scipy.spatial import distance as dist                       #for measuring euclidean distance and furthur calculation
import playsound                                                 #for playing alarm sound audio
from threading import Thread                                     #for playing audio simuntaneously with detection and execute multiple things simuntaneously

#________________________________________________________________________________________________________________________________________________________________________



MIN_AER = 0.30                                                  #eye aspect ratio to indicate blink
EYE_AR_CONSECAMES = 10                                          #number of consecutive frames


#________________________________________________________________________________________________________________________________________________________________________


COUNTER = 0                                                     #initialize and set the frame counter
ALARM_ON = False                                                #indicate when alarm is going off

#________________________________________________________________________________________________________________________________________________________________________


def eye_aspect_ratio(eye):
                                                                #euclidean distances between the two sets of vertical eye landmarks 
 A = dist.euclidean(eye[1], eye[5])
 B = dist.euclidean(eye[2], eye[4])

                                                                # euclidean distance between the horizontal eye landmark 
 C = dist.euclidean(eye[0], eye[3])

                                                                #eye aspect ratio
 ear = (A + B) / (2.0 * C)                                      #vertical divided by 2 times horizontal

                                                                # return the eye aspect ratio
 return ear

 #________________________________________________________________________________________________________________________________________________________________________


def sound_alarm(alarm_file):
                                                               #for playing alarm sound
 playsound.playsound(alarm_file)

 #________________________________________________________________________________________________________________________________________________________________________

 
def main():
    global COUNTER
    video_capture = cv2.VideoCapture(0)                        #capturing video 
    while True:
        ret, frame = video_capture.read(0)
        
        face_landmarks_list = face_recognition.face_landmarks(frame)

                                                               # getting eyes
        for face_landmark in face_landmarks_list:
                        leftEye = face_landmark['left_eye']
                        rightEye = face_landmark['right_eye']
                        #eye aspect ratio for left and right eyes
                        leftEAR = eye_aspect_ratio(leftEye)
                        rightEAR = eye_aspect_ratio(rightEye)
                        # average eye aspect ratio for both eyes
                        ear = (leftEAR + rightEAR) / 2
                        #left and right eye values in numpy arrays
                        lpts = np.array(leftEye)
                        rpts = np.array(rightEye)
                        #showing line from left of left eye and right of right eye
                        cv2.polylines(frame, [lpts],True ,(255,255,0), 1)
                        cv2.polylines(frame, [rpts],True ,(255,255,0), 1)
                        
                        #if the eye aspect ratio is below the blink threshold, increase the blink frame counter
                        if ear < MIN_AER:
                                COUNTER+= 1

                                # if the eyes were closed for a sufficient time then sound the alarm
                                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                                        # if the alarm is not on,then turn it on
                                        if not ALARM_ON:
                                                ALARM_ON = True
                                                t = Thread(target=sound_alarm,
                                                                args=('alarm.wav',))
                                                t.deamon = True#task completed main exits
                                                t.start()

                                        #set alarm on frame
                                        cv2.putText(frame, "DROWSINESS", (10, 30),
                                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        #else the "ear" is not below the blink threshold, so reset the counter & alarm
                        else:
                                COUNTER = 0
                                ALARM_ON = False

                        #sketch the computed "ear" on frame to set the correct "ear" thresholds and frame counters
                        cv2.putText(frame, "EAR: {:.2f}".format(ear), (500, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
 
                        # showing frame
                        cv2.imshow("DROWSINESS DETECTION SYSTEM", frame)

        # break from the loop when`k` key  pressed, 
        if cv2.waitKey(1) & 0xFF == ord('k'):
                break
    #clean
    video_capture.release()
    cv2.destroyAllWindows()

#________________________________________________________________________________________________________________________________________________________________________





#executes all of the code
if __name__ == "__main__":
        for char in __doc__:
                print(char,end='')
        print()
        main()
        