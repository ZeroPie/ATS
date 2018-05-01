import numpy as np
# coding: utf8
#import http://matplotlib.org/1.3.0/users/pyplot_tutorial.html
import matplotlib.pyplot as plt
from numpy import math
import sys

#Vars
i=0
plot =np.zeros((225,4), dtype=float, order='C')     #Init NumpyArray 225x4 Tupel with 0

#Degree in RAD
#DEG90
#DEG270
DEG90 = math.radians(90)
DEG270 = math.radians(270)

#Landmarks
lm1= np.array([3.5, 2])
lm2= np.array([3.5, -2])
lm3=np.array([0, -4])
#Homing position
home=np.array([0, 0])

#Plot homing positio and landmarks
plt.ylabel('y axis')
plt.xlabel('x axis')
plt.plot(3.5,2,'ro',markersize=10)
plt.plot(3.5,-2,'ro',markersize=10)
plt.plot(0,-4,'ro',markersize=10)
plt.plot(0,0,'rx',markersize=15)

#calculate the snapshot

#array([ 0.86824314,  0.49613894]))
#actually cos(2.0/3.5)=>0.86824314
LM1_SNAP=np.array( [ lm1[0]/(np.sqrt(lm1[0]**2+lm1[1]**2)) , lm1[1]/(np.sqrt(lm1[0]**2+lm1[1]**2)) ] )
#array([ 0.86824314, -0.49613894]))
LM2_SNAP=np.array( [ lm2[0]/(np.sqrt(lm2[0]**2+lm2[1]**2)) , lm2[1]/(np.sqrt(lm2[0]**2+lm2[1]**2)) ] )
#array([ 0., -1.]))
LM3_SNAP=np.array( [ lm3[0]/(np.sqrt(lm3[0]**2+lm3[1]**2)) , lm3[1]/(np.sqrt(lm3[0]**2+lm3[1]**2)) ] )

#print("LM1_SNAP:",LM1_SNAP)
#print("LM2_SNAP:",LM2_SNAP)
#print("LM3_SNAP:",LM3_SNAP)

#Angle bisector between LM1 and LM2 calculation
#actually => array(0,0.992)
absLM1LM2vec=LM1_SNAP-LM2_SNAP
#actually => array(0,0.992)
absLM1LM2=np.sqrt( absLM1LM2vec[0]**2 + absLM1LM2vec[1]**2 )
#py shows 0.51914611424652302 => 29,735 DEG but it could be naturally : 
#or just : ( asin(lm1[1]/sqrt(lm1[0]**2 + lm1[1]**2))) + acos(lm1[0]/sqrt(lm1[0]**2 + lm1[1]**2))) ) / 2 => 29,74 DEG
angleLM12s = (np.arccos((absLM1LM2**2-2)/-2)/2)



#Angle bisector between LM2 and LM3 calculation
absLM2LM3vec=LM2_SNAP-LM3_SNAP
absLM2LM3=np.sqrt( absLM2LM3vec[0]**2 + absLM2LM3vec[1]**2 )
angleLM23s = (np.arccos((absLM2LM3**2-2)/-2)/2)

#Angle bisector between LM3 and LM1 calculation. 2Pi because of whole 360 DEG
# actually 5.2382140866588767
angleLM31s=np.pi-angleLM12s-angleLM23s



#Rotate snapshot
#array(1,0)
sLM12R=np.array([
        np.round(np.cos(angleLM12s)*LM1_SNAP[0]         +   np.sin(angleLM12s)*LM1_SNAP[1],8),
        np.round(-1*(np.sin(angleLM12s)*LM1_SNAP[0])    +   np.cos(angleLM12s)*LM1_SNAP[1],8)
    ]);
    
#array(0.5018, -0.864)
sLM22R=np.array([
        np.round(np.cos(angleLM23s)*LM2_SNAP[0]         +   np.sin(angleLM23s)*LM2_SNAP[1],8),
        np.round(-1*(np.sin(angleLM23s)*LM2_SNAP[0])    +   np.cos(angleLM23s)*LM2_SNAP[1],8)
    ]);
#array( 0.8649 , -0.5019 )
sLM31R=np.array([
        np.round(np.cos(angleLM31s)*LM3_SNAP[0]         +   np.sin(angleLM31s)*LM3_SNAP[1],8),
        np.round(-1*(np.sin(angleLM31s)*LM3_SNAP[0])    +   np.cos(angleLM31s)*LM3_SNAP[1],8)
    ]);


#Angle from homing position to LM1
#~4.06 for LM1
hypotenuse=np.sqrt(lm1[0]**2+lm1[1]**2)
#14.22 DEG || 0.24822876392566609 RAD
LM1_snapshot=np.arccos((0.5**2-2*hypotenuse**2)/(-2*hypotenuse**2))*2

