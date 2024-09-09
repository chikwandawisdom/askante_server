import decimal
import os
import io
from datetime import datetime

import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from PIL import Image
from nanoid import generate
import boto3
from urllib.parse import quote

from fundamentals.custom_responses import success_w_data
from fundamentals.models import ZarRate


# image upload endpoint
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_image(request):
    params = request.query_params
    file_name = os.path.splitext(str(request.FILES['image']))[0]
    file_extension = os.path.splitext(str(request.FILES['image']))[1]
    final_file_name = 'sms-' + file_name + '-' + generate() + file_extension

    # uploading file to digital ocean space
    file = request.FILES['image']
    if params.get('width'):
        # Open the image file using Pillow
        image = Image.open(file)

        # Convert the image to RGB mode if it is in RGBA mode
        if image.mode == 'RGBA':
            image = image.convert('RGB')

        # Calculate the new width and height while maintaining the aspect ratio
        desired_width = int(params.get('width'))  # Adjust the desired width as needed
        aspect_ratio = image.width / image.height
        desired_height = round(desired_width / aspect_ratio)

        # Resize the image
        image = image.resize((desired_width, desired_height))

        # Compress the image by reducing the quality
        image.save(file, optimize=True, quality=90)

        # Get the optimized image file as bytes
        optimized_file = io.BytesIO()
        image.save(optimized_file, format='webp')

        # Seek back to the beginning of the file
        optimized_file.seek(0)
        file = optimized_file

    bucket = os.environ.get('S3_BUCKET')
    content_type = request.FILES['image'].content_type
    key = 'sys/' + final_file_name
    s3 = boto3.client('s3',
                      aws_access_key_id=os.environ.get('AWS_KEY'),
                      aws_secret_access_key=os.environ.get('AWS_SECRET'),
                      endpoint_url='https://school-management-sytem-ljas123d.s3.eu-west-2.amazonaws.com/')

    s3.upload_fileobj(file, bucket, key, ExtraArgs={'ContentType': content_type})

    # s3.put_object_acl(ACL='public-read', Bucket=bucket, Key=key)  # set permissions to public

    # creating new File object
    base_url = 'https://school-management-sytem-ljas123d.s3.eu-west-2.amazonaws.com/'
    file_url = base_url + bucket + '/' + key

    # encode the file url, remove special characters, spaces etc
    file_url = quote(file_url, safe=':/')

    response = {
        'secure_url': file_url
    }

    return success_w_data(response, 'Image uploaded successfully')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_zar_rate(request):

    current_date_existing_zar_rate = ZarRate.objects.filter(date=datetime.now().date()).first()
    if current_date_existing_zar_rate:
        print('ZAR rate fetched from the database')
        return success_w_data(decimal.Decimal(current_date_existing_zar_rate.rate), 'ZAR rate fetched successfully')

    response = requests.get('https://v6.exchangerate-api.com/v6/1df694211ad872dc8811c46c/latest/USD')
    data = response.json()

    zar_rate = round(data['conversion_rates']['ZAR'], 2)

    # save the fetched rate to the database
    ZarRate.objects.create(date=datetime.now().date(), rate=zar_rate)

    return success_w_data(zar_rate, 'ZAR rate fetched successfully')