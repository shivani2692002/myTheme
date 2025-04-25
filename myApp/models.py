from django.db import models
class User(models.Model):
	username=models.CharField(max_length=50)
	password=models.CharField(max_length=8)
	email=models.CharField(max_length=50)
	contact=models.CharField(max_length=10)
	image = models.ImageField(upload_to='media',blank=True)
	status=models.IntegerField(default=1)
	role=models.CharField(max_length=50,default='user')
	class Meta:
		db_table='user'
class Expense(models.Model):
	date=models.DateField()
	amount=models.FloatField()
	category=models.CharField(max_length=50)
	remark=models.CharField(max_length=50)
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	class Meta:
		db_table='expense'

class Income(models.Model):
	date=models.DateField()
	amount=models.FloatField()
	category=models.CharField(max_length=50)
	remark=models.CharField(max_length=50)
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	class Meta:
		db_table='income'

class Message(models.Model):
	message=models.CharField(max_length=50)
	status=models.IntegerField(default=0)
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	email=models.CharField(max_length=50,default='xyz')
	class Meta:
		db_table='message'



