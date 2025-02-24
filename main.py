from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from database_connector import get_db_connection
from agents import Agents
# Serve Static Files
from fastapi.staticfiles import StaticFiles
import query_validator
import decimal
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Jinja2 Template Directory
templates = Jinja2Templates(directory="templates")


app.mount("/static", StaticFiles(directory="static"), name="static")


# Handle favicon.ico request
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


def convert_decimal(obj):
    """ Recursively convert Decimal objects to float """
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    if isinstance(obj, dict):
        return {key: convert_decimal(value) for key, value in obj.items()}
    if isinstance(obj, list):
        return [convert_decimal(item) for item in obj]
    return obj


@app.post("/execute-query", response_class=HTMLResponse)
async def execute_query(request: Request, user_query: str = Form(...)):
    try:
        if not user_query:
            raise HTTPException(status_code=400, detail="User query is required.")

        # Generate SQL query
        sql_query = Agents.combined_sql_generation(user_query)
        refined_sql = query_validator.QueryValidator.extract_llm_response(sql_query)
        print(refined_sql)
        _ = query_validator.QueryValidator.validate_sql_query(refined_sql)
 
        
        logger.info(f"Generated SQL: {refined_sql}")

        # Execute the generated SQL query
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(refined_sql)

            # If it's a SELECT query, fetch and return the results
            if refined_sql.strip().lower().startswith("select"):
                result = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                data = [dict(zip(columns, row)) for row in result]

                # Convert Decimal to float
                data = convert_decimal(data)

                return templates.TemplateResponse("results.html", {
                    "request": request,
                    "query": refined_sql,
                    "result": data
                })
            else:
                conn.commit()
                return templates.TemplateResponse("results.html", {
                    "request": request,
                    "query": refined_sql,
                    "message": "Query executed successfully."
                })

    except Exception as e:
        return templates.TemplateResponse("results.html", {
            "request": request,
            "error": f"Error executing query: {str(e)}"
        })

