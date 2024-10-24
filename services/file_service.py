import os
import shutil
from fastapi import UploadFile, status

from constant import ROOT
from models.item import ItemOutDTO
from models.http_response import ErrorResponse
from services.hadoop_service import reduce_service


def count_word_in_text_service(
    file: UploadFile,
) -> list[ItemOutDTO]:
    file_path = upload_file_service(file)
    output_dir = reduce_service(file_path)
    return parse_result_service(output_dir)


def upload_file_service(
    file: UploadFile,
) -> str:
    file_name = file.filename
    if not file_name:
        raise ErrorResponse(
            status=status.HTTP_400_BAD_REQUEST,
            message="The file name is empty",
        )
    input_dir = os.path.join(ROOT, "input")
    file_path = os.path.join(input_dir, file_name)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return file_path


def parse_result_service(output_dir: str) -> list[ItemOutDTO]:
    with open(os.path.join(output_dir, "part-r-00000"), "r") as f:
        result = f.read()
        word_count_list = []
        for line in result.strip().split("\n"):
            word, count = line.split("\t")
            word_count_list.append(ItemOutDTO(word=word, count=int(count)))
            word_count_list.sort(key=lambda item: item.count, reverse=True)

    return word_count_list
