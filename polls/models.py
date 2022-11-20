from django.db import models

# Create your models here.
from django.db import models

# the following lines added:
import datetime
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    # In the Django Admin section, each model has a property called list_display which controls which fields are
    # displayed on the change list page of the admin page. In this case "was_published_recently" is a custom column
    # and the sort is ordered by the pub_date attribute (Refer to part 7 of the Django Poll tutorial for more detail).
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length = 200)
    votes = models.IntegerField(default = 0)

    def __str__(self):
        return self.choice_text