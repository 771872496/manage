from django.db import models


class Ltt(models.Model):
    c = models.ForeignKey('Class', models.CASCADE, related_name='Class')
    k = models.ForeignKey('Kind', models.CASCADE, related_name='Kind')
    p = models.ForeignKey('Project', models.CASCADE, related_name='project')
    ltt_id = models.CharField(max_length=200, blank=True, null=True)
    sn = models.CharField(max_length=1000)
    pn = models.CharField(max_length=200)
    pn_desc = models.CharField(max_length=1000)
    put_time = models.DateField(blank=True, null=True)
    out_time = models.DateField(blank=True, null=True)
    execute_user = models.CharField(max_length=100)
    start_time = models.DateField(blank=True, null=True)
    over_time = models.DateField(blank=True, null=True)
    result = models.CharField(max_length=200)
    log = models.FileField(upload_to='l_log', blank=True, null=True)
    remark = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'LTT'


class Class(models.Model):
    c_name = models.CharField(max_length=100)

    def __str__(self):
        return self.c_name

    class Meta:
        db_table = 'class'


class Kind(models.Model):
    k_name = models.CharField(max_length=100)


    def __str__(self):
        return self.k_name

    class Meta:
        db_table = 'kind'


class Project(models.Model):
    p_name = models.CharField(max_length=200)

    def __str__(self):
        return self.p_name

    class Meta:
        db_table = 'project'
