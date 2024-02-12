import boto3
from unittest.mock import patch
import pytest


@pytest.fixture 
#Defines a pytest fixture named aws_resources 
#that sets up mocked AWS resources for tests
def aws_resources():
    # Mock DynamoDB and S3 clients
    #Uses the patch function to mock boto3.client, 
    #intercepting calls to create AWS service clients.

    with patch('boto3.client') as mock_boto3_client:
        # Mock DynamoDB
        mock_dynamodb = mock_boto3_client.return_value
        mock_dynamodb.put_item.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}
        mock_dynamodb.get_item.return_value = {
            'Item': {'ID': {'N': '1'}, 'Name': {'S': 'John Doe'}}
        }
        
        #Reuses the mocked boto3.client for the S3 client as well, stored in mock_s3.
        mock_s3 = mock_boto3_client.return_value
        mock_s3.put_object.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}

        #Yields the mocked DynamoDB and S3 clients for use in the tests, and cleans up after the test runs.
        yield mock_dynamodb, mock_s3

# Here I write Function to Insert Data to DynamoDB Table
def insert_data_to_dynamodb(dynamodb, table_name, data):
    dynamodb.put_item(
        TableName=table_name,
        Item={
            'ID': {'N': str(data['ID'])},
            'Name': {'S': data['Name']}
        }
    )

# Here I write Function to Generate Report and Put it/upload to S3 Object
def generate_report_and_upload_to_s3(s3, bucket_name, report_data):
    s3.put_object(
        Bucket=bucket_name,
        Key='report.txt',
        Body=report_data
    )

# wite Unit Tests for insert_data_to_dynamodb function
def test_insert_data_to_dynamodb(aws_resources):
    # Arrange
    mock_dynamodb, _ = aws_resources
    table_name = 'MyTable'
    data = {'ID': 1, 'Name': 'John Doe'}
    
    # Act
    insert_data_to_dynamodb(mock_dynamodb, table_name, data)
    
    # Assert
    mock_dynamodb.put_item.assert_called_once_with(
        TableName=table_name,
        Item={'ID': {'N': '1'}, 'Name': {'S': 'John Doe'}}
    )

# write Unit Tests for generate_report_and_upload_to_s3 function
def test_generate_report_and_upload_to_s3(aws_resources):
    # Arrange
    _, mock_s3 = aws_resources
    bucket_name = 'my-bucket'
    report_data = 'Sample report content'
    
    # Act
    generate_report_and_upload_to_s3(mock_s3, bucket_name, report_data)
    
    # Assert
    mock_s3.put_object.assert_called_once_with(
        Bucket=bucket_name,
        Key='report.txt',
        Body=report_data
    )

if __name__ == "__main__":
    pytest.main(['-vv'])
