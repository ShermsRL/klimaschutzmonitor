# Generated by Django 4.1.7 on 2023-03-23 15:01

from django.db import migrations, models

# Previous values:

# ExecutionAssessment:
# UNKNOWN = 0, "unbekannt (grau)"
# AHEAD = 1, "vor dem Plan (grün)"
# AS_PLANNED = 2, "im Plan (grün)"
# DELAYED = 3, "zurückgestellt / verzögert (orange)"
# INSUFFICIENT = 4, "nicht ausreichend / in Teilen gescheitert (rot)"
# FAILED = 5, "gescheitert (rot)"
# MISSING = 6, "fehlt im Plan (rot)"

# ExecutionProgress
# UNKNOWN = 0, "unbekannt"
# NOT_PLANNED = 1, "ungeplant"
# PLANNED = 2, "in Zukunft geplant"
# IN_PROGRESS = 3, "läuft"
# FINISHED = 4, "abgeschlossen / gescheitert"

# New values:

# ExecutionStatus:
# UNKNOWN = 0, "unbekannt / ungeplant"
# AS_PLANNED = 2, "geplant / in Arbeit"
# COMPLETE = 4, "abgeschlossen"
# DELAYED = 6, "verzögert / fehlt"
# FAILED = 8, "gescheitert"


def set_execution_status(apps, schema_editor):
    Task = apps.get_model("cpmonitor", "Task")
    db_alias = schema_editor.connection.alias
    for task in Task.objects.using(db_alias).all():
        match (task.execution_assessment, task.execution_progress):
            case (0, _):
                task.execution_status = 0
            case (1, 4) | (2, 4):
                task.execution_status = 4
            case (1, _) | (2, _):
                task.execution_status = 2
            case (3, _):
                task.execution_status = 6
            case (4, _) | (5, _) | (6, _):
                task.execution_status = 8
        task.save()


def set_execution_assessment_and_progress(apps, schema_editor):
    Task = apps.get_model("cpmonitor", "Task")
    db_alias = schema_editor.connection.alias
    for task in Task.objects.using(db_alias).all():
        match task.execution_status:
            case 0:
                task.execution_assessment = 0
                task.execution_progress = 0
            case 2:
                task.execution_assessment = 2
                task.execution_progress = 2
            case 4:
                task.execution_assessment = 2
                task.execution_progress = 4
            case 6:
                task.execution_assessment = 3
                task.execution_progress = 2
            case 8:
                task.execution_assessment = 5
                task.execution_progress = 0
        task.save()


class Migration(migrations.Migration):
    dependencies = [
        ("cpmonitor", "0006_alter_task_city"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="execution_status",
            field=models.IntegerField(
                choices=[
                    (0, "unbekannt / ungeplant"),
                    (2, "geplant / in Arbeit"),
                    (4, "abgeschlossen"),
                    (6, "verzögert / fehlt"),
                    (8, "gescheitert"),
                ],
                default=0,
                help_text='\n            <p>Bei Maßnahmen: Wird/wurde die Maßnahme wie geplant umgesetzt?</p>\n            <dl>\n                <dt>unbekannt / ungeplant</dt><dd><ul>\n                    <li>Keine Infos vorhanden</li>\n                    <li>Es gibt einen unkonkreten Beschluss</li>\n                </ul></dd>\n                <dt>geplant / in Arbeit</dt><dd><ul>\n                    <li>Finden wir erstmal gut: Dinge werden bearbeitet.</li>\n                    <li>Maßnahmen, die im Zeitplan sind (sowohl begonnen als auch in Planung).</li>\n                    <li>Maßnahmen die in Umsetzung sind.</li>\n                    <li>Maßnahmen für die es einen positiven Beschluss + Zeitplan (Konkretisierung) gibt.</li>\n                </ul></dd>\n                <dt>abgeschlossen</dt><dd><ul>\n                    <li>Top und im Plan fertig.</li>\n                </ul></dd>\n                <dt>verzögert / fehlt</dt><dd><ul>\n                    <li>Maßnahmen, die nicht im Zeitplan sind.</li>\n                    <li>Maßnahmen, die im Prinzip noch vervollständigt werden können.</li>\n                    <li>Maßnahmen, die im KAP nicht aufgeführt sind, (und nicht bearbeitet weden)</li>\n                    <li>Im Prinzip könnten sie aber noch angegangen werden.</li>\n                </ul></dd>\n                <dt>gescheitert</dt><dd><ul>\n                    <li>Kann niemals mehr geschafft werden (Eiche ist gefällt, Moor ist mit einer Autobahn überbaut)</li>\n                    <li>Sowohl für Maßnahmen aus dem KAP, als auch Dinge, die gar nich im KAP aufgeführt waren.</li>\n                </ul></dd>\n            </dl>\n            <p>Bei Sektoren / Maßnahmengruppen:</p>\n            <p>Wenn hier "unbekannt" ausgewählt wird, werden die Umsetzungsstände der Maßnahmen in diesem Sektor / dieser Gruppe zusammengefasst.</p>\n            <p>Bei anderen Auswahlen wird diese Zusammenfassung überschrieben. Das sollte nur passieren, wenn sie unpassend oder irreführend ist.</p>\n        ',
                verbose_name="Umsetzungsstand",
            ),
        ),
        migrations.RunPython(
            set_execution_status, set_execution_assessment_and_progress
        ),
        migrations.RemoveField(
            model_name="task",
            name="execution_assessment",
        ),
        migrations.RemoveField(
            model_name="task",
            name="execution_progress",
        ),
        migrations.AlterField(
            model_name="task",
            name="execution_justification",
            field=models.TextField(
                blank=True,
                help_text="Die Auswahl bei Umsetzungsstand kann hier ausführlich begründet werden.",
                verbose_name="Begründung Umsetzungsstand",
            ),
        ),
    ]
