
# Moulding Machine Parameter Predictor
## Table of Contents
1.	[Introduction](#introduction)
2.	[Prerequisites](#prerequisites)
3.	[Download](#download)
4.	[Installation](#installation)
	- [As a Desktop App](#to-run-as-a-desktop-app)
	- [As a Web App](#to-run-as-a-web-app)
5.	[Usage](#usage)
	 - [Finding optimal machine parameters parameters](#finding-optimal-machine-parameters-parameters)
	 - [Managing the database](#managing-the-database)
		 - [Adding a single new entry to the database](#adding-a-single-new-entry-to-the-database)
		 - [Adding data entries from a csv file](#adding-data-entries-from-a-csv-file)
		 - [Deleting one entry from the database](#deleting-one-entry-from-the-database)
		 - [Deleting the entire database](#deleting-the-entire-database)
		 - [Export entire database as a CSV](#export-entire-database-as-a-csv)
		 - [Export CSV Format to add data to the database](#export-csv-format-to-add-data-to-the-database)
	 - [Managing the Artificial Neural Network](#managing-the-artificial-neural-network)
		 - [Understanding the performance of the ANN](#understanding-the-performance-of-the-ann)
		 - [Retrain the model](#retrain-the-model)
		 - [HyperTuning the Model](#hypertuning-the-model)
	-	[Getting Help](#getting-help)
6.	[Code Documentation](#code-documentation)
	- [Technology Documentation](#technology-documentation)	
	- [predictor/database.py](#python-script--database-.py)
	- [predictor/forms.py](#python-script-forms-.py)
	- [predictor/machine_learning.py](#python-script-machine_learning-.py)
	- [predictor/model.py](#python-script-models-.py)
	- [predictor/routes.py](#python-script-routes-.py)
	- [predictor/ui.py](#python-script--ui-.py)
	- [predictor/\_\_init\_\_.py](#python-script-__init__.py)
	- [run.py](#python-script-run-.py)
	- [run-server.py](#python-script-run-server-.py)
	- [man-recreatedb.py](#python-script-man-recreatedb-.py)
	- [man-overfit-test.py](#python-script-man-overfit-test-.py)
	- [man-hypertune,py](#python-script-man-hypertune-.py)
	- [get-dependencies.bat](#batch-script-get-dependencies-.bat)
	- [get-dependencies.sh](#shell-script-get-dependencies-.sh)
	- [source.cpp](#c-file-source.cpp)
7.	[Author and License](#author-and-license)
8.	[Contact](#contact)

___


## Introduction
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
pip install mathplotlib  
pip install numpy  
pip install pandas  
pip install os   
pip install shutil  
pip install joblib
```
## Download
-  Option 1 : 
Users can download the archive from [here](https://github.com/JOELKUNDU/MouldPredictor/archive/refs/heads/main.zip).

 - Option 2:
 Users can clone this repository using **git**, using the following commands.
	```
	git clone https://github.com/JOELKUNDU/MouldPredictor.git
	cd MouldPredictor
	```


## Installation
The user has to first extract the .zip archive that he has downloaded.
#### TO RUN AS A DESKTOP APP
##### ON WINDOWS
To run the utility on Windows, the user needs to run **Predictor.exe**
##### ON LINUX
To run the utility on Linux as a desktop app, the user can use the following command in the terminal ( in the directory )
```
make
```
This will make an executable with the name **Predictor-linux** which the user can then run.

#### TO RUN AS A WEB APP
The utility can be used as a desktop app or it can also be used as a web app hosted on a server. 
To host the utility on a server, the user has to follow the following steps.
- The user has to edit the **config.json** file in the predictor directory and change the value for ServerMode from False (default) to True (Case-sensitive) 
	```json
	{  
	  "ServerMode" : "True"  
	}
	```
-  The user has to install gunicorn with the command given below.
	```
	pip install gunicorn
	```
- Make sure all the dependencies are present. If not please refer to the dependencies section
- The user has to then open the terminal in the directory where the utility is saved and run the following command.
	```
	gunicorn -w 4 -b 127.0.0.1:5000 run-server:app
	``` 
- The web app would be hosted on **https://{ip address of the server}/5000/**
- To stop the server , the user can run the following comand.
	```
	 pkill gunicorn
	 ```

## Usage
### Finding optimal machine parameters parameters
To find the optimal machine parameter the user has to do the following steps.
- The user has to open the **Predict** tab from the navigation bar on the top of the screen
- The user has to fill the **Predict Form**
- The user has to click on the **Predict** button at the bottom of the **Predict Form**
- The output would be shown on the right pane under the **Output** section.
### Managing the database

#### Adding a single new entry to the database
It is recommended that the users regularly add new data into the database to improve the performance of the utility. To add a single new entry into the database the user has to follow the following steps.
- The user has to open the **Database** tab from the navigation bar on the top of the screen
- The user then has to then fill the form with the title **" Fill this form to add a new entry in the database "**
- The user has to click on the **ADD** button at the bottom of the form.
- The new entry would be the last in the database.

#### Adding data entries from a csv file
Before adding data from a CSV file, the user must ensure that **the columns in the csv file match the order of columns as shown in the database** displayed in the **Database** tab. 
To add data entries via a csv file the users have to follow the following steps.
- The user has to open the **Database** tab from the navigation bar on the top of the screen
- The user has to click on **Choose file** and then select the file in the dialog box that will open.
- The user has to then click on the **ADD** button below the text field.
- The new entries will be appended to the existing database.

#### Deleting one entry from the database
To delete one specific entry from the database the user has to follow the following steps.
- The user has to open the **Database** tab from the navigation bar on the top of the screen
- The user has to scroll down and find the entry he wishes to delete.
- The user can delete that specific entry by clicking on the delete button present on the right end of that row.

#### Deleting the entire database
It is recommended that the user exports the entire database before deleting it. To delete the entire database the user has to follow the following steps.
- The user has to open the **Database** tab from the navigation bar on the top of the screen
- The user has to scroll down to the bottom of the screen.
- The user has to then click on the red button labelled **WARNING: DELETE ENTIRE DATABASE**
- The entire database will be deleted
#### Export entire database as a CSV
To export the entire database as a CSV, the user has to follow the following steps.
- The user has to open the **Database** tab from the navigation bar on the top of the screen
- The user has to scroll down to the bottom of the screen.
- The user has to click on the green button labelled **EXPORT DATABASE AS CSV**
- The entire database will be exported as a database.csv file on the desktop
NOTE: Please ensure there is no database.csv file on the desktop else the function will fail.
- If the application is being used as a web app then the file will simply be downloaded on the client system.
#### Export CSV Format to add data to the database
To export the CSV format that the user can use to input data to the dataset the user has to follow the following steps.
- The user has to open the **Database** tab from the navigation bar on the top of the screen
- The user has to click on the **GET CSV FORMAT** button on the right of the add data via csv form.
- Format.csv file will be placed on the user's desktop.
NOTE Please ensure there is no Format.csv file on the desktop else the function will fail.
- If the application is being used as a web app then the file will simply be downloaded on the client system.

### Managing the Artificial Neural Network 
#### Understanding the performance of the ANN
To view the performance of the ANN, the user has to open the **Model** tab from the navigation bar on the top of the screen. When the screen loads, The user would be presented with a scatter plot ( Predicted weights vs Actual Weights ). The closer the scatters are to the diagonal of the chart, the better is the performance of the model. Below the plot, three performance metrics are shown.
- Absolute Mean Error ( lower the better )
- Maximum Error ( lower the better )
- Model Performance Score ( higher the better )

The performance of the model can be increased by regularly retraining the ANN on the expanding database.
The performance of the model can also be increased by occasionally hypertunning the model. However significant improvement might not happen after the first few uses of this tool

#### Retrain the model
Retraining the model allows the ANN to improve its performance by learning from the new data added to the database. To retrain the ANN the user has to follow the following steps.
- The user has to open the **Model** tab from the navigation bar on the top of the screen
- The user has to scroll down to the bottom of the screen.
- The user has to click on the button labelled **Retrain the model**
- This user can observe the process happening in the terminal window that opens along with the utility
- **NOTE**: This process will take time.

#### HyperTuning the Model
Hyper-Parameter tuning allows the model to tweak its setting automatically to better perform on the given dataset. This utility is fully automatic and requires no input from the user. To HyperTune the model, the user has to follow the following steps.
- The user has to open the **Model** tab from the navigation bar on the top of the screen
- The user has to scroll down to the bottom of the screen.
- - The user has to click on the button labelled **Auto-HyperTune the model**
- This user can observe the process happening in the terminal window that opens along with the utility
- **NOTE**: This process will take time.

### Getting Help
To resolve any issue related to how one can use the utility or to get information about the code, the user can refer to the manual that is present in the **Help** tab in the navigation bar. 

## Code Documentation
### Technology Documentation
This section includes links to the documentation or repositories of the technologies used in this project.

Flask
: [https://flask.palletsprojects.com/en/1.1.x/](https://flask.palletsprojects.com/en/1.1.x/)

Scikit-Learn
:  [https://scikit-learn.org/stable/](https://scikit-learn.org/stable/)

PyFlaDesk
: [https://github.com/smoqadam/PyFladesk](https://github.com/smoqadam/PyFladesk)

SQLAlchemy
: [https://docs.sqlalchemy.org/](https://docs.sqlalchemy.org/)

Flask WTF
: [https://flask-wtf.readthedocs.io/en/stable/](https://flask-wtf.readthedocs.io/en/stable/)

WTForms
: [https://wtforms.readthedocs.io/en/2.3.x/](https://wtforms.readthedocs.io/en/2.3.x/)

Numpy
: [https://numpy.org/doc/](https://numpy.org/doc/)

Pandas
: [https://pandas.pydata.org/docs/](https://pandas.pydata.org/docs/)

MathPlotLib
: [https://matplotlib.org/stable/contents.html](https://matplotlib.org/stable/contents.html)

Joblib
: [https://joblib.readthedocs.io/en/latest/](https://joblib.readthedocs.io/en/latest/)

Os
: [https://docs.python.org/3/library/os.html](https://docs.python.org/3/library/os.html)

Shutil
: [https://docs.python.org/3/library/shutil.html](https://docs.python.org/3/library/shutil.html)


___

### PYTHON SCRIPT : Database .py 
The functions in this script are mainly responsible for the retrieval and management of data to and from the database.
#### def add_from_csv(filepath)
```python
def add_from_csv(filepath):  
    dataframe = np.genfromtxt(filepath, delimiter=',')  
    dataframe = np.delete(dataframe, 0, 0)  
    rows = dataframe.shape[0]  
    for i in range(0, rows):  
        fill_time = dataframe[i][0]  
        injection_pres = dataframe[i][1]  
        holding_pres = dataframe[i][2]  
        holding_time = dataframe[i][3]  
        cooling_time = dataframe[i][4]  
  
        mould_temp = dataframe[i][5]  
        clamp_force = dataframe[i][6]  
        shot_weight = dataframe[i][7]  
  
        mould_SA = dataframe[i][8]  
        mould_vol = dataframe[i][9]  
        cavity_SA = dataframe[i][10]  
        cavity_vol = dataframe[i][11]  
  
        melt_temp = dataframe[i][12]  
        mat_density = dataframe[i][13]  
        mat_GF = dataframe[i][14]  
        mat_MMFR = dataframe[i][15]  
        part_weight = dataframe[i][16]  
        entry_to_create = Mould(  
								fill_time=fill_time,  
								injection_pres=injection_pres,  
								holding_pres=holding_pres,  
								holding_time=holding_time,  
								cooling_time=cooling_time,  
								mould_temp=mould_temp,  
								clamp_force=clamp_force,  
								shot_weight=shot_weight,  
								mould_SA=mould_SA,  
								mould_vol=mould_vol,  
								cavity_SA=cavity_SA,  
								cavity_vol=cavity_vol,  
								melt_temp=melt_temp,  
								mat_density=mat_density,  
								mat_GF=mat_GF,  
								mat_MMFR=mat_MMFR,  
								part_weight=part_weight,  
							  )  
        entry_to_create.add_self()
```
This method takes a string with the file path to the csv file as input and imports the dataset into the database from that .csv file. This method doesn't verify that the columns are in the correct sequence or have valid values. This has to be done by the user beforehand.

filepath
: String containing the path to the CSV file to be imported

NOTE: This function returns nothing
NOTE: In case of adding new attributes to the dataset this function has to be modified.

#### def get_datasets()
```python
def get_datasets():  
    entries = Mould.query.all()  
    dataframe = []  
  
    if entries:  
        for entry in entries:  
            data_object = [  
	              entry.fill_time,  
				  entry.injection_pres,  
				  entry.holding_pres,  
				  entry.holding_time,  
				  entry.cooling_time,  
				  
				  entry.mould_temp,  
				  entry.clamp_force,  
				  entry.shot_weight,  
				  
				  entry.mould_SA,  
				  entry.mould_vol,  
				  entry.cavity_SA,  
				  entry.cavity_vol,  
				  
				  entry.melt_temp,  
				  entry.mat_density,  
				  entry.mat_GF,  
				  entry.mat_MMFR,  
				  entry.part_weight  
            ]  
            dataframe.append(data_object)  
        dataframe = np.array(dataframe)  
  
        x = dataframe[:, :dataframe.shape[1] - 1]  
        y = dataframe[:, dataframe.shape[1] - 1]  
  
        return x, y  
    else:  
        return[[]], []
```
 This method loads the dataset from the sqlalchemy database (data.db) and returns the following arrays

x
: np.array containing all the features of the dataset.

y
: np.array containing all the part weights corresponding to the rows of features in x.
NOTE: In case of adding new attributes to the dataset this function has to be modified.
#### def purge():
```python
def purge():  
    entries = Mould.query.all()  
    for entry in entries:  
        entry.delete_self()
```
This method erases the entire database 
NOTE: This function returns nothing

####   def exportCSV():
```python
def exportCSV():  
    if os.name == 'nt':  
        dest = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop\\database.csv')  
    else:  
        desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')  
        dest = desktop + '/database.csv'  
  if os.path.exists(dest):  
        return False  
 else:  
        entries = Mould.query.all()  
        dataframe = []  
        for entry in entries:  
            data_object = [  
                  entry.fill_time,  
				  entry.injection_pres,  
				  entry.holding_pres,  
				  entry.holding_time,  
				  entry.cooling_time,  
				  
				  entry.mould_temp,  
				  entry.clamp_force,  
				  entry.shot_weight,  
				  
				  entry.mould_SA,  
				  entry.mould_vol,  
				  entry.cavity_SA,  
				  entry.cavity_vol,  
				  
				  entry.melt_temp,  
				  entry.mat_density,  
				  entry.mat_GF,  
				  entry.mat_MMFR,  
				  entry.part_weight  
            ]  
            dataframe.append(data_object)  
        dataframe = np.array(dataframe)  
        DF = pd.DataFrame(dataframe)  
        DF.to_csv('predictor/uploads/database.csv')  
        source = 'predictor/uploads/database.csv'  
	    shutil.copyfile(source, dest)  
        return True
```
This method exports the entire dataset in file name database.csv on the user's desktop. 
NOTE: This function returns true when successful, else it will return false.

#### def exportCSVFormat():
```python
def exportCSVFormat():  
    if os.name == 'nt':  
        dest = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop\\Format.csv')  
    else:  
        desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')  
        dest = desktop + '/Format.csv'  
	if os.path.exists(dest):  
	    return False  
	else:  
	    source = 'predictor/uploads/Format.csv'  
	shutil.copyfile(source, dest)  
	    return True
```
This method exports the CSV format that the user can then use to enter data into the database by using the add_from_csv function.
NOTE: This function returns true when successful, else it will return false

#### def serverExportCSV():
```python
def serverExportCSV():  
    entries = Mould.query.all()  
    dataframe = []  
    for entry in entries:  
        data_object = [  
			entry.fill_time,  
			entry.injection_pres,  
			entry.holding_pres,  
			entry.holding_time,  
			entry.cooling_time,  

			entry.mould_temp,  
			entry.clamp_force,  
			entry.shot_weight,  

			entry.mould_SA,  
			entry.mould_vol,  
			entry.cavity_SA,  
			entry.cavity_vol,  

			entry.melt_temp,  
			entry.mat_density,  
			entry.mat_GF,  
			entry.mat_MMFR,  
			entry.part_weight  
        ]  
        dataframe.append(data_object)  
    dataframe = np.array(dataframe)  
    DF = pd.DataFrame(dataframe)  
    source = os.path.join(app.config['CLIENT_CSV'], 'database.csv')  
    os.remove(source)  
    DF.to_csv(source)  
    return send_file(source, as_attachment=True, attachment_filename='database.csv')
```
This function converts the database to a csv file and sends it to the user when in web app mode.

#### def serverExportCSVFormat():
```python
def serverExportCSVFormat():  
    source = os.path.join(app.config['CLIENT_CSV'], 'format.csv')  
    return send_file(source, as_attachment=True, attachment_filename='format.csv')
```
This function sends the csv format to the user when in web app mode.
    
___

### PYTHON SCRIPT: Forms .py
The classes in this script define all the WTForms used across the utility. Detailed definitions of the wtforms functions used in this script can be found [here](https://flask-wtf.readthedocs.io/en/stable/)  and [here](https://wtforms.readthedocs.io/en/2.3.x/). 
NOTE: FlaskForm is a class provided by the flask_wtf module and its details can be found from the above links.
#### class PredictForm (FlaskForm)
```python
class PredictForm(FlaskForm):  
  
    Fill_time_min = IntegerField(label='Fill time Min', validators=[DataRequired(message='Please enter a valid input for Minimum Fill Time'), NumberRange(min=0, max=999999, message='Please enter a valid input for Minimum Fill Time')])  
    Fill_time_max = IntegerField(label='Fill time Max', validators=[DataRequired(message='Please enter a valid input for Maximum Fill Time'), NumberRange(min=0, max=999999, message='Please enter a valid input for Maximum Fill Time')])  
    Fill_time_res = IntegerField(label='Fill time Res', validators=[DataRequired(message='Please enter a valid input for Fill Time Resolution'), NumberRange(min=0, max=999999, message='Please enter a valid input for Fill Time Resolution')])  
  
    Injection_pres_min = IntegerField(label='Injection pressure Min', validators=[DataRequired(message='Please enter a valid input for Minimum Injection Pressure'), NumberRange(min=0, max=999999, message='Please enter a valid input for Minimum Injection Pressure')])  
    Injection_pres_max = IntegerField(label='Injection pressure Max', validators=[DataRequired(message='Please enter a valid input for Maximum Injection Pressure'), NumberRange(min=0, max=999999, message='Please enter a valid input for Maximum Injection Pressure')])  
    Injection_pres_res = IntegerField(label='Injection pressure Res', validators=[DataRequired(message='Please enter a valid input for Injection Pressure Resolution'), NumberRange(min=0, max=999999, message='Please enter a valid input for Injection Pressure Resolution')])  
  
    Holding_pres_min = IntegerField(label='Holding PressureMin', validators=[DataRequired(message='Please enter a valid input for Minimum Holding Pressure'), NumberRange(min=0, max=999999, message='Please enter a valid input for Minimum Holding Pressure')])  
    Holding_pres_max = IntegerField(label='Holding PressureMax', validators=[DataRequired(message='Please enter a valid input for Maximum Holding Pressure'), NumberRange(min=0, max=999999, message='Please enter a valid input for Maximum Holding Pressure')])  
    Holding_pres_res = IntegerField(label='Holding PressureRes', validators=[DataRequired(message='Please enter a valid input for Holding Pressure Resolution'), NumberRange(min=0, max=999999, message='Please enter a valid input for Holding Pressure Resolution')])  
  
    Holding_time_min = IntegerField(label='Holding time Min', validators=[DataRequired(message='Please enter a valid input for Minimum Holding Time'), NumberRange(min=0, max=999999, message='Please enter a valid input for Minimum Holding Time')])  
    Holding_time_max = IntegerField(label='Holding time Max', validators=[DataRequired(message='Please enter a valid input for Maximum Holding Time'), NumberRange(min=0, max=999999, message='Please enter a valid input for Maximum Holding Time')])  
    Holding_time_res = IntegerField(label='Holding time Res', validators=[DataRequired(message='Please enter a valid input for Holding Time Resolution'), NumberRange(min=0, max=999999, message='Please enter a valid input for Holding Time Resolution')])  
  
    Cooling_time_min = IntegerField(label='Cooling time Min', validators=[DataRequired(message='Please enter a valid input for Minimum Cooling Time'), NumberRange(min=0, max=999999, message='Please enter a valid input for Minimum Cooling Time')])  
    Cooling_time_max = IntegerField(label='Cooling time Max', validators=[DataRequired(message='Please enter a valid input for Maximum Cooling Time'), NumberRange(min=0, max=999999, message='Please enter a valid input for Maximum Cooling Time')])  
    Cooling_time_res = IntegerField(label='Cooling time Res', validators=[DataRequired(message='Please enter a valid input for Cooling Time Resolution'), NumberRange(min=0, max=999999, message='Please enter a valid input for Cooling Time Resolution')])  
  
    Mould_temp = IntegerField(label='Mould Temp in Cel', validators=[DataRequired(message='Please enter a valid input for Mould Temperature'), NumberRange(min=0, max=999999, message='Please enter a valid input for Mould Temperature')])  
    Clamp_force = IntegerField(label='Clamp force in tonnes', validators=[DataRequired(message='Please enter a valid input for Clamp Force'), NumberRange(min=0, max=999999, message='Please enter a valid input for Clamp Force')])  
    Shot_Weight = FloatField(label="Mould Surface Area in mm3", validators=[DataRequired(message='Please enter a valid input for Shot Weight'), NumberRange(min=0, max=999999, message='Please enter a valid input for Shot Weight')])  
  
    Mould_SA = FloatField(label="Mould Surface Area in mm3", validators=[DataRequired(message='Please enter a valid input for Mould Surface Area'), NumberRange(min=0, max=999999, message='Please enter a valid input for Mould Surface Area')])  
    Mould_vol = FloatField(label="Mould Volume in cm3", validators=[DataRequired(message='Please enter a valid input for Mould Volume'), NumberRange(min=0, max=999999, message='Please enter a valid input for Mould Volume')])  
    Cavity_SA = FloatField(label="Mould Surface Area in mm3", validators=[DataRequired(message='Please enter a valid input for Cavity Surface Area'), NumberRange(min=0, max=999999, message='Please enter a valid input for Cavity Surface Area')])  
    Cavity_vol = FloatField(label="Mould Volume in cm3", validators=[DataRequired(message='Please enter a valid input for Cavity Volume'), NumberRange(min=0, max=999999, message='Please enter a valid input for Cavity Volume')])  
  
    Mat_density = FloatField(label="Material Density g/cm3", validators=[DataRequired(message='Please enter a valid input for Material Density'), NumberRange(min=0, max=999999, message='Please enter a valid input for Material Density')])  
    Melt_temp = IntegerField(label='Melt Temp in Cel', validators=[DataRequired(message='Please enter a valid input for Material Melt Temperature'), NumberRange(min=0, max=999999, message='Please enter a valid input for Material Melt Temperature')])  
    Mat_GF = IntegerField(label='Melt Temp in Cel', validators=[DataRequired(message='Please enter a valid input for Material GF%'), NumberRange(min=0, max=999999, message='Please enter a valid input for Material GF%')])  
    Mat_MMFR = FloatField(label="Material Density g/cm3", validators=[DataRequired(message='Please enter a valid input for Material Melt Mass Flow Rate'), NumberRange(min=0, max=999999, message='Please enter a valid input for Material Melt Mass Flow Rate')])  
    submit = SubmitField(label='Predict')
```
This class defines the input fields for the Predict form the is shown in the Predict tab of the utility. 
NOTE: In case of adding new attributes to the dataset this class has to be modified.
#### class AddEntryForm (FlaskForm)
```python
class AddEntryForm(FlaskForm):  
    Fill_time = IntegerField(label='Fill time', validators=[DataRequired(message='Please enter a valid input for Fill Time'), NumberRange(min=0, max=999999, message='Please enter a valid input')])  
    Injection_pres = IntegerField(label='Injection pressure', validators=[DataRequired(message='Please enter a valid input for Injection Pressure'), NumberRange(min=0, max=999999, message='Please enter a valid input')])  
    Holding_pres = IntegerField(label='Holding Pressure', validators=[DataRequired(message='Please enter a valid input for Holding Pressure'), NumberRange(min=0, max=999999, message='Please enter a valid input')])  
    Holding_time = IntegerField(label='Holding time', validators=[DataRequired(message='Please enter a valid input for Holding Time'), NumberRange(min=0, max=999999, message='Please enter a valid input')])  
    Cooling_time = IntegerField(label='Cooling time', validators=[DataRequired(message='Please enter a valid input for Cooling Time'), NumberRange(min=0, max=999999, message='Please enter a valid input')])  
    Mould_temp = IntegerField(label='Mould Temp in Cel', validators=[DataRequired(message='Please enter a valid input for Mould Temp'), NumberRange(min=0, max=999999, message='Please enter a valid input')])  
    Clamp_force = IntegerField(label='Clamp force in tonnes', validators=[DataRequired(message='Please enter a valid input for Clamp Force'), NumberRange(min=0, max=999999, message='Please enter a valid input')])  
    Shot_Weight = FloatField(label="Mould Surface Area in mm3", validators=[DataRequired(message='Please enter a valid input for Shot Weight'), NumberRange(min=0, max=999999, message='Please enter a valid input')])  
    Mould_SA = FloatField(label="Mould Surface Area in mm3", validators=[DataRequired(message='Please enter a valid input for Mould Surface Area'), NumberRange(min=0, max=999999, message='Please enter a valid input')])  
    Mould_vol = FloatField(label="Mould Volume in cm3", validators=[DataRequired(message='Please enter a valid input for Mould Volume'), NumberRange(min=0, max=999999, message='Please enter a valid input')])  
    Cavity_SA = FloatField(label="Mould Surface Area in mm3", validators=[DataRequired(message='Please enter a valid input for Cavity Surface Area'), NumberRange(min=0, max=999999, message='Please enter a valid input')])  
    Cavity_vol = FloatField(label="Mould Volume in cm3", validators=[DataRequired(message='Please enter a valid input for Cavity Volume'), NumberRange(min=0, max=999999, message='Please enter a valid input')])  
    Mat_density = FloatField(label="Material Density g/cm3", validators=[DataRequired(message='Please enter a valid input for Material Density'), NumberRange(min=0, max=999999, message='Please enter a valid input')])  
    Melt_temp = IntegerField(label='Melt Temp in Cel', validators=[DataRequired(message='Please enter a valid input for Material Melt Temperature'), NumberRange(min=0, max=999999, message='Please enter a valid input')])  
    Mat_GF = IntegerField(label='Melt Temp in Cel', validators=[DataRequired(message='Please enter a valid input for Material GF%'), NumberRange(min=0, max=999999, message='Please enter a valid input')])  
    Mat_MMFR = FloatField(label="Material Density g/cm3", validators=[DataRequired(message='Please enter a valid input for Material Melt Mass Flow Rate'), NumberRange(min=0, max=999999, message='Please enter a valid input')])  
    Part_weight = FloatField(label="Part Weight", validators=[DataRequired(message='Please enter a valid input for Part Weight'), NumberRange(min=0, max=999999, message='Please enter a valid input')])  
    submit = SubmitField(label='ADD')
```
This class defines the input fields for the form to add a new entry to the dataset in the database tab of the utility. 
NOTE: In case of adding new attributes to the dataset this class has to be modified.
#### class AddEntryCSV(FlaskForm)
```python
class AddEntryCSV(FlaskForm):  
    file = FileField(label="csv file path", validators=[DataRequired(message='Please enter a valid input for ')])  
    submit = SubmitField(label='ADD')
```
This class defines the input field for the form to add data to the dataset using a csv file that is available in the database tab of the utility.
#### class DeleteEntryForm(FlaskForm)
```python
  
class DeleteEntryForm(FlaskForm):  
    submit = SubmitField(label="DELETE")
```
This class defines the delete button present in each row of the dataset the is shown when the user accesses the database tab of the utility
#### class class DeleteAllEntries(FlaskForm)
```python
class DeleteAllEntries(FlaskForm):  
    submit = SubmitField(label="WARNING: DELETE ENTIRE DATABASE")
```
This class defines the delete entire database button on the bottom of the screen of the database tab.
#### class ExportAllEntries(FlaskForm)
```python
class ExportAllEntries(FlaskForm):  
    submit = SubmitField(label="EXPORT DATABASE AS CSV")
```
This class defines the EXPORT DATABASE AS CSV button on the bottom of the screen of the database tab. 
#### class GetCSVFormat(Flask Form)
```python
class GetCSVFormatForm(FlaskForm):  
    submit = SubmitField(label="GET CSV FORMAT")
```
This class defines the GET CSV FORMAT button shown beside the add data form csv form in the database tab.
####   class RetrainModel(FlaskForm)
```python
class RetrainModel(FlaskForm):  
    submit = SubmitField(label="Retrain the model")
```
This class defines the Retrain the model button shown at the bottom of the screen of the model tab.
####   class HyperTuneModel(FlaskForm)
```python
class HyperTuneModel(FlaskForm):  
    submit = SubmitField(label="Auto-HyperTune the model")
```
This class defines the Auto Hyper-Tune the model button shown at the bottom of the screen of the model tab.

User can refer to the functions in models .py, machine_learning .py, database .py or routes .py to understand how each of these form's logic is implemented.
___

### PYTHON SCRIPT: Machine_learning .py
This script implements all the functions that enable machine learning aspects of the utility. Detailed documentation about the scikit-learn library can be found [here](https://scikit-learn.org/stable/).

#### class ModelMetric
```python
class ModelMetrics:  
    absolute_mean_error = 0.0  
	modelScore = 0.0  
	max_error = 0.0  
  
	def printMetric(self):  
        print(self.modelScore)  
        print(self.max_error)  
        print(self.absolute_mean_error)  
  
    def savePerformance(self):  
        DBModelMetrics(absolute_mean_error=self.absolute_mean_error,  
		model_score=self.modelScore,  
		max_error=self.max_error).save()  
  
    def loadPerformance(self):  
        perf = DBModelMetrics.query.filter_by(id=1).first()  
        self.absolute_mean_error = perf.absolute_mean_error  
        self.modelScore = perf.model_score  
        self.max_error = perf.max_error  
        self.printMetric()  
  
  
ml_metrics = ModelMetrics()
```
The main function of the object of this class is to save data about the model's performance from training and tuning events and to store and retrieve them from the database. The following performance metrics are stored.

absolute_mean_error
: This is a measure of errors between paired observations expressing the same phenomenon. 

max_error
: This is the maximum amount you expect a system to be off by.

modelScore
: This return the coefficient of determination R^2 of the prediction,
details of which can be found [here](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPRegressor.html?highlight=mlp%20regressor) (score method of MLPRegressor model).

Other methods of the class are described below.

 - **def printMetric(self)**
	 - This function prints the values stored in the object on the console window.
- **def savePerformance(self)**
	- This function saves the values stored in object in the database.
- **def loadPerformance(self)**
	- This function loads previously saved data about the model's performance from the database.
#### def hyperTune()
```python
def hyperTune():  
    parameter_space = {  
			'hidden_layer_sizes': [(50, 50, 50)],  
			'activation': ['tanh', 'relu', 'logistic', 'identity'],  
			'solver': ['sgd', 'adam', 'lbfgs'],  
			'alpha':  [0.001, 0.01, 0.1, 0.0001,  
			0.002, 0.02, 0.2, 0.0002,  
			0.003, 0.03, 0.3, 0.0003,  
			0.004, 0.04, 0.4, 0.0004,  
			0.005, 0.05, 0.5, 0.0005,  
			0.006, 0.06, 0.6, 0.0006,  
			0.007, 0.07, 0.7, 0.0007,  
			0.008, 0.08, 0.8, 0.0008,  
			0.009, 0.09, 0.9, 0.0009],  
			'learning_rate': ['constant', 'adaptive', 'invscaling'],  
			'learning_rate_init': [0.001, 0.01, 0.1, 0.0001,  
			0.002, 0.02, 0.2, 0.0002,  
			0.003, 0.03, 0.3, 0.0003,  
			0.004, 0.04, 0.4, 0.0004,  
			0.005, 0.05, 0.5, 0.0005,  
			0.006, 0.06, 0.6, 0.0006,  
			0.007, 0.07, 0.7, 0.0007,  
			0.008, 0.08, 0.8, 0.0008,  
			0.009, 0.09, 0.9, 0.0009],  
			'random_state': [1399],  
			'warm_start': [True],  
			'max_iter': [100000, 75000, 125000],  
			'verbose': [True]  
    }  
    trained_model = MLPRegressor()  
    X, y = database.get_datasets()  
    X, X_test, y, y_test = train_test_split(X, y, test_size=0.33, random_state=1)  
    clf = RandomizedSearchCV(trained_model, parameter_space, n_jobs=-1, cv=2, verbose=10)  
    clf.fit(X, y)  
    print('\n\n\nBEST PARAMS', clf.best_params_)  
    print('\n\n\nResults', clf.cv_results_)  
    jl.dump(clf, 'predictor/static/ML/config.joblib')  
    retrain()
```
This function uses [RandomizedSearchCV](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.RandomizedSearchCV.html?highlight=randomized#sklearn.model_selection.RandomizedSearchCV) from scikit learn library to set the optimal parameters for the ANN. Since the method is randomized a few executions of this method might be required before optimal parameters can be set. This function is also responsible for saving the optimized model for later use. This is implemented using the joblib library
#### def MLPRmodel(X_test)
```python
def MLPRmodel(X_test):    
  if os.path.exists('predictor/static/ML/config.joblib'):  
        model = jl.load('predictor/static/ML/config.joblib')  
    else:  
        hyperTune()  
        model = jl.load('predictor/static/ML/config.joblib')   
  pred = model.predict(X_test)    
  return pred
```
This function verifies if a trained model exists else it will call the hypertune() function to create and optimized the model first. Then this function will load the optimized model and use it to make predictions using the data passed in the **X_test** list and returns those predictions as a list.
#### def getScore():
```python
def getScore():  
	trained_model = jl.load('predictor/static/ML/config.joblib')  
	X, y = database.get_datasets()   
	return trained_model.score(X, y)
```
This return the coefficient of determination R^2 of the predictions made by the model,
details of which can be found [here](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPRegressor.html?highlight=mlp%20regressor) (score method of MLPRegressor model).
#### def init_load_up()
```python
def init_load_up():  
    if not os.path.exists('predictor/static/ML/config.joblib'):  
        hyperTune()  
        X, y = database.get_datasets()  
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=1)  
        pred = MLPRmodel(X_test)  
  
        ml_metrics.absolute_mean_error = metrics.mean_absolute_error(y_test, pred)  
        ml_metrics.modelScore = getScore()  
        ml_metrics.max_error = metrics.max_error(y_test, pred)  
        ml_metrics.savePerformance()  
  
        plt.scatter(y_test, pred, color='b')  
        plt.xlabel('Actual Weight')  
        plt.ylabel('Predicted Weight')  
        plt.title('Scatter Plot (Actual vs Predicted Part Weight)')  
        # save the plot  
    plt.savefig('predictor/static/ML/performance.png', bbox_inches='tight')  
    ml_metrics.loadPerformance()
```
This function is executed whenever the utility is loaded and this ensures that the model exists. if not then it calls on the hypertune() function to create an optimized model. It will then measure the model's performance and will save it into the database. This function also creates the scatter plot chart shown in the model tab using the MathPlotLib library.
#### def retrain()
```python
def retrain():  
    X, y = database.get_datasets()  
    # Splitting the data into test and trained data  
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=1)  
    # Training the model and verifying the mean absolute error  
  
    trained_model = jl.load('predictor/static/ML/config.joblib')  
  
    trained_model.fit(X_train, y_train)  
    pred = trained_model.predict(X_test)  
  
    ml_metrics.absolute_mean_error = metrics.mean_absolute_error(y_test, pred)  
    ml_metrics.modelScore = getScore()  
    ml_metrics.max_error = metrics.max_error(y_test, pred)  
    ml_metrics.savePerformance()  
  
    pred = trained_model.predict(X)  
  
    # Preparing the scatter plot of the model's prediction  
	plt.scatter(y, pred, color='b')  
    plt.xlabel('Actual Weight')  
    plt.ylabel('Predicted Weight')  
    plt.title('Scatter Plot (Actual vs Predicted Part Weight)')  
    # save the plot  
    plt.savefig('predictor/static/ML/performance.png', bbox_inches='tight')  
    ml_metrics.loadPerformance()
```
This function loads the database and divides it into training and testing data. This function then loads the ANN model and retrains it on the training data and calculates the model's performance metrics using the testing data. This function also recreates the scatter plot of the model's performance using the MathPlotLib library.
#### def getPredict (Fill_time, Injection_pres, Holding_pres, Holding_time, Cooling_time, Mould_temp, Clamp_force, Shot_Weight, Mould_SA, Mould_vol, Cavity_SA, Cavity_vol, Melt_temp, Mat_density, Mat_GF, Mat_MMFR)
```python
def getPredict(Fill_time, Injection_pres, Holding_pres, Holding_time, Cooling_time,  
  Mould_temp, Clamp_force, Shot_Weight,  
  Mould_SA, Mould_vol, Cavity_SA, Cavity_vol,  
  Melt_temp, Mat_density, Mat_GF, Mat_MMFR):  
    init_load_up()  
    trained_model = jl.load('predictor/static/ML/config.joblib')  
    X = [[Fill_time, Injection_pres, Holding_pres, Holding_time, Cooling_time,  
		  Mould_temp, Clamp_force, Shot_Weight,  
		  Mould_SA, Mould_vol, Cavity_SA, Cavity_vol,  
		  Melt_temp, Mat_density, Mat_GF, Mat_MMFR]]  
    pred = trained_model.predict(X)  
    return pred[0]
```
This functions takes the values from the variables in the parameter list, converts them into a list that can be passed into the model. It then loads the model and passes the previously created list to get one prediction. The function then returns this prediction.

#### def predict (Fill_time_min, Fill_time_max, Fill_time_res, Injection_pres_min, Injection_pres_max, Injection_pres_res,  Holding_pres_min, Holding_pres_max, Holding_pres_res,  Holding_time_min, Holding_time_max, Holding_time_res,  Cooling_time_min, Cooling_time_max, Cooling_time_res,  Mould_temp, Clamp_force, Shot_Weight,  Mould_SA, Mould_vol, Cavity_SA, Cavity_vol,  Mat_density, Melt_temp, Mat_GF, Mat_MMFR)
```python
def predict(  
  Fill_time_min, Fill_time_max, Fill_time_res,  
  Injection_pres_min, Injection_pres_max, Injection_pres_res,  
  Holding_pres_min, Holding_pres_max, Holding_pres_res,  
  Holding_time_min, Holding_time_max, Holding_time_res,  
  Cooling_time_min, Cooling_time_max, Cooling_time_res,  
  Mould_temp, Clamp_force, Shot_Weight,  
  Mould_SA, Mould_vol, Cavity_SA, Cavity_vol,  
  Mat_density, Melt_temp, Mat_GF, Mat_MMFR  
):  
    init_load_up()  
    trained_model = jl.load('predictor/static/ML/config.joblib')  
    weight_actual = Mould_vol * Mat_density  
    print("\nweight:", weight_actual)  
    first_pred = True  
	param = []  
    for ft in range(Fill_time_min, Fill_time_max + 1, Fill_time_res):  
        for ip in range(Injection_pres_min, Injection_pres_max + 1, Injection_pres_res):  
            for hp in range(Holding_pres_min, Holding_pres_max + 1, Holding_pres_res):  
                for ht in range(Holding_time_min, Holding_time_max + 1, Holding_time_res):  
                    for ct in range(Cooling_time_min, Cooling_time_max + 1, Cooling_time_res):  
                        X = [[ft, ip, hp, ht, ct,  
							  Mould_temp, Clamp_force, Shot_Weight,  
							  Mould_SA, Mould_vol, Cavity_SA, Cavity_vol,  
							  Melt_temp, Mat_density, Mat_GF, Mat_MMFR]]  
                        pred = trained_model.predict(X)  
                        print("param:", X, "\nPred:", pred, "\nweight:", weight_actual)  
                        if weight_actual <= pred[0] <= weight_actual * 1.01:  
                            if first_pred:  
                                param = X[0]  
                                param.append(pred[0])  
                                param.append(weight_actual)  
                                break  
					 else:  
                        continue  
				 break else:  
                    continue  
			 break else:  
                continue  
		 break else:  
            continue  
	 break return param
```
This function takes the values from the variables in the parameter list, then it starts to iterate through all the possible combination of the individual parameters bounded by the upper and lower (minimum and maximum) values that were also passed in as a parameter. The function then passes each iteration through the ANN and verifies if the predicted weight is greater than the value we would get from mould volume x raw material density. If it verifies true then that combination is returned as the optimal set of machine parameters.
___
### PYTHON SCRIPT: Models .py
This python script defines all the tables that are stored in the SQLAlchemy database. Detailed documentation about the SQLAlchemy functions used in this script can be found [here](https://docs.sqlalchemy.org/).
#### def initDb()
```python
def initDb():  
    if not os.path.exists('predictor/data.db'):  
        db.create_all()  
        db.session.commit()
```
This function ensures that the data.db file exists and is already configured.

#### class Mould(db.Model)
```python
class Mould(db.Model):  
    id = db.Column(db.Integer(), primary_key=True)  
    fill_time = db.Column(db.Integer(), nullable=False)  
    injection_pres = db.Column(db.Integer(), nullable=False)  
    holding_pres = db.Column(db.Integer(), nullable=False)  
    holding_time = db.Column(db.Integer(), nullable=False)  
    cooling_time = db.Column(db.Integer(), nullable=False)  
  
    mould_temp = db.Column(db.Integer(), nullable=False)  
    clamp_force = db.Column(db.Integer(), nullable=False)  
    shot_weight = db.Column(db.Float(), nullable=False)  
  
    mould_SA = db.Column(db.Float(), nullable=False)  
    mould_vol = db.Column(db.Float(), nullable=False)  
    cavity_SA = db.Column(db.Float(), nullable=False)  
    cavity_vol = db.Column(db.Float(), nullable=False)  
  
    melt_temp = db.Column(db.Float(), nullable=False)  
    mat_density = db.Column(db.Float(), nullable=False)  
    mat_GF = db.Column(db.Integer(), nullable=False)  
    mat_MMFR = db.Column(db.Float(), nullable=False)  
  
    part_weight = dbf.Column(db.Float(), nullable=False)  
  
    def delete_self(self):  
        db.session.delete(self)  
        db.session.commit()  
  
    def add_self(self):  
        db.session.add(self)  
        db.session.commit()
```
This class defines the table that stores the entire database on which the ANN is trained. The following methods are also present in this class.

def delete_self(self)
: This deletes the specific entry that the object of this class is referring to, from the database.

def add_self(self)
: This function adds the new entry saved in the object of this class into the database.

#### class DBModelMetrics(db.Model)
```python
class DBModelMetrics(db.Model):  
    id = db.Column(db.Integer(), primary_key=True)  
    absolute_mean_error = db.Column(db.Float(), nullable=True)  
    model_score = db.Column(db.Float(), nullable=True)  
    max_error = db.Column(db.Float(), nullable=True)  
  
    def save(self):  
        DBModelMetrics.query.filter_by(id=1).delete()  
        db.session.add(self)  
        db.session.commit()
```
This class defines the table that stores the model's performance metrics. The following method is also present in this class.

def save(self)
: This deletes the presently stored metric and saves the new metrics save in the object in the database.
___
### PYTHON SCRIPT: Routes .py
This script handles the app routing for the Flask App. App routing is used to map the specific URL with the associated function that is intended to perform some task. It is used to access some particular page like the predict page or the database page. 
#### def home_page()
```python
@app.route('/')  
@app.route('/home')  
def home_page():  
    return render_template('home.html')
```
This function is responsible for rendering the home page of the app.
#### def main_page() 
```python
@app.route('/main-page')  
def main_page():  
    return render_template('main.html')
```
This function is responsible for rendering the main landing page of the app.
#### def predict_page()
```python
@app.route('/predict-page', methods=['GET', 'POST'])  
def predict_page():  
    predict_form = PredictForm()  
    output = np.zeros(shape=10)  
    if request.method == 'POST':  
        if predict_form.validate_on_submit():  
            output = ml.predict(  
				                  Fill_time_min=predict_form.Fill_time_min.data,  
								  Fill_time_max=predict_form.Fill_time_max.data,  
								  Fill_time_res=predict_form.Fill_time_res.data,  
								  Injection_pres_min=predict_form.Injection_pres_min.data,  
								  Injection_pres_max=predict_form.Injection_pres_max.data,  
								  Injection_pres_res=predict_form.Injection_pres_res.data,  
								  Holding_pres_min=predict_form.Holding_pres_min.data,  
								  Holding_pres_max=predict_form.Holding_pres_max.data,  
								  Holding_pres_res=predict_form.Holding_pres_res.data,  
								  Holding_time_min=predict_form.Holding_time_min.data,  
								  Holding_time_max=predict_form.Holding_time_max.data,  
								  Holding_time_res=predict_form.Holding_time_res.data,  
								  Cooling_time_min=predict_form.Cooling_time_min.data,  
								  Cooling_time_max=predict_form.Cooling_time_max.data,  
								  Cooling_time_res=predict_form.Cooling_time_res.data,  
								  
								  Mould_temp=predict_form.Mould_temp.data,  
								  Clamp_force=predict_form.Clamp_force.data,  
								  Shot_Weight=predict_form.Shot_Weight.data,  
								  
								  Mould_SA=predict_form.Mould_SA.data,  
								  Mould_vol=predict_form.Mould_vol.data,  
								  Cavity_SA=predict_form.Cavity_SA.data,  
								  Cavity_vol=predict_form.Cavity_vol.data,  
								  
								  Melt_temp=predict_form.Melt_temp.data,  
								  Mat_density=predict_form.Mat_density.data,  
								  Mat_GF=predict_form.Mat_GF.data,  
								  Mat_MMFR=predict_form.Mat_MMFR.data  
            )  
            print('Results: ', output)  
            if not output:  
                output = [0.0, 0.0, 0.0, 0.0, 0.0]  
                flash('No optimal machine parameters were found for the given constraints', 'error')  
                return render_template('predict.html', form=predict_form, output=output)  
            else:  
                flash('Successfully found optimal parameters', 'Success')  
                return render_template('predict.html', form=predict_form, output=output)  
        if predict_form.errors != {}:  
            flash('Invalid values in Predict Form', category='error')  
            return redirect(url_for('predict_page'))  
    if request.method == 'GET':  
        return render_template('predict.html', form=predict_form, output=output)
```
This function is responsible for rendering and implementing the logic behind the predict page of the app. This function accepts the values entered in the predict form (POST method) and then passes it to predict() function from machine_learning.py script and then shows the output of the function by re-rendering the predict page and passing the predicted values to it.
#### def model_page()
```python
@app.route('/model-page', methods=['POST', 'GET'])  
def model_page():  
    ml.init_load_up()  
    retrainmodel = RetrainModel()  
    hypertunemodel = HyperTuneModel()  
    absMeanError = ml.ml_metrics.absolute_mean_error  
    modelScore = ml.ml_metrics.modelScore  
    maxError = ml.ml_metrics.max_error  
    if request.method == 'POST':  
        retrain = request.form.get('Retrain-model')  
        if retrain:  
            ml.retrain()  
            flash('Model Retrained Successfully', 'success')  
            return render_template('model.html',  
								  absMeanError=absMeanError,  
								  modelScore=modelScore,  
								  maxError=maxError,  
								  RetrainModel=retrainmodel,  
								  HyperTuneModel=hypertunemodel)  
        retrain = request.form.get('HyperTune-model')  
        if retrain:  
            flash('Model HyperTuned Successfully', 'success')  
            flash('If the model\'s performance has decreased then you need to run the HyperTune utility again', 'info')  
            ml.hyperTune()  
            return render_template('model.html',  
								  absMeanError=absMeanError,  
								  modelScore=modelScore,  
								  maxError=maxError,  
								  RetrainModel=retrainmodel,  
								  HyperTuneModel=hypertunemodel)  
    if request.method == 'GET':  
        return render_template('model.html',  
							  absMeanError=absMeanError,  
							  modelScore=modelScore,  
							  maxError=maxError,  
							  RetrainModel=retrainmodel,  
							  HyperTuneModel=hypertunemodel)
```
This function is responsible for rendering and implementing the logic behind the model page of the app. 
#### def database_page()
```python
  
@app.route('/database-page', methods=['GET', 'POST'])  
def database_page():  
    addentryform = AddEntryForm()  
    addentrycsv = AddEntryCSV()  
    deleteentryform = DeleteEntryForm()  
    deleteallentries = DeleteAllEntries()  
    exportallentries = ExportAllEntries()  
    getCSVFormat = GetCSVFormatForm()  
    if request.method == "POST":  
        # add entry logic  
	  if addentryform.validate_on_submit():  
			  entry_to_create = Mould(  
	              fill_time=addentryform.Fill_time.data,  
				  injection_pres=addentryform.Injection_pres.data,  
				  holding_pres=addentryform.Holding_pres.data,  
				  holding_time=addentryform.Holding_time.data,  
				  cooling_time=addentryform.Cooling_time.data,  
				  mould_temp=addentryform.Mould_temp.data,  
				  clamp_force=addentryform.Clamp_force.data,  
				  shot_weight=addentryform.Shot_Weight.data,  
				  mould_SA=addentryform.Mould_SA.data,  
				  mould_vol=addentryform.Mould_vol.data,  
				  cavity_SA=addentryform.Cavity_SA.data,  
				  cavity_vol=addentryform.Cavity_vol.data,  
				  melt_temp=addentryform.Melt_temp.data,  
				  mat_density=addentryform.Mat_density.data,  
				  mat_GF=addentryform.Mat_GF.data,  
				  mat_MMFR=addentryform.Mat_MMFR.data,  
				  part_weight=addentryform.Part_weight.data  
	            )  
            entry_to_create.add_self()  
            flash('Entry added successfully', 'success')  
            return redirect(url_for('database_page'))  
  
        # add entry logic with csv  
	  if addentrycsv.validate_on_submit():  
		   filename = secure_filename(addentrycsv.file.data.filename)  
		   addentrycsv.file.data.save(os.path.join(app.config['UPLOADS'], filename))  
		   add_from_csv(os.path.join(app.config['UPLOADS'], filename))  
		   flash('CSV dataset added successfully', 'success')  
		   return redirect(url_for('database_page')) 
  
      if getCSVFormat.validate_on_submit() and request.form.get('Get-CSV'):  
            getCSV = request.form.get('Get-CSV')  
            if state.queryServerState():  
                print('sending format')  
                results = serverExportCSVFormat()  
                return results  
            else:  
                if getCSV:  
                    if exportCSVFormat():  
                        flash('format.csv placed on your desktop', 'success')  
                        return redirect(url_for('database_page'))  
                    else:  
                        flash('Error in placing format.csv on your desktop as a file with the same name exists on your desktop', 'error')  
                        return redirect(url_for('database_page'))  
  
  
        # delete entry logic  
	  if deleteentryform.validate_on_submit():  
            deleted_entry = request.form.get('deleted_entry')  
            d_entry_object = Mould.query.filter_by(id=deleted_entry).first()  
            if d_entry_object:  
                d_entry_object.delete_self()  
                flash('Entry deleted successfully', 'success')  
                return redirect(url_for('database_page'))  
  
      if exportallentries.validate_on_submit() and request.form.get('Export-DB'):  
            export_db = request.form.get('Export-DB')  
            print('sending database')  
            if export_db:  
                if state.queryServerState():  
                    return serverExportCSV()  
                else:  
                    if exportCSV():  
                        flash('Dataset exported to database.csv on your desktop', 'success')  
                        return redirect(url_for('database_page'))  
                    else:  
                        flash('Dataset could not be exported as Database.csv file already exists on your desktop', 'error')  
                        return redirect(url_for('database_page'))  
  
       if deleteallentries.validate_on_submit():  
            purge_db = request.form.get('Purge-DB')  
            if purge_db:  
                purge()  
                flash('Dataset erased successfully', 'success')  
                return redirect(url_for('database_page'))  
  
      if addentrycsv.file.data and addentrycsv.errors != {}:  
		  for err_msg in addentrycsv.errors.values():  
		                flash(err_msg[0], category='error')  
		            return redirect(url_for('database_page'))  
  
      if addentryform.Fill_time.raw_data and addentryform.errors != {}:  
		  flash('Invalid Values in New Entry Form', 'error')  
		            return redirect(url_for('database_page'))  
  
  
    if request.method == "GET":  
        entries = Mould.query.all()  
        return render_template(  
			  'database.html',  
			  AddEntryForm=addentryform,  
			  DeleteEntryForm=deleteentryform,  
			  AddEntryCSV=addentrycsv,  
			  GetCSVFormatForm=getCSVFormat,  
			  DeleteAllEntries=deleteallentries,  
			  ExportAllEntries=exportallentries,  
			  entries=entries,  
			  getPredict=ml.getPredict  
        )
```
This function is responsible for rendering and implementing the logic behind the database page of the app.
#### def help_page()
```python
@app.route('/help-page')  
def help_page():  
    return render_template('help.html')
```
This function is responsible for rendering the main landing page of the app.
___

### PYTHON SCRIPT : UI .py 
```python
import sys  
from PyQt5 import QtCore, QtWidgets, QtGui, QtWebEngineWidgets  
import socket  
import ctypes  
from sys import platform
  
  
class ApplicationThread(QtCore.QThread):  
    def __init__(self, application, port=5000):  
        super(ApplicationThread, self).__init__()  
        self.application = application  
        self.port = port  
  
    def __del__(self):  
        self.wait()  
  
    def run(self):  
        self.application.run(port=self.port, threaded=True)  
  
  
class WebPage(QtWebEngineWidgets.QWebEnginePage):  
    def __init__(self, root_url):  
        super(WebPage, self).__init__()  
        self.root_url = root_url  
  
    def home(self):  
        self.load(QtCore.QUrl(self.root_url))  
  
    def acceptNavigationRequest(self, url, kind, is_main_frame):  
        ready_url = url.toEncoded().data().decode()  
        is_clicked = kind == self.NavigationTypeLinkClicked  
        if is_clicked and self.root_url not in ready_url:  
            QtGui.QDesktopServices.openUrl(url)  
            return False  
	return super(WebPage, self).acceptNavigationRequest(url, kind, is_main_frame)  
  
  
def init_gui(application, port=0, width=800, height=600,  
  window_title="title", icon="icon1.ico", argv=None):  
  
    myAppID = 'JoelKundu.Predictor'  
	if platform == "win32":
	   ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppID)  
  
    if argv is None:  
        argv = sys.argv  
  
    if port == 0:  
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        sock.bind(('localhost', 0))  
        port = sock.getsockname()[1]  
        sock.close()  
  
    qtapp = QtWidgets.QApplication(argv)  
    webapp = ApplicationThread(application, port)  
    webapp.start()  
    qtapp.aboutToQuit.connect(webapp.terminate)  
  
    window = QtWidgets.QMainWindow()  
    window.resize(width, height)  
    window.setWindowTitle(window_title)  
    window.setWindowIcon(QtGui.QIcon(icon))  
  
    webView = QtWebEngineWidgets.QWebEngineView(window)  
    window.setCentralWidget(webView)  
  
    page = WebPage('http://localhost:{}'.format(port))  
    page.home()  
    webView.setPage(page)  
  
    window.show()  
    return qtapp.exec_()
```

This file is a local copy of the PyFlaDesk module and more information about this file can be found [here](https://github.com/smoqadam/PyFladesk).

___
### PYTHON SCRIPT: \_\_init\_\_.py
```python
from flask import Flask  
from flask_sqlalchemy import SQLAlchemy  
import os  
import json  
  
  
class AppState(object):  
    _serverState = False  
  
 def __init__(self):  
        self._serverState = False  
  
 def serverModeOn(self):  
        self._serverState = True  
  
 def serverModeOff(self):  
        self._serverState = False  
  
 def queryServerState(self):  
        if self._serverState:  
            return True  
 else:  
            return False  
  
  
state = AppState()  
modulePath = os.path.abspath(__name__)  
csvPath = 'static/client/csv/'  
uploadPath = 'uploads/'  
clientUploadPath = os.path.normpath(os.path.join(modulePath, uploadPath))  
clientCSVPath = os.path.normpath(os.path.join(modulePath, csvPath))  
  
  
app = Flask(__name__)  
configPath = os.path.join(app.root_path, 'config.json')  
config = open(configPath)  
data = json.load(config)  
if data["ServerMode"] == "True":  
    print(" * Running in SERVER MODE")  
    state.serverModeOn()  
  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  
app.config['SECRET_KEY'] = '9a257ea9a3b0b646c25ec6f8'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  
app.config['CLIENT_CSV'] = clientCSVPath  
app.config['UPLOADS'] = clientUploadPath  
db = SQLAlchemy(app)  
  
  
from predictor import routes
```
This script is responsible for initializing and configuring the Flask app and detailed documentation about the functions used in the scripts can be found in [FLASK Documentation](https://flask.palletsprojects.com/en/1.1.x/)
___
### PYTHON SCRIPT: Run .py
```python
from predictor import app  
from pyfladesk import init_gui  
  
  
if __name__ == '__main__':  
    init_gui(app, width=1600, height=900, window_title="Moulding Machine Parameter Predictor", icon='predictor/static/resources/icon.ico')
```
This script is responsible for launching the desktop app. It uses pyfladesk to create a barebones browser window in which the web app is rendered.
___
### PYTHON SCRIPT: Run-Server .py
```python
from predictor import app, state  
  
if __name__ == '__main__':  
    state.serverModeOn()  
    app.run(debug=True)
```
This script is responsible for launching the server that will host the web app version of the utility.
___
### PYTHON SCRIPT: Man-ReCreateDB .py
```python
import os  
from predictor import db  
  
if __name__ == '__main__':  
    os.remove('predictor/data.db')  
    db.create_all()
```
This script is provided in case there are issues with data.db file. This script will recreate data.db file however all data stored in the database will be lost.
___
### PYTHON SCRIPT: Man-Overfit-Test .py
```python
import joblib as jl  
import predictor.database as database  
from sklearn.model_selection import train_test_split  
  
X, y = database.get_datasets()  
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=1)  
  
trained_model = jl.load('predictor/static/ML/config.joblib')  
  
print('Training Score:', trained_model.score(X_train, y_train))  
print('Testing Score:', trained_model.score(X_test, y_test))  
print('Full Score:', trained_model.score(X, y))
```
This script was created to ensure that the model hasn't been overtrained on the given data. In case the model has been overtrained the model score on the training data will be higher than the testing data. In an ideal case, the scores should be approximately equal to each other.
### PYTHON SCRIPT: Man-HyperTune .py
```python
from sklearn.neural_network import MLPRegressor  
from sklearn.model_selection import train_test_split  
from sklearn.model_selection import GridSearchCV  
import predictor.machine_learning as ml  
import predictor.database as database  
import joblib as jl  
  
if __name__ == '__main__':  
    parameter_space = {  
		  'hidden_layer_sizes': [(50, 50, 50)],  
		  'activation': ['tanh', 'relu', 'logistic', 'identity'],  
		  'solver': ['sgd', 'adam', 'lbfgs'],  
		  'alpha':  [0.001, 0.01, 0.1, 0.0001,  
		  0.002, 0.02, 0.2, 0.0002,  
		  0.003, 0.03, 0.3, 0.0003,  
		  0.004, 0.04, 0.4, 0.0004,  
		  0.005, 0.05, 0.5, 0.0005,  
		  0.006, 0.06, 0.6, 0.0006,  
		  0.007, 0.07, 0.7, 0.0007,  
		  0.008, 0.08, 0.8, 0.0008,  
		  0.009, 0.09, 0.9, 0.0009],  
		  'learning_rate': ['constant', 'adaptive', 'invscaling'],  
		  'learning_rate_init': [0.001, 0.01, 0.1, 0.0001,  
		  0.002, 0.02, 0.2, 0.0002,  
		  0.003, 0.03, 0.3, 0.0003,  
		  0.004, 0.04, 0.4, 0.0004,  
		  0.005, 0.05, 0.5, 0.0005,  
		  0.006, 0.06, 0.6, 0.0006,  
		  0.007, 0.07, 0.7, 0.0007,  
		  0.008, 0.08, 0.8, 0.0008,  
		  0.009, 0.09, 0.9, 0.0009],  
		  'random_state': [1399],  
		  'warm_start': [True],  
		  'max_iter': [100000, 75000, 125000],  
		  'verbose': [True]  
    }  
    trained_model = MLPRegressor()  
    X, y = database.get_datasets()  
    X, X_test, y, y_test = train_test_split(X, y, test_size=0.33, random_state=1)  
    clf = GridSearchCV(trained_model, parameter_space, n_jobs=-1, cv=2, verbose=10)  
    clf.fit(X, y)  
    print('\n\n\nBEST PARAMS', clf.best_params_)  
    print('\n\n\nResults', clf.cv_results_)  
    jl.dump(clf, 'predictor/static/ML/config.joblib')  
    ml.retrain()
```
This script will automatically optimize and retrain the stored model on the dataset stored in the database without opening the app. This script uses GridSearchCV hence takes longer than the RandomizedSearchCV function used by the Auto-HyperTune function. However, this script will optimize the model the best performing configuration in a single execution.

___

### BATCH SCRIPT Get-Dependencies .bat
```batch
pip install flask  
pip install flask-sqlalchemy  
pip install flask-wtf  
pip install wtforms  
pip install pyfladesk  
pip install sklearn  
pip install mathplotlib  
pip install numpy  
pip install pandas  
pip install os  
pip install shutil  
pip install joblib
```
This file is responsible for installing all the dependencies of the project using the pip installer that is provided with python. (for Windows)
### SHELL SCRIPT Get-Dependencies .sh
```bash
#! /bin/sh  
pip install flask  
pip install flask-sqlalchemy  
pip install flask-wtf  
pip install wtforms  
pip install pyfladesk  
pip install sklearn  
pip install mathplotlib  
pip install numpy  
pip install pandas  
pip install os  
pip install shutil  
pip install joblib
```
This file is responsible for installing all the dependencies of the project using the pip installer that is provided with python. (for Linux)

### C++ FILE source.cpp
```c
#include <stdlib.h>  
int main() {  
   system("python run.py");  
   return 0;  
}
```
This file when build creates a binary that will use the terminal to run the command `python run.py`.

___
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

   You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

## Contact
The author can be contacted via the following emails:
- f20171399@hyderabad.bits-pilani.ac.in
- jdevcode02@gmail.com