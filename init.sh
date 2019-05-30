S3Bucket=$1
StackName=$2

aws cloudformation package --template-file template.yaml --output-template-file template.packaged.yaml --s3-bucket $S3Bucket
aws cloudformation deploy --template-file ./template.packaged.yaml --stack-name $StackName --capabilities CAPABILITY_IAM
aws dynamodb batch-write-item --request-items file://dynamodb_init.json