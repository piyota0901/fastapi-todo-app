#!/bin/bash
set -e
psql <<-EOSQL
	CREATE DATABASE TODODB;
	CREATE TABLE todos (
		id UUID PRIMARY KEY,
		title VARCHAR(20) NOT NULL,
		comment TEXT NOT NULL,
		isdone BOOLEAN NOT NULL,
		created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
	);
	-- コメント設定
	COMMENT ON TABLE todos IS 'TODOを格納するテーブル';
	COMMENT ON COLUMN todos.id IS 'UUID4で作成されたID';
	COMMENT ON COLUMN todos.title IS NULL;
	COMMENT ON COLUMN todos.comment IS NULL;
	COMMENT ON COLUMN todos.isDone IS 'todoの完了フラグ';
	COMMENT ON COLUMN todos.created_at IS '作成された日時';
EOSQL