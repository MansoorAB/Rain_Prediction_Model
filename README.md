
# Rainfall Prediction for Tomorrow based on today's weather parameters

## Table of Content
  * [Demo](#demo)
  * [Overview](#overview)
  * [Motivation](#motivation)
  * [Technical Aspect](#technical-aspect)
  * [Web Request](#web-form-request)
  * [API Call](#api-call-via-postman)
  * [Deployment](#deployment)
  * [Execution](#execution-preparation-and-steps)
  * [Technology Used](#technology-used)
  * [Authors](#authors)
  
## Demo
Link: [https://mb-rain-prediction-app.herokuapp.com/](https://mb-rain-prediction-app.herokuapp.com/)

[![](https://imgur.com/0t3Bco8)](https://mb-rain-prediction-app.herokuapp.com/)

## Overview
This app helps user to predict if it would rain or not tomorrow, based on the weather information of today. 

This model was built to demonstrate decission tree classifier and how recall would improve if data gets balanced. Hence other models like XGBoost, Random Forest are not considered though it would improve the recall. 

## Motivation
By knowing whether it would rain or not tomorrow, the user can better plan his outdoor activity like picnic etc..,

## Technical Aspect 
Decission tree classifier is built on original data and then data is balanced using various techniques to see if recall for class=1 (i.e. RainTomorrow=Yes) would improve.

## Web Form Request

```http
  https://mb-rain-prediction-app.herokuapp.com/
```

| Parameter | Type     | Possible Values  | Required?   |
| :-------- | :------- | :--------------- | ----------- |
| `Did it Rain today?` | `Option` |  `Yes, No` | `Yes` |
| `Humidity 3PM` | `Number` |  `0 to 100` | `Yes` |
| `Cloud 3PM` | `Number` |  `0 to 9` | `Yes` |
| `Sunshine` | `Number` |  `0 to 14.5` | `Yes` |
| `Cloud 9AM` | `Number` |  `0 to 9` | `Yes` |
| `WindGust Direction` | `string` | `East, West, North, South` |  `Yes` |

## API call (via postman)

```http
  POST https://mb-rain-prediction-app.herokuapp.com/predict
```

| Parameter | Type     | Possible Values  | Required?   |
| :-------- | :------- | :--------------- | ----------- |
| `Did it Rain today?` | `Option` |  `Yes, No` | `Yes` |
| `Humidity 3PM` | `Number` |  `0 to 100` | `Yes` |
| `Cloud 3PM` | `Number` |  `0 to 9` | `Yes` |
| `Sunshine` | `Number` |  `0 to 14.5` | `Yes` |
| `Cloud 9AM` | `Number` |  `0 to 9` | `Yes` |
| `WindGust Direction` | `string` | `East, West, North, South` |  `Yes` |

## Deployment

To deploy this project, please follow the below steps in the same order 

create environment

```bash
  conda create -n <envname> python=3.8 -y
```

activate the environment

```bash
  conda activate <envname>
```

install the requirements file

```bash
  pip install -r requirements.txt
```

download the data from (if you want to build the model by yourself, else the .pkl are already provided)

```http
  https://drive.google.com/drive/folders/1vcGMUEFcg0bIKHfr9AWM0wHYkm155VD3?usp=sharing
```

create a working directory to hold this project and use the below git commands 
to push work directory contents to your git repo

```bash
    git init
    git add . && git commit -m "first commit"
    git remote add origin https://github.com/.......git
    git branch -M main
    git push origin main
```


## Execution Preparation and Steps:
1. The decission tree model and other related files like scaler, lable encoder mapping, column 
names are already pickled and can be found in prediction_service/model folder when you download this repo
2. Above pickle files are prepared using the ipynb notebooks provided in the repo.
3. Initially datapreperation and model building were done on a random sample of 10% data for quick turnaround during DEV phase. Once things are fine, the sample data prep and model building strategy are applied to larger data. The filename of various .ipynb are self evident and further information are incorporated as comments in corresponding .ipynb
4. For conveniance, only the top 6 features are considered to train the model.
5. To test locally, navigate to project folder and run "python app.py" from your IDE terminal or Anaconda prompt. Provide the details as requested and you should see the prediction.
6. Once all the things are in place, the user can deploy this to cloud platform like AWS etc..,

## Technology Used
<p align="left">

<a href="https://www.python.org" target="_blank"> 
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" 
width="40" height="40"/> </a>

<a href="https://scikit-learn.org/" target="_blank"> 
<img src="https://upload.wikimedia.org/wikipedia/commons/0/05/Scikit_learn_logo_small.svg" alt="scikit_learn" 
width="40" height="40"/> </a>

<a href="https://imbalanced-learn.org/stable/" target="_blank"> 
<img src="https://imgur.com/U43W65a.png" alt="imblearn" width="40" height="40"/> </a>

<a href="https://flask.palletsprojects.com/" target="_blank"> 
<img src="https://www.vectorlogo.zone/logos/pocoo_flask/pocoo_flask-icon.svg" alt="flask" width="40" height="40"/> </a>

<a href="https://heroku.com" target="_blank"> 
<img src="https://www.vectorlogo.zone/logos/heroku/heroku-icon.svg" alt="heroku" width="40" height="40"/> </a>

<a href="https://www.w3schools.com/html/" target="_blank"> 
<img src="https://www.vectorlogo.zone/logos/w3_html5/w3_html5-icon.svg" alt="html5" width="40" height="40"/> </a>

<a href="https://www.w3schools.com/css/" target="_blank"> 
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original-wordmark.svg" 
alt="css3" width="40" height="40"/> </a>

</p>


## Authors

- [@Mansoor Baig](https://github.com/MansoorAB)

  


  