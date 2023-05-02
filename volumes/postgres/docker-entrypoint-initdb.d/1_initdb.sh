#!/bin/bash
set -e
psql <<-EOSQL
	-- *******************
	-- ユーザー作成
	-- *******************
	CREATE USER todo_app with password 'password' createdb;
	CREATE DATABASE tododb OWNER todo_app;
EOSQL