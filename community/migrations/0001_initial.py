from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CommunityCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('icon', models.CharField(default='💬', max_length=10)),
                ('description', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CommunityPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(default='Anonyme', max_length=100)),
                ('author_role', models.CharField(default='Habitué du Café', max_length=100)),
                ('author_avatar', models.CharField(default='☕', max_length=10)),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('category_slug', models.CharField(default='demarches', max_length=50)),
                ('likes_count', models.IntegerField(default=0)),
                ('replies_count', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('sent_to_discord', models.BooleanField(default=False)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='community.communitycategory')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='CommunityReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(default='Barista IA', max_length=100)),
                ('author_role', models.CharField(default='Mentor Certifié', max_length=100)),
                ('author_avatar', models.CharField(default='👨‍🍳', max_length=10)),
                ('content', models.TextField()),
                ('is_official_answer', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('sent_to_discord', models.BooleanField(default=False)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='community.communitypost')),
            ],
        ),
    ]
