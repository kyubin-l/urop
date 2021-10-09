# Machine Learning for Modelling Random Nonlinear Vibration
This repository contains all the necessary scripts used in my UROP project in summer 2021. 

For a brief summary of what was done, look at [UROP poster.pdf](https://github.com/kyubin-l/urop/files/7315961/UROP.poster.pdf)
 and  [urop_writeup.pdf](https://github.com/kyubin-l/urop/files/7315962/urop_writeup.pdf). 
 
 Most of the training was done using data created using a duffing oscillator simulator built in MATLAB, which is not available in the repository. The NonLinearSystemAnalysis folder contains a Python implementation of the simulator, but is significantly slower than MATLAB. 
 
 The "cnn_nonlinear_vibration.ipynb" script creates, initilises, and trains the model using functions written in CNNfunctions.py. 
 The "intermediate_layers.ipynb" scipt analyses the intermediate outputs in detail using signal processing tools. The necessary functions are in mcoherence.py.
 The "noise_car_damper.ipynb" script creates a new model and trains them on an adjusted dataset including additional output noise, and on real-life car damper data. 

The data can be found in this [folder](https://drive.google.com/drive/folders/1ZQN36-FSyHuJF0JHRrbZisdtrAmi33nK?usp=sharing). The white_noise folder contains force displacement data using white noise as input. The nonlinear damping cases are labelled as "nonlinear_damping_#" and the nonlinear stiffnesss casesa re labelled as "nonlinear_stiffness_#". The output_noise folder contains data for the nonlinear damping case with additional noise output.

The real life car damper data used in "noise_car_damper.ipynb" can be found in this [folder](https://drive.google.com/drive/folders/1E7n_iI5yOj757e0VXBJ3SKonVb6BJlvH?usp=sharing). 

Some benchmark models can be found [here](https://drive.google.com/drive/folders/1bv3UP_33k0g7RTKQVv2VWoDjO-fm7q-E?usp=sharing). These can be imported using the command load_model(file_path_to_model). Information on some of the benchmark models can be found in the folder benchmark_models. 

This project was supervised by Dr. Matthew de Brett, who developed the "CNNfunctions.py" script and much of the "cnn_nonlinear_vibration.ipynb" script. 



