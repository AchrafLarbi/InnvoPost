# Generated by Django 5.0.6 on 2024-12-01 07:27

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("feedback", "0003_formfeedback_langue_formfeedback_sentiment_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Alert",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "feedback_type",
                    models.CharField(
                        choices=[
                            ("QRCodeFeedback", "QRCodeFeedback"),
                            ("FormFeedback", "FormFeedback"),
                            ("SocialMediaFeedback", "SocialMediaFeedback"),
                        ],
                        max_length=100,
                    ),
                ),
                ("feedback_id", models.PositiveIntegerField()),
                ("message", models.TextField()),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("is_traitement", models.BooleanField(default=False)),
            ],
        ),
    ]
