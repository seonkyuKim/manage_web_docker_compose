from django.contrib import admin

import nested_admin

from .models import (
    Restaurant, Review, Menu, Food, LargeCategory, SmallCategory,
    SalesInfo, BreakTime, LastOrder, BusinessHour, Address, Days24h, DaysOff,
    MenuImage, MenuBoardImage, InteriorImage, OtherImage
)

################### Image model #####################


# MenuImage belongs to Menu
class MenuImageInline(nested_admin.NestedStackedInline):
    model = MenuImage
    fields = ('image', 'image_tag',)
    readonly_fields = ('image_tag', )
    extra = 0

# These belong to Review
class MenuBoardImageInline(nested_admin.NestedStackedInline):
    model = MenuBoardImage
    fields = ('image', 'image_tag',)
    readonly_fields = ('image_tag', )
    extra = 0

class InteriorImageInline(nested_admin.NestedStackedInline):
    model = InteriorImage
    fields = ('image', 'image_tag',)
    readonly_fields = ('image_tag', )
    extra = 0

class OtherImageInline(nested_admin.NestedStackedInline):
    model = OtherImage
    fields = ('image', 'image_tag',)
    readonly_fields = ('image_tag', )
    extra = 0


#################### Review model ###################


class FoodInline(nested_admin.NestedStackedInline):
    model = Food
    exclude= ()
    extra = 0


class MenuInline(nested_admin.NestedStackedInline):
    model = Menu
    exclude= ()
 
    inlines = [MenuImageInline, FoodInline, ]
    extra = 0


class ReviewInline(nested_admin.NestedStackedInline):
    model = Review
    exclude = ()
    
    inlines = [MenuInline, MenuBoardImageInline, InteriorImageInline, OtherImageInline]
    extra = 0


class ReviewAdmin(nested_admin.NestedModelAdmin):
    model = Review
    exclude = ()

    inlines = [MenuInline, MenuBoardImageInline, InteriorImageInline, OtherImageInline]
    extra = 0


################## Restaurant Sales info #####################

class Days24hInline(nested_admin.NestedStackedInline):
    model = Days24h
    exclude = []
    extra = 0

class DaysOffInline(nested_admin.NestedStackedInline):
    model = DaysOff
    exclude = []
    extra = 0

class BreakTimeInline(nested_admin.NestedStackedInline):
    model = BreakTime
    exclude = []
    extra = 0

class BusinessHourInline(nested_admin.NestedStackedInline):
    model = BusinessHour
    exclude = []
    extra = 0

class LastOrderHourInline(nested_admin.NestedStackedInline):
    model = LastOrder
    exclude = []
    extra = 0


class SalesInfoInline(nested_admin.NestedStackedInline):
    model = SalesInfo
    exclude = []
    extra = 0
    inlines = [BreakTimeInline, BusinessHourInline, LastOrderHourInline, Days24hInline, DaysOffInline]

#################### Restaurant model ########################

class LargeCategoryInline(nested_admin.NestedStackedInline):
    model = LargeCategory
    exclude = []
    extra = 0
    
class SmallCategoryInline(nested_admin.NestedStackedInline):
    model = SmallCategory
    exclude = []
    extra = 0


class RestaurantAdmin(nested_admin.NestedModelAdmin):
    search_fields = ['name']
    exclude = ()
    inlines = [

        ReviewInline, 
        SalesInfoInline, 
        LargeCategoryInline, 
        SmallCategoryInline, 
    ]
    readonly_fields = ('image_tag', )



admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Address)