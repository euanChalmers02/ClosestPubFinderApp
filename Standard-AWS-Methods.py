import boto3
from botocore.exceptions import NoCredentialsError
import pandas as pd

ACCESS_KEY = ''
SECRET_KEY = ''

# simplify by removing the list comp to remove the filter
def get_all_files_in_bucket_filter(filtr):
    keys = []
    
    session = boto3.Session( 
             aws_access_key_id=ACCESS_KEY, 
             aws_secret_access_key=SECRET_KEY)

    #Then use the session to get the resource
    s3 = session.resource('s3')

    my_bucket = s3.Bucket('webpagebucket77')

    for my_bucket_object in my_bucket.objects.all():
        keys.append((my_bucket_object.key))

    newlist = [x for x in keys if filtr in x]
    print(newlist)

def delete_dynomodb(log_id):
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.Table('TABLE-NAME')
    response = table.delete_item(Key={"LogID": str(log_id)})
    return True
  
def get_from_dynomo():
dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
table = dynamodb.Table('TABLE-NAME')
response = table.scan()
data = response['Items']

while 'LastEvaluatedKey' in response:
    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    data.extend(response['Items'])
# print(data)
df = pd.DataFrame(data)
return df
  

def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
