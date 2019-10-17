import boto3
import stack
import functions
from botocore.client import ClientError
import database_creation_insertion as db

import variables


# uploading templates and job file to S3

def upload_template_python_scripts():
    s3 = boto3.client('s3', region_name=variables.REGION)
    try:
        s3.create_bucket(Bucket=variables.DATA_BUCKET,
                         CreateBucketConfiguration={'LocationConstraint': variables.REGION})
    except ClientError as ce:
        if ce.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            print("Data Bucket Already Created")
        else:
            print(ce)
    except Exception as e:
        print(e)
        exit()
    functions.upload_file_folder(variables.DATA_BUCKET, "Template")
    functions.upload_zip_object(variables.DATA_BUCKET, "lambda_function.py", "lambda_function.zip", "lambda_function.zip")


if __name__ == "__main__":
    upload_template_python_scripts()
    Stack = stack.Stack(variables.STACK_NAME, variables.TEMPLATE_URL, variables.DATABASE_NAME,
                        variables.DB_INSTANCE_IDENTIFIER, variables.LAMBDA_FUNCTION_NAME, variables.API_NAME,
                        variables.HOSTING_S3_NAME)
    status = Stack.create_update_stack()

    # creation and insertion of data to database

    DB = db.Database(variables.DB_INSTANCE_IDENTIFIER, variables.USERNAME, variables.PASSWORD, variables.DATABASE_NAME)
    DB.create_table()
    DB.insert_data()
    HOST = DB.get_host()

    # updating environment variable for lambda function

    client_lambda = boto3.client('lambda', region_name=variables.REGION)
    client_lambda.update_function_configuration(
        FunctionName=variables.LAMBDA_FUNCTION_NAME,
        Environment={
            'Variables': {
                'host': HOST,
                'username': variables.USERNAME,
                'password': variables.PASSWORD,
                'database_name': variables.DATABASE_NAME
            }
        }
    )
