# ID2223-Air-Quality-Project
This repository contains the code for the project in the KTH course ID2223. The project is a model capable of predicting future air quality conditions over the next seven days in a selection of cities. The measurement used for air quality, AQI, is based on levels of different substances in the air; a lower AQI indicates less polluted air and a higher indicates more polluted air. The application bases its predictions on past and predicted future weather conditions and on past air quality measurements.

The finished application will be accessible through a Hugging Face space.

## Data sources
Data for weather conditions was gathered from Visual Crossing (https://www.visualcrossing.com/) and data for air quality was gathered from the World Air Quality Project (https://aqicn.org//here/).

## Project architecture
The primary files making up the project, in the order in which they are run, are as follows:
* Backfill_feature_groups.py parses and uploads historical weather and air quality data from the Visual Crossing and the World Air Quality Project.
* Feature_pipeline.py is a feature pipeline that downloads and uploads daily data.
* Feature_views_and_training_dataset.py combines the uploaded data (weather and air quality) into a single feature view, which is then used in a training pipeline
* Model_training.py trains the actual model using a Gradient Boosting Regressor. The model is validated using F1 score.
* (''not done yet'') App.py is the code for the Gradio application running in Hugging Face.

The architecture and inner workings of the project were closely based on the Air Quality Prediction tutorial from Hopsworks (https://github.com/logicalclocks/hopsworks-tutorials/tree/master/advanced_tutorials/air_quality)
