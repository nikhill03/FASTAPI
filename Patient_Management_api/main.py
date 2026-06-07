from fastapi import FastAPI, HTTPException, Path, Query
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal

app = FastAPI()

class Patient(BaseModel):

    id: Annotated[str, Field(..., description="ID of the patient", examples=['P001'])]
    name: Annotated[str, Field(..., description="Name of the patient")]
    city: Annotated[str, Field(..., description="City of the patient")]
    age: Annotated[int, Field(..., gt=0,  lt=120)]
    gender: Annotated[Literal['male', 'female','others'], Field(..., description="Gender of the patient")]
    height: Annotated[float, Field(..., gt=0,  description="Height of the patient in mtrs")]
    weight: Annotated[float, Field(..., gt=0,  description="City of the patient in kgs")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height**2) , 2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'        

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
def view_patient(patient_id: str = Path(..., description="ID of patient in DB", example="P001")):
    # load all patients
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    # return {'error' : 'Patient not found'}
    raise HTTPException(status_code=404, detail ="Patient not found")


# path or query with ... means required parameter.
@app.get("/sort")
def sort_patient(sort_by: str = Query(..., description="Sort on the basis of parameters in DB"), order: str = Query('asc', description="Sort in asc or desc order")):
    valid_fields = ['height','weight','bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field. Select from {valid_fields}")

    if order not in ['asc','desc']:
        raise HTTPException(status_code=400, detail=f"Invalid field. Select between asc and desc")


    # load all patients
    data = load_data()

    sort_order = True if order=='desc' else False

    sorted_data = sorted(data.values(), key=lambda x:x.get(sort_by, 0), reverse=sort_order)
    return sorted_data

@app.get("")

@app.get("/routes")
def routes():
    return [route.path for route in app.routes]

# command -  uvicorn main:app --reload