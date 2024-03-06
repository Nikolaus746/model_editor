from django.conf import settings as SETTINGS
from django.contrib.contenttypes.models import ContentType
from django.db import connection
from celery import shared_task
from celery_progress.backend import ProgressRecorder

from celery import states
import time

def check_model(model_name, operated_model, original, change):

    # Получаем модель, объект которой нужно изменить
    model_type = ContentType.objects.get(app_label=SETTINGS.CORRECTOR_TARGET_APP, model=model_name)
    model_class = model_type.model_class()

    # Получаем поля модели, объект которой нужно изменить, чтобы найти в них связанные с запрашивающей
    # таблицей поля.
    fields = model_class._meta.get_fields()
    with connection.cursor() as cursor:
        for field in fields:

                try:
                    # Если поле найдено, то проверяем, есть ли в нём заменяемый объект
                    # и заменям на требуемый
                   if field.related_model == operated_model:
                       objects = model_class.objects.raw(F'SELECT * FROM {SETTINGS.CORRECTOR_TARGET_APP}_{model_class._meta.model_name} WHERE {field.name}_id = %s', [change])
                       for ob in objects:
                           cursor.execute(F"UPDATE {SETTINGS.CORRECTOR_TARGET_APP}_{model_class._meta.model_name} SET {field.name}_id = %s WHERE id = %s", [original, str(ob.pk)])

                except:
                    pass
        cursor.fetchall()

@shared_task(bind=True)
def do_all(self, operated, original, change):
    progress_recorder = ProgressRecorder(self)
    # Получаем модель, связь с которой нужно установить
    model_type_operated = ContentType.objects.get(app_label=SETTINGS.CORRECTOR_TARGET_APP, model=operated)
    model_class_operated = model_type_operated.model_class()
    ct_obj = ContentType.objects.filter(app_label=SETTINGS.CORRECTOR_TARGET_APP)
    models = [model.model for model in ct_obj]

    # Проверяем все таблицы кроме текущей
    for i, model_name in enumerate(models):
        # Эмуляция задержки
        time.sleep(3)
        if model_name != operated:
            check_model(model_name, model_class_operated, original, change)
        progress_recorder.set_progress(i+1, len(models), F"on {i}")
    # Удаляем уже не связанные объекты
    model_class_operated.objects.filter(id=change).delete()

    return ("done")


