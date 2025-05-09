from roles.models import Permission, Role, Role_Permission, Module
from utils.models import Gender, Customer_Type, City, Court, Litigation_Type
from cases.models import Company_Representative
from judgements.models import Execution_State, Execution_Type
from session.models import ConsultationType
from agencies.models import AgencyType


permissions_list = [
    {'module':'المستخدمين', 'key':'permissions.users.view', 'label':'عرض جميع المستخدمين'},
    {'module':'المستخدمين', 'key':'permissions.users.add', 'label':'إضافة مستخدم'},
    {'module':'المستخدمين', 'key':'permissions.users.edit', 'label':'تعديل مستخدم'},
    
    {'module':'المحامين', 'key':'permissions.lawyers.view', 'label':'عرض جميع محامين'},
    {'module':'المحامين', 'key':'permissions.lawyers.add', 'label':'إضافة محامي'},
    {'module':'المحامين', 'key':'permissions.lawyers.edit', 'label':'تعديل محامي'},
    
    {'module':'الأدوار', 'key':'permissions.roles.view', 'label':'عرض جميع الأدوار'},
    {'module':'الأدوار', 'key':'permissions.roles.add', 'label':'إضافة دور'},
    {'module':'الأدوار', 'key':'permissions.roles.edit', 'label':'تعديل دور'},
    {'module':'الأدوار', 'key':'permissions.roles.delete', 'label':'حذف دور'},
    {'module':'الأدوار', 'key':'permissions.roles.edit.permissions', 'label':'تعديل صلاحيات دور'},

    {'module':'القضايا', 'key':'permissions.cases.view.all', 'label':'عرض جميع القضايا'},
    {'module':'القضايا', 'key':'permissions.cases.view', 'label':'عرض قضية'},
    {'module':'القضايا', 'key':'permissions.cases.add', 'label':'إضافة قضية'},
    {'module':'القضايا', 'key':'permissions.cases.edit', 'label':'تعديل قضية'},
    {'module':'القضايا', 'key':'permissions.cases.delete', 'label':'حذف قضية'},


    {'module':'الجلسات', 'key':'permissions.sessions.view.all', 'label':'عرض جميع الجلسات'},
    {'module':'الجلسات', 'key':'permissions.sessions.view.weekly', 'label':'عرض الجلسات الأسبوعية'},
    {'module':'الجلسات', 'key':'permissions.sessions.view.mine', 'label':'عرض الجلسات الخاصة بي'},
    {'module':'الجلسات', 'key':'permissions.sessions.add', 'label':'إضافة جلسة'},
    {'module':'الجلسات', 'key':'permissions.sessions.edit', 'label':'تعديل جلسة'},
    {'module':'الجلسات', 'key':'permissions.sessions.delete', 'label':'حذف جلسة'},
    
    {'module':'الإستشارات', 'key':'permissions.consultations.view.all', 'label':'عرض جميع الإستشارات'},
    {'module':'الإستشارات', 'key':'permissions.consultations.view', 'label':'عرض إستشارة'},
    {'module':'الإستشارات', 'key':'permissions.consultations.add', 'label':'إضافة إستشارة'},
    {'module':'الإستشارات', 'key':'permissions.consultations.edit', 'label':'تعديل إستشارة'},

    {'module':'الأحكام', 'key': 'permissions.judgements.view', 'label':'عرض الأحكام'},
    {'module':'الأحكام', 'key': 'permissions.judgements.add', 'label':'إضافة حكم'},
    {'module':'الأحكام', 'key': 'permissions.judgements.edit', 'label':'تعديل حكم'},
    {'module':'الأحكام', 'key': 'permissions.judgements.delete', 'label':'حذف حكم'},

    {'module':'الإعتراضات', 'key': 'permissions.appeals.view', 'label':'عرض الإعتراضات'},
    {'module':'الإعتراضات', 'key': 'permissions.appeals.add', 'label':'إضافة إعتراض'},
    {'module':'الإعتراضات', 'key': 'permissions.appeals.edit', 'label':'تعديل إعتراض'},
    {'module':'الإعتراضات', 'key': 'permissions.appeals.delete', 'label':'حذف إعتراض'},
    
    {'module':'التنفيذات', 'key': 'permissions.executions.view', 'label':'عرض التنفيذات'},
    {'module':'التنفيذات', 'key': 'permissions.executions.add', 'label':'إضافة تنفيذ'},
    {'module':'التنفيذات', 'key': 'permissions.executions.edit', 'label':'تعديل تنفيذ'},
    {'module':'التنفيذات', 'key': 'permissions.executions.delete', 'label':'حذف تنفيذ'},

    {'module':'المدن', 'key':'permissions.cities.view', 'label':'عرض جميع المدن'},
    {'module':'المدن', 'key':'permissions.cities.add', 'label':'إضافة مدينة'},
    {'module':'المدن', 'key':'permissions.cities.edit', 'label':'تعديل مدينة'},
    {'module':'المدن', 'key':'permissions.cities.delete', 'label':'حذف مدينة'},

    {'module':'المحاكم', 'key':'permissions.court.view', 'label':'عرض جميع المحاكم'},
    {'module':'المحاكم', 'key':'permissions.court.add', 'label':'إضافة محكمة'},
    {'module':'المحاكم', 'key':'permissions.court.edit', 'label':'تعديل محكمة'},
    {'module':'المحاكم', 'key':'permissions.court.delete', 'label':'حذف محكمة'},
    
    {'module':'حالات القضايا', 'key':'permissions.state.view', 'label':'عرض جميع حالات القضايا'},
    {'module':'حالات القضايا', 'key':'permissions.state.add', 'label':'إضافة حالة قضية'},
    {'module':'حالات القضايا', 'key':'permissions.state.edit', 'label':'تعديل حالة قضية'},
    {'module':'حالات القضايا', 'key':'permissions.state.delete', 'label':'حذف حالة قضية'},
    
    {'module':'العملاء', 'key':'permissions.customers.view', 'label':'عرض جميع العملاء'},
    {'module':'العملاء', 'key':'permissions.customers.add', 'label':'إضافة عميل'},
    {'module':'العملاء', 'key':'permissions.customers.edit', 'label':'تعديل عميل'},
    {'module':'العملاء', 'key':'permissions.customers.delete', 'label':'حذف عميل'},
    
    {'module':'أنواع القضايا', 'key':'permissions.litigation_type.view', 'label':'عرض جميع أنواع القضايا'},
    {'module':'أنواع القضايا', 'key':'permissions.litigation_type.add', 'label':'إضافة نوع قضية'},
    {'module':'أنواع القضايا', 'key':'permissions.litigation_type.edit', 'label':'تعديل نوع قضية'},
    {'module':'أنواع القضايا', 'key':'permissions.litigation_type.delete', 'label':'حذف نوع قضية'},
    
    
    {'module':'الوكالات', 'key':'permissions.agencies.view', 'label':'عرض الوكالات'},
    {'module':'الوكالات', 'key':'permissions.agencies.add', 'label':'إضافة وكالة'},
    {'module':'الوكالات', 'key':'permissions.agencies.edit', 'label':'تعديل وكالة'},
    {'module':'الوكالات', 'key':'permissions.agencies.delete', 'label':'حذف وكالة'},
    
    

]


