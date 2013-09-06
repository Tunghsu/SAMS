from django.db import models

# Create your models here.

class Administrator(models.Model):
	aID = models.IntegerField(primary_key=True)
	aName =  models.CharField(max_length=50)
	aPasswd = models.CharField(max_length=30)
	aMail = models.EmailField(max_length=75)
	aPriv = models.IntegerField()

class Teacher(models.Model):
	tID = models.IntegerField(primary_key=True)
	tName =  models.CharField(max_length=50)
	tPasswd = models.CharField(max_length=30)
	tMail = models.EmailField(max_length=75)
	tPriv = models.IntegerField()

class Student(models.Model):
	sID = models.IntegerField(primary_key=True)
	sName =  models.CharField(max_length=50)
	sPasswd = models.CharField(max_length=30)
	sMail = models.EmailField(max_length=75)
	sNum = models.CharField(max_length=50)
	sAffi = models.CharField(max_length=75)

class Course(models.Model):
	cID = models.IntegerField(primary_key=True)
	cFileType = models.CharField(max_length=50)
	cName = models.CharField(max_length=50)

class Assignment(models.Model):
	asID = models.IntegerField(primary_key=True)
	asTXT = models.TextField()
	clID = models.IntegerField()
	asClID = models.IntegerField()
	asDate = models.DateTimeField(auto_now=True)

class AssignmentFile(models.Model):
	asfID = models.IntegerField(primary_key=True)
	asfType = models.CharField(max_length=50)
	asfDir = models.CharField(max_length=50)
	sID = models.IntegerField()
	asfDate = models.DateTimeField(auto_now=True)
	
class Notification(models.Model):
	ntID = models.IntegerField(primary_key=True)
	ntTxT = models.TextField()
	ntClID = models.IntegerField()
	ntDate = models.DateTimeField(auto_now=True)

class Class_Course_Relation(models.Model):
	clID = models.IntegerField(primary_key=True)
	cID = models.IntegerField()
	tID = models.IntegerField()

class Student_Class_Relation(models.Model):
	sID = models.IntegerField(primary_key=True)
	sClID = models.IntegerField()
	clID = models.IntegerField()
	
	