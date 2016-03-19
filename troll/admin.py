from django.contrib import admin
from django.apps import apps

app = apps.get_app_config('troll')


class IdeaAdmin(admin.ModelAdmin):
    list_display = ('name', 'valid', 'likes')
    list_filter = ('name', 'valid', 'likes')


for model_name, model in app.models.items():
    exclude = ['baseuser_groups', 'baseuser_user_permissions']
    if model_name == 'idea':
        admin.site.register(model, IdeaAdmin)
    elif model_name not in exclude:
        admin.site.register(model)
