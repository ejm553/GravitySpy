#gravspy_main2 script by Luke Calian, 6/29/16
#before running, run generate_toy_data_trainingandtest in matlab, select all the variables and save as data.mat
#then run run_main in matlab and save each batch as a .mat file

#import modules
import numpy as np
import pandas as pd
from scipy.io import loadmat

#read data generated by generate_toy_data_trainingandtest.m that is saved as .mat file
data = loadmat('data.mat')

#calculate prior probability of each image
no_labels = np.histogram((data['true_labels'][0]),np.unique((data['true_labels'][0])))
priors = no_labels[1]/len(data['true_labels'][0])

#main function to evaluate batch of images
def main_trainingandtest(batch_name):
  
  batch = loadmat(batch_name) #read batch file
  
  R_lim = 23 #initialize R, max # of citizens who can look at an image before it is passed to a higher level if consensus is not reached 
  N = len(data['images']) #initialize N, # of images in batch
  t = .4*np.ones((data['C'][0][0],1)) #initialize t, threshold vector of .4 for each class
  
  dec_matrix = np.zeros((1,N)) #define dec_matrix, matrix of each image's decision
  class_matrix = np.zeros((1,N)) #define class_matrix, matrix of each decision's class
  
  pp_matrices_rack = np.zeros((15,21,N)) #create 3D matrix of all posterior matrices
  
  #main for loop to iterate over images
  for i in range(N):
  
    if data['images'][i]['type'][0][0] == 'G': #check if golden set image
      labels = data['images'][i]['labels'][0][0] #take citizen labels of image
      IDs = data['images'][i]['IDs'][0][0] #take IDs of citizens who label image
      tlabel = data['images'][i]['truelabel'][0][0][0] #take true label of image
      
      for ii in range(len(IDs)): #iterate over IDs of image
        conf_matrix = data['conf_matrices'][IDs[ii]-1][0] #take confusion matrix of citizen
        conf_matrix[tlabel-1,labels[ii]-1] = conf_matrix[tlabel-1,labels[ii]-1]+1 #update confusion matrix
        data['conf_matrices'][IDs[ii]-1][0] = conf_matrix #confusion matrix put back in stack
      
      dec_matrix[0,i] = 0
      class_matrix[0,i] = tlabel
      print('The image is from the training set')
    
    else: #if image not in golden set
      
      labels = data['images'][i]['labels'][0][0] #take citizen labels of image
      IDs = data['images'][i]['IDs'][0][0] #take IDs of citizens who label image
      no_annotators = len(labels) #define number of citizens who annotate image
      ML_dec = data['images'][i]['ML_posterior'][0][0] #take ML posteriors of image
      imageID = data['images'][i]['imageID'][0][0] #take ID of image
      image_prior = priors #set priors for image to original priors
      
      for y in range(1,len(data['images'][i]['PP_matrices'][0][0])):
        x = 5
      
      for j in range(1,data['C'][0][0]+1): #iterate over classes
        for k in range(1,no_annotators+1): #iterate over citizens that labeled image
          conf = data['conf_matrices'][IDs[k-1]-1][0] #take confusion matrix of each citizen
          conf_divided = np.diag(sum(conf,2))/conf #calculate p(l|j) value
          pp_matrix = np.zeros([data['C'][0][0],no_annotators]) #create posterior matrix
          #import pdb
          #pdb.set_trace()
          pp_matrix[j-1,k-1] = ((conf_divided[j-1,(labels[k-1]-1)])*priors[j-1])/sum(conf_divided[:,(labels[k-1]-1)]*priors) #calculate posteriors
      
      #pp_matrices_rack[:,:,i] = pp_matrix #assign values to pp_matrices_rack
  
#for loop to iterate over each batch
for i in range(1,2): #change 2 to 11
  batch_name = 'batch' + str(i) + '.mat' #batch1.mat, batch2.mat, etc
  main_trainingandtest(batch_name) #call main_trainingandtest function to evaluate batch
  print('batch done')
