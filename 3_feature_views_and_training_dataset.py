#Connect to Hopsworks
import hopsworks
project = hopsworks.login()
fs = project.get_feature_store() 

air_quality_fg = fs.get_or_create_feature_group(
    name = 'air_quality_fg',
    version = 1
)
weather_fg = fs.get_or_create_feature_group(
    name = 'weather_fg',
    version = 1
)

print("PRINT 1 --------------------------------------------------")

query = air_quality_fg.select_all().join(weather_fg.select_all())
query.read()

print("PRINT 2 --------------------------------------------------")

query = air_quality_fg.select_all().join(weather_fg.select_all())
query_show = query.show(5)
print(query_show)

print("PRINT 3 --------------------------------------------------")

col_names = query_show.columns
print(query_show)

print("PRINT 4 --------------------------------------------------")

[t_func.name for t_func in fs.get_transformation_functions()]
category_cols = ['city', 'date','conditions','aqi']
mapping_transformers = {col_name:fs.get_transformation_function(name='standard_scaler') for col_name in col_names if col_name not in category_cols}
category_cols = {col_name:fs.get_transformation_function(name='label_encoder') for col_name in category_cols if col_name not in ['date','aqi']}
mapping_transformers.update(category_cols)

print("PRINT 5 --------------------------------------------------")

feature_view = fs.create_feature_view(
    name = 'air_quality_fv',
    version = 1,
    transformation_functions = mapping_transformers,
    query = query
)

print("PRINT 6 --------------------------------------------------")

feature_view = fs.get_feature_view(
    name = 'air_quality_fv',
    version = 1
)

print("PRINT 7 --------------------------------------------------")

feature_view.create_training_data()