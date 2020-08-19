from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from django.utils.translation import ugettext_lazy as _
from typedmodels.models import TypedModel
from mptt.models import MPTTModel, TreeForeignKey

User = get_user_model()


class Survey(models.Model):
    name = models.CharField(max_length=200)
    version = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        unique_together = ['name', 'version']


class Category(models.Model):
    name = models.CharField(max_length=200)


class Question(TypedModel):
    text = models.TextField(_("Text"))
    choices = JSONField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, verbose_name=_("Category"), related_name="questions"
    )
    survey = models.ManyToManyField(
        Survey,
        through='SurveyItem',
        through_fields=('question', 'survey'),
    )


class NumberRangeQuestion(Question):
    pass


class MultipleChoiceQuestion(Question):
    pass


class BooleanQuestion(Question):
    pass


class SurveyItem(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)


class SurveyItemRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    item = models.ForeignKey(SurveyItem, on_delete=models.PROTECT)
    answer = JSONField()
