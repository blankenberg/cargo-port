#!/usr/bin/env python
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

HEADER_KEYS = ['id', 'version', 'platform', 'arch', 'url', 'ext', 'sha']
PACKAGE_SERVER = 'https://depot.galaxyproject.org/software/'

def yield_packages(handle, meta=False, retcode=None):
    for lineno, line in enumerate(handle):
        if line.startswith('#'):
            continue
        try:
            data = line.strip().split('\t')
            if len(data) != len(HEADER_KEYS):
                log.error('[%s] data has wrong number of columns. %s != %s', lineno + 1, len(data), len(HEADER_KEYS))
                retcode = 1

            ld = {k: v for (k, v) in zip(HEADER_KEYS, data)}

            if meta:
                yield ld, lineno, line, retcode
            else:
                yield ld
        except Exception, e:
            log.error(str(e))

def package_name(ld):
    return '_'.join(ld[key] for key in HEADER_KEYS[0:4]) + ld['ext']

def depot_url(ld):
    return PACKAGE_SERVER + '{id}/{id}_{version}_{platform}_{arch}{ext}'.format(**ld)