#Angle from homing position to LM2
#~4.06 for LM2
hypotenuse=np.sqrt(lm2[0]**2+lm2[1]**2)
#14.22 DEG || 0.24822876392566609 RAD
LM2_snapshot=np.arccos((0.5**2-2*hypotenuse**2)/(-2*hypotenuse**2))*2

#Angle from homing position to LM3
#~4.03 for LM3
hypotenuse=np.sqrt(lm3[0]**2+lm3[1]**2)
#14.00 DEG || 0.25016304718596555 RAD
LM3_snapshot=np.arccos((0.5**2-2*hypotenuse**2)/(-2*hypotenuse**2))*2

#1 RAD => 57,2958

#Passthrough
#0.79006346456737986 => 45.26 DEG
LM1_pass=2*angleLM12s-0.5*LM1_snapshot-0.5*LM2_snapshot
#0.80245430699255793 => 45.97 DEG
LM2_pass=2*angleLM23s-0.5*LM2_snapshot-0.5*LM3_snapshot
#10.227232267761938 => 
#LM3_pass=2*angleLM31s-0.5*LM3_snapshot-0.5*LM1_snapshot
LM3_pass=LM1_pass+LM2_pass

#sys.exit(0)

#Variablen fuer Vturn und Vp
Vturn=np.zeros((1,2), dtype=float, order='C')
Vapproach=np.zeros((1,2), dtype=float, order='C')


#sys.exit(0)

