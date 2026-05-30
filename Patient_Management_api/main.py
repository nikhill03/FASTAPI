from fastapi import FastAPI
import json

app = FastAPI()

#helper function
def load_data():
    with open('Patient_Management_api/patients.json','r') as f:
        data = json.load(f)
    
    return data

# Endpoint 1
@app.get("/")
def hello():
    return {"message" : "Patient Management System API !"}

# Endpoint 2
@app.get("/about")
def about():
    return {'message':'A fully functional API to manage patient records'}

# Endpoint 3
@app.get("/view")
def view():
    data = load_data()
    return data

# path params logic for dynamic fields in URL
@app.get("/patient/{patient_id}")
def view_patient(patient_id: str):
    # load all patients
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    return {'error' : 'Patient not found'}

@app.get("/routes")
def routes():
    return [route.path for route in app.routes]

# command -  uvicorn main:app --reload