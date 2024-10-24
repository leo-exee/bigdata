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


async def count_word_in_genome_service(file: UploadFile, chunk_size: int) -> ItemOutDTO:
    content = await parse_content_service(file, chunk_size)
    file_path = generate_file_path_service()
    with open(file_path, "w") as output_file:
        output_file.write(content)
    output_dir = reduce_service(file_path)
    return parse_result_service(output_dir)[0]


def generate_file_path_service() -> str:
    dir = os.path.join(ROOT, "input")
    os.makedirs(dir, exist_ok=True)
    file_path = os.path.join(dir, "genome_chunks.txt")
    return file_path


async def parse_content_service(file: UploadFile, chunk_size: int) -> str:
    content = (await file.read()).decode("utf-8")
    content = "\n".join(content.split("\n")[1:])
    content.replace("\n", "")
    content = "".join(filter(str.isalpha, content))
    chunks = [content[i : i + chunk_size] for i in range(0, len(content), chunk_size)]
    formatted_chunks = [" ".join(chunks[i : i + 4]) for i in range(0, len(chunks), 4)]
    formatted_content = "\n".join(formatted_chunks)
    return formatted_content


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
