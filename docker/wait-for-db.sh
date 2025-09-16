#!/bin/sh
set -e

python - <<'PY'
import os, time, re
import psycopg2

# SQLAlchemy URL → psycopg2 URL (на случай +psycopg2)
url = os.environ.get('DATABASE_URL', 'postgresql://cryptolab:cryptolab@db:5432/cryptolab')
url = re.sub(r'^postgresql\+psycopg2://', 'postgresql://', url)

for i in range(60):
    try:
        psycopg2.connect(url).close()
        print('DB is up')
        break
    except Exception as e:
        print('Waiting for DB...', e)
        time.sleep(2)
else:
    raise SystemExit('DB not reachable')
PY
