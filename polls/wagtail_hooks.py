from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register, ModelAdminGroup)
from .models import Question, Choice


class QuestionsModelAdmin(ModelAdmin):
    model = Question
    menu_label = 'Question Model'  # ditch this to use verbose_name_plural from model
    menu_icon = 'date'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('question_text', 'pub_date')
    list_filter = ('question_text', 'pub_date')
    search_fields = ('question_text',)

class ChoicesModelAdmin(ModelAdmin):
    model = Choice
    menu_label = 'Choice Model'
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('question', 'choice_text')
    list_filter = ('question', 'choice_text')
    search_fields = ('question',)

class QuestionAdminGroup(ModelAdminGroup):
    menu_label = 'My App'
    menu_icon = 'folder-open-inverse'  # change as required
    menu_order = 200
    items = (QuestionsModelAdmin, ChoicesModelAdmin)


# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(QuestionAdminGroup)