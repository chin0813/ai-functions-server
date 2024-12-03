from fastapi import APIRouter, HTTPException
from app.utils.ai_functions import AIFunctions
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

for entry in AIFunctions.get_registered_functions():
    print(f"Creating endpoint for {entry['name']}")
    func_name = entry["name"]
    input_model = entry["input_model"]
    output_model = entry["output_model"]
    function = entry["function"]
    print("input_model: ", input_model)
    print("output_model: ", output_model)
    print("function: ", function)

    def create_endpoint(func_name, input_model, output_model, function):
        @router.post(f"/{func_name}", response_model=output_model, operation_id=func_name)
        async def dynamic_endpoint(payload: input_model):
            try:
                return function(payload)
            except ValueError as e:
                logger.error(f"ValueError in {func_name}: {str(e)}")
                raise HTTPException(status_code=400, detail=f"Value error in {func_name}: {str(e)}")
            except TypeError as e:
                logger.error(f"TypeError in {func_name}: {str(e)}")
                raise HTTPException(status_code=422, detail=f"Type error in {func_name}: {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error in {func_name}: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Unexpected error in {func_name}: {str(e)}")

    create_endpoint(func_name, input_model, output_model, function)