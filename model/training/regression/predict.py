import joblib
import pandas as pd

xgb_model = joblib.load('xgb_model.pkl')

def load_model_and_predict(features):
    input_data = pd.DataFrame([features])
    prediction = xgb_model.predict(input_data)
    return prediction[0]

input_features = {
    'tavg': 25.5,        
    'tmin': 20.0,        
    'tmax': 30.0,        
    'PM2.5': 40.0,       
    'PM10': 60.0,        
    'NO': 0.02,          
    'NO2': 0.03,         
    'NOx': 0.05,         
    'NH3': 0.01,         
    'CO': 1.2,           
    'SO2': 0.02,         
    'O3': 0.04,          
    'Benzene': 0.006,    
    'Toluene': 0.008,    
    'Xylene': 0.004,     
    'year': 2024,        
    'month': 1,          
    'day': 28,           
    'City_encoded': 2    
}

prediction = load_model_and_predict(input_features)
print("Predicted AQI:", prediction)
