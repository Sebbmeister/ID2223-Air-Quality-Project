import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import f1_score
import warnings
from hsml.schema import Schema
from hsml.model_schema import ModelSchema
import joblib
warnings.filterwarnings("ignore")

#Connect to hopsworks and get feature view
import hopsworks
project = hopsworks.login() 
fs = project.get_feature_store() 

feature_view = fs.get_feature_view(
    name = 'air_quality_fv',
    version = 1
)

#Get training data
train_data = feature_view.get_training_data(1)[0]
print(train_data.head())

#Tinker with the data
train_data = train_data.sort_values(by=["date", 'city'], ascending=[False, True]).reset_index(drop=True)
train_data["aqi_next_day"] = train_data.groupby('city')['aqi'].shift(1)
print(train_data.head(5))
X = train_data.drop(columns=["date", "o3", "pm10", "pm25", "aqi_next_day", "city", "conditions"]).fillna(0)

#Drop other air quality features
#X = X.drop(columns = ["pm25", "pm10", "o3"])
print(X)

#y = X.pop("aqi_next_day")
y = X.pop("aqi")

#Fit model
gb = GradientBoostingRegressor()
gb.fit(X, y)

#F1 score
f1_score(y.astype('int'), [int(pred) for pred in gb.predict(X)], average='micro')

#Check y
print(y.iloc[4:10].values)

#Create dataframe with predictions
pred_df = pd.DataFrame({
    'aqi_real': y.iloc[4:10].values,
    'aqi_pred': map(int, gb.predict(X.iloc[4:10]))
}
)
print(pred_df)

#Create model registry and schema
mr = project.get_model_registry()
input_schema = Schema(X)
output_schema = Schema(y)
model_schema = ModelSchema(input_schema=input_schema, output_schema=output_schema)
model_schema.to_dict()

#Save model

joblib.dump(gb, 'model5.pkl')
model = mr.sklearn.create_model(
    name="gradient_boost_model5",
    metrics={"f1": "0.5"},
    description="Gradient Boost Regressor 5.",
    input_example=X.sample(),
    model_schema=model_schema
)
model.save('model5.pkl')