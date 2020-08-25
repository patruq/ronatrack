from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from django.utils.translation import ugettext_lazy as _
from typedmodels.models import TypedModel
from mptt.models import MPTTModel, TreeForeignKey
from model_utils.models import TimeStampedModel
User = get_user_model()


class Survey(models.Model):
    name = models.CharField(max_length=200)
    version = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    metadata = JSONField(null=True, blank=True)

    class Meta:
        unique_together = ['name', 'version']

class Catageory(models.Model):
    name = models.CharField(max_length=200)

class AnswerType(TypedModel):
    default_choice = {}
    choices = JSONField()

    def save(self, *args, **kwargs):
        if self.choices is None:
            self.choices = self.default_choice
        super(AnswerType, self).save(*args, **kwargs)


class IntAnswer(AnswerType):
    default_choice = {'value': None}


class ZipCodeAnswer(IntAnswer):
    pass


class NumberRangeAnswer(AnswerType):
    default_choice = {'max': 5, 'min': 0}


class MultipleChoiceAnswer(AnswerType):
    default_choice = {1: 'Yes', 2: 'No', 3: 'Maybe', 4: "I don't know"}


class BooleanAnswer(AnswerType):
    default_choice = {False: 'No', True: 'Yes'}


class Question(MPTTModel):
    text = models.TextField(_("Text"))
    metadata = JSONField(null=True, blank=True)
    catageory = models.ForeignKey(Catageory, on_delete=models.CASCADE)
    conditional_trigger = JSONField(null=True, blank=True)

    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    choices = models.ForeignKey(
        AnswerType, on_delete=models.PROTECT, verbose_name=_("AnswerType"), related_name="questions"
    )
    survey = models.ManyToManyField(
        Survey,
        through='SurveyItem',
        through_fields=('question', 'survey'),
    )

    def save(self, *args, **kwargs):
        if isinstance(type(dict), type(self.choices)):
            self.choices, _ = AnswerType.objects.get_or_create(choices=self.choices)
        super(Question, self).save(*args, **kwargs)



class SurveyItem(MPTTModel):
    order = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        unique_together = ['question', 'survey']

    class MPTTMeta:
        order_insertion_by = ['order']
        
class SurveyItemRecord(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    item = models.ForeignKey(SurveyItem, on_delete=models.PROTECT)
    answer = JSONField()

    class Meta:
        unique_together = ['user', 'item']
