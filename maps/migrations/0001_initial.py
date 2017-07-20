# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-20 19:06
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'цепь',
                'verbose_name_plural': 'цепи',
            },
        ),
        migrations.CreateModel(
            name='ChoiceAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=100, verbose_name='текст')),
                ('right', models.BooleanField(default=False, verbose_name='правильность')),
            ],
            options={
                'verbose_name': 'вариант ответа',
                'verbose_name_plural': 'варианты ответов',
            },
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime.now, verbose_name='дата прохождения')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_management.SimpleUser', verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'экзамен',
                'verbose_name_plural': 'экзамены',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400, verbose_name='имя')),
                ('text', models.TextField(max_length=4000, verbose_name='текст')),
                ('image', models.ImageField(blank=True, default='map_images/no-img.jpg', upload_to='', verbose_name='изображение')),
            ],
            options={
                'verbose_name': 'урок',
                'verbose_name_plural': 'уроки',
            },
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='имя')),
                ('image', models.ImageField(default='map_images/no-img.jpg', upload_to='', verbose_name='изображение')),
                ('them', models.CharField(max_length=40, verbose_name='тема')),
            ],
            options={
                'verbose_name': 'карта',
                'verbose_name_plural': 'карты',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=400, verbose_name='текст')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maps.Lesson', verbose_name='урок пользователя')),
            ],
            options={
                'verbose_name': 'вопрос',
                'verbose_name_plural': 'вопросы',
            },
        ),
        migrations.CreateModel(
            name='ReadyQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('right', models.BooleanField(default=False, verbose_name='правильность')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maps.Question', verbose_name='вопрос')),
            ],
            options={
                'verbose_name': 'готовый вопрос',
                'verbose_name_plural': 'готовые вопросы',
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime.now, verbose_name='дата прохождения')),
            ],
            options={
                'verbose_name': 'тест',
                'verbose_name_plural': 'тесты',
            },
        ),
        migrations.CreateModel(
            name='UserLesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent', models.IntegerField(default=0, verbose_name='процент')),
                ('comlite', models.BooleanField(default=False, verbose_name='прохождение')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maps.Lesson', verbose_name='урок')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_management.SimpleUser', verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'урок пользователя',
                'verbose_name_plural': 'уроки пользователя',
            },
        ),
        migrations.CreateModel(
            name='UserMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent', models.IntegerField(default=0, verbose_name='процент')),
                ('comlite', models.BooleanField(default=False, verbose_name='прохождение')),
                ('map', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maps.Map', verbose_name='карта')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_management.SimpleUser', verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'карта пользователя',
                'verbose_name_plural': 'карты пользователя',
            },
        ),
        migrations.AddField(
            model_name='test',
            name='user_lesson',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='maps.UserLesson', verbose_name='урок пользователя'),
        ),
        migrations.AddField(
            model_name='readyquestion',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maps.Test', verbose_name='тест'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='map',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maps.Map', verbose_name='карта'),
        ),
        migrations.AddField(
            model_name='choiceanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maps.Question', verbose_name='вопрос'),
        ),
        migrations.AddField(
            model_name='chain',
            name='lesson_child',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child', to='maps.Lesson', verbose_name='наследник'),
        ),
        migrations.AddField(
            model_name='chain',
            name='lesson_parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='maps.Lesson', verbose_name='родитель'),
        ),
    ]