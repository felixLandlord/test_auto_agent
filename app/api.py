from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.service import CalculatorService

router = APIRouter(prefix="/calculator")

class CalculationInput(BaseModel):
    a: float
    b: float | None = None

class RootInput(BaseModel):
    a: float
    n: float = 2

class LogInput(BaseModel):
    a: float
    base: float = 2.718281828459045 # math.e

class ResultOutput(BaseModel):
    operation: str
    result: float | int

@router.post("/add", response_model=ResultOutput)
async def add(input: CalculationInput):
    if input.b is None:
        raise HTTPException(status_code=400, detail="Missing parameter 'b' for addition")
    result = CalculatorService.add(input.a, input.b)
    return ResultOutput(operation="addition", result=result)

@router.post("/subtract", response_model=ResultOutput)
async def subtract(input: CalculationInput):
    if input.b is None:
        raise HTTPException(status_code=400, detail="Missing parameter 'b' for subtraction")
    result = CalculatorService.subtract(input.a, input.b)
    return ResultOutput(operation="subtraction", result=result)

@router.post("/multiply", response_model=ResultOutput)
async def multiply(input: CalculationInput):
    if input.b is None:
        raise HTTPException(status_code=400, detail="Missing parameter 'b' for multiplication")
    result = CalculatorService.multiply(input.a, input.b)
    return ResultOutput(operation="multiplication", result=result)

@router.post("/divide", response_model=ResultOutput)
async def divide(input: CalculationInput):
    if input.b is None:
        raise HTTPException(status_code=400, detail="Missing parameter 'b' for division")
    try:
        result = CalculatorService.divide(input.a, input.b)
        return ResultOutput(operation="division", result=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/modulo", response_model=ResultOutput)
async def modulo(input: CalculationInput):
    if input.b is None:
        raise HTTPException(status_code=400, detail="Missing parameter 'b' for modulo")
    try:
        result = CalculatorService.modulo(input.a, input.b)
        return ResultOutput(operation="modulo", result=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/floor-divide", response_model=ResultOutput)
async def floor_divide(input: CalculationInput):
    if input.b is None:
        raise HTTPException(status_code=400, detail="Missing parameter 'b' for floor division")
    try:
        result = CalculatorService.floor_divide(input.a, input.b)
        return ResultOutput(operation="floor_division", result=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/power", response_model=ResultOutput)
async def power(input: CalculationInput):
    if input.b is None:
        raise HTTPException(status_code=400, detail="Missing parameter 'b' for power")
    result = CalculatorService.power(input.a, input.b)
    return ResultOutput(operation="power", result=result)

@router.post("/square", response_model=ResultOutput)
async def square(input: CalculationInput):
    result = CalculatorService.square(input.a)
    return ResultOutput(operation="square", result=result)

@router.post("/root", response_model=ResultOutput)
async def root(input: RootInput):
    try:
        result = CalculatorService.root(input.a, input.n)
        return ResultOutput(operation=f"{input.n}-th root", result=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/absolute", response_model=ResultOutput)
async def absolute(input: CalculationInput):
    result = CalculatorService.absolute(input.a)
    return ResultOutput(operation="absolute", result=result)

@router.post("/factorial", response_model=ResultOutput)
async def factorial(input: CalculationInput):
    try:
        result = CalculatorService.factorial(int(input.a))
        return ResultOutput(operation="factorial", result=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/log", response_model=ResultOutput)
async def log(input: LogInput):
    try:
        result = CalculatorService.log(input.a, input.base)
        return ResultOutput(operation="logarithm", result=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
