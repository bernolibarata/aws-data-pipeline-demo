import json
import os
import csv
import boto3
import io

s3 = boto3.client("s3")

DEST_PREFIX = os.environ.get("DEST_PREFIX", "processed/")

def _process_rows(rows):
    #If there is a column named 'value', replace negative values with 0.
    #Otherwise, just pass-through
    if not rows:
        return rows
    
    header = rows[0]
    if "value" not in header:
        return rows
    
    value_idx = header.index("value")
    out = [header]

    for r in rows[1:]:
        if len(r) <= value_idx:
            out.append(r)
            continue
        try:
            v=float(r[value_idx])
            if v < 0:
                r[value_idx] = "0"

        except Exception:
            pass

        out.append(r)

    return out

def lambda_handler(event, context):
    
    for record in event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]

        # Only handle CSV in raw/
        if not key.startswith("raw/") or not key.endswith(".csv"):
            print(f"Skipping object: s3://{bucket}/{key}")
            continue

        print(f"Processing: s3://{bucket}/{key}")

        obj = s3.get_object(Bucket=bucket, Key=key)
        body = obj["Body"].read().decode("utf-8", errors="replace")

        # Read CSV
        reader = csv.reader(io.StringIO(body))
        rows = list(reader)

        # Transform
        processed_rows = _process_rows(rows)

        # Write CSV back
        out_buf = io.StringIO()
        writer = csv.writer(out_buf)
        writer.writerows(processed_rows)
        out_bytes = out_buf.getvalue().encode("utf-8")

        filename = key.split("/")[-1]
        out_key = f"{DEST_PREFIX}processed_{filename}"

        s3.put_object(
            Bucket=bucket,
            Key=out_key,
            Body=out_bytes,
            ContentType="text/csv"
        )

        print(f"Saved: s3://{bucket}/{out_key}")



    return {"status": "ok"}
