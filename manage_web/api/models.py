from time import strftime

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from accounts.models import Reviewer
from api.validators import validate_not_null

import uuid

# Create your models here.

class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address = models.CharField('주소', max_length=50)
    latitude = models.DecimalField('y 좌표', max_digits=10, decimal_places=7, null=True)
    longitude = models.DecimalField('x 좌표', max_digits=10, decimal_places=7, null=True)
    road_address = models.CharField('도로명 주소', max_length=50, blank=True)


    def __str__(self):
        return self.address


def signboard_directory_path(instance, filename):
    return '{0}_{1}/signboard/{2}'.format(
        instance.__str__(), 
        instance.id, 
        filename
    )


class Restaurant(models.Model):
    status_choices = (
        ('Disapproved', 'Disapproved'),
        ('Standby', 'Standby'),
        ('Approved', 'Approved')
    )

    size_choices = (
        ('소', '소'),
        ('중', '중'),
        ('대', '대'),
        ('특대', '특대'),

    )

    restroom_cleanliness_choices = (
        ('High', '상'),
        ('Mid', '중'),
        ('Low', '하'),
    )

    self_service_choices = (
        ('없음', '없음'),
        ('결제', '결제'),
        ('배식', '배식'),
        ('퇴식', '퇴식'),
    )

    restroom_choices = (
        ('없음', '없음'),
        ('내부', '내부'),
        ('외부', '외부'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('음식점 이름', max_length=50)
    branch_name = models.CharField('지점 이름', max_length=30, blank=True)
    address = models.CharField('주소', max_length=50)
    floor = models.IntegerField('층', null=True)
    
    is_restaurant_possible = models.BooleanField(default=False)
    is_bar_possible = models.BooleanField(default=False)
    is_cafe_possible = models.BooleanField(default=False)

    status = models.CharField('상태', max_length=13, choices=status_choices, default='Standby')
    registered_time = models.DateTimeField('등록 시간', auto_now_add=True)
    is_active = models.BooleanField('활성여부', default=True)
    active = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    reviewer = models.ForeignKey(Reviewer, on_delete=models.PROTECT, verbose_name='리뷰어', db_column='reviewer')
    rejected_reason = models.CharField('거절사유', max_length=300, blank=True)

    size = models.CharField('크기', max_length=1, choices=size_choices, blank=True)
    self_service = models.CharField('셀프서비스', max_length=2, blank=True, choices=self_service_choices)
    restroom = models.CharField('화장실', max_length=2, blank=True, choices=restroom_choices)

    is_duplex = models.BooleanField('복층', null=True)
    is_room = models.BooleanField('룸', null=True)    
    is_bar_table = models.BooleanField('바테이블', null=True)
    
    restroom_cleanliness = models.CharField('화장실 청결도', max_length=4, choices=restroom_cleanliness_choices, blank=True)

    image = models.ImageField('간판사진', max_length=255, upload_to=signboard_directory_path)
  

    def image_tag(self):
        # used in the admin site model as a "thumbnail"
        return mark_safe('<img src="{}" width="150" height="150" />'.format(self.image.url))
    

    def __str__(self):
        if self.branch_name == '':
            return self.name
        else:
            return '{0}({1})'.format(self.name, self.branch_name)

    def get_sales_info_id(self):
        return self.salesinfo.id
    
    def is_restaurant_registered(self):
        if Review.objects.filter(restaurant=self, type='RSTRT').exists():
            return True
        else:
            return False

    def is_bar_registered(self):
        if Review.objects.filter(restaurant=self, type='BAR').exists():
            return True
        else:
            return False

    def is_cafe_registered(self):
        if Review.objects.filter(restaurant=self, type='CAFE').exists():
            return True
        else:
            return False

    def info_register_time(self):
        pass

    def get_longitude(self):
        try:
            address = Address.objects.get(address=self.address)
            return address.longitude
        except:
            return None
        

    def get_latitude(self):
        try:
            address = Address.objects.get(address=self.address)
            return address.latitude
        except:
            return None

    def get_reviewer_name(self):
        return self.reviewer.__str__()




class Review(models.Model):

    type_choices = (
        ('cafe', 'cafe'),
        ('restaurant', 'restaurant'),
        ('bar', 'bar'),
    )

    status_choices = (
        # ('Deleted', 'Deleted'),
        # ('Writing', 'Writing'),
        ('Modified', 'Modified'),  # 리뷰어 수정
        # ('Deactivated', 'Deactivated'),
        ('Standby', 'Standby'),   # 검토대기
        ('Approved', 'Approved'),   # 승인

    )

    score_choices = (
        (0.5, '0.5'),
        (1.0, '1'),
        (1.5, '1.5'),
        (2.0, '2'),
        (2.5, '2.5'),
        (3.0, '3'),
        (3.5, '3.5'),
        (4.0, '4'),
        (4.5, '4.5'),
        (5.0, '5'),
    )

   
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.SET_NULL, verbose_name='음식점 이름',
        db_column='restaurant', blank=True, null=True)
    register_time = models.DateTimeField('등록 시간', auto_now=True)    # Save 될 때마다 저장
    status = models.CharField('상태', max_length=11, choices=status_choices, default='StandBy')
    type = models.CharField('리뷰 타입', max_length=10, choices=type_choices)
    visit_date = models.DateField('방문 날짜')
    reviewer = models.ForeignKey(Reviewer, on_delete=models.SET_NULL, verbose_name='리뷰어', db_column='reviewer', blank=True, null=True)

    rstrt_overview = models.CharField('음식점 개요', max_length=500)
    rstrt_overview_feedback = models.CharField('음식점 개요 피드백', blank=True, max_length=500)

    rstrt_atmosphere = models.CharField('분위기 설명', max_length=500)
    rstrt_atmosphere_feedback = models.CharField('분위기 설명 피드백', blank=True, max_length=500)

    comment = models.CharField('자유로운 말', max_length=500)
    comment_feedback = models.CharField('자유로운 말 피드백', blank=True, max_length=500)

    flavor_score = models.FloatField('맛점수', blank=True, null=True, choices=score_choices)
    flavor_summary = models.CharField('맛요약', max_length=45)
    flavor_summary_feedback = models.CharField('맛요약 피드백', blank=True, max_length=150)

    atmosphere_score = models.FloatField('분위기 점수', blank=True, null=True, choices=score_choices)
    atmosphere_summary = models.CharField('분위기 요약', max_length=45)
    atmosphere_summary_feedback = models.CharField('분위기 요약 피드백', blank=True, max_length=150)

    efficiency_score = models.FloatField('가성비 점수', blank=True, null=True, choices=score_choices)
    efficiency_summary = models.CharField('가성비 요약', max_length=45)
    efficiency_summary_feedback = models.CharField('가성비 요약 피드백', blank=True, max_length=150)

    summary = models.CharField('한마디', max_length=40)
    summary_feedback = models.CharField('한마디 피드백', max_length=150, blank=True, null=True)

    assessment = models.CharField('평가', max_length=500, blank=True)
    
    menuboard_image_feedback = models.CharField('메뉴판사진 피드백', blank=True, max_length=500)
    interior_image_feedback = models.CharField('매장사진 피드백', blank=True, max_length=500)
    other_image_feedback = models.CharField('기타음식사진 피드백', blank=True, max_length=500)
    pic_feedback = models.CharField('사진 피드백', blank=True, max_length=500)
    total_feedback = models.CharField('전체 피드백', blank=True, max_length=500)


    def __str__(self):
        return self.restaurant.__str__() + ' 리뷰'

    def clean(self):
        # if review type is not possible
        if not getattr(self.restaurant, 'is_{0}_possible'.format(self.type)):
            raise ValidationError(_('선택하신 {0} 유형은 가능한 리뷰 유형이 아닙니다.'.format(self.type)))


    def register_time_formatting(self):
        return self.register_time.strftime('%y.%m.%d %p %I:%M')

    register_time_formatting.short_description = "등록 시간"


    def visit_date_formatting(self):
        return self.register_time.strftime('%y.%m.%d')

    def get_restaurant_name(self):
        return self.restaurant.__str__()

    visit_date_formatting.short_description = "짜 날짜"


class SalesInfo(models.Model):
    parking_lot_choices = (
        ('건물주차장', '건물주차장'),    # 건물주차장
        ('외부주차장', '외부주차장'),  # 외부주차장
        ('없음', '없음'),        # 없음
    )

    price_range_type_choices = (
        ('일반', '일반'),     # 일반
        ('중량', '즁량'),     # 중량
        ('인분', '인분'),     # 인분
        ('크기', '크기'),           # 크기
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = PhoneNumberField()
    
    is_group_reservation = models.BooleanField('단체예약', null=True, validators=[validate_not_null])
    group_reservation_maximum = models.IntegerField('단체예약최대인원', blank=True, null=True)   
    parking_lot = models.CharField('주차장', max_length=7, choices=parking_lot_choices)
    parking_lot_info = models.CharField('주차장위치비용정보', max_length=100, blank=True)
    is_valet_parking = models.BooleanField('발렛파킹', null=True, validators=[validate_not_null])
    valet_parking_price = models.CharField('발렛파킹비용정보', max_length=100, blank=True)
    is_package = models.BooleanField('포장', null=True, validators=[validate_not_null])
    is_delivery = models.BooleanField('배달', null=True, validators=[validate_not_null])
    is_corkage = models.BooleanField('콜키지', null=True, validators=[validate_not_null])
    corkage_price = models.CharField('콜키지비용정보', max_length=100, blank=True)
    price_range_type = models.CharField('가격대유형', max_length=7, choices=price_range_type_choices)
    price_range_unit = models.CharField('가격대단위', max_length=10)        # 일반일 경우 x, 중량일 경우 g, 인분일 경우 1인분, 크기일 경우 특대
    price_range = models.PositiveIntegerField('가격대크기')
    restaurant = models.OneToOneField(Restaurant, models.CASCADE, verbose_name='음식점',
        null=True, related_name='sales_info')


    def clean(self):
        pass

class DaysOff(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sales_info = models.OneToOneField(SalesInfo, models.CASCADE, related_name='days_off')
    monday = models.BooleanField()
    tuesday = models.BooleanField()
    wednesday = models.BooleanField()
    thursday = models.BooleanField()
    friday = models.BooleanField()
    saturday = models.BooleanField()
    sunday = models.BooleanField()
    


class Days24h(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sales_info = models.OneToOneField(SalesInfo, models.CASCADE, related_name='days_24h')
    monday = models.BooleanField()
    tuesday = models.BooleanField()
    wednesday = models.BooleanField()
    thursday = models.BooleanField()
    friday = models.BooleanField()
    saturday = models.BooleanField()
    sunday = models.BooleanField()


class BreakTime(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    monday_start = models.TimeField(null=True)
    monday_end = models.TimeField(null=True)
    tuesday_start = models.TimeField(null=True)
    tuesday_end = models.TimeField(null=True)
    wednesday_start = models.TimeField(null=True)
    wednesday_end = models.TimeField(null=True)
    thursday_start = models.TimeField(null=True)
    thursday_end = models.TimeField(null=True)
    friday_start = models.TimeField(null=True)
    friday_end = models.TimeField(null=True)
    saturday_start = models.TimeField(null=True)
    saturday_end = models.TimeField(null=True)
    sunday_start = models.TimeField(null=True)
    sunday_end = models.TimeField(null=True)
    sales_info = models.OneToOneField(SalesInfo, models.CASCADE, related_name='break_time')

    


class BusinessHour(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    monday_start = models.TimeField(null=True)
    monday_end = models.TimeField(null=True)
    tuesday_start = models.TimeField(null=True)
    tuesday_end = models.TimeField(null=True)
    wednesday_start = models.TimeField(null=True)
    wednesday_end = models.TimeField(null=True)
    thursday_start = models.TimeField(null=True)
    thursday_end = models.TimeField(null=True)
    friday_start = models.TimeField(null=True)
    friday_end = models.TimeField(null=True)
    saturday_start = models.TimeField(null=True)
    saturday_end = models.TimeField(null=True)
    sunday_start = models.TimeField(null=True)
    sunday_end = models.TimeField(null=True)
    sales_info = models.OneToOneField(SalesInfo, models.CASCADE, related_name='business_hour')


class LastOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    monday = models.TimeField(null=True)
    tuesday = models.TimeField(null=True)
    wednesday = models.TimeField(null=True)
    thursday = models.TimeField(null=True)
    friday = models.TimeField(null=True)
    saturday = models.TimeField(null=True)
    sunday = models.TimeField(null=True)
    sales_info = models.OneToOneField(SalesInfo, models.CASCADE, related_name='last_order')

  


class Menu(models.Model):

    type_choices = (
        ('일반', '일반 메뉴'),
        ('세트', '세트 메뉴'),
        ('코스', '코스 메뉴'),
        ('뷔페', '뷔페 메뉴'),
    )

    price_type_choices = (
        ('일반', '일반'),
        ('인분', '인분'),
        ('크기', '크기'),
    )

    score_choices = (
        (0.5, '0.5'),
        (1.0, '1.0'),
        (1.5, '1.5'),
        (2.0, '2.0'),
        (2.5, '2.5'),
        (3.0, '3.0'),
        (3.5, '3.5'),
        (4.0, '4.0'),
        (4.5, '4.5'),
        (5.0, '5.0'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    review = models.ForeignKey(Review, models.CASCADE, null=True, verbose_name='리뷰')
    type = models.CharField('메뉴유형', max_length=2, choices=type_choices)
    name = models.CharField('메뉴이름', max_length=50)
    description = models.CharField('메뉴리뷰', max_length=500)
    description_feedback = models.CharField('메뉴리뷰 피드백', max_length=500, blank=True)
    price_type = models.CharField('가격유형', max_length=2,choices=price_type_choices, blank=True)
    price_unit = models.CharField('가격단위', max_length=10)
    price = models.PositiveIntegerField('가격 크기', null=True)
    star_rating = models.FloatField('별점', null=True, choices=score_choices)
    menu_image_feedback = models.CharField('메뉴사진 피드백', max_length=500, blank=True)
   

    def __str__(self):
        return self.name


class Food(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    menu = models.ForeignKey(Menu, models.CASCADE, null=True, verbose_name='메뉴')
    name = models.CharField('음식 이름', max_length=50)
    description = models.CharField('음식 설명', max_length=500)
    description_feedback = models.CharField('음식 설명 피드백', max_length=500, blank=True)


    def __str__(self):
        return self.name


class LargeCategory(models.Model):
    
    category_choices = (
        ('한식','한식'),
        ('중식','중식'),
        ('일식','일식'),
        ('분식', '분식'),
        ('세계음식','세계음식'),
        ('양식','양식'),
        ('카페/베이커리','카페/베이커리'),
        ('뷔페/무한리필','뷔페/무한리필'),
        ('술집','술집'),
        
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    large_category = models.CharField('대분류', max_length=10, choices=category_choices)
    restaurant = models.ForeignKey(Restaurant, models.CASCADE)





class SmallCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    small_category = models.CharField('소분류', max_length=10)
    restaurant = models.ForeignKey(Restaurant, models.CASCADE)






######################## Handling image model #############################


    


def menu_directory_path(instance, filename):
    return '{0}_{1}/review_{2}/menu_{3}/{4}'.format(
        instance.menu.review.restaurant.__str__(), 
        instance.menu.review.restaurant.id, 
        instance.menu.review.id, 
        instance.menu.id, 
        filename
    )

class MenuImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    menu = models.ForeignKey(Menu, models.CASCADE, verbose_name='메뉴')
    image = models.ImageField('메뉴사진', max_length=255, upload_to=menu_directory_path)



    def image_tag(self):
        # used in the admin site model as a "thumbnail"
        return mark_safe('<img src="{}" width="150" height="150" />'.format(self.image.url))



def menuboard_directory_path(instance, filename):
    return '{0}_{1}/review_{2}/menuboard/{3}'.format(
        instance.review.restaurant.__str__(), 
        instance.review.restaurant.id, 
        instance.review.id, 
        filename
    )

class MenuBoardImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    review = models.ForeignKey(Review, models.CASCADE, verbose_name='리뷰')
    image = models.ImageField('메뉴판사진', max_length=255, upload_to=menuboard_directory_path)


    def image_tag(self):
        # used in the admin site model as a "thumbnail"
        return mark_safe('<img src="{}" width="150" height="150" />'.format(self.image.url))

def interior_directory_path(instance, filename):
    return '{0}_{1}/review_{2}/interior/{3}'.format(
        instance.review.restaurant.__str__(), 
        instance.review.restaurant.id, 
        instance.review.id, 
        filename
    )

class InteriorImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    review = models.ForeignKey(Review, models.CASCADE, verbose_name='리뷰')
    image = models.ImageField('내부사진', max_length=255, upload_to=interior_directory_path)

  

    def image_tag(self):
        # used in the admin site model as a "thumbnail"
        return mark_safe('<img src="{}" width="150" height="150" />'.format(self.image.url))




def other_directory_path(instance, filename):
    return '{0}_{1}/review_{2}/other/{3}'.format(
        instance.review.restaurant.__str__(), 
        instance.review.restaurant.id, 
        instance.review.id, 
        filename
    )

class OtherImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    review = models.ForeignKey(Review, models.CASCADE, verbose_name='리뷰')
    image = models.ImageField('기타사진', max_length=255, upload_to=other_directory_path)



    def image_tag(self):
        # used in the admin site model as a "thumbnail"
        return mark_safe('<img src="{}" width="150" height="150" />'.format(self.image.url))