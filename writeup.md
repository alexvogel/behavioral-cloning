# **Behavioral Cloning** 
---
**Behavioral Cloning Project**

The goals / steps of this project are the following:
* Use the simulator to collect data of good driving behavior
* Build, a convolution neural network in Keras that predicts steering angles from images
* Train and validate the model with a training and validation set
* Test that the model successfully drives around track one without leaving the road
* Summarize the results with a written report


[//]: # (Image References)

[image1]: ./writeup_media/car_problem_spot_water.png "Problem Spot Water"
[image2]: ./writeup_media/car_problem_spot_sand.png "Problem Spot Sand"
[image3]: ./writeup_media/car_center.png "Center Lane"
[image4]: ./writeup_media/car_recovery_1.png "Recovery 1"
[image5]: ./writeup_media/car_recovery_2.png "Recovery 2"
[image6]: ./writeup_media/car_recovery_3.png "Recovery 3"
[image7]: ./writeup_media/centercam_org.jpg "Center Cam Org"
[image8]: ./writeup_media/centercam_flipped.jpg "Center Cam Flipped"
[image9]: ./writeup_media/animation.gif "Autonomous Mode Center Cam"

## Rubric Points
### Here I will consider the [rubric points](https://review.udacity.com/#!/rubrics/432/view) individually and describe how I addressed each point in my implementation.  

---
### Files Submitted & Code Quality

#### 1. Submission includes all required files and can be used to run the simulator in autonomous mode

My project includes the following files:
* bin/model.py containing the script to create and train the model
* bin/drive.py for driving the car in autonomous mode
* model.h5.gz containing a trained convolution neural network 
* run13.mp4 a video of the successfull drive in autonomous mode on track 1

#### 2. Submission includes functional code
Using the Udacity provided simulator and my drive.py file, the car can be driven autonomously around the track by executing 
```sh
python drive.py model.h5
```

#### 3. Submission code is usable and readable

The model.py file contains the code for training and saving the convolution neural network. The file shows the pipeline I used for training and validating the model, and it contains comments to explain how the code works.

### Model Architecture and Training Strategy

#### 1. Solution Design Approach

My first step was to use a convolution neural network model similar to LeNet. I thought this model might be appropriate because it works well for image classification and the task at hand is very similar.

In order to gauge how well the model was working, I split my image and steering angle data into a training and validation set. I found that my first model had a low mean squared error on the training set but a high mean squared error on the validation set. This implied that the model was overfitting.

To combat the overfitting, I introduced a dropout layer after every fully connected layer with a keep-probability of 50%. This was sufficient to prevent the model from overfitting.

The final step was to run the simulator to see how well the car was driving around track one. There were two spots where the vehicle fell off the track.

At this position the model confuses the water on the right with the road on the left and chose to drive off road down into the water.

![alt text][image1]

At this position the model also confuses the 'sand'-area with the paved road. The car left the road and followed the sand into the lot.

![alt text][image2]

To improve the driving behavior in these cases, I recorded several additional 'recovery'-actions at exactly these two spots.

At the end of the process, the vehicle is able to drive autonomously around the track without leaving the road.

#### 2. Final Model Architecture

The final model architecture (model.py lines 83-116) consisted of a convolution neural network with the following layers and layer sizes ...

Here is a visualization of the architecture

| Layer         	|Line |     Description                               | 
|:-----------------:|:---:|:---------------------------------------------:| 
| Input         	| 83  | 160x320x3 rgb image                           | 
| Cropping2D     	| 83  | cropping 50upper, 20lower to 90x320x3 image   | 
| Lambda            | 86  | normalization and zero-mean                   |
| Convolution2D    	| 89  | 6 kernels 5x5                                 |
| RELU				| 89  |                                               |
| Max pooling	    | 92  | 2x2 stride                                    |
| Convolution2D    	| 95  | 6 kernels 5x5                                 |
| RELU				| 95  |                                               |
| Max pooling	    | 98  | 2x2 stride                                    |
| Flatten           | 101 |                                               |
| Fully Connected   | 104 | 1024 nodes                                    |
| Dropout			| 107 | 0.5                                           |
| Fully Connected   | 110 | 100 nodes                                     |
| Dropout			| 113 | 0.5                                           |
| Output            | 116 | 1 node                                        |

#### 3. Creation of the Training Set & Training Process

To capture good driving behavior, I first recorded two laps on track one using center lane driving. Here is an example image of center lane driving:

![alt text][image3]

I then recorded the vehicle recovering from the left side and right side of the road back to center so that the vehicle would learn to recover to the center after it deviates to one side. These images show what a recovery looks like...

![alt text][image4] ![alt text][image5] ![alt text][image6]

To augment the data set, I also flipped images and angles thinking that this would prevent the car having a left steering bias, because the track is an anti-clockwise round track. Copying and flipping every image balances the amount of the left and right steering images. For example, here is an image that has then been flipped:

![alt text][image7] ![alt text][image8]

I tried to use the data from the left and the right camera with adjusted steering angles. The amount of datapoints tripled and I ran out of memory on my training machine. Since I saw good results with only using the center camera, I left off the data from the outer cameras.

After the collection- and augmentation process, I had 69358 number of data points.

I finally randomly shuffled the data set and put 20% of the data into a validation set. 

I used this training data for training the model. The validation set helped determine if the model was over or under fitting. The ideal number of epochs was 3 as evidenced by the course of the validation loss. I used an adam optimizer so that manually training the learning rate wasn't necessary.

### Autonomous Drive

This is how it looks like - the car drives autonomously around the track.

![alt text][image9]
