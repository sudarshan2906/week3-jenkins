import boto3
import variables
import functions
import webbrowser

client = boto3.client('apigateway', region_name="ap-south-1")


class Api:
    def __init__(self, api_name):
        self.api_name = api_name
        self.api_id = ""
        self.deploy_id = ""

    def get_api_id(self):
        response = client.get_rest_apis()
        for api in response['items']:
            if api['name'] == self.api_name:
                self.api_id = api['id']
        return self.api_id

    def create_deployment(self):
        response = client.create_deployment(restApiId=self.api_id, stageName='test')
        self.deploy_id = response['id']


# deployment of api gateway

if __name__ == "__main__":

    Api_Gateway = Api(variables.API_NAME)
    api_id = Api_Gateway.get_api_id()
    Api_Gateway.create_deployment()
    print("Api Deployed")
    api_url = api_id + ".execute-api.ap-south-1.amazonaws.com/test"
    print(api_url)

    # updating api_url value in html
    # uploading html to s3 for static page hosting

    client_s3 = boto3.resource("s3")
    functions.upload_html(variables.HOSTING_S3_NAME, 'index.html')
    url = "http://" + variables.HOSTING_S3_NAME + ".s3-website.ap-south-1.amazonaws.com"
    print(url)
    webbrowser.open(url, new=2)
