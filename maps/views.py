from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from maps.models import *


# Create your views here.

@login_required
def map_create(request):
    args = {}
    user = request.user
    simple = SimpleUser.objects.get(user=user)
    if not simple.moder:
        raise Http404
    if request.method == 'POST':
        name = request.POST['name']
        them = request.POST['them']
        args.update({'name': name, 'them': them})
        map = Map(name=name, them=them)
        map.save()
        if request.FILES.get('image'):
            image = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save('map/' + image.name, image)
            map.image.name = filename
            map.save()
        return HttpResponseRedirect(reverse('maps:maps'))
    return render(request, 'maps/map_create.html', args)


@login_required
def map_all(request):
    if request.method == 'GET':
        user = request.user
        simple = SimpleUser.objects.get(user=user)
        if not simple.moder:
            raise Http404
        maps = Map.objects.all()
    return render(request, 'maps/all.html', {'maps': maps})


@login_required
def lesson_create(request, map_id):
    args = {}
    user = request.user
    simple = SimpleUser.objects.get(user=user)
    if not simple.moder:
        raise Http404
    map = Map.objects.get(id=map_id)
    args['map'] = map
    if request.method == 'POST':
        name = request.POST['name']
        text = request.POST['text']
        args.update({'name': name, 'text': text})
        lesson = Lesson(name=name, text=text, map=map)
        lesson.save()

        if request.FILES.get('image'):
            image = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save('maps/' + str(map_id) + '/lesson/' + str(lesson.id) + image.name, image)
            lesson.image.name = filename
            lesson.save()
        return HttpResponseRedirect(reverse('maps:lessons', kwargs={'map_id': map_id}))
    return render(request, 'maps/lesson_create.html', args)


@login_required
def lesson_page(request, map_id, lesson_id):
    args = {}
    lesson = Lesson.objects.get(id=lesson_id)
    args['lesson'] = lesson
    args['map_id'] = map_id
    user = request.user
    simple = SimpleUser.objects.get(user=user)
    lesson_user = UserLesson.objects.filter(user=simple, lesson=lesson).first()
    parents = Chain.objects.filter(lesson_child=lesson)
    childs = Chain.objects.filter(lesson_parent=lesson)
    lessons = Lesson.objects.all()
    args['user'] = simple
    args['lesson_user'] = lesson_user
    args['parent_list'] = parents
    args['child_list'] = childs
    args['lessons'] = lessons
    if request.method == 'POST':
        lesson_parent_id = request.POST['chain_']
        lesson_parent = Lesson.objects.get(id=lesson_parent_id)
        chain = Chain(lesson_child=lesson, lesson_parent=lesson_parent)
        chain.save()
    return render(request, "maps/lesson.html", args)


@login_required
def lessons_list(request, map_id):
    if request.method == 'GET':
        lessons = [elem for elem in Lesson.objects.filter(map=Map.objects.get(id=map_id))]
        return render(request, "maps/lessons_list.html", {'lessons': lessons, 'map_id': map_id})


@login_required
def question_create(request, map_id, lesson_id):
    args = {}
    user = request.user
    simple = SimpleUser.objects.get(user=user)
    if not simple.moder:
        raise Http404
    lesson = Lesson.objects.get(id=lesson_id)
    if request.method == 'POST':
        text = request.POST['text']
        args['text'] = text
        question = Question(text=text, lesson=lesson)
        question.save()

        for i in range(1, 5):
            answer = request.POST['answer' + str(i)]
            answer = ChoiceAnswer(text=answer,
                                  question=question)
            if request.POST.get('right' + str(i)):
                answer.right = True
            answer.save()
        return HttpResponseRedirect(reverse('maps:questions', kwargs={'map_id': map_id, 'lesson_id': lesson_id}))
    return render(request, 'maps/question_create.html', args)


@login_required
def question_list(request, map_id, lesson_id):
    user = request.user
    simple = SimpleUser.objects.get(user=user)
    if not simple.moder:
        raise Http404
    lesson = Lesson.objects.get(id=lesson_id)
    questions = Question.objects.filter(lesson=lesson)
    return render(request, 'maps/questions_list.html',
                  {'questions': questions, 'map_id': map_id, 'lesson_id': lesson_id})


@login_required
def lesson_test(request, map_id, lesson_id):
    args = {}
    percent = 0
    count = 5
    args['map_id'] = map_id
    args['lesson_id'] = lesson_id
    lesson = Lesson.objects.get(id=lesson_id)
    user = request.user
    simple = SimpleUser.objects.get(user=user)
    questions = Question.objects.filter(lesson=lesson)
    if request.method == 'GET':
        args['test'] = questions
    if request.method == 'POST':
        test = Test()
        test.save()
        for i in questions:
            question_id = request.POST['question' + str(i.id)]
            ready_answer = request.POST['answer' + str(i.id)]
            right = False
            question = Question.objects.get(id=question_id)
            if ChoiceAnswer.objects.filter(id=int(ready_answer), right=True):
                right = True
                percent += 1
            ready_question = ReadyQuestion(question=question, test=test, right=right)
            ready_question.save()
        percent = (percent / count) * 100
        print(percent)
        user_lesson = UserLesson(user=simple, lesson=lesson, percent=percent, comlite=True)
        user_lesson.save()
        test = Test(user_lesson=user_lesson)
        test.save()
        return HttpResponseRedirect(reverse('maps:lesson_page', kwargs={'map_id': map_id, 'lesson_id': lesson_id}))
    return render(request, 'maps/test_page.html', args)


def get_ids(questions):
    ids = []
    for question in questions:
        ids.append(str(question.id))
    return ids
