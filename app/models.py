from django.db import models

# [用户:学生/教师/教务账户]
class User(models.Model):
    username = models.CharField(null=False, unique=True, max_length=32, help_text='学号/工号')
    password = models.CharField(null=False, max_length=64)
    photo = models.FileField(help_text='用于人脸识别的照片')
    classID = models.CharField(max_length=16, help_text='班号')
    ROLE = (
        ('student', '学生'),
        ('teahcer', '教师'),
        ('admin', '教务'),
    )
    role = models.CharField(max_length=16, choices=ROLE, default='学生')
    name = models.CharField(null=False, max_length=32, help_text='实名')
    GENDER = (
        ('male', '男'),
        ('female', '女'),
    )
    gender = models.CharField(max_length=8, choices=GENDER, default='男')
    tel = models.CharField(max_length=11, help_text='电话')
    email = models.CharField(max_length=64)

# [学期]
class Term(models.Model):
    info = models.TextField(help_text='说明性信息')
    year = models.IntegerField()
    SEMESTER = (
        ('spring', '春'),
        ('autumn', '秋'),
    )
    semester = models.CharField(max_length=8, choices=SEMESTER, default='春')
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    # TODO: 周次安排？！！

# [团队元信息]
class TeamMeta(models.Model):
    minNum = models.PositiveSmallIntegerField(default=1)
    maxNum = models.PositiveSmallIntegerField(default=10)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()

# [课程]==[学期]&[团队元信息]
class Course(models.Model):
    term = models.ForeignKey(Term)         # 外键：学期
    teamMeta = models.ForeignKey(TeamMeta)    # 外键：团队元信息
    name = models.CharField(max_length=64)
    info = models.TextField(help_text='课程要求/其他说明')
    syllabus = models.TextField(help_text='课程大纲')
    classroom = models.CharField(max_length=64, help_text='上课地点')
    credit = models.PositiveSmallIntegerField(default=0)
    STATUS = (
        ('unstarted', '未开始'),
        ('ongoing', '正在进行'),
        ('ended', '已结束'),
    )
    status = models.CharField(max_length=16, choices=STATUS, default='未开始')
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()

# <选课>==[课程]&[用户:学生/教师账户]
class Enroll(models.Model):
    course = models.ForeignKey(Course)
    user = models.ForeignKey(User)

# [团队]==[课程]&[用户:学生账户]
class Team(models.Model):
    course = models.ForeignKey(Course)
    name = models.CharField(max_length=32, help_text='取代ID的备用策略')
    STATUS = (
        ('unsubmitted', '未提交'),
        ('auditing', '待审核'),
        ('passed', '已通过'),
        ('rejected', '已驳回')
    )
    status = models.CharField(max_length=16, choices=STATUS, default='未提交')
    info = models.TextField(help_text='通过欢迎信息/驳回理由')

# <团队成员>==[团队]&[用户:学生账户]
class Member(models.Model):
    team = models.ForeignKey(Team)
    user = models.ForeignKey(User)
    ROLE = (
        ('leader', '队长'),
        ('member', '队员'),
    )
    role = models.CharField(max_length=16, choices=ROLE, default='队员')
    contribution = models.FloatField(help_text='成员贡献度:0.4~1.2')

# [作业任务]~~<附件>
class WorkMeta(models.Model):
    user = models.ForeignKey(User, help_text='发布者:教师')
    content = models.TextField()
    proportion = models.FloatField(help_text='总分折算占比:0.0~1.0')
    submits = models.SmallIntegerField(default=-1, help_text='可提交次数，默认-1为无限')
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()

# [作业提交]~~<附件>
class Work(models.Model):
    workMeta = models.ForeignKey(WorkMeta, help_text='作业任务元信息')
    team = models.ForeignKey(Team, help_text='提交者:团队')
    content = models.TextField()
    review = models.TextField(help_text='教师简评')
    score = models.FloatField(help_text='得分: 0.0~10.0')

# [资源文件]
class File(models.Model):
    user = models.ForeignKey(User, help_text='上传者')
    file = models.FileField()
    path = models.FilePathField()
    TYPE = (
        ('text', '文本'),
        ('document', '文档'),
        ('media', '视频'),
    )
    type = models.CharField(max_length=16, choices=TYPE, default='作业任务')

# <附件>==[作业任务|作业提交]&[资源文件]
class Attachment(models.Model):
    file = models.ForeignKey(File)
    workMeta = models.ForeignKey(WorkMeta)
    work = models.ForeignKey(Work)
    TYPE = (
        ('workmeta', '作业任务'),
        ('work', '作业提交'),
    )
    type = models.CharField(max_length=16, choices=TYPE, default='作业任务')

# [日志]
class Log(models.Model):
    user = models.ForeignKey(User, help_text='操作员')
    event = models.TextField(help_text='日志事件记录')
    time = models.DateTimeField()