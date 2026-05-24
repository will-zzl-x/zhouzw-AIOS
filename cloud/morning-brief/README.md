# Morning Brief — Cloud Function

Two-way Todoist loop for the AIOS.

- **Morning** (7am AZ): reads AIOS context from GitHub, generates 3–5 daily moves via Claude API, writes them to Todoist project "AIOS Daily"
- **Evening** (9pm AZ): fetches today's Todoist state, appends a completion entry to `journals/daily-log.md` via GitHub API

## Local development

```bash
cd cloud/morning-brief
pip install -r requirements.txt
cp ../../.env .env       # or symlink — needs ANTHROPIC_API_KEY, TODOIST_API_KEY, GITHUB_TOKEN
python main.py --dry-run # prints brief, doesn't write
python main.py morning   # writes to Todoist
python main.py evening   # commits archive entry to daily-log.md
```

## Deploy to Google Cloud Functions

```bash
PROJECT=ai-os-496000
REGION=us-west3   # closest to Phoenix
gcloud config set project $PROJECT

# Secrets (one-time)
echo -n "$ANTHROPIC_API_KEY" | gcloud secrets create anthropic-api-key --data-file=-
echo -n "$TODOIST_API_KEY"   | gcloud secrets create todoist-api-key   --data-file=-
echo -n "$GITHUB_TOKEN"      | gcloud secrets create github-token      --data-file=-

# Morning function
gcloud functions deploy morning-brief \
  --gen2 --runtime=python312 --region=$REGION \
  --source=. --entry-point=morning_brief --trigger-http --no-allow-unauthenticated \
  --set-secrets=ANTHROPIC_API_KEY=anthropic-api-key:latest,TODOIST_API_KEY=todoist-api-key:latest,GITHUB_TOKEN=github-token:latest

# Evening function
gcloud functions deploy evening-archive \
  --gen2 --runtime=python312 --region=$REGION \
  --source=. --entry-point=evening_archive --trigger-http --no-allow-unauthenticated \
  --set-secrets=ANTHROPIC_API_KEY=anthropic-api-key:latest,TODOIST_API_KEY=todoist-api-key:latest,GITHUB_TOKEN=github-token:latest

# Schedulers (America/Phoenix has no DST)
MORNING_URL=$(gcloud functions describe morning-brief --gen2 --region=$REGION --format='value(serviceConfig.uri)')
EVENING_URL=$(gcloud functions describe evening-archive --gen2 --region=$REGION --format='value(serviceConfig.uri)')
SA="$(gcloud projects describe $PROJECT --format='value(projectNumber)')-compute@developer.gserviceaccount.com"

gcloud scheduler jobs create http morning-brief-trigger \
  --location=$REGION --schedule="0 7 * * *" --time-zone="America/Phoenix" \
  --uri="$MORNING_URL" --http-method=POST \
  --oidc-service-account-email="$SA"

gcloud scheduler jobs create http evening-archive-trigger \
  --location=$REGION --schedule="0 21 * * *" --time-zone="America/Phoenix" \
  --uri="$EVENING_URL" --http-method=POST \
  --oidc-service-account-email="$SA"
```

## Architecture

- **No state.** Both functions are stateless — AIOS markdown lives in GitHub.
- **No clone.** Files are fetched via raw GitHub URLs.
- **Writes only to `journals/daily-log.md`**, via GitHub Contents API. Commits to the active branch.
- **Todoist project name is fixed:** `AIOS Daily`. Created on first run if missing.

## Required env vars

| Var | Purpose |
|-----|---------|
| `ANTHROPIC_API_KEY` | Claude API call in morning function |
| `TODOIST_API_KEY` | Todoist REST API |
| `GITHUB_TOKEN` | Read AIOS files + commit to daily-log.md (fine-grained, contents:write on this repo) |
| `AIOS_BRANCH` | Optional — defaults to `claude/build-coding-skills-K5mpd` |
