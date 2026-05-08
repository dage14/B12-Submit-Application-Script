# B12 Job Application Submission Script

This Python script automates the submission of job applications to B12.io. It creates a signed payload with applicant details and submits it via HTTP POST.

## Features

- Generates a timestamped JSON payload with applicant information
- Creates an HMAC-SHA256 signature for authentication
- Submits the application to the B12 API endpoint
- Handles success and error responses

## Prerequisites

- Python 3.x
- Environment variables set for applicant details and signing secret

## Setup

1. Clone or download the repository.
2. Ensure Python 3 is installed on your system.

## Environment Variables

Set the following environment variables:

- `APPLICANT_NAME`: Your full name (default: 'Dagmawi Debru Gebremeskel')
- `APPLICANT_EMAIL`: Your email address (default: 'dagmawidebru14@gmail.com')
- `RESUME_LINK`: Link to your resume (default: Google Drive link)
- `REPOSITORY_LINK`: Link to your repository (default: GitHub repo)
- `ACTION_RUN_LINK`: Link to the GitHub Actions run (optional, auto-generated if in GitHub environment)
- `B12_SIGNING_SECRET`: The signing secret provided by B12 (required)

For GitHub Actions, the script automatically constructs `ACTION_RUN_LINK` from `GITHUB_SERVER_URL`, `GITHUB_REPOSITORY`, and `GITHUB_RUN_ID`.

## Usage

Run the script locally:

```bash
python main.py
```

The script will:

1. Create the submission payload
2. Generate the signature
3. Submit the application
4. Display the response, including a receipt on success

## GitHub Actions Workflow

For automated submission via GitHub Actions, create a workflow file (e.g., `.github/workflows/submit-B12-application.yml`) with the following content:

```yaml
name: Submit B12 Job Application

on:
  workflow_dispatch:

jobs:
  submit:
    runs-on: ubuntu-latest
    environment: B12-Environment
    
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Run submission
      env:
        # From Environment VARIABLES
        APPLICANT_NAME: ${{ vars.APPLICANT_NAME }}
        APPLICANT_EMAIL: ${{ vars.APPLICANT_EMAIL }}
        RESUME_LINK: ${{ vars.RESUME_LINK }}
        REPOSITORY_LINK: ${{ vars.REPOSITORY_LINK }}
        
        # From Environment SECRETS
        B12_SIGNING_SECRET: ${{ secrets.B12_SIGNING_SECRET }}
        
      run: python main.py
```

### Setup for GitHub Actions

1. In your repository, go to Settings > Environments and create an environment named `B12-Environment`.
2. Under the environment, add the following variables:
   - `APPLICANT_NAME`
   - `APPLICANT_EMAIL`
   - `RESUME_LINK`
   - `REPOSITORY_LINK`
3. Add the secret `B12_SIGNING_SECRET` under Settings > Secrets and variables > Actions > Repository secrets.
4. The workflow will automatically generate the `ACTION_RUN_LINK` from the GitHub context.

Trigger the workflow manually from the Actions tab in your repository.

## Output

On successful submission:

- HTTP 200 status
- JSON response with success flag and receipt
- Receipt printed for copying

On failure:

- Error status code and message
- Script exits with code 1

## Troubleshooting

- Ensure `B12_SIGNING_SECRET` is set; the script will exit if not found.
- Check network connectivity for the API call.
- Verify all links are valid and accessible.
- For GitHub Actions, ensure the workflow has the necessary permissions to access run details.

