-- Migration: 0001_init
-- Create voice agent sessions table

CREATE TABLE IF NOT EXISTS voice_agent_sessions (
    session_id VARCHAR(255) PRIMARY KEY,
    meeting_id VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
