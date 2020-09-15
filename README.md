# ECS runningCount to Cloudwatch metrics

## local exec lambci/lambda:python3.8

```
cp -p .env.example .env
docker run --rm --env-file ./.env -v "$PWD":/var/task:ro lambci/lambda:python3.8 lambda_function.lambda_handler
```

## AWS Iam policies

- ecs:DescribeServices
- cloudwatch:PutMetricData

## set Cloudwatch Event

```
rate(1 minute)
```
