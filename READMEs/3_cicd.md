# TLDR

Setting up CICD

## Create the Service Account

A "service account" is a fancy name for a username and password that we give to a computer to use on our behalf as opposed to a human.

```sh
touch scripts/generate_service_account.sh
chmod +x scripts/generate_service_account.sh
```

## Add the cicd.yaml

```sh
mkdir -p .github/workflows
touch .github/workflows/cicd.yaml # populate based on https://github.com/thaddavis/research-agents-supercharged/blob/main/.github/workflows/cicd.yaml
```

# Add the Service Account to the GitHub Actions Settings tab

- https://github.com/COMMAND-LABS/research-agents-boilerplate/settings/secrets/actions

## PRO SHIT: Ignore the Service Account

Add `research-agents-cicd-sa.json` to .gitignore
