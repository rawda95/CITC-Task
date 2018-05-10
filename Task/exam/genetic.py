import random

from .models import Question

questions = list(Question.objects.all())
population = []


def init():
    print(len(questions))
    for i in range(0, 5):
        chromosomes = random.sample(questions, 6)
        population.append(chromosomes)


def compute_objective_function(coures):
    for chromosomes in population:
        print('chromosomes: ', chromosomes)
        objective = objective_percentage(chromosomes)
        difficulty = difficulty_percentage(chromosomes)
        chapter = chapter_percentage(chromosomes, coures)
        total = (((objective + difficulty + chapter) / 300)*100)
        print(total)


def objective_percentage(chromosome):
    reminding = 0
    understanding = 0
    creativity = 0
    total = len(chromosome) / 3
    for question in chromosome:
        if question.objective == 'R':
            reminding += 1
        elif question.objective == 'U':
            understanding += 1
        elif question.objective == 'C':
            creativity += 1
    reminding_p = (reminding / total)
    if reminding_p > 1.0:
        reminding_p = 1.0
    understanding_p = (understanding / total)
    if understanding_p > 1.0:
        understanding_p = 1.0
    creativity_p = (creativity / total)
    if creativity_p > 1.0:
        creativity_p = 1.0

    total = ((reminding_p + understanding_p + creativity_p) / 3) * 100
    print(total)

    ''''
    print('reminding:', reminding, 'reminding_p: ', reminding_p)
    print('understanding:', understanding, 'understanding_p:', understanding_p)
    print('creativity_p:', creativity, 'creativity_p :', creativity_p)
    print('total:', total)
    '''
    return total


def difficulty_percentage(chromosome):
    difficult = 0
    simple = 0
    total = len(chromosome) / 2
    for question in chromosome:
        if question.difficulty == 'D':
            difficult += 1
        elif question.difficulty == 'S':
            simple += 1

    difficulty_p = (difficult / total)
    if difficulty_p > 1.0:
        difficulty_p = 1.0
    simple_p = (simple / total)
    if simple_p > 1.0:
        simple_p = 1.0

    total = (((difficulty_p + simple_p) / 2) * 100)
    print(total)
    ''''
    print('difficult:', difficult, 'difficult_p:', difficulty_p)
    print('simple:', simple, 'simple_p :', simple_p)
    print('total:', total)
    '''
    return total


def chapter_percentage(chromosome, coures):
    num_of_chapter = coures.chapter_set.count()
    chapters = {chapter.name: 0 for chapter in coures.chapter_set.all()}
    total = len(chromosome) / num_of_chapter
    for question in chromosome:
        chapters[question.chapter.name] += 1

    for k in chapters.keys():
        c = chapters[k] / total
        if c > 1.0:
            c = 1.0
        chapters[k] = c
    s = 0
    for k in chapters.keys():
        s += chapters[k]
    total = (s / num_of_chapter) * 100
    print(total)
    return total
