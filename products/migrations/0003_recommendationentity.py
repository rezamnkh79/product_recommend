# Generated by Django 5.1.3 on 2024-11-10 14:26

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecommendationEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField(default=datetime.datetime(2024, 11, 11, 14, 26, 6, 530010, tzinfo=datetime.timezone.utc))),
                ('source', models.CharField(choices=[('viewed', 'Viewed'), ('purchased', 'Purchased'), ('popular', 'Popular'), ('seasonal', 'Seasonal')], default='viewed', max_length=50)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.productentity')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommended_products', to='users.customuserentity')),
            ],
        ),
    ]