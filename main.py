import logging
from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse

from models.http_response import ErrorResponse
from models.item import ItemOutDTO
from services.file_service import count_word_in_text_service
from utils.format_util import format_error_response

app = FastAPI()

REDUCE = "$HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.2.1.jar"


@app.post(
    "/text",
    response_model=list[ItemOutDTO],
    summary="Count the words in a text",
    description="Take a file, count the words and return the word count list",
)
async def count_word_in_text_controller(file: UploadFile):
    return count_word_in_text_service(file)


@app.post(
    "/",
    response_model=list[ItemOutDTO],
    summary="Count the words in a genom",
    description="Take a file, count the words and return the word count list",
)
async def count_word_in_genom_controller(file: UploadFile):
    return count_word_in_text_service(file)


@app.exception_handler(ErrorResponse)
def ERRRORResponseHandler(error: ErrorResponse) -> JSONResponse:
    logging.error(error.message)
    return JSONResponse(
        status_code=error.status,
        content=format_error_response(error.status, error.message, error.details),
    )
