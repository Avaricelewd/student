from django.shortcuts import render,reverse
from math import ceil
from django.db.models import Max
from student import models
from .models import Student,Class  # from .models import *
# Create your views here.
import xlwt
from io import BytesIO
from django_student import settings
import os
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect,HttpResponse


def index(request):
    """获取学生列表"""
    # 计算分页索引
    page_no = int(request.GET.get('page_no',1))
    page_size = int(request.GET.get('page_size',3))
    start_index = (page_no - 1) * page_size
    end_index = page_no * page_size

    # todo 多条件过滤
    # name_like="明"  gender="女"
    # Student.object.filter().count()

    # 查询
    rows_amount = Student.objects.all().count()
    # print(rows_amount)
    # page_amount = (rows_amount-0.1) // page_size + 1    # 9条/每页3条  整除时导致总页数多算了1， 解决方法一  行数-0.1 再除； 方法二ceil返回大于等于整数
    page_amount = ceil(rows_amount / page_size)
    student_list = Student.objects.all().order_by('no')[start_index: end_index]
    page_amount_list = [i for  i in range(page_amount)]   # [0,1,2]

    if page_no > page_amount :
        page_no=page_amount
        # error_message = '请求页码数超过最大页码'
    # e = error_message
    context={
        "student_list":student_list,
        'page_amount_list':page_amount_list,
        'page_no':page_no,
        # 'error_message':e,
        'page_previous' : page_no -1 or 1 ,
        'page_nex' : page_no +1 ,
    }
    return render(request,'student/index.html',context)

def select(request):
    # 模糊查询
    if request.method == 'GET':
        return render(request,'student/select.html',context={})
    if request.method == 'POST':
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        if gender == '未选择':
            gender = '0'
        elif gender == '男':
            gender = '1'
        elif gender  == '女':
            gender = '2'
        elif gender == '保密':
            gender = '3'
        if name!= '' and gender !='':
            student_list = Student.objects.filter(name__icontains= name,gender=gender)
        elif name == '' and gender != '':
            student_list = Student.objects.filter(gender=gender)
        elif name != '' and gender == '':
            student_list = Student.objects.filter(name__icontains=name)
        context = {
            'student_list':student_list,
        }
        return render(request,'student/select.html',context)





def add(request):
    max_no = Student.objects.aggregate(Max('no'))
    next_no = max_no['no__max'] + 1
    context = {
        'next_no':next_no,
    }
    return render(request,'student/add.html',context)

def do_add(request):
    assert request.method == 'POST'
    no = request.POST['no']
    name = request.POST['name']
    age = request.POST['age']
    gender = request.POST['gender']
    phone = request.POST['phone']
    avatar = request.FILES.get('avatar')

    # 存储图片
    # files = request.FILES  # 文件img存储字段，open打开
    # file = files['avatar']
    # _file_name = file.name
    # _upload_to = Student.avatar.field.upload_to
    # avatar = _avatar_db_path = os.path.join(_upload_to,_file_name)
    models.Student.objects.create(no=no,name=name,age=age,gender=gender,phone=phone,avatar=avatar)
    context = {}
    # if no < 0 or no > 10000:
    #     error_message = '输入非法，学号范围为1-9999'
    # if Student.objects.filter(no=no).exists():
    #     max_no = Student.objects.aggregate(Max('no'))['max__no']
    #     error_message = f'学号已存在，目前最大学号为{max_no},建议学号设置为{max_no+1}。'
    # if gender not in [i[0] for i in Student.GENDER_CHOICES]:
    #     error_message = '性别可选值不正确'
    # if  error_message :
    #     context = {
    #         'error_message': error_message
    #     }
    return render(request,'student/success.html',context)

def update(request,id):
    student= Student.objects.get(id=id)
    text = Student.objects.filter(id=student.id)
    context = {
        "students":student,
        'stu':text,
    }
    return render(request,'student/update.html',context=context)

def do_update(request,id):
    assert request.method == 'POST'
    no = request.POST['no']
    name = request.POST['name']
    age = request.POST['age']
    gender = request.POST['gender']
    phone = request.POST['phone']
    avatar = request.FILES.get('avatar')
    student = Student.objects.get(id=id)
    student.no = no
    student.name = name
    student.age = age
    student.gender = gender
    student.phone = phone
    student.avatar = avatar
    student.save()
    return render(request, 'student/do_update.html', context={})

def delete(request,id):
    student = Student.objects.filter(id=id).delete()
    return render(request, 'student/delete.html')


def export_excel(request):
    """导出所有学生信息到excel文件"""
    # 设置HTTPResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')
    # 定义表名字
    response['Content-Disposition'] = 'attachment;filename=student.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    sheet = wb.add_sheet('student-order')
    # 写入文件标题
    sheet.write(0,0,'学号')
    sheet.write(0,1,'姓名')
    sheet.write(0,2,'年龄')
    sheet.write(0,3,'性别')
    sheet.write(0,4,'电话号码')
    # sheet.write(0,6,'头像')
    sheet.write(0,5,'加入时间')
    # 写入数据
    data_row = 1
    for i in Student.objects.all():
        join_time = i.join_time.strftime('%Y-%m-%d')[:10]
        # print(join_time)
        sheet.write(data_row,5,join_time)
        sheet.write(data_row,0,i.no)
        sheet.write(data_row,1,i.name)
        sheet.write(data_row,2,i.age)
        sheet.write(data_row,3,i.gender)
        sheet.write(data_row,4,i.phone)
        data_row = data_row +1
    # 写到IO
    output = BytesIO()
    wb.save(output)
    # 重新定位到开始
    output.seek(0)
    response.write(output.getvalue())
    return response


def api_index(request):
    """

    :param request:
    :return:
    """
    pass


# def cloth_sale_line(request):
#     # 后端渲染。 缺点不适合做动态图
#     #获取数据。 请求其他接口读数据库
#     #拼前端表格所需变量



    # 数据库查询查询学生信息
    # 数据拼成二维数组（第一行为字段名，后面的数据行，（选做）合并前两行、填充背景色和修改字体字号）
    # save(data.after="media/download/student_info.xlsx")
    # redirect(to="域名/media/download/student_info.xlsx")















# SELECT * from student_student LIMIT 0,3;   -- 学生1到学生3（包含3）
# SELECT * from student_student LIMIT 1,3;    --学生2到4
# -- limit跟python中的列表切片很像但参数含义不一样。 limit  1,3  下标（从0开始计第一行)1, 3 表示向后取的行数
# SELECT * from student_student LIMIT 6,3;
# SELECT  count(id) as amount from student_student;  --计算总行数

# page_no 第几页  page_size  一页显示几条 page_amount 总数据个数
#   1                   10
#  SELECT * from student_student LIMIT 0,{page_size};
# 第1页  每页10条                             0   10
# 第2页                                      10   10
#                                            20   10
#                                           start_index =  {page_no-1}*page_size
# 总页数    总行除以每页数向上取整             page_amount//page_size+1

# student_list = Student.objects.all().order_by('no')[1: 3]
#           start_index =  {page_no-1}*page_size
#           end_index = page_no * page_size

