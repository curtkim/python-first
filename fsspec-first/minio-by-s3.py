import s3fs
s3 = s3fs.S3FileSystem(
   key='minio',
   secret='minio123',
   client_kwargs={
      'endpoint_url': 'http://localhost:9000',
      'region_name': 'us-east-1'
   },
   config_kwargs={
      'signature_version': 's3v4'
   }
)

s3.ls('my-bucket')