from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render

from .forms import QuestionForm, CouresForm
from .generate_exam import gen_exam
from .models import Course, Chapter, Question, Choice


# Create your views here.

# main page list all Courses
def index(request):
    courses = Course.objects.all()
    return render(request, 'exam/index.html', {'courses': courses})


# Course CRD
def create_course(request):
    form = CouresForm(request.POST or None)
    if request.method == "POST":

        if form.is_valid():
            course = form.save(commit=False)
            course.save()
            num_of_chapter = form.cleaned_data['numberOfChapter']
            for i in range(1, num_of_chapter + 1):
                chapter = Chapter(name=str(i), course=course)
                chapter.save()
            # print(course.pk)
            return redirect('exam:course-detail', course_id=course.pk)

    return render(request, 'exam/CreateCourse.html', {'form': form})


def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    # print(course.chapter_set)
    return render(request, 'exam/course-detail.html', {'course': course})


def course_delete(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    course.delete()
    return redirect('exam:index')


# chapters
def create_chapter(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    name = course.chapter_set.count() + 1
    chapter = Chapter(name=str(name), course=course)
    chapter.save()
    context = {'course': course,
               }
    return redirect('exam:course-detail', course_id=course.pk)


def chapter_delete(request, course_id, chapter_name):
    course = get_object_or_404(Course, pk=course_id)
    chapter = get_object_or_404(Chapter, name=chapter_name, course=course)
    chapter.delete()
    return redirect('exam:course-detail', course_id=course.pk)


def chapter_detail(request, course_id, chapter_name):
    course = get_object_or_404(Course, pk=course_id)
    chapter = get_object_or_404(Chapter, name=chapter_name, course=course)
    num_of_q = chapter.question_set.count()
    context = {'course': course,
               'chapter': chapter,
               'num_of_q': num_of_q,
               }
    return render(request, 'exam/chapter-detail.html', context)


def create_question(request, course_id, chapter_name):
    course = get_object_or_404(Course, pk=course_id)
    chapter = get_object_or_404(Chapter, name=chapter_name, course=course)
    # print(chapter.name)
    form = QuestionForm(request.POST or None)
    error = ''
    if request.method == "POST":
        if form.is_valid():
            if 12 > chapter.question_set.count():
                objective = form.cleaned_data['objective']
                objective_type = ob_chapter(objective, chapter)
                # print(objective)
                difficulty = form.cleaned_data['difficulty']
                difficulty_type = db_chapter(difficulty, chapter)
                # print(difficulty)
                if 6 > difficulty_type:
                    if 4 > objective_type:
                        question = form.save(commit=False)
                        question.chapter = chapter
                        db_chapter_add(difficulty, chapter, True)
                        ob_chapter_add(objective, chapter, True)

                        question.save()
                        choices = []
                        for i in range(1, 4):
                            choice = Choice(content=form.cleaned_data['Choice' + str(i)], question=question)
                            choice.save()
                            choices.append(choice)
                        correct_answer = form.cleaned_data['correct_answer']
                        choices[correct_answer - 1].is_correct = True
                        choices[correct_answer - 1].save()

                        return redirect('exam:chapter_detail', course_id=course.pk, chapter_name=chapter_name)
                    else:
                        error += "\n the number of  objective  question should be  equal"
                else:
                    error += "\n the number of difficulty question should be  equal"



            else:
                error += '\n each chapter can have only 12 question'

    context = {'course': course,
               'chapter': chapter,
               'error': error,
               'form': form}
    return render(request, 'exam/create_question.html', context)


def delete_question(request, course_id, chapter_name, question_id):
    course = get_object_or_404(Course, pk=course_id)
    chapter = get_object_or_404(Chapter, name=chapter_name, course=course)
    question = get_object_or_404(Question, pk=question_id, chapter=chapter)
    db_chapter_add(question.difficulty, chapter, False)
    ob_chapter_add(question.objective, chapter, False)
    question.delete()
    return redirect('exam:chapter_detail', course_id=course.pk, chapter_name=chapter_name)


def update_question(request, course_id, chapter_name, question_id):
    course = get_object_or_404(Course, pk=course_id)
    chapter = get_object_or_404(Chapter, name=chapter_name, course=course)
    question = get_object_or_404(Question, pk=question_id, chapter=chapter)

    correct_answer = 1
    for i in range(0, question.choice_set.count()):
        if question.choice_set.all()[i].is_correct:
            correct_answer = i + 1

    initial = {'Choice1': question.choice_set.all()[0],
               'Choice2': question.choice_set.all()[1],
               'Choice3': question.choice_set.all()[2],
               'correct_answer': correct_answer
               }
    error = ''
    form = QuestionForm(request.POST or None, instance=question, initial=initial)
    if form.is_valid():
        # print(chapter.difficulty_num, '---', question.difficulty)
        # print(chapter.reminding_num, '----', question.objective)
        ob_chapter_add(question.objective, chapter, False)
        db_chapter_add(question.difficulty, chapter, False)
        # print(chapter.difficulty_num, '---', question.difficulty)
        # print(chapter.reminding_num, '----', question.objective)
        objective = form.cleaned_data['objective']
        difficulty = form.cleaned_data['difficulty']
        objective_type = ob_chapter(objective, chapter)
        difficulty_type = db_chapter(difficulty, chapter)
        # print(objective, '------', objective_type)
        # print(difficulty, '-----', difficulty_type)

        if 6 > objective_type:
            if 4 > difficulty_type:
                question = form.save(commit=False)
                question.save()
                db_chapter_add(difficulty, chapter, True)
                ob_chapter_add(objective, chapter, True)
                # print(chapter.difficulty_num, '---', question.difficulty)
                # print(chapter.reminding_num, '----', question.objective)

                return redirect('exam:chapter_detail', course_id=course.pk, chapter_name=chapter_name)
            else:
                error += "\n the number of  objective  question should be  equal"
        else:
            error += "\n the number of difficulty question should be  equal"
    context = {'course': course,
               'chapter': chapter,
               'question': question,
               'error': error,
               'form': form}

    return render(request, 'exam/update_question.html', context)


def exam_view(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == "POST":
        reminding = request.POST['reminding']
        understanding = request.POST['understanding']
        creativity = request.POST['creativity']
        num_of_objective = [int(reminding), int(understanding), int(creativity)]
        exam = create_exam(course_id, num_of_objective)
        return render(request, 'exam/create_exam.html', {'course': course, 'exam': exam})

    return render(request, 'exam/create_exam.html', {'course': course})


def create_exam(course_id, num_of_objective):
    exam = []
    course = get_object_or_404(Course, pk=course_id)
    chapters = course.chapter_set.all()
    remaining = [0, 0, 0]
    # / each objectivte ber chapter
    num_of_objective_div = [i // len(chapters) for i in num_of_objective]
    # check for reminder
    for i in range(len(num_of_objective_div)):
        if num_of_objective_div[i] * course.chapter_set.count() < num_of_objective[i]:
            remaining[i] = num_of_objective[i] - num_of_objective_div[i] * len(chapters)
    # create exam for each chapter
    for i in range(len(chapters) - 1):
        questions = chapters[i].question_set.all()
        #   print('num_of_objective_div', num_of_objective_div)
        #  print('remaining',remaining)
        # print('--- gen_ exam ---')
        # print('---chapter', i, '-----')
        # print(gen_exam(questions, num_of_objective_div))
        exam.append(gen_exam(questions, num_of_objective_div))
        # create exam for last chapter
        # print('exam:', exam)
    for i in range(len(remaining)):
        remaining[i] += num_of_objective_div[i]
    # print('remaining',remaining)
    l = len(chapters) - 1
    # print('--- gen_ exam ---')
    # print('---chapter', l, '-----')
    # print(gen_exam(chapters[l].question_set.all(), remaining))
    exam.append(gen_exam(chapters[l].question_set.all(), remaining))
    # for i in exam:
    #    for j in i:
    #       print(i)
    # a = objective_chapter(question, [2, 2, 2])
    # diffculty_chapter(a, [3, 3])
    # compute_objective_function(course)
    print('-----exam------')
    final_exam = []
    for chapter in exam:
        for ty in chapter:
            for q in ty:
                final_exam.append(q)
    print(final_exam)
    return final_exam


def ob_chapter(objective, chapter):
    objective_type = 0
    if objective == 'R':
        objective_type = chapter.reminding_num
    elif objective == 'U':
        objective_type = chapter.understanding_num
    elif objective == 'C':
        objective_type = chapter.creativity_num
    return objective_type


def ob_chapter_add(objective, chapter, T):
    if objective == 'R':
        if T:
            chapter.reminding_num += 1
        else:
            chapter.reminding_num -= 1
        chapter.save()
    elif objective == 'U':
        if T:
            chapter.understanding_num += 1
        else:
            chapter.understanding_num -= 1
        chapter.save()
    elif objective == 'C':
        if T:
            chapter.creativity_num += 1
        else:
            chapter.creativity_num -= 1
        chapter.save()


def db_chapter(difficulty, chapter):
    difficulty_type = 0
    if difficulty == 'D':
        difficulty_type = chapter.difficulty_num
    elif difficulty == 'S':
        difficulty_type = chapter.simple_num
    return difficulty_type


def db_chapter_add(difficulty, chapter, T):
    if difficulty == 'D':
        if T:
            chapter.difficulty_num += 1
        else:
            chapter.difficulty_num -= 1
        chapter.save()
    elif difficulty == 'S':
        if T:
            chapter.simple_num += 1
        else:
            chapter.simple_num -= 1
        chapter.save()
