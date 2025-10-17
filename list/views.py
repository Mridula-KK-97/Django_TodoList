from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Task

def frontpage(request):
    tasks = Task.objects.all().order_by('-created_at')
    current_date = timezone.now().date()

    for task in tasks:
        if task.due_date:
            if task.due_date == current_date:
                task.status_text = "Due Today"
            elif task.due_date < current_date:
                task.status_text = "Overdue"
            else:
                task.status_text = "On Track"
        else:
            task.status_text = "No Due Date"

    return render(request, 'list/frontpage.html', {'tasks': tasks})

def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.status == "Pending":
        task.status = "Completed"
    else:
        task.status = "Pending"
    task.save()
    return redirect('frontpage')

def add_task(request):
    if request.method == 'POST':
        # Use the correct key 'title' here, not 'task'
        title = request.POST['title']
        due_date = request.POST['due_date']
        
        Task.objects.create(title=title, due_date=due_date)
    
    return redirect('frontpage')


def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.title = request.POST['title']
        task.due_date = request.POST.get('due_date')
        task.save()
        return redirect('frontpage')
    return render(request, 'list/edit_task.html', {'task': task})


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('frontpage')
