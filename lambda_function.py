import boto3
import os
import sys
from pprint import pprint

def main():
	# target cluster/service
	region = os.environ.get('AWS_REGION', 'ap-northeast-1')
	dryrun = int(os.environ.get('dryrun', 0))
	namespace = os.environ.get('NAMESPACE', 'ECS/describeServices')
	cluster = os.environ.get('CLUSTER', '')
	service = os.environ.get('SERVICE', '')

	data = {'desiredCount':0, 'runningCount':0, 'pendingCount':0}

	if len(namespace)==0 or len(cluster)==0 or len(service)==0:
		raise Exception('NO PARAMETER')

	ecs = boto3.client('ecs', region_name=region)

	services = ecs.describe_services(
		cluster=cluster,
		services=[service]
	)['services']

	if (len(services)):
		data['desiredCount'] = services[0]['desiredCount']
		data['runningCount'] = services[0]['runningCount']
		data['pendingCount'] = services[0]['pendingCount']

		if dryrun==0:
			cloudwatch = boto3.client('cloudwatch', region_name=region)
			cloudwatch.put_metric_data(
				Namespace=namespace,
				MetricData=[
					{
						'MetricName': 'desiredCount',
						'Dimensions': [{'Name':'Service','Value':'{}/{}'.format(cluster, service)}],
						'Value': data['desiredCount'],
						'Unit': 'Count',
					},
					{
						'MetricName': 'runningCount',
						'Dimensions': [{'Name':'Service','Value':'{}/{}'.format(cluster, service)}],
						'Value': data['runningCount'],
						'Unit': 'Count',
					},
					{
						'MetricName': 'pendingCount',
						'Dimensions': [{'Name':'Service','Value':'{}/{}'.format(cluster, service)}],
						'Value': data['pendingCount'],
						'Unit': 'Count',
					},
				]
			)
		else:
			pprint(data)

	return {
		'dryrun': dryrun,
		'service_num': len(services),
		'data': data,
	}

def lambda_handler(event, context):
	try:
		return main()
	except Exception as e:
		errmsg = 'Exception:{}'.format(e.args)
	except:
		errmsg = 'Unexpected error:{}'.format(sys.exc_info()[0])

	print(errmsg, file=sys.stderr)
	return errmsg
