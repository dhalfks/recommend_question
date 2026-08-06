from fastapi import HTTPException
from sqlalchemy.orm import Query

from models import Question, User, UserRole


def question_owner_id(user: User) -> int | None:
    if user.role == UserRole.PROFESSOR:
        return user.id
    if user.role == UserRole.STUDENT:
        return user.professor_id
    return None


def scope_questions(query: Query, user: User) -> Query:
    if user.role == UserRole.ADMIN:
        return query
    owner_id = question_owner_id(user)
    if owner_id is None:
        return query.filter(Question.id == -1)
    return query.filter(Question.professor_id == owner_id)


def ensure_question_access(question: Question | None, user: User) -> Question:
    if question is None:
        raise HTTPException(status_code=404, detail="문항을 찾을 수 없습니다.")
    if user.role != UserRole.ADMIN and question.professor_id != question_owner_id(user):
        raise HTTPException(status_code=404, detail="문항을 찾을 수 없습니다.")
    return question
