from django.db import models

class Board(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Column(models.Model):
    board = models.ForeignKey(Board, related_name='columns', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default='#ffffff')

    def __str__(self):
        return f'{self.name} ({self.board.name})'
    
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    column = models.ForeignKey("Column", related_name="tasks", on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    description = models.TextField(max_length=2000, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    expired_date = models.DateTimeField()
    tags = models.CharField(max_length=200, blank=True)
    assignee = models.CharField(max_length=150, blank=True)
    author = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.title