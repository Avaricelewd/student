from django.db import models


# Create your models here.

class Student(models.Model):
    GENDER_CHOICES = (
        (0,'未选择'),
        (1,'男'),
        (2,'女'),
        (3,'保密'),
    )
    no = models.IntegerField(verbose_name='学号',unique=True)
    name = models.CharField(verbose_name='姓名',max_length=20)
    age = models.PositiveIntegerField(verbose_name='年龄')
    gender = models.SmallIntegerField(verbose_name='性别',choices=GENDER_CHOICES,default=0)
    phone = models.CharField(verbose_name='电话号码',null=True,blank=True,max_length=50)
    avatar = models.ImageField(verbose_name='头像',upload_to='image/avatar')
    join_time = models.DateTimeField(verbose_name='加入时间',auto_now_add=True)
    last_modified_time = models.DateTimeField(verbose_name='上次修改时间', auto_now=True)

    # 初中生，班级对学生一对多关系，外键。  大学生换教室 多对多
    # class_ = models.ForeignKey(to='student.Class',on_delete=models.SET_NULL)
    # classes = models.ManyToManyField(to='student.Class')
    def __str__(self):
        return self.name

    # choices属性，前台取值  stu.get_field_display  原理写法
    # @property
    # def get_gender_display(self):
    #     for index,item in enumerate(self.GENDER_CHOICES):
    #         if item[0] == self.gender:
    #             value = item[1]
    #     return value

class Class(models.Model):
    GRADE_CHOICES = (
        (1,'小学一年级'),
        (2,'小学二年级'),
        (3,'小学三年级'),
        (4,'小学四年级'),
        (5,'小学五年级'),
        (6,'小学六年级'),
        (7,'初中一年级'),
    )
    no = models.IntegerField(verbose_name='班级号', unique=True)
    name = models.CharField(verbose_name='班级名', max_length=20)
    grade = models.SmallIntegerField(verbose_name='年级',choices=GRADE_CHOICES)
    capacity = models.IntegerField('容纳人数')
    address = models.CharField(verbose_name='班级位置',max_length=100)
    students = models.ManyToManyField(to='student.Student')







# question.choice_set  这种由一查多的思维跟原始sql相反，反向查询
# django manytomany 报错 reversename clish，反向查询名字冲突。结论 只需在一张表中写多对多字段

# 创建数据库，字段长度事先定义，不能太短存不进去，不能太长浪费空间age年龄可以small int，一个字节，整数范围-127到127。如果正整数0-255
# sql：create table name()
#      age Integer unsigned
# )


# 字段类默认不允许不插入空数据。如果某个字段可选是否插入数据，设置null和blank为True
# phone = models.CharField(verbose_name='电话号码',null=True,blank=True)

#
#  gender = models.SmallIntegerField(verbose_name='性别',choices=GENDER_CHOICES,