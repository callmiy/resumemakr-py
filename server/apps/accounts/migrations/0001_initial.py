# Generated by Django 2.2.6 on 2019-11-02 12:01

import django.db.models.deletion
import ulid2
from django.db import migrations, models

from server.migration_utils import add_fkey


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Credential",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=ulid2.generate_ulid_as_uuid,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("source", models.CharField(max_length=255)),
                ("token", models.CharField(max_length=255)),
                ("inserted_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("recovery_token", models.TextField(blank=True, null=True)),
                (
                    "recovery_token_expires",
                    models.DateTimeField(blank=True, null=True),
                ),  # noqa
            ],
            options={"db_table": "credentials"},
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=ulid2.generate_ulid_as_uuid,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=254)),
                ("inserted_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"db_table": "users"},
        ),
        migrations.AddField(
            model_name="credential",
            name="user",
            field=models.ForeignKey(
                db_constraint=False,
                db_index=False,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="accounts.User",
            ),
        ),
        migrations.AddIndex(
            model_name="credential",
            index=models.Index(
                fields=["user"], name="credentials_user_id_index"
            ),  # noqa
        ),
        migrations.RunSQL(
            """
                CREATE UNIQUE INDEX users_email_index
                ON users(email);

                CREATE UNIQUE INDEX credentials_source_token_index
                ON credentials(source, token);

                CREATE UNIQUE INDEX credentials_user_id_source_index
                ON credentials(user_id, source);

                {}
            """.format(
                add_fkey("credentials", "user_id", "users")
            )
        ),
    ]