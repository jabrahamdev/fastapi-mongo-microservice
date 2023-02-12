from fastapi import FastAPI
from models import Employee
from mongoengine import connect
import json


app = FastAPI()

connect(db="hrms", host="localhost", port=27017)

@app.get("/")
def home():
    return {"message": "Hello underworld!"}





@app.get("/employees")
def get_all_employees():
    employees = json.loads(Employee.objects().to_json())
    return {"employees": employees}

#For validation pruposes / para validaciónnnn
from fastapi import Path

@app.get("/employee/{emp_id}")
def get_employee(emp_id: int = Path(...,gt=0)):
    employee = Employee.objects.get(emp_id=emp_id)
    #return {"employee": employee}
    employee_dict = {
        "emp_id": employee.emp_id,
        "name": employee.name,
        "age": employee.age,
        "teams": employee.teams
    }
    return employee_dict



from fastapi import Query
from mongoengine.queryset.visitor  import Q # with this operator the age value can be optional
@app.get("/search_employees")
def search_employees(name: str, age: int = Query(None, gt=18)): # age is optional
    # age: int = Query(None, gt=18) this means that value can be None and when passed greater than 18
    employees = json.loads(Employee.objects.filter(Q(name__icontains=name) | Q(age=age)).to_json()) # Q() | Q() makes the values optional
    #name__icontains  >> case insensitivity
    return {"employees": employees}


# When we want to add something to the db we use Request Body
# we gotta to define the data with BaseModel

from pydantic import BaseModel

from fastapi import Body # similar to Query and Path
class NewEmployee(BaseModel):
    emp_id : int
    name: str
    age: int = Body(None, gt=18) # age can be none but when provided must be >= 18
    teams: list 


@app.post("/add_employee")
def add_employee(employee: NewEmployee): # receives a NewEmployee type
    new_employee = Employee(emp_id=employee.emp_id, # from the new employee extract data and create a new Employee object with it
                            name=employee.name,
                            age=employee.age,
                            teams=employee.teams)
    new_employee.save() # this will update the db

    return {"message": "Employee added successfully"}


    
