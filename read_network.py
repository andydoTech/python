import boto3
import boto.cloudformation
conn = boto.cloudformation.connect_to_region('us-west-2')  # or your favorite region
stacks = conn.describe_stacks('network-2')
for stack in stacks:
	print stack.stack_name
	print stack.stack_id
	print stack.stack_status
	print stack.creation_time
	print stack.parameters
	print stack.capabilities
	print stack.tags
	print stack.outputs
	#for output in stack.outputs:
	#	print('%s=%s (%s)' % (output.key, output.value, output.description))
