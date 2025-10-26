
#  ALB Target Group Health Check (Datadog Custom Check)

This Datadog custom check (`ALB_TG_Check.py`) monitors the health of AWS Application Load Balancer (ALB) Target Groups using the AWS SDK (`boto3`).
It collects and reports the number of **healthy targets** per target group as a custom metric in Datadog.

---

## 📄 Overview

This check connects to AWS via `boto3` and queries the **Target Health** status of each ALB Target Group you specify.
It then submits the following metric to Datadog:

| Metric Name                      | Type  | Description                                                          |
| -------------------------------- | ----- | -------------------------------------------------------------------- |
| `application_lb.healthy_targets` | Gauge | Number of targets in the Target Group that are in a `healthy` state. |

You can use this metric to create dashboards, alerts, and monitor the overall health of your application backend targets behind an ALB.

---

## Files

### `ALB_TG_Check.py`

The main check file implementing the Datadog Agent custom check.
It:

* Connects to AWS ELBv2 using `boto3`.
* Fetches Target Group health states.
* Sends metrics to Datadog.

### `ALB_TG_Check.yaml`

Configuration file for the check.
Defines which Target Groups to monitor and how often to run the check.

---

##  Configuration

1. **Copy the check files**
   Place both files in your Datadog Agent’s custom check directory:

   ```bash
   /etc/datadog-agent/checks.d/ALB_TG_Check.py
   /etc/datadog-agent/conf.d/ALB_TG_Check.yaml
   ```

2. **Edit the configuration file**
   Open `ALB_TG_Check.yaml` and replace the placeholder ARNs with your own Target Group ARNs:

   ```yaml
   init_config:

   instances:
     - name: alb_target_check
       target_group_arns:
         - arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/my-web-app-tg/abcdef1234567890
         - arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/my-web-app-tg-2/abcdef1234567890
       min_collection_interval: 60
   ```

3. **(Optional) Specify AWS region**
   If your Target Groups are in a different region, you can include:

   ```yaml
   region: us-west-2
   ```

4. **Ensure the Datadog Agent has AWS credentials**
   The Agent must have access to AWS credentials (via environment variables, an instance profile, or `~/.aws/credentials`).
   The IAM role or user should have the following permissions:

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "elasticloadbalancing:DescribeTargetGroups",
           "elasticloadbalancing:DescribeTargetHealth"
         ],
         "Resource": "*"
       }
     ]
   }
   ```

---

##  Metrics

| Metric Name                      | Type  | Description                                   | Tags                        |
| -------------------------------- | ----- | --------------------------------------------- | --------------------------- |
| `application_lb.healthy_targets` | Gauge | Count of healthy targets in the Target Group. | `target_group:<group_name>` |

---

##  Example Output

Example Datadog log output when the check runs:

```
INFO | Checking target group: my-web-app-tg
INFO | Checking target group: my-web-app-tg-2
```

And the metric reported:

```
application_lb.healthy_targets{target_group:my-web-app-tg} = 3
application_lb.healthy_targets{target_group:my-web-app-tg-2} = 5
```

---

# Troubleshooting

* **No metrics appearing:**

  * Ensure the check files are correctly placed under `checks.d/` and `conf.d/`.
  * Verify the AWS credentials are valid and accessible to the Agent.
  * Run `datadog-agent check ALB_TG_Check` manually to test.

* **Error in logs:**
  Check `/var/log/datadog/agent.log` for any errors like permission issues or missing ARNs.


