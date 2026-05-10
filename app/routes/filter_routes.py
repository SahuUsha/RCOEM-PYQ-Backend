from fastapi import APIRouter, HTTPException
from app.services.db_service import (
    get_subjects,
    get_years_by_subject,
    get_questions_by_year_subject,
    get_marks_by_year_subject,
    get_questions_by_year_subject_marks,
)

router = APIRouter(prefix="/filter", tags=["Filter"])


# ─────────────────────────────────────────
# STEP 1 → GET ALL SUBJECTS
# ─────────────────────────────────────────
@router.get("/subjects")
def fetch_all_subjects():
    """Return every distinct subject in the database."""
    subjects = get_subjects()
    if not subjects:
        raise HTTPException(status_code=404, detail="No subjects found")
    return {"subjects": subjects}


# ─────────────────────────────────────────
# STEP 2 → GET YEARS AVAILABLE FOR A SUBJECT
# ─────────────────────────────────────────
@router.get("/years/{subject}")
def fetch_years_for_subject(subject: str):
    """Given a subject, return all years that have questions for it."""
    years = get_years_by_subject(subject)
    if not years:
        raise HTTPException(
            status_code=404,
            detail=f"No years found for subject '{subject}'"
        )
    return {"subject": subject, "years": years}


# ─────────────────────────────────────────
# STEP 3 → GET QUESTIONS BY SUBJECT + YEAR
# ─────────────────────────────────────────
@router.get("/questions")
def fetch_questions(subject: str, year: int):
    """Return all questions filtered by subject and year."""
    questions = get_questions_by_year_subject(year, subject)
    return {
        "subject": subject,
        "year": year,
        "total": len(questions),
        "questions": questions,
    }


# ─────────────────────────────────────────
# STEP 4 → GET MARKS BY SUBJECT + YEAR
# ─────────────────────────────────────────
@router.get("/marks/{subject}/{year}")
def fetch_marks_for_subject_year(subject: str, year: int):
    """Given a subject and year, return all available marks categories."""
    marks = get_marks_by_year_subject(year, subject)
    if not marks:
        raise HTTPException(
            status_code=404,
            detail=f"No marks found for subject '{subject}' and year '{year}'"
        )
    return {"subject": subject, "year": year, "marks": marks}


# ─────────────────────────────────────────
# STEP 5 → GET QUESTIONS BY SUBJECT + YEAR + MARKS
# ─────────────────────────────────────────
@router.get("/questions/marks")
def fetch_questions_by_marks(subject: str, year: int, marks: str):
    """Return all questions filtered by subject, year, and marks."""
    questions = get_questions_by_year_subject_marks(year, subject, marks)
    return {
        "subject": subject,
        "year": year,
        "marks": marks,
        "total": len(questions),
        "questions": questions,
    }
