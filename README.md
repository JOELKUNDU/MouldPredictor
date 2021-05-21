
# Moulding Machine Parameter Predictor

## Description
Injection moulding is the most popular and widely used manufacturing process for the mass production of plastic products. In the process, a polymer is melted by electric and frictional heat and is injected into a metal mould under high pressure. The quality of the part produced is greatly influenced by process conditions. These process conditions can be changed by changing the machine parameters and is usually done by an experienced engineer. Whenever a new mould is created an engineer will experimentally determine the optimal parameters via repeated trials and visual inspection of the created product. This method is necessary as there is no theoretical method to predict the quality of the part produced given a set of machine parameters. This makes the process highly dependant on the knowledge and experience of the engineer which makes it hard to transfer the skill to a new operator. Wastage in the form of defective products, machine downtime, labour and energy also happen due to the experimental method. Another alternative to the experimental method is simulations. However, simulations are slow and computationally expensive.

Machine learning is a subset of artificial intelligence and is the area of computational science that focuses on analysing and interpreting pattern and structures in data to enable learning, reasoning and decision making outside of human interaction. Machine learning allows the user to feed a computer algorithm with a lot of data and have the computer analyse and make data-driven recommendations and decisions based on only the input data. Leveraging these benefits of machine learning, the author is designing a utility that can predict the optimal machine parameters as an output while taking mould geometry details, raw material properties and known process parameters as the inputs.

This utility will attempt to eliminate the experimental method currently being used. It will reduce the wastage and costs associated with the experimental method. This method will also be faster than both the experimental and simulation method. Also, the intuitive nature of the process will be eliminated allowing for less trained staff to easily control the machines.

This utility uses an Artificial Neural Network (ANN), that has been already trained on a mix of real and simulated data. The trained ANN predicts the weight of the final part produced based on a set of machine parameters given as input. To find the optimal machine parameters, the utility first finds the actual weight of the part by multiplying the mould volume and raw material's density. Then the ANN cycles through all the possible machine parameters in a predefined range, predicting the part weight for each combination. The utility then outputs the optimal combination for which the predicted weight is greater or equal to the actual weight of the part.

## Prerequisites
The user requires **Python3** to be already installed on their systems to use this utility. 
#### ON WINDOWS
To install python3 on windows, the user can get the installer from [here](https://www.python.org/downloads/).
#### ON LINUX
To install python3 on Linux, the user can run the following command in the terminal
```
sudo apt-get update
sudo apt-get install python3
```

#### Other Dependencies
The user can then manually install the dependencies of the project using the commands given below. Alternatively, they can run the get-dependencies.bat ( on Windows ) or get-dependencies.sh ( on Linux ) to install the dependencies.
```
pip install flask 
pip install flask-sqlalchemy
pip install flask-wtf
pip install wtforms
pip install pyfladesk
pip install sklearn
pip install tensorflow
pip install numpy
pip install pandas
pip install joblib
```
## Installation
The utility is provided as a .zip archive. The user has to simply extract the archive to install the utility.
#### ON WINDOWS
To run the utility on Windows, the user needs to run **Predictor.exe**
#### ON LINUX
To run the utility on Linux, the user can use the following command in the terminal ( in the directory )
```
python3 run.py
```
or 
```
python run.py
```

## Author and License
Copyright (C) 2021 Joel Kundu

   This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

   This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

## Contact
The author can be contacted via the following emails:
- f20171399@hyderabad.bits-pilani.ac.in
- jdevcode02@gmail.com
