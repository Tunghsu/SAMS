#coding=utf-8
from django.db import models

# Create your models here.

class Administrator(models.Model):
	def __unicode__(self):
			return self.title
	aID = models.IntegerField(primary_key=True)
	aName =  models.CharField(max_length=50)
	aPasswd = models.CharField(max_length=30)
	aMail = models.EmailField(max_length=75)
	aPriv = models.IntegerField()

class Teacher(models.Model):
	def __unicode__(self):
			return self.title
	tID = models.IntegerField(primary_key=True)
	tName =  models.CharField(max_length=50)
	tPasswd = models.CharField(max_length=30)
	tMail = models.EmailField(max_length=75)
	tPriv = models.IntegerField()

class Student(models.Model):
	def __unicode__(self):
			return self.title
	sID = models.IntegerField(primary_key=True)
	sName =  models.CharField(max_length=50)
	sPasswd = models.CharField(max_length=30)
	sMail = models.EmailField(max_length=75)
	sNum = models.CharField(max_length=50)
	sAffi = models.CharField(max_length=75)

class Course(models.Model):
	def __unicode__(self):
			return self.title
	cID = models.IntegerField(primary_key=True)
	cFileType = models.CharField(max_length=50)
	cName = models.CharField(max_length=50)

class Assignment(models.Model):
	def __unicode__(self):
			return self.title
	asID = models.IntegerField(primary_key=True)
	asTXT = models.TextField()
	clID = models.IntegerField()
	asClID = models.IntegerField()
	asDate = models.DateTimeField(auto_now=True)
	asExpire = models.DateTimeField(auto_now=False)
	asFinishPopu = models.IntegerField()

class AssignmentFile(models.Model):
	def __unicode__(self):
			return self.title
	asfID = models.IntegerField(primary_key=True)
	asID = models.IntegerField()
	asfType = models.CharField(max_length=50)
	asFile = models.FileField(upload_to = 'assignment')
	sID = models.IntegerField()
	asfDate = models.DateTimeField(auto_now=True)
	asfMark = models.IntegerField()
	asfComment =  models.TextField()
	
class Notification(models.Model):
	def __unicode__(self):
			return self.title
	ntID = models.IntegerField(primary_key=True)
	ntTxT = models.TextField()
	ntClID = models.IntegerField()
	ntDate = models.DateTimeField(auto_now=True)

class Class_Course_Relation(models.Model):
	def __unicode__(self):
			return self.title
	clID = models.IntegerField(primary_key=True)
	cID = models.IntegerField()
	tID = models.IntegerField()
	cPopu = models.IntegerField()

class Student_Class_Relation(models.Model):
	def __unicode__(self):
			return self.title	
	sID = models.IntegerField(primary_key=True)
	sClID = models.IntegerField()
	clID = models.IntegerField()
	
	