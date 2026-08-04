#!/usr/bin/env python3
"""
로컬 환경 테스트 스크립트
SQLite DB를 생성하고 샘플 데이터를 삽입합니다.
"""

import os
import sys

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import create_tables, SessionLocal, Subject, Question, DifficultyLevel, QuestionType
from datetime import datetime

def init_local_db():
    """로컬 SQLite 데이터베이스 초기화"""
    
    print("📚 로컬 데이터베이스 초기화 중...")
    
    # 테이블 생성
    create_tables()
    print("✅ 테이블 생성 완료")
    
    db = SessionLocal()
    
    try:
        # 샘플 과목 생성
        subjects = [
            Subject(name="Python 기초", description="Python 프로그래밍 기초"),
            Subject(name="JavaScript", description="JavaScript 및 Web 개발"),
            Subject(name="SQL", description="데이터베이스 쿼리"),
        ]
        
        for subject in subjects:
            db.add(subject)
        db.commit()
        print(f"✅ {len(subjects)}개 과목 생성 완료")
        
        # 각 과목에 샘플 문제 생성
        for i, subject in enumerate(subjects):
            questions = [
                Question(
                    subject_id=subject.id,
                    question_type=QuestionType.EXCEL,
                    title=f"{subject.name} - 기본 개념 {j+1}",
                    content=f"다음 중 {subject.name}에 대한 설명으로 가장 올바른 것은?",
                    correct_answer="2",
                    explanation=f"이것은 {subject.name}의 기본 개념입니다.",
                    difficulty=DifficultyLevel.EASY if j == 0 else DifficultyLevel.MEDIUM,
                    options='["선택지 1", "정답", "선택지 3", "선택지 4"]',
                    tags=subject.name.split()[0].lower()
                )
                for j in range(3)
            ]
            
            for question in questions:
                db.add(question)
        
        db.commit()
        print("✅ 샘플 문제 생성 완료")
        
        # 통계 출력
        total_questions = db.query(Question).count()
        print(f"\n📊 데이터베이스 통계:")
        print(f"   - 과목: {db.query(Subject).count()}개")
        print(f"   - 문제: {total_questions}개")
        
        # 난이도별 통계
        easy = db.query(Question).filter(Question.difficulty == DifficultyLevel.EASY).count()
        medium = db.query(Question).filter(Question.difficulty == DifficultyLevel.MEDIUM).count()
        hard = db.query(Question).filter(Question.difficulty == DifficultyLevel.HARD).count()
        print(f"\n📈 난이도별 문제:")
        print(f"   - EASY: {easy}개")
        print(f"   - MEDIUM: {medium}개")
        print(f"   - HARD: {hard}개")
        
        print("\n✨ 로컬 DB 초기화 완료!")
        print("\n🚀 다음 명령으로 서버를 시작하세요:")
        print("   python main.py")
        print("\n📖 API 문서 확인:")
        print("   http://localhost:8000/docs")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_local_db()
