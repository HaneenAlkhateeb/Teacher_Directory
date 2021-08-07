from django.db import models

# Teacher model to save teacher info
class teacher(models.Model):
    first_name      = models.CharField(max_length=200)
    last_name       = models.CharField(max_length=200)
    profile_picture = models.TextField(null=True)
    email           = models.TextField(unique=True)
    phone           = models.IntegerField(default=0)
    room_no         = models.CharField(max_length=200)
    subjects_taught = models.TextField()
    

    def __str__(self):
        return self.first_name

# Teacher model to save teacher info
class subjects(models.Model):
    name    = models.CharField(max_length=200) 
    def __str__(self):
        return self.name

# Teacher model to save teacher info
class teacher_subjects(models.Model):
    teacher_id = models.ForeignKey(teacher, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(subjects, on_delete=models.CASCADE)


class users(models.Model):
    username   = models.CharField(max_length=200)
    password   = models.TextField()
