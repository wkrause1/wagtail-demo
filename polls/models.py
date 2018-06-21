import datetime
from django import forms
from django.utils import timezone
from django.http import HttpResponse
from django.db import models
from django.template.response import TemplateResponse

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.core.models import Page
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel



# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now-datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class PollPage(RoutablePageMixin, Page):
    questions = ParentalManyToManyField(Question, blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('questions', widget=forms.CheckboxSelectMultiple),
    ]
    @route(r'^$')
    def poll_view(self, request):
        if (request.method == "GET"):
            return TemplateResponse(
                request,
                self.get_template(request),
                self.get_context(request)
            )
        if (request.method == "POST"):
            for key in request.POST:
                if 'answer_' in key:
                    choice = Choice.objects.get(pk=request.POST[key])
                    choice.votes += 1
                    choice.save()
                    print('{}: {}'.format(choice, choice.votes))
            return HttpResponse("Thanks!")

       

