# TLDR

Setting up CICD

## Add the cicd.yaml and create the Service Account

A "service account" is a fancy name for a username and password that we give to a computer to use on our behalf as opposed to a human.

```sh
mkdir -p .github/workflows
touch .github/workflows/cicd.yaml # populate based on https://github.com/thaddavis/research-agents-supercharged/blob/main/.github/workflows/cicd.yaml
touch scripts/generate_service_account.sh
chmod +x scripts/generate_service_account.sh
```

Then add the Service Account to the GitHub Actions Settings tab

## PRO SHIT: Ignore the Service Account

Add `insurtech-news-crew-cicd-sa.json` to .gitignore