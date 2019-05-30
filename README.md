

# MESSENTE!

This is the implementation of Messente's test task named. 

### Where to get it
The source code is currently hosted on GitHub at: [https://github.com/ismajilv/messente_test]

### Usage
Clone the repository:
```
$ git clone https://github.com/ismajilv/veriff_test
```
To deploy to AWS, S3 bucket needs to be created to store all the artifacts. To create S3 bucket, run:
```
$ aws s3api create-bucket --bucket {bucket_name} --region {region}
```
To upload artifacts to S3 bucket run:
```
aws cloudformation package --template-file template.yaml --output-template-file template.packaged.yaml --s3-bucket {bucket_name}
```
At this time, we only need to deploy. So, run:
```
aws cloudformation deploy --template-file ./template.packaged.yaml --stack-name {choose_stcack_name} --capabilities CAPABILITY_IAM
```

RESTful API allows Messente's customers to add, remove and list phone number(s) to/from their blacklist.
```
$ curl --user messente:piret https://9q588comi6.execute-api.eu-west-1.amazonaws.com/Prod/blacklist
```
```json
{
    "Items": [
        4,
        5
    ],
    "Count": 2,
    "Message": "All the numbers in the blacklist."
}
```
```
curl -X POST -H --user messente:piret --data '{"number": "3"}' https://9q588comi6.execute-api.eu-west-1.amazonaws.com/Prod/blacklist
```
```json
{"message": "Number: 3 is added to blacklist."}
```

```
curl -X "DELETE" --user messente:piret https://9q588comi6.execute-api.eu-west-1.amazonaws.com/Prod/blacklist/3
```
```json
{"message": "Number: 3 is deleted from blacklist."}
```
## Overview


Thanks!
