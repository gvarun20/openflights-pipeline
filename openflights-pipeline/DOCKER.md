# Docker Learning Guide — Option 2

Hands-on path for learning **Docker Compose profiles, batch jobs, multi-stage builds, and test stacks** using this project.

**Prerequisites:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

All commands run from:

```powershell
cd E:\SUMMER_PROJECT\openflights-pipeline
```

---

## What you will learn

| Lesson | Docker concept | Project feature |
|--------|----------------|-----------------|
| 1 | Images & containers | Build the ETL image |
| 2 | Compose services & networks | Start Postgres |
| 3 | Profiles | dev vs pipeline vs test |
| 4 | Volumes | Persist DB data |
| 5 | Init scripts | Auto-run schema on first boot |
| 6 | Healthchecks & depends_on | Wait for Postgres before ETL |
| 7 | `compose run --rm` | One-off batch jobs |
| 8 | Multi-stage Dockerfile | Smaller, safer images |
| 9 | Compose overrides | Test stack for CI |
| 10 | Full pipeline in Docker | End-to-end workflow |

---

## Lesson 1 — Build your first image (15 min)

**Concept:** A Dockerfile is a recipe; `docker build` creates an **image**; `docker run` starts a **container** from that image.

```powershell
docker build -t openflights-etl:latest .
```

**Inspect what you built:**

```powershell
docker images openflights-etl
docker history openflights-etl:latest
```

**Run a throwaway container:**

```powershell
docker run --rm openflights-etl:latest python -m etl.run_etl --help
```

**Learn:**
- `--rm` deletes the container when it exits
- `CMD` in Dockerfile is the default command
- Image runs as non-root user `appuser` (check Lesson 8)

---

## Lesson 2 — Start Postgres with Compose (20 min)

**Concept:** `docker-compose.yml` defines **services**. Compose creates a **network** so containers can talk by service name.

```powershell
copy .env.example .env
docker compose --profile pipeline up -d postgres
```

**Verify:**

```powershell
docker compose ps
docker compose logs postgres
docker exec openflights-postgres psql -U openflights -d openflights_dw -c "\dt"
```

**Learn:**
- Service name `postgres` is the hostname other containers use (`DB_HOST=postgres`)
- `-d` runs in background
- Port `5432` is mapped to your machine

**Stop:**

```powershell
docker compose --profile pipeline down
```

---

## Lesson 3 — Compose profiles (20 min)

**Concept:** Profiles turn groups of services on/off without separate compose files.

| Profile | Services | Use when |
|---------|----------|----------|
| `dev` | postgres, pgAdmin, nginx dashboard | Exploring data & UI |
| `pipeline` | postgres + job containers (etl, quality, export) | Running the ETL pipeline |
| `test` | postgres + test runner | CI / integration testing |

**Start dev stack (database + tools):**

```powershell
docker compose --profile dev up -d
```

Open:
- **pgAdmin:** http://localhost:5050 (login from `.env`: `admin@openflights.local` / `admin`)
- **Dashboard:** http://localhost:8080

**Connect pgAdmin to Postgres:**

| Field | Value |
|-------|-------|
| Host | `postgres` (not localhost!) |
| Port | `5432` |
| Database | `openflights_dw` |
| Username | `openflights` |
| Password | `openflights` |

**Why `postgres` not `localhost`?** Inside Docker, each container has its own network. pgAdmin reaches Postgres via the Compose network DNS name.

**Stop dev stack:**

```powershell
docker compose --profile dev down
```

---

## Lesson 4 — Named volumes (15 min)

**Concept:** A **named volume** persists data even when containers are deleted.

```powershell
docker compose --profile pipeline up -d postgres
docker volume ls
docker volume inspect openflights_openflights_pgdata
```

Load some data (Lesson 7), then:

```powershell
docker compose --profile pipeline down
docker compose --profile pipeline up -d postgres
# Data still there if you didn't use down -v
```

**Delete data intentionally:**

```powershell
docker compose --profile pipeline down -v
```

**Learn:** `-v` removes named volumes — fresh empty database next start.

---

## Lesson 5 — Postgres init scripts (15 min)

**Concept:** Files in `/docker-entrypoint-initdb.d/` run **once** when the data directory is empty.

We mount:

```
./sql/schema.sql → /docker-entrypoint-initdb.d/01-schema.sql
```

**Try it:**

```powershell
docker compose --profile pipeline down -v
docker compose --profile pipeline up -d postgres
docker exec openflights-postgres psql -U openflights -d openflights_dw -c "\dt"
```

You should see tables before ETL runs. The ETL `--init` flag still drop/recreates schema — that is intentional (teaches difference between **DB bootstrap** and **ETL reload**).

---

## Lesson 6 — Healthchecks & depends_on (15 min)

**Concept:** `healthcheck` tells Compose when Postgres is ready. `depends_on: condition: service_healthy` prevents ETL from starting too early.

**Watch health status:**

```powershell
docker compose --profile pipeline up -d postgres
docker inspect openflights-postgres --format "{{.State.Health.Status}}"
```

