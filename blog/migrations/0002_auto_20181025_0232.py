# Generated by Django 2.1.2 on 2018-10-25 02:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=300, verbose_name='内容')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.Comment', verbose_name='父级评论')),
            ],
            options={
                'verbose_name': '博客评论',
                'verbose_name_plural': '博客评论',
                'ordering': ['-create_time'],
            },
        ),
        migrations.RenameField(
            model_name='post',
            old_name='comment',
            new_name='comment_num',
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Post', verbose_name='博客'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者'),
        ),
    ]
