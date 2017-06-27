# coding:utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse
from forms import LoginForm, RegisterForm, FileForm, BulletinForm
from . import utils
import xlrd
from openpyxl.reader.excel import load_workbook
from django.db import models
from users import models
import datetime
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
import json

# Create your views here.
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        publisher = utils.auth_publisher(form)
        if publisher:
            request.session['islogin'] = True
            request.session['loginname'] = form.cleaned_data['loginname']
            request.session['publisher_id'] = publisher[0].id_adminpublisher
            request.session['hospital_id'] = publisher[0].id_hospital_id
            request.session.set_expiry(3600)
            return redirect('/publisher')
        else:
            form = LoginForm()
            return render(request, 'publisher/login.html', {'form': form, 'error_message': '用户名或密码不正确'})
    else:
        form = LoginForm()
        return render(request, 'publisher/login.html', {'form': form})


def logout(request):
    request.session.clear()
    return redirect('/publisher/login/')


def success(request):
    return render(request, 'publisher/regsuccess.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data['password'] == form.cleaned_data['second_password']:
                form = RegisterForm()
                return render(request, 'publisher/register.html', {'form': form, 'error_message': '两次密码输入不一致!'})
            elif utils.publisher_exists(form.cleaned_data['loginname']):
                return render(request, 'publisher/register.html', {'form': form, 'error_message': '用户名已存在!'})
            else:
                utils.add_publisher(form)
                return render(request, 'publisher/regsuccess.html')
        else:
            form = RegisterForm()
            return render(request, 'publisher/register.html', {'form': form, 'error_message': '请输入正确信息!'})
    else:
        form = RegisterForm()
        return render(request, 'publisher/register.html', {'form': form})


def index(request):
    session = request.session
    islogin = session.get('islogin', False)
    if islogin:
        bulletins = utils.select_all_bulletin(request.session['hospital_id'])
        if not bulletins:
            return render(request, 'publisher/index.html', {'loginname': session['loginname'], 'message': '尚未发布任何预约信息！'})
        return render(request, 'publisher/index.html', {'loginname': session['loginname'], 'bulletins': bulletins})
    else:
        return redirect('/publisher/login/')


#修改预约信息
def alter_bulletin(request):
    if request.method == 'POST':
        session = request.session
        form = BulletinForm(request.POST, hospital_id=session['hospital_id'])
        if form.is_valid():
            utils.alter_bulletin(form, session)
            return redirect('/publisher/')
    else:
        session = request.session
        session['id_bulletin'] = request.GET.get('id_bulletin',-1)
        fee = request.GET.get('fee', -1)
        availabletime = request.GET.get('availabletime', -1)
        countavailable = request.GET.get('countavailable', -1)
        countoccupied = request.GET.get('countoccupied', -1)
        department = request.GET.get('department',-1)
        doctor = request.GET.get('doctor',-1)
        form = BulletinForm(hospital_id=session['hospital_id'])
        return render(request, 'publisher/bulletin.html', {'loginname': session['loginname'],
                                                           'form': form,
                                                          'fee': fee,
                                                          'availabletime': availabletime,
                                                          'countavailable': countavailable,
                                                          'countoccupied': countoccupied,
                                                          'department': department,
                                                          'doctor': doctor,
                                                          'doctor_department': json.dumps(utils.get_doctor_department(
                                                               session['hospital_id']))
                                                           })


# 删除预约信息
def delete_bulletin(request, bulletin_id):
    models.Bulletin.objects.get(pk=bulletin_id).delete()
    return redirect('/publisher')


# 发布预约信息
def create_bulletin(request):
    session = request.session
    islogin = session.get('islogin', False)
    if not islogin:
        return redirect('/publisher/login')
    if request.method == 'POST':
        session = request.session
        form = BulletinForm(request.POST, hospital_id=session['hospital_id'])
        if form.is_valid():
            utils.create_bulletin(form,session)
            return redirect('/publisher/')
        else:
            error_message = '您填写的信息有错误，请重新填写！'
            return render(request, 'publisher/bulletin.html',
                          {'loginname': request.session['loginname'],
                           'form': form, 'error_message': error_message,
                           'doctor_department': json.dumps(utils.get_doctor_department(
                               session['hospital_id']))
                           })
    else:
        form= BulletinForm(hospital_id=session['hospital_id'])
        return render(request, 'publisher/bulletin.html',
                      {'loginname': request.session['loginname'],
                       'form': form,
                       'doctor_department': json.dumps(utils.get_doctor_department(session['hospital_id']))
                     })


def batch_import_bulletin_by_excel(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            if request.FILES['filefield'].name.split('.')[-1] == 'xlsx':
                try:
                    utils.handle_uploaded_file(request, f=request.FILES['filefield'])
                except ObjectDoesNotExist, e:
                    error_message = '科室和医生组合不存在，请检查所上传表格内容后重新上传'
                    return render(request, 'publisher/file.html',
                                  {'form': form, 'error_message': error_message,
                                   'loginname': request.session['loginname']})
                return render(request, 'publisher/file.html',
                              {'form': form, 'error_message': '上传成功！',
                               'loginname': request.session['loginname']})
            else:
                error_message = '文件格式错误，请上传Excel文件（.xlsl)'
                form = FileForm()
                return render(request, 'publisher/file.html', {'form': form, 'error_message': error_message, 'loginname': request.session['loginname']})
    else:
        form = FileForm()
        return render(request, 'publisher/file.html', {'form': form, 'loginname': request.session['loginname']})
