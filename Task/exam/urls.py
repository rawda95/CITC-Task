from django.urls import path

from .views import index, create_course, course_detail, \
    course_delete, chapter_detail, create_question, create_chapter, \
    chapter_delete, delete_question, update_question, exam_view

app_name = 'exam'
urlpatterns = [
    path('', index, name='index'),
    # course
    path('create-course', create_course, name='create-course'),
    path('<int:course_id>/detail', course_detail, name='course-detail'),
    path('<int:course_id>/delete', course_delete, name='course_delete'),
    # chapter
    path('<int:course_id>/create_chapter', create_chapter, name='create_chapter'),
    path('<int:course_id>/<int:chapter_name>', chapter_detail, name='chapter_detail'),
    path('<int:course_id>/<int:chapter_name>/delete', chapter_delete, name='chapter_delete'),
    path('<int:course_id>/<int:chapter_name>/question', create_question, name='create_question'),
    # question
    path('<int:course_id>/<int:chapter_name>/<int:question_id>/edit', update_question, name='update_question'),
    path('<int:course_id>/<int:chapter_name>/<int:question_id>/delete', delete_question, name='delete_question'),

    # exam
    path('<int:course_id>/exam', exam_view , name='exam_view')
]
