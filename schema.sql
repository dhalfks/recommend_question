-- 과목 테이블
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(30) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(512) NOT NULL,
    role VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE subjects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 문제 테이블
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    subject_id INTEGER NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    question_type VARCHAR(20) NOT NULL,  -- EXCEL, CODE
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    correct_answer TEXT,
    explanation TEXT,
    difficulty VARCHAR(20) NOT NULL,  -- EASY, MEDIUM, HARD, EXPERT
    source_file VARCHAR(255),
    options TEXT,  -- JSON 형식
    tags TEXT,
    external_id INTEGER,
    subject_code VARCHAR(50),
    subject_unit VARCHAR(255),
    code_snippet TEXT,
    answer_code_snippet TEXT,
    benchmark_time INTEGER,
    correct_option INTEGER,
    is_required BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Excel 문제 기록 테이블
CREATE TABLE excel_questions (
    id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    excel_row_number INTEGER NOT NULL,
    file_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 코드 파일 테이블
CREATE TABLE code_files (
    id SERIAL PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_type VARCHAR(20) NOT NULL,  -- java, js, sql, txt, md
    file_content TEXT NOT NULL,
    subject_id INTEGER REFERENCES subjects(id) ON DELETE SET NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 사용자 풀이 기록 테이블
CREATE TABLE user_progress (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    is_correct VARCHAR(20),  -- CORRECT, INCORRECT, SKIP
    user_answer TEXT,
    session_id VARCHAR(36),
    sequence_number INTEGER,
    elapsed_seconds FLOAT,
    achievement_score FLOAT,
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE quiz_sessions (
    id VARCHAR(36) PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    total_seconds FLOAT NOT NULL,
    total_questions INTEGER NOT NULL,
    correct_answers INTEGER NOT NULL,
    score_percent FLOAT NOT NULL,
    achievement_score FLOAT NOT NULL,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 인덱스
CREATE INDEX idx_questions_subject_id ON questions(subject_id);
CREATE INDEX idx_questions_difficulty ON questions(difficulty);
CREATE INDEX idx_questions_created_at ON questions(created_at);
CREATE INDEX idx_questions_external_id ON questions(external_id);
CREATE INDEX idx_questions_subject_code ON questions(subject_code);
CREATE INDEX idx_code_files_subject_id ON code_files(subject_id);
CREATE INDEX idx_user_progress_user_id ON user_progress(user_id);
CREATE INDEX idx_user_progress_question_id ON user_progress(question_id);
