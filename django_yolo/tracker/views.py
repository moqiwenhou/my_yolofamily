from pathlib import Path
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RegisterForm, TrackingTaskForm
from .models import TrackingTask
from .services import run_yolo_tracking


def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, '注册成功，请登录。')
        return redirect('login')
    return render(request, 'tracker/register.html', {'form': form})


@login_required
def dashboard(request):
    form = TrackingTaskForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        task = form.save(commit=False)
        task.owner = request.user
        task.status = 'uploaded'
        task.save()
        messages.success(request, '视频上传成功，请点击开始跟踪按钮。')
        return redirect('dashboard')

    tasks = TrackingTask.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'tracker/dashboard.html', {'form': form, 'tasks': tasks})


@login_required
def run_tracking(request, task_id):
    task = get_object_or_404(TrackingTask, id=task_id, owner=request.user)
    if request.method == 'POST':
        task.status = 'running'
        task.save(update_fields=['status'])

        output_name = f'track_{task.id}.avi'
        output_path = Path(settings.MEDIA_ROOT) / 'output_videos' / output_name
        output_path.parent.mkdir(parents=True, exist_ok=True)

        result = run_yolo_tracking(Path(task.input_video.path), output_path, task.detect_class, task.model_weight)

        task.output_video.name = f'output_videos/{output_name}'
        task.total_frames = result['total_frames']
        task.tracked_frames = result['tracked_frames']
        task.unique_ids = result['unique_ids']
        task.status = 'done'
        task.save()

        messages.success(request, '跟踪完成。')
    return redirect('dashboard')
