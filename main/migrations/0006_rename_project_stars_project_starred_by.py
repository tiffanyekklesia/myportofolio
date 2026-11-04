from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0005_experience_stars"),
    ]

    operations = [
        migrations.RenameField(
            model_name="project",
            old_name="stars",
            new_name="starred_by",
        ),
    ]
