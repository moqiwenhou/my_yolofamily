from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TrackingTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_video', models.FileField(upload_to='input_videos/')),
                ('output_video', models.FileField(blank=True, null=True, upload_to='output_videos/')),
                ('model_weight', models.CharField(default='yolov9c.pt', max_length=255)),
                ('detect_class', models.PositiveIntegerField(default=0)),
                ('total_frames', models.PositiveIntegerField(default=0)),
                ('tracked_frames', models.PositiveIntegerField(default=0)),
                ('unique_ids', models.PositiveIntegerField(default=0)),
                ('status', models.CharField(default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
