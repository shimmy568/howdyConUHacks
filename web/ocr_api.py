import boto3

KEY = "test_ocr.png"

aws_id = 'AKIAII5QLFINZ4EFSX4Q'
aws_pass = 'mztQG5rsG3nGLF2g728YhPSO50YuXYQPu99cMGxg'

def detect_text(key, region="us-east-1"):
    rekognition = boto3.client("rekognition", aws_access_key_id=aws_id,
    aws_secret_access_key=aws_pass,)
    
    with open(key, "rb") as imageFile:
          f = imageFile.read()
          img_bytes = bytearray(f)
      
    response = rekognition.detect_text(
        Image={
            'Bytes': img_bytes,
            }
        )

    return response

source_face = detect_text(KEY)
print(source_face)
