from datadog_checks.base import AgentCheck
import boto3

class ALBCheck(AgentCheck):
    def check(self, instance):
        #results = []
        region = instance.get('region', 'us-east-1')
        elbv2 = boto3.client('elbv2', region_name=region)
        target_group_arns = instance.get('target_group_arns', [])

        if not target_group_arns:
            self.log.error("No target_group_arns provided in instance config.")
            return

        try:
            for target_group_arn in target_group_arns:
                target_group = elbv2.describe_target_groups(TargetGroupArns=[target_group_arn])['TargetGroups'][0]['TargetGroupName']
                self.log.info(f"Checking target group: {target_group}")

                response = elbv2.describe_target_health(TargetGroupArn=target_group_arn)
                healthy_count = sum(
                    1 for target in response['TargetHealthDescriptions']
                    if target['TargetHealth']['State'] == 'healthy'
                )

                # Send metric to Datadog
                self.gauge(
                    'application_lb.healthy_targets',
                    healthy_count,
                    tags=[f"target_group:{target_group}"]
                )

                #results.append((target_group, healthy_count))

        except Exception as e:
            self.log.error(f"Error checking target group health: {e}")
