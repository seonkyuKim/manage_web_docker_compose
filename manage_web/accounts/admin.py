from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Reviewer, Editor

import nested_admin

# Register your models here.

class ReviewerAdmin(nested_admin.NestedModelAdmin):
    model = Reviewer
    exclude = ()
    readonly_fields = ['image_tag', ]


class ReviewerInline(nested_admin.NestedStackedInline):
    model = Reviewer
    exclude = ()
    extra = 0
    readonly_fields = ['image_tag', ]

class EditorAdmin(nested_admin.NestedModelAdmin):
    model = Editor
    exclude = ()
    readonly_fields = ['image_tag', ]
    inlines = [ReviewerInline, ]

admin.site.register(User, UserAdmin)
admin.site.register(Editor, EditorAdmin)
admin.site.register(Reviewer, ReviewerAdmin)



