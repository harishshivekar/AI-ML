from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

# Load the dataset
dataset = pd.read_csv('Crop and fertilizer dataset.csv')

# Train the model
encoder = OneHotEncoder(handle_unknown='ignore')
X_encoded = encoder.fit_transform(dataset[['District_Name', 'Soil_color']])
model_crop = RandomForestClassifier()
model_crop.fit(X_encoded, dataset['Crop'])

# Serve the HTML template
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/getDistricts', methods=['GET'])
def get_districts():
    districts = dataset['District_Name'].unique().tolist()
    return jsonify({'districts': districts})

@app.route('/getSoilColors', methods=['GET'])
def get_soil_colors():
    district = request.args.get('district')
    soil_colors = dataset[dataset['District_Name'] == district]['Soil_color'].unique().tolist()
    return jsonify({'soilColors': soil_colors})

@app.route('/recommendCrop', methods=['POST'])
def recommend_crop():
    data = request.get_json()
    district = data['district']
    soil_color = data['soilColor']
    nitrogen = data['nitrogen']
    phosphorus = data['phosphorus']
    potassium = data['potassium']
    pH = data['ph']
    rainfall = data['rainfall']
    temperature = data['temperature']

    # Prepare input data
    input_data = pd.DataFrame([[nitrogen, phosphorus, potassium, pH, rainfall, temperature, district, soil_color]],
                              columns=['Nitrogen', 'Phosphorus', 'Potassium', 'pH', 'Rainfall', 'Temperature', 'District_Name', 'Soil_color'])

    input_data_encoded = encoder.transform(input_data[['District_Name', 'Soil_color']])

    # Make prediction
    predicted_crop = model_crop.predict(input_data_encoded)
    recommended_fertilizer = dataset[dataset['Crop'] == predicted_crop[0]]['Fertilizer'].values[0]

    return jsonify({'crop': predicted_crop[0], 'fertilizer': recommended_fertilizer})

if __name__ == '__main__':
    app.run(debug=True)