for j in xrange(-7,8): 			# x axis
	for k in xrange(-7,8):			# y axis
		if i<plot.shape[0]:				
			#-----------------------------------------
			if(j==0 and k==-4):
				continue
			else:
				
				orth=np.zeros((1,2),dtype=float,order='C')
                
                #example (3.5,2) - (7,7) = (-3.5,-5)
				LM_dist=lm1-np.array([j,k])
                #sqrt(-3.5^2 + -5^2)
				hypotenuse=np.sqrt((LM_dist[0])**2+(LM_dist[1])**2)
                #array(3.5/6.03=0.573*2, 5/6.03=0.8192*2)
                #55DEG * 2 and 35DEG * 2
				LM1R=np.array([(LM_dist[0]/hypotenuse)*2,(LM_dist[1]/hypotenuse)*2])
                #array(3.5/6.03=0.573, 5/6.03=0.8192)
				LM1RL1=np.array([(LM_dist[0]/hypotenuse),(LM_dist[1]/hypotenuse)])
				
				#LM2R
				LM_dist=lm2-np.array([j,k])
                #9.656 DEG
				hypotenuse=np.sqrt((LM_dist[0])**2+(LM_dist[1])**2)

				LM2R=np.array([(LM_dist[0]/hypotenuse)*2,(LM_dist[1]/hypotenuse)*2])
                #3.5/9.656 = 0.362
                #9/9.656 = 0.9320
				LM2RL1=np.array([(LM_dist[0]/hypotenuse),(LM_dist[1]/hypotenuse)])

				#LM3R
				LM_dist=lm3-np.array([j,k])
				hypotenuse=np.sqrt((LM_dist[0])**2+(LM_dist[1])**2)
				LM3R=np.array([(LM_dist[0]/hypotenuse)*2,(LM_dist[1]/hypotenuse)*2])
				LM3RL1=np.array([(LM_dist[0]/hypotenuse),(LM_dist[1]/hypotenuse)])

				#Angle between LM1 and LM2 calculate RAD
				absLM1LM2vec=LM1R-LM2R
				absLM1LM2=np.sqrt(absLM1LM2vec[0]**2+absLM1LM2vec[1]**2)
				angle12r = np.arccos((absLM1LM2**2-8)/-8)/2


				#Angle between LM2 and LM3 calculate RAD
				absLM2LM3vec=LM2R-LM3R
				absLM2LM3=np.sqrt(absLM2LM3vec[0]**2+absLM2LM3vec[1]**2)
				angle23r = (np.arccos((absLM2LM3**2-8)/-8)/2)

                #Angle between LM3 and LM1 calculate RAD should use 2pi
				angle31r=np.pi-angle12r-angle23r
				
				#Rotate position with angles
                #
				r12H=np.array([
                    np.round(np.cos(angle12r)*LM1R[0]+np.sin(angle12r)*LM1R[1],8),
                    np.round(-1*(np.sin(angle12r)*LM1R[0])+np.cos(angle12r)*LM1R[1],8)
                ])
                    
				r23H=np.array([
                    np.round(np.cos(angle23r)*LM2R[0]+np.sin(angle23r)*LM2R[1],8),
                    np.round(-1*(np.sin(angle23r)*LM2R[0])+np.cos(angle23r)*LM2R[1],8)
                ])
                
				r31H=np.array([
                    np.round(np.cos(angle31r)*LM3R[0]+np.sin(angle31r)*LM3R[1],8),
                    np.round(-1*(np.sin(angle31r)*LM3R[0])+np.cos(angle31r)*LM3R[1],8)
                ])
				
				length=np.sqrt(r12H[0]**2+r12H[1]**2)
				r12Hl1=np.array([r12H[0]/length, r12H[1]/length])
				
				length=np.sqrt(r23H[0]**2+r23H[1]**2)
				r23Hl1=np.array([r23H[0]/length, r23H[1]/length])
				
				length=np.sqrt(r31H[0]**2+r31H[1]**2)
				r31Hl1=np.array([r31H[0]/length, r31H[1]/length])

				hypotenuse=np.sqrt((lm1[0]-j)**2+(lm1[1]-k)**2)
				bLM1R=np.arccos((0.5**2-2*hypotenuse**2)/(-2*hypotenuse**2))*2

				hypotenuse=np.sqrt((lm2[0]-j)**2+(lm2[1]-k)**2)
				bLM2R=np.arccos((0.5**2-2*hypotenuse**2)/(-2*hypotenuse**2))*2

				hypotenuse=np.sqrt((lm3[0]-j)**2+(lm3[1]-k)**2)
				bLM3R=np.arccos((0.5**2-2*hypotenuse**2)/(-2*hypotenuse**2))*2

				
				bLM1HR=2*angle12r-0.5*bLM1R-0.5*bLM2R
				bLM2HR=2*angle23r-0.5*bLM2R-0.5*bLM3R
				bLM3HR=2*angle31r-0.5*bLM3R-0.5*bLM1R


				lmsArray=[LM1_SNAP,LM2_SNAP,LM3_SNAP]
				lmrArray=[LM1R,LM2R,LM3R]
				blmsArray=[LM1_snapshot,LM2_snapshot,LM3_snapshot]
				lmshArray=[sLM12R,sLM22R,sLM31R]
				lmrhArray=[r12H,r23H,r31H]
				lmrl1=[LM1RL1,LM2RL1,LM3RL1]
				hrl1=[r12Hl1,r23Hl1,r31Hl1]

				blmshArray=[LM1_pass,LM2_pass,LM3_pass]

				Vapproach=np.array([0,0])
				Vturn=np.array([0,0])

				
				for q in xrange(0,3):

					ab1=lmsArray[q]-lmrArray[0]
					a1=np.sqrt((ab1[0])**2+(ab1[1])**2)

					hab1=lmshArray[q]-lmrhArray[0]
					ha1=np.sqrt((hab1[0])**2+(hab1[1])**2)

					ab2=lmsArray[q]-lmrArray[1]
					a2=np.sqrt((ab2[0])**2+(ab2[1])**2)

					hab2=lmshArray[q]-lmrhArray[1]
					ha2=np.sqrt((hab2[0])**2+(hab2[1])**2)

					ab3=lmsArray[q]-lmrArray[2]
					a3=np.sqrt((ab3[0])**2+(ab3[1])**2)

					hab3=lmshArray[q]-lmrhArray[2]
					ha3=np.sqrt((hab3[0])**2+(hab3[1])**2)
					

                    # Case 1
					if a1<=a2 and a1<=a3:



						if lmsArray[q][1] <= lmrArray[0][1]:
							

							if lmrArray[0][0]>=0:
								if lmrl1[0][1]>lmsArray[q][1]:

									orth=np.array([np.round(np.cos(DEG270)*lmrArray[0][0]+np.sin(DEG270)*lmrArray[0][1],8),np.round(-1*(np.sin(DEG270)*lmrArray[0][0])+np.cos(DEG270)*lmrArray[0][1],8)])

								else:
									orth=np.array([np.round(np.cos(DEG90)*lmrArray[0][0]+np.sin(DEG90)*lmrArray[0][1],8),np.round(-1*(np.sin(DEG90)*lmrArray[0][0])+np.cos(DEG90)*lmrArray[0][1],8)])	
							else:

								if lmrl1[0][1]>lmsArray[q][1]:
									orth=np.array([np.round(np.cos(DEG90)*lmrArray[0][0]+np.sin(DEG90)*lmrArray[0][1],8),np.round(-1*(np.sin(DEG90)*lmrArray[0][0])+np.cos(DEG90)*lmrArray[0][1],8)])
								else:
									orth=np.array([np.round(np.cos(DEG270)*lmrArray[0][0]+np.sin(DEG270)*lmrArray[0][1],8),np.round(-1*(np.sin(DEG270)*lmrArray[0][0])+np.cos(DEG270)*lmrArray[0][1],8)])


							length=np.sqrt(orth[1]**2+orth[1]**2)
							orth=np.array([orth[0]/length,orth[1]/length])
					
							Vturn=Vturn+orth
					
							if bLM1R < blmsArray[q]:
								length=np.sqrt(LM1R[0]**2+LM1R[1]**2)
								position=np.array([LM1R[0]/length,LM1R[1]/length])
								Vapproach=Vapproach+position

							else:
								length=np.sqrt(LM1R[0]**2+LM1R[1]**2)
								position=np.array([LM1R[0]/length,LM1R[1]/length])
								Vapproach=Vapproach+(position*-1)



						else:
				

							if (lmrArray[0][0]>=0):
								if lmrl1[0][1]>lmsArray[q][1]:

									orth=np.array([np.round(np.cos(DEG90)*lmrArray[0][0]+np.sin(DEG90)*lmrArray[0][1],8),np.round(-1*(np.sin(DEG90)*lmrArray[0][0])+np.cos(DEG90)*lmrArray[0][1],8)])

								else:
									orth=np.array([np.round(np.cos(DEG270)*lmrArray[0][0]+np.sin(DEG270)*lmrArray[0][1],8),np.round(-1*(np.sin(DEG270)*lmrArray[0][0])+np.cos(DEG270)*lmrArray[0][1],8)])
							else:

								if lmrl1[0][1]>lmsArray[q][1]:
									orth=np.array([np.round(np.cos(DEG270)*lmrArray[0][0]+np.sin(DEG270)*lmrArray[0][1],8),np.round(-1*(np.sin(DEG270)*lmrArray[0][0])+np.cos(DEG270)*lmrArray[0][1],8)])
								else:
									orth=np.array([np.round(np.cos(DEG90)*lmrArray[0][0]+np.sin(DEG90)*lmrArray[0][1],8),np.round(-1*(np.sin(DEG90)*lmrArray[0][0])+np.cos(DEG90)*lmrArray[0][1],8)])

							length = np.sqrt(orth[0]**2+orth[1]**2)
							orth=np.array([orth[0]/length,orth[1]/length])

							Vturn=Vturn+orth
							print (Vturn)

							if bLM1R < blmsArray[q]:
								length=np.sqrt(LM1R[0]**2+LM1R[1]**2)
								position=np.array([LM1R[0]/length,LM1R[1]/length])
								Vapproach=Vapproach+position

							else:
								length=np.sqrt(LM1R[0]**2+LM1R[1]**2)
								position=np.array([LM1R[0]/length,LM1R[1]/length])
								Vapproach=Vapproach+(position*-1)


					#Case 2
					if a2<=a1 and a2<=a3:


						if lmsArray[q][1] <= lmrArray[1][1]:


							if lmrArray[1][0]>=0:
								if lmrl1[1][1]>lmsArray[q][1]:

									orth=np.array([np.round(np.cos(DEG270)*lmrArray[1][0]+np.sin(DEG270)*lmrArray[1][1],8),np.round(-1*(np.sin(DEG270)*lmrArray[1][0])+np.cos(DEG270)*lmrArray[1][1],8)])

								else:
									orth=np.array([np.round(np.cos(DEG90)*lmrArray[1][0]+np.sin(DEG90)*lmrArray[1][1],8),np.round(-1*(np.sin(DEG90)*lmrArray[1][0])+np.cos(DEG90)*lmrArray[1][1],8)])
								
							else:

								if lmrl1[1][1]>lmsArray[q][1]:
									orth=np.array([np.round(np.cos(DEG90)*lmrArray[1][0]+np.sin(DEG90)*lmrArray[1][1],8),np.round(-1*(np.sin(DEG90)*lmrArray[1][0])+np.cos(DEG90)*lmrArray[1][1],8)])
								else:
									orth=np.array([np.round(np.cos(DEG270)*lmrArray[1][0]+np.sin(DEG270)*lmrArray[1][1],8),np.round(-1*(np.sin(DEG270)*lmrArray[1][0])+np.cos(DEG270)*lmrArray[1][1],8)])


							length=np.sqrt(orth[1]**2+orth[1]**2)
							orth=np.array([orth[0]/length,orth[1]/length])

							Vturn=Vturn+orth
			

							if bLM2R < blmsArray[q]:
								length=np.sqrt(LM2R[0]**2+LM2R[1]**2)
								position=np.array([LM2R[0]/length,LM2R[1]/length])
								Vapproach=Vapproach+position

							else:
								length=np.sqrt(LM2R[0]**2+LM2R[1]**2)
								position=np.array([LM2R[0]/length,LM2R[1]/length])
								Vapproach=Vapproach+(position*-1)



						else:


							if lmrArray[1][0]>=0:
								if lmrl1[1][1]>lmsArray[q][1]:

									orth=np.array([np.round(np.cos(DEG90)*lmrArray[1][0]+np.sin(DEG90)*lmrArray[1][1],8),np.round(-1*(np.sin(DEG90)*lmrArray[1][0])+np.cos(DEG90)*lmrArray[1][1],8)])

								else:
									orth=np.array([np.round(np.cos(DEG270)*lmrArray[1][0]+np.sin(DEG270)*lmrArray[1][1],8),np.round(-1*(np.sin(DEG270)*lmrArray[1][0])+np.cos(DEG270)*lmrArray[1][1],8)])
									
							else:

								if lmrl1[1][1]>lmsArray[q][1]:
									orth=np.array([np.round(np.cos(DEG270)*lmrArray[1][0]+np.sin(DEG270)*lmrArray[1][1],8),np.round(-1*(np.sin(DEG270)*lmrArray[1][0])+np.cos(DEG270)*lmrArray[1][1],8)])
								else:
									orth=np.array([np.round(np.cos(DEG90)*lmrArray[1][0]+np.sin(DEG90)*lmrArray[1][1],8),np.round(-1*(np.sin(DEG90)*lmrArray[1][0])+np.cos(DEG90)*lmrArray[1][1],8)])


							length=np.sqrt(orth[0]**2+orth[1]**2)
							orth=np.array([orth[0]/length,orth[1]/length])

		
							Vturn=Vturn+orth
					


							if bLM2R < blmsArray[q]:
								length=np.sqrt(LM2R[0]**2+LM2R[1]**2)
								position=np.array([LM2R[0]/length,LM2R[1]/length])
								Vapproach=Vapproach+position

							else:
								length=np.sqrt(LM2R[0]**2+LM2R[1]**2)
								position=np.array([LM2R[0]/length,LM2R[1]/length])
								Vapproach=Vapproach+(position*-1)

					#Case 3		
					if a3<=a2 and a3<=a1:




						if lmsArray[q][1] <= lmrArray[2][1]:


							if lmrArray[2][0]>=0:
								if lmrl1[2][1]>lmsArray[q][1]:

									orth=np.array([np.round(np.cos(DEG270)*lmrArray[2][0]+np.sin(DEG270)*lmrArray[2][1],8),np.round(-1*(np.sin(DEG270)*lmrArray[2][0])+np.cos(DEG270)*lmrArray[2][1],8)])

								else:
									orth=np.array([np.round(np.cos(DEG90)*lmrArray[2][0]+np.sin(DEG90)*lmrArray[2][1],8),np.round(-1*(np.sin(DEG90)*lmrArray[2][0])+np.cos(DEG90)*lmrArray[2][1],8)])
								
							else:

								if lmrl1[2][1]>lmsArray[q][1]:
									orth=np.array([np.round(np.cos(DEG90)*lmrArray[2][0]+np.sin(DEG90)*lmrArray[2][1],8),np.round(-1*(np.sin(DEG90)*lmrArray[2][0])+np.cos(DEG90)*lmrArray[2][1],8)])
								else:
									orth=np.array([np.round(np.cos(DEG270)*lmrArray[2][0]+np.sin(DEG270)*lmrArray[2][1],8),np.round(-1*(np.sin(DEG270)*lmrArray[2][0])+np.cos(DEG270)*lmrArray[2][1],8)])


							length=np.sqrt(orth[1]**2+orth[1]**2)
							orth=np.array([orth[0]/length,orth[1]/length])
					
							Vturn=Vturn+orth
				

							if bLM2R < blmsArray[q]:
								length=np.sqrt(LM3R[0]**2+LM3R[1]**2)
								position=np.array([LM3R[0]/length,LM3R[1]/length])
								Vapproach=Vapproach+position

							else:
								length=np.sqrt(LM3R[0]**2+LM3R[1]**2)
								position=np.array([LM3R[0]/length,LM3R[1]/length])
								Vapproach=Vapproach+(position*-1)



						else:
							

							if lmrArray[2][0]>=0:
								if lmrl1[2][1]>lmsArray[q][1]:

									orth=np.array([np.round(np.cos(DEG90)*lmrArray[2][0]+np.sin(DEG90)*lmrArray[2][1],8),np.round(-1*(np.sin(DEG90)*lmrArray[2][0])+np.cos(DEG90)*lmrArray[2][1],8)])

								else:
									orth=np.array([np.round(np.cos(DEG270)*lmrArray[2][0]+np.sin(DEG270)*lmrArray[2][1],8),np.round(-1*(np.sin(DEG270)*lmrArray[2][0])+np.cos(DEG270)*lmrArray[2][1],8)])
								
							else:

								if lmrl1[2][1]>lmsArray[q][1]:
									orth=np.array([np.round(np.cos(DEG270)*lmrArray[2][0]+np.sin(DEG270)*lmrArray[2][1],8),np.round(-1*(np.sin(DEG270)*lmrArray[2][0])+np.cos(DEG270)*lmrArray[2][1],8)])
								else:
									orth=np.array([np.round(np.cos(DEG90)*lmrArray[2][0]+np.sin(DEG90)*lmrArray[2][1],8),np.round(-1*(np.sin(DEG90)*lmrArray[2][0])+np.cos(DEG90)*lmrArray[2][1],8)])


							length=np.sqrt(orth[0]**2+orth[1]**2)
							orth=np.array([orth[0]/length,orth[1]/length])

							
							Vturn=Vturn+orth
							


							if bLM3R < blmsArray[q]:
								length=np.sqrt(LM3R[0]**2+LM3R[1]**2)
								position=np.array([LM3R[0]/length,LM3R[1]/length])
								Vapproach=Vapproach+position

							else:
								length=np.sqrt(LM3R[0]**2+LM3R[1]**2)
								position=np.array([LM3R[0]/length,LM3R[1]/length])
								Vapproach=Vapproach+(position*-1)



                                        # Vturn und Vapproach  					
					if ha1<=ha2 and ha1<=ha3:



						if lmshArray[q][1] <= lmrhArray[0][1]:
				

							if lmrhArray[0][0]>=0:
								if hrl1[0][1]>lmshArray[q][1]:

									orth=np.array([np.round(np.cos(DEG270)*lmrhArray[0][0]+np.sin(DEG270)*lmrhArray[0][1],8),np.round(-1*(np.sin(DEG270)*lmrhArray[0][0])+np.cos(DEG270)*lmrhArray[0][1],8)])

								else:
									orth=np.array([np.round(np.cos(DEG90)*lmrhArray[0][0]+np.sin(DEG90)*lmrhArray[0][1],8),np.round(-1*(np.sin(DEG90)*lmrhArray[0][0])+np.cos(DEG90)*lmrhArray[0][1],8)])
									
							else:
								if hrl1[0][1]>lmshArray[q][1]:

									orth=np.array([np.round(np.cos(DEG90)*lmrhArray[0][0]+np.sin(DEG90)*lmrhArray[0][1],8),np.round(-1*(np.sin(DEG90)*lmrhArray[0][0])+np.cos(DEG90)*lmrhArray[0][1],8)])

								else:
									orth=np.array([np.round(np.cos(DEG270)*lmrhArray[0][0]+np.sin(DEG270)*lmrhArray[0][1],8),np.round(-1*(np.sin(DEG270)*lmrhArray[0][0])+np.cos(DEG270)*lmrhArray[0][1],8)])
									

							length=np.sqrt(orth[1]**2+orth[1]**2)
							orth=np.array([orth[0]/length,orth[1]/length])
					
							Vturn=Vturn+orth
				
							if bLM1HR < blmshArray[q]:
								length=np.sqrt(r12H[0]**2+r12H[1]**2)
								position=np.array([r12H[0]/length,r12H[1]/length])
								if bLM1HR < np.round(np.pi,8):
									Vapproach=Vapproach+position
								else:
									Vapproach=Vapproach-position

							else:
								length=np.sqrt(r12H[0]**2+r12H[1]**2)
								position=np.array([r12H[0]/length,r12H[1]/length])
								if bLM3HR<np.round(np.pi,8):
									Vapproach=Vapproach-position
								else:
									Vapproach=Vapproach+position



						else:
				

							if lmrhArray[0][0]>=0:
								if hrl1[0][1]>lmshArray[q][1]:

									orth=np.array([np.round(np.cos(DEG90)*lmrhArray[0][0]+np.sin(DEG90)*lmrhArray[0][1],8),np.round(-1*(np.sin(DEG90)*lmrhArray[0][0])+np.cos(DEG90)*lmrhArray[0][1],8)])

								else:
									orth=np.array([np.round(np.cos(DEG270)*lmrhArray[0][0]+np.sin(DEG270)*lmrhArray[0][1],8),np.round(-1*(np.sin(DEG270)*lmrhArray[0][0])+np.cos(DEG270)*lmrhArray[0][1],8)])
								
							else:
								if hrl1[0][1]>lmshArray[q][1]:

									orth=np.array([np.round(np.cos(DEG270)*lmrhArray[0][0]+np.sin(DEG270)*lmrhArray[0][1],8),np.round(-1*(np.sin(DEG270)*lmrhArray[0][0])+np.cos(DEG270)*lmrhArray[0][1],8)])

								else:
									orth=np.array([np.round(np.cos(DEG90)*lmrhArray[0][0]+np.sin(DEG90)*lmrhArray[0][1],8),np.round(-1*(np.sin(DEG90)*lmrhArray[0][0])+np.cos(DEG90)*lmrhArray[0][1],8)])
									

							length=np.sqrt(orth[0]**2+orth[1]**2)
							orth=np.array([orth[0]/length,orth[1]/length])

				
							Vturn=Vturn+orth
							


							if bLM1HR < blmshArray[q]:
								length=np.sqrt(r12H[0]**2+r12H[1]**2)
								position=np.array([r12H[0]/length,r12H[1]/length])
								if bLM1HR < np.round(np.pi,8):
									Vapproach=Vapproach+position
								else:
									Vapproach=Vapproach-position

							else:
								length=np.sqrt(r12H[0]**2+r12H[1]**2)
								position=np.array([r12H[0]/length,r12H[1]/length])
								if bLM3HR<np.round(np.pi,8):
									Vapproach=Vapproach-position
								else:
									Vapproach=Vapproach+position

						

					if ha2<=ha1 and ha2<=ha3:



						if lmshArray[q][1] <= lmrhArray[1][1] :
							

							if lmrhArray[1][0]>=0:
								if hrl1[1][1]>lmshArray[q][1]:

									orth=np.array([np.round(np.cos(DEG270)*lmrhArray[1][0]+np.sin(DEG270)*lmrhArray[1][1],8),np.round(-1*(np.sin(DEG270)*lmrhArray[1][0])+np.cos(DEG270)*lmrhArray[1][1],8)])

								else:
									orth=np.array([np.round(np.cos(DEG90)*lmrhArray[1][0]+np.sin(DEG90)*lmrhArray[1][1],8),np.round(-1*(np.sin(DEG90)*lmrhArray[1][0])+np.cos(DEG90)*lmrhArray[1][1],8)])
										
							else:
								if hrl1[1][1]>lmshArray[q][1]:

									orth=np.array([np.round(np.cos(DEG90)*lmrhArray[1][0]+np.sin(DEG90)*lmrhArray[1][1],8),np.round(-1*(np.sin(DEG90)*lmrhArray[1][0])+np.cos(DEG90)*lmrhArray[1][1],8)])

								else:
									orth=np.array([np.round(np.cos(DEG270)*lmrhArray[1][0]+np.sin(DEG270)*lmrhArray[1][1],8),np.round(-1*(np.sin(DEG270)*lmrhArray[1][0])+np.cos(DEG270)*lmrhArray[1][1],8)])
									

							length=np.sqrt(orth[1]**2+orth[1]**2)
							orth=np.array([orth[0]/length,orth[1]/length])
							
							Vturn=Vturn+orth
				

							if bLM2HR < blmshArray[q]:
								length=np.sqrt(r23H[0]**2+r23H[1]**2)
								position=np.array([r23H[0]/length,r23H[1]/length])
								if bLM2HR < np.round(np.pi,8):
									Vapproach=Vapproach+position
								else:
									Vapproach=Vapproach-position

							else:
								length=np.sqrt(r23H[0]**2+r23H[1]**2)
								position=np.array([r23H[0]/length,r23H[1]/length])
								if bLM3HR<np.round(np.pi,8):
									Vapproach=Vapproach-position
								else:
									Vapproach=Vapproach+position



						else:
					

							if lmrhArray[1][0]>=0:
								if hrl1[1][1]>lmshArray[q][1]:

									orth=np.array([np.round(np.cos(DEG90)*lmrhArray[1][0]+np.sin(DEG90)*lmrhArray[1][1],8),np.round(-1*(np.sin(DEG90)*lmrhArray[1][0])+np.cos(DEG90)*lmrhArray[1][1],8)])

								else:
									orth=np.array([np.round(np.cos(DEG270)*lmrhArray[1][0]+np.sin(DEG270)*lmrhArray[1][1],8),np.round(-1*(np.sin(DEG270)*lmrhArray[1][0])+np.cos(DEG270)*lmrhArray[1][1],8)])
								
							else:
								if hrl1[1][1]>lmshArray[q][1]:

									orth=np.array([np.round(np.cos(DEG270)*lmrhArray[1][0]+np.sin(DEG270)*lmrhArray[1][1],8),np.round(-1*(np.sin(DEG270)*lmrhArray[1][0])+np.cos(DEG270)*lmrhArray[1][1],8)])

								else:
									orth=np.array([np.round(np.cos(DEG90)*lmrhArray[1][0]+np.sin(DEG90)*lmrhArray[1][1],8),np.round(-1*(np.sin(DEG90)*lmrhArray[1][0])+np.cos(DEG90)*lmrhArray[1][1],8)])
									


							length=np.sqrt(orth[0]**2+orth[1]**2)
							orth=np.array([orth[0]/length,orth[1]/length])

							Vturn=Vturn+orth


							if bLM2HR < blmshArray[q]:
								length=np.sqrt(r23H[0]**2+r23H[1]**2)
								position=np.array([r23H[0]/length,r23H[1]/length])
								if bLM2HR < np.round(np.pi,8):
									Vapproach=Vapproach+position
								else:
									Vapproach=Vapproach-position

							else:
								length=np.sqrt(r23H[0]**2+r23H[1]**2)
								position=np.array([r23H[0]/length,r23H[1]/length])
								if bLM3HR<np.round(np.pi,8):
									Vapproach=Vapproach-position
								else:
									Vapproach=Vapproach+position



					if ha3<=ha2 and ha3<=ha1:
						
                        
						if lmshArray[q][1] <= lmrhArray[2][1]:
						

							if lmrhArray[2][0]>=0:
								if hrl1[2][1]>lmshArray[q][1]:

									orth=np.array([np.round(np.cos(DEG270)*lmrhArray[2][0]+np.sin(DEG270)*lmrhArray[2][1],8),np.round(-1*(np.sin(DEG270)*lmrhArray[2][0])+np.cos(DEG270)*lmrhArray[2][1],8)])

								else:
									orth=np.array([np.round(np.cos(DEG90)*lmrhArray[2][0]+np.sin(DEG90)*lmrhArray[2][1],8),np.round(-1*(np.sin(DEG90)*lmrhArray[2][0])+np.cos(DEG90)*lmrhArray[2][1],8)])
																		
							else:
								if hrl1[2][1]>lmshArray[q][1]:

									orth=np.array([np.round(np.cos(DEG90)*lmrhArray[2][0]+np.sin(DEG90)*lmrhArray[2][1],8),np.round(-1*(np.sin(DEG90)*lmrhArray[2][0])+np.cos(DEG90)*lmrhArray[2][1],8)])

								else:
									orth=np.array([np.round(np.cos(DEG270)*lmrhArray[2][0]+np.sin(DEG270)*lmrhArray[2][1],8),np.round(-1*(np.sin(DEG270)*lmrhArray[2][0])+np.cos(DEG270)*lmrhArray[2][1],8)])
									

							length=np.sqrt(orth[1]**2+orth[1]**2)
							orth=np.array([orth[0]/length,orth[1]/length])
							
							Vturn=Vturn+orth
						

							if bLM3HR < blmshArray[q]:
								length=np.sqrt(r31H[0]**2+r31H[1]**2)
								position=np.array([r31H[0]/length,r31H[1]/length])
								if bLM3HR < np.round(np.pi,8):
									Vapproach=Vapproach+position
								else:
									Vapproach=Vapproach-position

							else:
								length=np.sqrt(r31H[0]**2+r31H[1]**2)
								position=np.array([r31H[0]/length,r31H[1]/length])
								if bLM3HR<np.round(np.pi,8):
									Vapproach=Vapproach-position
								else:
									Vapproach=Vapproach+position


						else:
							

							if lmrhArray[2][0]>=0 and hrl1[1][1]>lmshArray[q][1]:
								if lmrhArray[2][1] < lmshArray[q][1] :

									orth=np.array([np.round(np.cos(DEG90)*lmrhArray[2][0]+np.sin(DEG90)*lmrhArray[2][1],8),np.round(-1*(np.sin(DEG90)*lmrhArray[2][0])+np.cos(DEG90)*lmrhArray[2][1],8)])

								else:
									orth=np.array([np.round(np.cos(DEG270)*lmrhArray[2][0]+np.sin(DEG270)*lmrhArray[2][1],8),np.round(-1*(np.sin(DEG270)*lmrhArray[2][0])+np.cos(DEG270)*lmrhArray[2][1],8)])
								
							else:
								if lmrhArray[2][1] > lmshArray[q][1] :

									orth=np.array([np.round(np.cos(DEG270)*lmrhArray[2][0]+np.sin(DEG270)*lmrhArray[2][1],8),np.round(-1*(np.sin(DEG270)*lmrhArray[2][0])+np.cos(DEG270)*lmrhArray[2][1],8)])

								else:
									orth=np.array([np.round(np.cos(DEG90)*lmrhArray[2][0]+np.sin(DEG90)*lmrhArray[2][1],8),np.round(-1*(np.sin(DEG90)*lmrhArray[2][0])+np.cos(DEG90)*lmrhArray[2][1],8)])

							length=np.sqrt(orth[0]**2+orth[1]**2)
							orth=np.array([orth[0]/length,orth[1]/length])
						
							Vturn=Vturn+orth
					


							if bLM2HR < blmshArray[q]:
								length=np.sqrt(r31H[0]**2+r31H[1]**2)
								position=np.array([r31H[0]/length,r31H[1]/length])
								if bLM2HR < np.round(np.pi,8):
									Vapproach=Vapproach+position
								else:
									Vapproach=Vapproach-position

							else:
								length=np.sqrt(r31H[0]**2+r31H[1]**2)
								position=np.array([r31H[0]/length,r31H[1]/length])
								if bLM3HR<np.round(np.pi,8):
									Vapproach=Vapproach-position
								else:
									Vapproach=Vapproach+position


				vektor=(3*Vapproach)+Vturn
				length=np.sqrt(vektor[0]**2+vektor[1]**2)
				vektorl1 = np.array([vektor[0]/length,vektor[1]/length])
			

				plot.itemset((i,0),j)
				plot.itemset((i,1),k)			
				plot.itemset((i,2),vektorl1[0])
				plot.itemset((i,3),vektorl1[1])
				i=i+1
			
X,Y,U,V = zip(*plot)
ax=plt.gca()
ax.quiver(X,Y,U,V,angles='xy',scale_units='xy',scale=1)

ax.set_xlim([-8,8])
ax.set_ylim([-8,8])
plt.suptitle('Team A1', fontsize=20)
plt.draw()
plt.savefig('team_a1.jpg')
plt.show()
