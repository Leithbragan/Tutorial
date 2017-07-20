import datetime
from django.db import models

# Create your models here.
from user_management.models import SimpleUser


class Map(models.Model):
    class Meta:
        verbose_name = u'карта'
        verbose_name_plural = u'карты'

    name = models.CharField(max_length=40, verbose_name=u'имя')
    image = models.ImageField(default='map_images/no-img.jpg', verbose_name=u'изображение')
    them = models.CharField(max_length=40, verbose_name=u'тема')

    def __str__(self):
        return '%s %s' %(self.id, self.name)


class UserMap(models.Model):
    class Meta:
        verbose_name = u'карта пользователя'
        verbose_name_plural = u'карты пользователя'

    user = models.ForeignKey(SimpleUser, verbose_name=u'пользователь')
    map = models.ForeignKey(Map, verbose_name=u'карта')
    percent = models.IntegerField(default=0, verbose_name=u'процент')
    comlite = models.BooleanField(default=False, verbose_name=u'прохождение')


class Lesson(models.Model):
    class Meta:
        verbose_name = u'урок'
        verbose_name_plural = u'уроки'

    name = models.CharField(max_length=400, verbose_name=u'имя')
    text = models.TextField(max_length=4000, verbose_name=u'текст')
    image = models.ImageField(default='map_images/no-img.jpg', blank=True, verbose_name=u'изображение')
    map = models.ForeignKey(Map, verbose_name=u'карта')

    def __str__(self):
        return self.name

    def get_user_lesson(self):
        return UserLesson.objects.filter(lesson=self)


class UserLesson(models.Model):
    class Meta:
        verbose_name = u'урок пользователя'
        verbose_name_plural = u'уроки пользователя'

    user = models.ForeignKey(SimpleUser, verbose_name=u'пользователь')
    lesson = models.ForeignKey(Lesson, verbose_name=u'урок')
    percent = models.IntegerField(default=0, verbose_name=u'процент')
    comlite = models.BooleanField(default=False, verbose_name=u'прохождение')

    def __str__(self):
        return '%s %s' %('урок пользователя к уроку', self.lesson.id)


class Chain(models.Model):
    class Meta:
        verbose_name = u'цепь'
        verbose_name_plural = u'цепи'

    lesson_child = models.ForeignKey(Lesson, verbose_name=u'наследник', related_name='child')
    lesson_parent = models.ForeignKey(Lesson, verbose_name=u'родитель', related_name='parent')

    def __str__(self):
        return '%s <- [%s]' %(self.lesson_parent.id, self.lesson_child.id)


class Question(models.Model):
    class Meta:
        verbose_name = u'вопрос'
        verbose_name_plural = u'вопросы'

    text = models.TextField(max_length=400, verbose_name=u'текст')
    lesson = models.ForeignKey(Lesson, verbose_name=u'урок пользователя')

    def __str__(self):
        return '%s %s' %('вопрос к у року', self.lesson)

    def get_choices(self):
        return ChoiceAnswer.objects.filter(question=self)


class ChoiceAnswer(models.Model):
    class Meta:
        verbose_name = u'вариант ответа'
        verbose_name_plural = u'варианты ответов'

    text = models.TextField(max_length=100, verbose_name=u'текст')
    question = models.ForeignKey(Question, verbose_name=u'вопрос')
    right = models.BooleanField(default=False, verbose_name=u'правильность')


class Test(models.Model):
    class Meta:
        verbose_name = u'тест'
        verbose_name_plural = u'тесты'

    user_lesson = models.ForeignKey(UserLesson, null=True, verbose_name=u'урок пользователя')
    date = models.DateTimeField(default=datetime.datetime.now, verbose_name=u'дата прохождения')
    def __str__(self):
        return '%s' %( self.date)


class Exam(models.Model):
    class Meta:
        verbose_name = u'экзамен'
        verbose_name_plural = u'экзамены'
    user = models.ForeignKey(SimpleUser, verbose_name=u'пользователь')
    date = models.DateTimeField(default=datetime.datetime.now, verbose_name=u'дата прохождения')


class ReadyQuestion(models.Model):
    class Meta:
        verbose_name = u'готовый вопрос'
        verbose_name_plural = u'готовые вопросы'

    test = models.ForeignKey(Test, verbose_name=u'тест')
    question = models.ForeignKey(Question, verbose_name=u'вопрос')
    right = models.BooleanField(default=False, verbose_name=u'правильность')




