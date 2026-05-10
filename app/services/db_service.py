from app.database import SessionLocal
from app.models import Question


def save_question(
    question_text,
    subject=None,
    year=None,
    semester=None,
    exam_type=None,
    marks=None,
):

    db = SessionLocal()

    try:

        question = Question(
            question_text=question_text,
            subject=subject,
            year=year,
            semester=semester,
            exam_type=exam_type,
            marks=marks,
        )

        db.add(question)
        db.commit()
        db.refresh(question)

        print("Question saved:", question.id)

        return question

    except Exception as e:

        db.rollback()
        print("DB ERROR:", str(e))
        raise

    finally:
        db.close()


def get_questions_by_ids(ids):

    db = SessionLocal()

    try:

        questions = db.query(Question).filter(Question.id.in_(ids)).all()

        return [
            {
                "id": q.id,
                "question": q.question_text,
                "subject": q.subject,
                "year": q.year,
                "semester": q.semester,
                "exam_type": q.exam_type,
                "marks": q.marks
            }
            for q in questions
        ]

    finally:
        db.close()


def get_subjects():

    db = SessionLocal()

    try:

        rows = (
            db.query(Question.subject)
            .distinct()
            .order_by(Question.subject)
            .all()
        )

        return [r[0] for r in rows if r[0] is not None]

    finally:
        db.close()


def get_years_by_subject(subject: str):

    db = SessionLocal()

    try:

        rows = (
            db.query(Question.year)
            .filter(Question.subject == subject)
            .distinct()
            .order_by(Question.year.desc())
            .all()
        )

        return [r[0] for r in rows if r[0] is not None]

    finally:
        db.close()


def get_years():

    db = SessionLocal()

    try:

        rows = db.query(Question.year).distinct().order_by(Question.year.desc()).all()

        return [r[0] for r in rows if r[0] is not None]

    finally:
        db.close()


def get_subjects_by_year(year: int):

    db = SessionLocal()

    try:

        rows = (
            db.query(Question.subject)
            .filter(Question.year == year)
            .distinct()
            .order_by(Question.subject)
            .all()
        )

        return [r[0] for r in rows if r[0] is not None]

    finally:
        db.close()


def get_questions_by_year_subject(year: int, subject: str):

    db = SessionLocal()

    try:

        questions = (
            db.query(Question)
            .filter(Question.year == year, Question.subject == subject)
            .order_by(Question.id)
            .all()
        )

        return [
            {
                "id": q.id,
                "question": q.question_text,
                "subject": q.subject,
                "year": q.year,
                "semester": q.semester,
                "exam_type": q.exam_type,
                "marks": q.marks,
            }
            for q in questions
        ]

    finally:
        db.close()


def get_marks_by_year_subject(year: int, subject: str):

    db = SessionLocal()

    try:

        rows = (
            db.query(Question.marks)
            .filter(Question.year == year, Question.subject == subject)
            .distinct()
            .order_by(Question.marks)
            .all()
        )

        return [r[0] for r in rows if r[0] is not None]

    finally:
        db.close()


def get_questions_by_year_subject_marks(year: int, subject: str, marks: str):

    db = SessionLocal()

    try:

        questions = (
            db.query(Question)
            .filter(
                Question.year == year,
                Question.subject == subject,
                Question.marks == marks
            )
            .order_by(Question.id)
            .all()
        )

        return [
            {
                "id": q.id,
                "question": q.question_text,
                "subject": q.subject,
                "year": q.year,
                "semester": q.semester,
                "exam_type": q.exam_type,
                "marks": q.marks,
            }
            for q in questions
        ]

    finally:
        db.close()