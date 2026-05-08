#!/usr/bin/env python3

import json
import hmac
import hashlib
from datetime import datetime, timezone
import os
import sys
import urllib.request
import urllib.error

def create_submission_payload(name, email, resume_link, repository_link, action_run_link):
    timestamp = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    
    # Create payload dictionary
    payload = {
        "action_run_link": action_run_link,
        "email": email,
        "name": name,
        "repository_link": repository_link,
        "resume_link": resume_link,
        "timestamp": timestamp
    }
    
    compact_payload = json.dumps(payload, separators=(',', ':'), sort_keys=True)
    
    return compact_payload

def generate_signature(payload, secret):
    signature = hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return f"sha256={signature}"

def submit_application(payload, signature):
    url = "https://b12.io/apply/submission"
    
    headers = {
        'X-Signature-256': signature,
        'Content-Type': 'application/json',
        'Content-Length': str(len(payload))
    }
    
    req = urllib.request.Request(
        url,
        data=payload.encode('utf-8'),
        headers=headers,
        method='POST'
    )
    
    try:
        # Send request
        with urllib.request.urlopen(req) as response:
            response_data = response.read().decode('utf-8')
            return response.getcode(), response_data
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8')
    except urllib.error.URLError as e:
        return None, str(e)

def main():
    name = os.getenv('APPLICANT_NAME', 'Dagmawi Debru Gebremeskel')
    email = os.getenv('APPLICANT_EMAIL', 'dagmawidebru14@gmail.com')
    resume_link = os.getenv('RESUME_LINK', 'https://drive.google.com/file/d/14VIgqVVAcqKRagWfkvgI7m8riY-eZYR8/view')
    repository_link = os.getenv('REPOSITORY_LINK', 'https://github.com/dage14/B12-Submit-Application-Script')
    #action_run_link = "https://link-to-github-or-another-forge.example.com/your/repository/actions/runs/run_id"
    
    # name = os.getenv('APPLICANT_NAME', 'Test User')
    # email = os.getenv('APPLICANT_EMAIL', 'test@example.com')
    # resume_link = os.getenv('RESUME_LINK', 'https://linkedin.com/in/testuser')
    # repository_link = os.getenv('REPOSITORY_LINK', 'https://github.com/testuser/test-repo')
    # action_run_link = os.getenv('ACTION_RUN_LINK', 'https://github.com/testuser/test-repo/actions/runs/123456')
    #SECRET_TEST = "dagmawi-Job-Application-b12"

    server_url = os.getenv('GITHUB_SERVER_URL', 'https://github.com')
    repository = os.getenv('GITHUB_REPOSITORY')
    run_id = os.getenv('GITHUB_RUN_ID')
    if repository and run_id:
        action_run_link = f"{server_url}/{repository}/actions/runs/{run_id}"
    else:
        print(" Error: GITHUB_REPOSITORY and/or GITHUB_RUN_ID environment variables not set")
        sys.exit(1)
        #action_run_link = os.getenv('ACTION_RUN_LINK', 'https://link-to-github-or-another-forge.example.com/your/repository/actions/runs/run_id')
    SECRET = os.getenv('B12_SIGNING_SECRET')
    if not SECRET:
        print(" Error: B12_SIGNING_SECRET environment variable not set")
        sys.exit(1)
    
    print("Creating submission payload...")
    payload = create_submission_payload(name, email, resume_link, repository_link, action_run_link)
    print(f"Payload: {payload}")
    
    print("\nGenerating HMAC-SHA256 signature...")
    signature = generate_signature(payload, SECRET)
    print(f"Signature: {signature}")
    
    print("\nSubmitting application...")
    status_code, response = submit_application(payload, signature)
    
    if status_code == 200:
        print(f"\n Success! HTTP {status_code}")
        print(f"Response: {response}")
        
        # Parse and display receipt
        try:
            response_json = json.loads(response)
            if response_json.get('success'):
                print(f"\n Application submitted successfully!")
                print(f" Receipt: {response_json.get('receipt')}")
                print("\nPlease copy this receipt into the field below:")
                print(f"\n{response_json.get('receipt')}")
        except json.JSONDecodeError:
            print(f"\nResponse received but couldn't parse JSON: {response}")
    else:
        print(f"\n Error: Submission failed with HTTP {status_code}")
        print(f"Response: {response}")
        sys.exit(1)

if __name__ == "__main__":
    main()