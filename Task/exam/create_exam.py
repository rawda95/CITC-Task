import random


def init(question_num, difficulty, objective, chapters):
    chapters_num = len(chapters)
    difficulty_ber_chapter = [i // chapters_num for i in difficulty]
    objective_ber_chapter = [i // chapters_num for i in objective]
    print(difficulty_ber_chapter)
    print(objective_ber_chapter)


def diffculty_chapter(questions, difficulty_ber_chapter):
    difficult_q = []
    simple_q = []
    for question in questions:
        if question.difficulty == 'D':
            difficult_q.append(question)
        elif question.difficulty == 'S':
            simple_q.append(question)
    difficult_q_sub =[]
    simple_q_sub= []

    if difficult_q:
        difficult_q_sub = random.sample(difficult_q, difficulty_ber_chapter[0])
    if simple_q:
        simple_q_sub = random.sample(simple_q, difficulty_ber_chapter[1])
    print('diffculty_chapter :')
    print(difficult_q_sub)
    print('--------------------------')
    print(simple_q_sub)
    print('end diffculty_chapter ')
    return difficult_q_sub + simple_q_sub


def objective_chapter(questions, objective_ber_chapter):
    reminding_q = []
    understanding_q = []
    creativity_q = []
    for question in questions:
        if question.objective == 'R':
            reminding_q.append(question)
        elif question.objective == 'U':
            understanding_q.append(question)
        elif question.objective == 'C':
            creativity_q.append(question)
    reminding_q_sub = random.sample(reminding_q, objective_ber_chapter[0])
    understanding_q_sub = random.sample(understanding_q, objective_ber_chapter[1])
    creativity_q_sub = random.sample(creativity_q, objective_ber_chapter[2])
    print('objective_chapter  : ')
    print(reminding_q_sub)
    print('--------------------------')
    print(understanding_q_sub)
    print('--------------------------')
    print(creativity_q_sub)
    print('end objective_chapter ')
    return reminding_q_sub + understanding_q_sub + creativity_q_sub


init(30, [10, 20], [15, 5, 10], [10, 10, 10])
