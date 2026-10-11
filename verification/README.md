# Runtime verification

These files preserve the Iacon behavior tests and integration rehearsal from the
parent repositories. They run inside the parent applications, where the shared
database, authentication, owner context, configuration and queue are available.

With both projects checked out at the commits in `source-manifest.json`, run:

```sh
# From the SPEDA repository, with its Python dependencies installed:
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=packages/igor python -m pytest packages/igor/tests/test_library_hall_records.py packages/igor/tests/test_config_precedence.py -q
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=packages/igor python packages/igor/scripts/verify_iacon.py --hisar-checkout ../hisar

# From Hisar, with its Python and Node dependencies installed:
PYTHONDONTWRITEBYTECODE=1 python -m pytest tests -q
npm run build
```

PowerShell uses `$env:PYTHONDONTWRITEBYTECODE='1'` and
`$env:PYTHONPATH='packages/igor'` before the Python commands. Keep pytest scratch
files in the OS temporary directory. On Windows without symlink privileges,
the existing Hisar symlink tests can be excluded with `-k 'not symlink'`.

The API rehearsal creates a disposable vault and derived database. It never
connects to production. The standalone snapshot workflow deliberately checks
integrity and syntax only; it does not advertise a partial application as runnable.
