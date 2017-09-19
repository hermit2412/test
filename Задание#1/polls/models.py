import datetime
from django.db import models
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse

# Создаем tuple со всеми вариантами state
STATE = (
    ('N','New'),
    ('A','Active'),
    ('F','Finished'),

    )


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    # Добовляем поле state к нашей модели Вопроса
    state = models.CharField(max_length=1,choices=STATE,default='N')
    # Поле для отслеживания предыдущего значения state
    old_state = models.CharField(max_length=1,default='N')
        
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    """
     Переписываем метод save для получения дополнительно функционала:
     - Новый метод позволяет изменять значения state только в след. порядке New -> Active -> Finished
     - Обновляется поле old_state
     """
    def save(self,*args,**kwargs):
        if (self.state == 'N') and (self.old_state == 'N'):
            super(Question,self).save(*args,**kwargs)
        elif (self.state == 'A') and ((self.old_state == 'N') and self.has_one_vote()):
            self.old_state = 'A'
            super(Question,self).save(*args,**kwargs)
        elif (self.state == 'F') and (self.old_state == 'A'):
            self.old_state = 'F'
            super(Question,self).save(*args,**kwargs)
        else:
            pass

    """
    Следующие два метода выполняют проверку поля state
    и в зависимости от значения этого поля возвращают имена полей,
    которые необходимо выставить в readonly_fields в модуле admin.
    """        
    def question_state_check(self):
        if self.state == 'F':
            return [field.name for field in self._meta.get_fields()]
        else: 
            return []

    def choice_state_check(self):
        choice = self.choice_set.all()[0]
        if self.state == 'A':
            field = choice._meta.get_field('choice_text')
            return [field.name,]
        elif self.state == 'F':
            return [field.name for field in choice._meta.get_fields() if field.name != 'id']
        else:
            return []

    """
    Метод has_one_vote выполяет проверку поля votes из модели Choice
    на наличие хотя-бы одного голоса. Данная проверка нужна для выполнения следующего условия:
    - В состояние Активный можно перейти только из состояния Новый и если есть более 1 Выбора
    """
    def has_one_vote(self):
        choices_query = self.choice_set.all()
        one_vote = False
        for choice in choices_query:
            if int(choice.votes) >= 1:
                one_vote = True
        return one_vote

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
