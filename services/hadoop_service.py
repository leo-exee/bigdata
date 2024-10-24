import logging
import os
import shutil
from fastapi import status
from constant import REDUCE, ROOT
from models.http_response import ErrorResponse


def reduce_service(file_path: str) -> str:
    try:
        logging.info("Running the reduce service")
        os.system(f"hdfs dfs -copyFromLocal -f {file_path} /input")
        os.system("hadoop fs -rm -r /output")
        os.system(f"hadoop jar {REDUCE} wordcount /input /output")
        output_dir = os.path.join(ROOT, "output")
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.system(f"hdfs dfs -copyToLocal /output {ROOT}")
        return output_dir
    except Exception as e:
        raise ErrorResponse(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="The input directory has not been created",
            details=str(e),
        )
