# Ethnicity Detection - Tensorflow with CNN

By means of TensorFlow we will implement 4 different Models for detecting different Ethnic groups:

1. Own Model
2. VGG19
3. NASNet
4. Inception-ResNet-v2

##### Ethnic Groups:

1. Caucasoid (white)
2. Negroid (black)
3. Mongoloid
4. Australoid
5. Others

##### Dataset download link:

https://drive.google.com/u/0/uc?id=1GTK3NwzQscKO3zxRk0R8SHoT9EXV_TvS&export=download"

#### Steps to create the Models

1. Generating the dataset
2. Inspecting the data
   - Image Preprocessing
3. Building a Convulutional Neural Network Model
4. Evaluating the Model
5. Adjusting the Model parameters
6. Making prediction with our trained Model

--
**Few things we could try to continue to improve our model:**

1. Increase the number of model layers (e.g. add more convolutional layers).
2. Increase the number of filters in each convolutional layer (e.g. from 10 to 32, 64, or 128, these numbers aren't set in stone either, they are usually found through trial and error).
3. Train for longer (more epochs).
4. Finding an ideal learning rate.
5. Get more data (give the model more opportunities to learn).
6. Use transfer learning to leverage what another image model has learned and adjust it for our own use case.