Wait until `healthy`, then run ETL (Lesson 7).

---

## Lesson 7 — Batch jobs with `compose run --rm` (30 min)

**Concept:** Long-running servers (`up -d`) vs one-off jobs (`run --rm`). Data pipelines use **jobs**.

**Full pipeline:**

```powershell
# 1. Start database
docker compose --profile pipeline up -d postgres

# 2. ETL + Soda validation (container removed after exit)
docker compose --profile pipeline run --rm etl

# 3. Quality checks only (optional — already in --validate)
docker compose --profile pipeline run --rm quality

# 4. Export dashboard JSON to ../docs
docker compose --profile pipeline run --rm export
```

**Verify load:**

```powershell
docker exec openflights-postgres psql -U openflights -d openflights_dw -c "SELECT COUNT(*) FROM fact_routes;"
```

Expected: **66316**

**Learn:**
- `run --rm` = create container → run command → delete container
- Each job is a separate container with one responsibility
- `etl` mounts `./data` read-only

---

## Lesson 8 — Multi-stage Dockerfile (20 min)

**Concept:** Stage 1 installs dependencies; stage 2 copies only what is needed. Result: smaller image, faster builds, non-root user.

Open `Dockerfile` and compare:

| Stage | Purpose |
|-------|---------|
| `builder` | `pip install` (heavy, cached layer) |
| `runtime` | App code + non-root `appuser` |

**Compare image size** (before/after if you kept old Dockerfile):

```powershell
docker images openflights-etl
```

**Security check — container runs as non-root:**

```powershell
docker compose --profile pipeline run --rm etl whoami
```

Expected: `appuser`

---

## Lesson 9 — Test stack with compose override (25 min)

**Concept:** `docker-compose.test.yml` **overrides** the base file — same pattern used in CI.

```powershell
docker compose -f docker-compose.yml -f docker-compose.test.yml --profile test up --build --abort-on-container-exit
```

This will:
1. Start Postgres
2. Build image
3. Run ETL + validate + full pytest
4. Exit when test container finishes

**Cleanup:**

```powershell
docker compose -f docker-compose.yml -f docker-compose.test.yml --profile test down -v
```

**Learn:**
- `-f` can be repeated to merge compose files
- `--abort-on-container-exit` stops stack when test job completes
- `test` service runs both ETL and pytest in one job

---

## Lesson 10 — Full workflow cheat sheet

### Daily dev (explore data)

```powershell
docker compose --profile dev up -d
# pgAdmin :5050 | dashboard :8080 | postgres :5432
```

### Run pipeline (load warehouse)

```powershell
docker compose --profile pipeline up -d postgres
docker compose --profile pipeline run --rm etl
docker compose --profile pipeline run --rm export
```

### Run tests in Docker

```powershell
docker compose -f docker-compose.yml -f docker-compose.test.yml --profile test up --build --abort-on-container-exit
```

### Tear down everything

```powershell
docker compose --profile dev --profile pipeline down
docker compose -f docker-compose.yml -f docker-compose.test.yml --profile test down -v
```

---

## Useful debug commands (memorise these)

```powershell
docker compose ps                          # running services
docker compose logs postgres               # service logs
docker compose logs -f etl                 # follow logs
docker network inspect openflights_openflights-net
docker exec -it openflights-postgres psql -U openflights -d openflights_dw
docker system df                           # disk usage
docker builder prune                         # clear build cache (careful)
```

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Using `localhost` inside containers | Use service name `postgres` |
| ETL fails "connection refused" | Wait for healthcheck; start postgres first |
| Empty tables after restart | Run `docker compose run --rm etl` again |
| Port 5432 already in use | Stop local PostgreSQL or change `DB_PORT` in `.env` |
| pgAdmin can't connect | Host must be `postgres`, not `127.0.0.1` |
| Lost all data unexpectedly | You ran `down -v` which deletes volumes |

---

## Next steps after Option 2

| Topic | What to add later |
|-------|-------------------|
| Observability | Grafana + postgres_exporter profile |
| Secrets | Docker secrets or external vault (not `.env` in prod) |
| Kubernetes | Deploy same images to K8s Jobs |
| CI | GitHub Actions `docker compose --profile test` (already wired) |

---

## Quick reference — service map

```
┌─────────────────────────────────────────────────────────────┐
│  profile: dev                                                 │
│  ┌──────────┐  ┌──────────┐  ┌────────────┐                 │
│  │ postgres │  │ pgAdmin  │  │ dashboard  │                 │
│  │  :5432   │  │  :5050   │  │   :8080    │                 │
│  └──────────┘  └──────────┘  └────────────┘                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  profile: pipeline (jobs via run --rm)                      │
│  postgres ──► etl ──► quality / export                      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  profile: test                                              │
│  postgres ──► test (ETL + pytest)                           │
└─────────────────────────────────────────────────────────────┘
```

---

*Start with Lesson 1 today. Do one lesson per session — hands-on beats reading.*
