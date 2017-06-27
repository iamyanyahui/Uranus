from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse('teacher page')


#在线预览课程资源
def preview_source_online(request):
    return render(request, 'teacher/sourcePreview.html')


def view_word(request):
    pass


#设置分数和评论
def set_grade_and_comments(request):
    pass


#下载学生作业
def download_stu_homework(request):
    pass


#设置作业占分比例
def set_rate_of_homework(request):
    pass


#生成个人得分表
def generate_stu_score_table(request):
    pass


#生成小组最终成绩
def generate_group_score_table(request):
    pass
