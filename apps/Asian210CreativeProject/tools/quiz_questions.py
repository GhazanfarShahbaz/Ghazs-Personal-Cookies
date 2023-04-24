from json import load
from typing import Set, Dict, Callable, List
from random import randint


from apps.Asian210CreativeProject.tools.timeline_json import get_timeline_json, date_to_datetime

def get_random_index(size: int, indices_to_avoid: Set[str]) -> int:
    index: int = randint(0, size - 1)
    
    while index in indices_to_avoid:
        index = randint(0, size - 1)
        
    return index


def generate_quiz_question_one(timeline_json: dict, answer_index: int, incorrect_indices: Set[int]) -> dict:
    return {
        "question_type": 1, 
        "question": f"What happened during {timeline_json[answer_index]['date']}?",
        "choices": [timeline_json[index]["name"] for index in incorrect_indices] + [timeline_json[answer_index]["name"]],
        "answer": timeline_json[answer_index]["name"]
    }


def generate_quiz_question_two(timeline_json: dict, answer_index: int, incorrect_indices: Set[int]) -> dict:
    return {
        "question_type": 2, 
        "question": f"Which happened during the following event: {timeline_json[answer_index]['name']}?",
        "choices": [timeline_json[index]["description"] for index in incorrect_indices] + [timeline_json[answer_index]["description"]],
        "answer": timeline_json[answer_index]["description"]
    }


def generate_quiz_question_three(timeline_json: dict, answer_index: int, incorrect_indices: Set[int]) -> dict:
    earliest_date, date_index = date_to_datetime(timeline_json[answer_index]["dateToSortOn"]), answer_index
    
    for index in incorrect_indices:
        item = timeline_json[index]
        
        if date_to_datetime(item["dateToSortOn"]) < earliest_date:
            earliest_date, date_index = date_to_datetime(item["dateToSortOn"]), index
            
    if date_index != answer_index:
        incorrect_indices.remove(date_index)
        incorrect_indices.add(answer_index)
        answer_index = date_index
    
    return {
        "question_type": 3, 
        "question": f"Which of the following events occurred first?",
        "choices": [timeline_json[index]["name"] for index in incorrect_indices] + [timeline_json[answer_index]["name"]],
        "answer": timeline_json[answer_index]["name"]
    }

def generate_quiz_question_four(timeline_json: dict, answer_index: int, incorrect_indices: Set[int]) -> dict:
    earliest_date, date_index = date_to_datetime(timeline_json[answer_index]["dateToSortOn"]), answer_index
    
    for index in incorrect_indices:
        item = timeline_json[index]
        
        if date_to_datetime(item["dateToSortOn"]) > earliest_date:
            earliest_date, date_index = date_to_datetime(item["dateToSortOn"]), index
            
    if date_index != answer_index:
        incorrect_indices.remove(date_index)
        incorrect_indices.add(answer_index)
        answer_index = date_index
    
    return {
        "question_type": 4, 
        "question": f"Which of the following events occurred last?",
        "choices": [timeline_json[index]["name"] for index in incorrect_indices] + [timeline_json[answer_index]["name"]],
        "answer": timeline_json[answer_index]["name"]
    }

def generate_quiz_question_five(timeline_json: dict, answer_index: int, incorrect_indices: Set[int]) -> dict:
    return {
        "question_type": 5,
        "question": f"When did the following event occur: {timeline_json[answer_index]['date']}?",
        "choices": [timeline_json[index]["date"] for index in incorrect_indices] + [timeline_json[answer_index]["name"]],
        "answer": timeline_json[answer_index]["date"]
    }
    


def generate_question(timeline_json: List[dict]) -> dict: 
    quiz_question_templates: Dict[int, Callable] = {
        1: generate_quiz_question_one,
        2: generate_quiz_question_two,
        3: generate_quiz_question_three,
        4: generate_quiz_question_four,
        5: generate_quiz_question_five
    }
    
    question_index: int = randint(1, len(quiz_question_templates.keys()))
    size: int = len(timeline_json)
    
    answer_index: int = get_random_index(size, set())
    indices_to_avoid: Set[int] = {answer_index}
    incorrect_indices: Set[int] = set()
    
    for i in range(3):
        new_index = get_random_index(size, indices_to_avoid)
        indices_to_avoid.add(new_index)
        incorrect_indices.add(new_index)
        
    return quiz_question_templates[question_index](timeline_json, answer_index, incorrect_indices)


def generate_quiz_questions(number_of_questions: int) -> dict:
    timeline_json: List[dict] = get_timeline_json()
    quiz_questions: List[dict] = []
    
    for i in range(number_of_questions):
        quiz_questions.append(generate_question(timeline_json))
        
    return quiz_questions
