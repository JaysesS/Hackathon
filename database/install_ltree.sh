#!/bin/bash
set -e

psql postgresql://flash:dydka@localhost:5432/database -v ON_ERROR_STOP=1 <<-EOSQL
create extension ltree;
select * FROM pg_extension;
EOSQL