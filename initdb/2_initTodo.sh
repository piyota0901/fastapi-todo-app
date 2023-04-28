#!/bin/bash
set -e

psql <<-EOSQL
	INSERT INTO todos (
        id,
        title,
        comment,
        isDone
    ) VALUES (
        '2ae9a1d9-20b0-4962-9754-d8f6972e425f',
        'sample1',
        'sample1です',
        false
    ), (
        'd8b45d0a-0419-4798-8f36-2603ef588ab7',
        'sample2',
        'sample2です',
        false
    ), (
        'd35a6b0c-2ce7-4992-9f73-a5ac2a121797',
        'sample3',
        'sample3です',
        false
    )
EOSQL