from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "seed database for testing and development."


    def handle(self, *args, **options):
        run_seed(self)


def run_seed(self):

    ########################################
    role, _ = Role.objects.get_or_create(name='Admin')
    role.save()

    for per in permissions_list:
        module, _       = Module.objects.get_or_create(name=per['module'])
        permission, _   = Permission.objects.get_or_create(key=per['key'], label=per['label'], module=module)

        Role_Permission.objects.get_or_create(role=role, permission=permission)
    #########################################



    male, _     = Gender.objects.get_or_create(name='Male', ar_name='ذكر')
    female, _   = Gender.objects.get_or_create(name='Female', ar_name='أنثى')

    
    #########################################
    Company_Representative.objects.get_or_create(name='مالك بن دينار', gender=male)
    Company_Representative.objects.get_or_create(name='فاطمة العنزي', gender=female)

    #########################################

    Execution_Type.objects.get_or_create(name='لصالح الشركة', key='in-favor')
    Execution_Type.objects.get_or_create(name='ضد الشركة', key='against')
    Execution_Type.objects.get_or_create(name='استرداد الأصول', key='asset-recovery')
    
    #########################################
    
    Execution_State.objects.get_or_create(name='منتهي بالسداد')
    Execution_State.objects.get_or_create(name='منتهي بعدم السداد')

    #########################################

    ConsultationType.objects.get_or_create(name='إنشاء مذكرة رد')
    ConsultationType.objects.get_or_create(name='مرفقات')
    ConsultationType.objects.get_or_create(name='مراجعة مذكرة رد')
    ConsultationType.objects.get_or_create(name='طلب إستشارة قانونية')

    #########################################

    City.objects.get_or_create(name='الرياض')
    City.objects.get_or_create(name='الخبر')
    City.objects.get_or_create(name='جدة')

    #########################################

    Court.objects.get_or_create(name='العامة') 
    Court.objects.get_or_create(name='الجنائية') 
    Court.objects.get_or_create(name='العامة')

    #########################################
    
    Litigation_Type.objects.get_or_create(name='تزوير') 
    Litigation_Type.objects.get_or_create(name='جنائية') 
    Litigation_Type.objects.get_or_create(name='مالية')

    #########################################
    
    Customer_Type.objects.get_or_create(name='شركة التيسير العربية')
    Customer_Type.objects.get_or_create(name='شركة دلوف للسيارات المحدودة')
    
    #########################################
    
    AgencyType.objects.get_or_create(name='العملاء')
    AgencyType.objects.get_or_create(name='الموظفين')
    AgencyType.objects.get_or_create(name='المكاتب الخارجية')
    
        
        