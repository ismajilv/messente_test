

# MESSENTE!

This is the implementation of Messente's test task named task sent by Piret. 

### Where to get it
The source code is currently hosted on GitHub at: [https://github.com/ismajilv/messente_test]

### Overall
This is AWS Cloudformation template design as a diagram. 
![template1-designer](https://user-images.githubusercontent.com/34252511/58658906-5043da80-832a-11e9-9ddc-f6c25d7e36ae.png)
It has 2 main Lambda functions one for Authorization and Authentication(Node.js),
another for API call(Python3.7). Besides the Function itself, diagram also shows the sub Functions. API GateWay has 2 stage one is Prod another
one is Test. Dynamodb table named blacklist_table keep the userid and blacklist. IAM Roles are created based on Policies specified 
in the [template.yaml](./template.yaml). The Cloud infrastructure is designed in [template.yaml](./template.yaml) file and the nice thing is that
you can build the same stack with one call to [init.sh](./init.sh) in your own AWS account. Just run 
```bash
$ bash init.sh {S3_bucket_name} {stack_name} 
```
and the same implementation is up and running in your AWS account. 
Content of [init.sh](./init.sh) file:
```bash
S3Bucket=$1
StackName=$2

aws cloudformation package --template-file template.yaml --output-template-file template.packaged.yaml --s3-bucket $S3Bucket
aws cloudformation deploy --template-file ./template.packaged.yaml --stack-name $StackName --capabilities CAPABILITY_IAM
aws dynamodb batch-write-item --request-items file://dynamodb_init.json
```
It takes S3 bucket name as a first and Cloudformation stack name as 2nd argument. You may need to create S3 bucket(more info: https://docs.aws.amazon.com/cli/latest/reference/s3/index.html).
Last comment just populates blacklist_table with userids and empty blacklists.

Custom authentication and authorization is implemented in [authorizer.js](./src/authorizer.js). Which accepts
Authentication header with Basic Authentication and return a "Accept" or "Deny" policy with a principalId as an example below:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "execute-api:Invoke",
      "Effect": "Allow",
      "Resource": "arn:aws:execute-api:region:0000000000:29xe3xpvca/ESTestInvoke-stage/GET/"
    }
  ]
}
```
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "execute-api:Invoke",
      "Effect": "Deny",
      "Resource": "arn:aws:execute-api:region:0000000000:29xe3xpvca/ESTestInvoke-stage/GET/"
    }
  ]
}
```
Python microservice is in [index.py](/src/index.py). Depending on request it calls different functions.

### Usage
API small documentation is published in url below:
https://documenter.getpostman.com/view/7171976/S1TVVwpM?version=latest

## Final thoughts
Usage of many try catches are avoided to have simple implementation. I believe that validation of input should
be done before the function accepts the input which AWS provide a way to do. 

## Improvements
Get request can be supplied with query string to better listing. 
The user's blacklist can be analysed in Dynamodb and if the pattern is found among those numbers, the user
should be informed about it. Possible patterns can be, short numbers that can represent advertisement companies
and further call from same kind of numbers can be blocked automatically. 

## Challanges I faced
During implementation, the hardest task for me to remove element from list in Dynamodb. To remove a number from
the blacklist, there was no one call way to Dynamodb as number being paratemer to remove it from blacklist. The way was to get the
list and find index of that element in this list and send the the index to Dynamodb to remove the element. I spent time reading documentations,
but could not make it with one call to db. And, I implemented in mentioned way. 
2nd was, I wanted to store blacklist as a set to eliminate checking whether given element is in set already or not to prevent
error. But Dynamodb did not let defining empty Set attribute. This is still as open issue in stackoverflow and
people complaining about it.


Thanks!
