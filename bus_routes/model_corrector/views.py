from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.conf import settings as SETTINGS
from django.http import JsonResponse, HttpResponse
from django.core.serializers import serialize
from django.contrib import messages
from .task import do_all

# @login_required(login_url='/admin/login/?next=/admin/')
def edit_base(request):
    """
    Заявленная цель программы корректировки данных или устранения дублей без возможности
    внесения корректив в файл модели. 
    Главный менеджер программы. CORRECTOR_TARGET_APP настраивается,
    чтобы ограничить выборку оределённым приложением, тем самым исключая возможность
    удаления важных записей. Присутствует небольшая валидация.
    """
    ct_obj = ContentType.objects.filter(app_label=SETTINGS.CORRECTOR_TARGET_APP)
    models = [model.model for model in ct_obj]
    if request.method == "POST":
        cd = request.POST
        operated = cd['operated']
        original = cd['original']
        change = cd['change']
        if operated and original and change:
            if  original != change:
                result = do_all.delay(operated, original, change)

            else:
                messages.warning(request, 'Поля не должны совпадать!')
                return render(request, 'model_corrector/index.html', {'models': models, })

            return render(request, 'model_corrector/display_progress.html', context={'task_id': result.task_id})
        else:
            messages.warning(request, 'Поля не могут быть пустыми!')
            return render(request, 'model_corrector/index.html', {'models': models, })

    return render(request, 'model_corrector/index.html', {'models': models, })


def get_model_objects(request):
    '''
    Простой API для вывода объектов по имени модели. Нет смысла подключать DRF
    '''
    if request.method == 'GET':
        cd = request.GET
        model_name = cd['model']
        try:
            model_type = ContentType.objects.get(app_label=SETTINGS.CORRECTOR_TARGET_APP, model=model_name)
            model_class = model_type.model_class()
            obj = model_class.objects.all()
            data = serialize("json", obj)
            return JsonResponse({"obj": data})
        except ContentType.DoesNotExist:
            return HttpResponse("Model doesn't exist!")
        except Exception as e:
            print(e)
            return HttpResponse("Fatal error!")


