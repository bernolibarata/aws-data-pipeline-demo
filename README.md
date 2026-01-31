# AWS Serverless Data Pipeline Demo (S3 → Lambda → S3)


## Overview
This project demonstrates a simple serverless data pipeline built on AWS.  
When a CSV file is uploaded to an Amazon S3 bucket under the `raw/` prefix, an AWS Lambda function (Python) is automatically triggered to process the data and store the output back in S3 under the `processed/` prefix.

The project focuses on core data engineering concepts such as event-driven processing, data cleaning, and cloud-native architectures.

---

## Architecture
Amazon S3 (raw/) → AWS Lambda (Python) → Amazon S3 (processed/)  
Monitoring and logs are handled through Amazon CloudWatch.

---

## AWS Services Used
- Amazon S3  
- AWS Lambda  
- AWS IAM  
- Amazon CloudWatch (Logs)

---

## Data Processing Logic
The Lambda function performs a simple data cleaning task:
- If the dataset contains a column named `value`, all negative numeric values are replaced with `0`
- If the column does not exist, the file is passed through unchanged

---

## How to Reproduce
1. Create an Amazon S3 bucket and add two prefixes:
   - `raw/`
   - `processed/`
2. Create an AWS Lambda function using Python
3. Attach an IAM role allowing read and write access to the S3 bucket
4. Configure an S3 trigger for `ObjectCreated` events with:
   - Prefix: `raw/`
   - Suffix: `.csv`
5. Upload a CSV file to `raw/`
6. Verify that the processed output is written to `processed/` and check execution logs in CloudWatch

---

## Example Execution
Screenshots included in the `docs/screenshots/` folder show:
- Successful Lambda execution logs in CloudWatch
- The generated processed file stored in the S3 `processed/` prefix

---

## Security Notes
- No AWS credentials are stored in the code
- The Lambda function accesses AWS resources using an IAM role
- Only a small, non-sensitive sample dataset is included in the repository

---

## Future Improvements
- Add schema validation and error handling (e.g. dead-letter queues)
- Add automated tests and CI integration
- Extend transformations and support multiple data formats
- Add metrics and alerts for pipeline monitoring

---

## Project Status
Completed
