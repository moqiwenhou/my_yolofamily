from django.conf import settings
from django.db import models


class TrackingTask(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    input_video = models.FileField(upload_to='input_videos/')
    output_video = models.FileField(upload_to='output_videos/', blank=True, null=True)
    model_weight = models.CharField(max_length=255, default='yolov9c.pt')
    detect_class = models.PositiveIntegerField(default=0)
    total_frames = models.PositiveIntegerField(default=0)
    tracked_frames = models.PositiveIntegerField(default=0)
    unique_ids = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Task#{self.id} - {self.owner.username}'
