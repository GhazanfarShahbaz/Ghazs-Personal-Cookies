from model import Session as Sess, CodingQuestion
from sqlalchemy.orm import Session, Query
from typing import List


class CodingQuestionRepository(object):
    def __init__(self):
        self.session: Session = Sess()

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        self.session.close()

    def insert(self, coding_questions: List[CodingQuestion]) -> None:
        for coding_question in coding_questions:
            self.session.add(coding_question)

        self.session.commit()

    def update(self, question_id: int, update_dictionary: dict) -> None:
        coding_question: CodingQuestion = self.session.query(
            CodingQuestion).filter(CodingQuestion.QuestionId == question_id).first()

        if update_dictionary.get("QuestionId"):
            coding_question.QuestionId = update_dictionary["QuestionId"]

        if update_dictionary.get("QuestionLink"):
            coding_question.QuestionLink = update_dictionary["QuestionLink"]

        if update_dictionary.get("Difficulty"):
            coding_question.Difficulty = update_dictionary["Difficulty"]

        if update_dictionary.get("AcceptanceRate"):
            coding_question.AcceptanceRate = update_dictionary["AcceptanceRate"]

        if update_dictionary.get("Tags"):
            coding_question.Tags = update_dictionary["Tags"]

        if update_dictionary.get("RequiresSubscription"):
            coding_question.RequiresSubscription = update_dictionary["RequiresSubscription"]

        self.session.commit()

    def get(self, filters: dict) -> List[CodingQuestion]:
        query: Query = self.session.query(CodingQuestion)

        if filters.get("QuestionIds"):
            query = query.filter(
                CodingQuestion.QuestionId.in_(filters["QuestionIds"]))

        if filters.get("QuestionName"):
            if filters.get("QuestionNameExact") is None or filters["QuestionNameExact"] is True:
                query = query.filter(
                    CodingQuestion.QuestionName == filters["QuestionName"])
            else:
                query = query.filter(
                    CodingQuestion.QuestionName.like(filters["QuestionName"]))

        if filters.get("QuestionLink"):
            query = query.filter(
                CodingQuestion.QuestionLink == filters["QuestionLink"])

        if filters.get("Difficulties"):
            query = query.filter(
                CodingQuestion.Difficulty.in_(filters["Difficulties"]))

        if filters.get("AcceptanceRateFrom"):
            query = query.filter(
                CodingQuestion.AcceptanceRate >= filters["AcceptanceRateFrom"])

        if filters.get("AcceptanceRateTo"):
            query = query.filter(
                CodingQuestion.AcceptanceRate >= filters["AcceptanceRateTo"])

        if filters.get("RequiresSubscription") is not None:
            query = query.filter(
                CodingQuestion.RequiresSubscription == filters["RequiresSubscription"])

        return query.all()

    def delete(self, filters: dict) -> None:
        query: Query = self.session.query(CodingQuestion)

        if filters.get("QuestionIds"):
            query = query.filter(
                CodingQuestion.QuestionId.in_(filters["QuestionIds"]))

        if filters.get("QuestionName"):
            if filters.get("QuestionNameExact") is None or filters["QuestionNameExact"] is True:
                query = query.filter(
                    CodingQuestion.QuestionName == filters["QuestionName"])
            else:
                query = query.filter(
                    CodingQuestion.QuestionName.like(filters["QuestionName"]))

        if filters.get("QuestionLink"):
            query = query.filter(
                CodingQuestion.QuestionLink == filters["QuestionLink"])

        if filters.get("Difficulties"):
            query = query.filter(
                CodingQuestion.Difficulty.in_(filters["Difficulties"]))

        if filters.get("AcceptanceRateFrom"):
            query = query.filter(
                CodingQuestion.AcceptanceRate >= filters["AcceptanceRateFrom"])

        if filters.get("AcceptanceRateTo"):
            query = query.filter(
                CodingQuestion.AcceptanceRate >= filters["AcceptanceRateTo"])

        if filters.get("RequiresSubscription") is not None:
            query = query.filter(
                CodingQuestion.RequiresSubscription == filters["RequiresSubscription"])

        query.delete()
        self.session.commit()
