from django.shortcuts import render, redirect, get_object_or_404
from .models import Board, Column, Task
from .forms import BoardForm, ColumnForm, TaskForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def board_list(request):
    boards = Board.objects.all()
    return render(request, 'kanban/board_list.html', {'boards': boards})

def add_board(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('kanban:board_list')
    else:
        form = BoardForm()
    return render(request, 'kanban/add_board.html', {'form': form})

def edit_board(request, board_id):
    board = get_object_or_404(Board, id=board_id)

    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            form.save()
            return redirect('kanban:board_detail', board_id=board.id)
    else:
        form = BoardForm(instance=board)

    return render(request, 'kanban/edit_board.html', {'form': form, 'board': board})

def delete_board(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    
    if request.method == 'POST':
        board.delete()
        return redirect('kanban:board_list')
    return render(request, 'kanban/delete_board.html', {'board': board})

def board_detail(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    columns = board.columns.all()
    return render(request, 'kanban/board_detail.html', {'board': board, 'columns': columns})

def add_column(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    if request.method == "POST":
        form = ColumnForm(request.POST)
        if form.is_valid():
            new_column = form.save(commit=False)
            new_column.board = board
            new_column.save()
            return redirect('kanban:board_detail', board_id=board.id)
    else:
        form = ColumnForm()

    return render(request, 'kanban/add_column.html', {'form': form})

def edit_column(request, column_id):
    column = get_object_or_404(Column, id=column_id)
    if request.method == "POST":
        form = ColumnForm(request.POST, instance=column)
        if form.is_valid():
            form.save()
            return redirect('kanban:board_detail', board_id=column.board.id)
    else:
        form = ColumnForm(instance=column)

    return render(request, 'kanban/edit_column.html', {'form': form, 'column': column})

def delete_column(request, column_id):
    column = get_object_or_404(Column, id=column_id)
    board_id = column.board.id
    column.delete()
    return redirect('kanban:board_detail', board_id=board_id)

def add_task(request, column_id):
    column = get_object_or_404(Column, id=column_id)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.column = column
            task.save()
            form.save_m2m() 
            return redirect('kanban:board_detail', board_id=column.board.id)
    else:
        form = TaskForm()

    return render(request, "kanban/add_task.html", {"form": form, "column": column})

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('kanban:board_detail', board_id=task.column.board.id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'kanban/edit_task.html', {'form': form, 'task': task})

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    board_id = task.column.board.id
    task.delete()
    return redirect('kanban:board_detail', board_id=board_id)

def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'kanban/task_detail.html', {'task': task})

@csrf_exempt
def move_task(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        task_id = data.get('task_id')
        new_column_id = data.get('new_column_id')
        
        try:
            task = Task.objects.get(id=task_id)
            new_column = Column.objects.get(id=new_column_id)
            task.column = new_column
            task.save()
            return JsonResponse({'status': 'success'})
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)
        except Column.DoesNotExist:
            return JsonResponse({'error': 'Column not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
