# TLDR

Setting up CICD

## Create the Service Account and add the cicd.yaml

A "service account" is a fancy name for a username and password that we give to a computer to use on our behalf as opposed to a human.

```sh
touch scripts/generate_service_account.sh
chmod +x scripts/generate_service_account.sh
mkdir -p .github/workflows
touch .github/workflows/cicd.yaml # populate based on https://github.com/thaddavis/research-agents-supercharged/blob/main/.github/workflows/cicd.yaml
```

Then add the Service Account to the GitHub Actions Settings tab

## PRO SHIT: Ignore the Service Account

Add `research-agents-cicd-sa.json` to .gitignore