from django.shortcuts import render, get_list_or_404
from .models import SheepPathogen, SheepDrug


def index(request):
    sheep_pathogen = get_list_or_404(SheepPathogen)
    context = {'sheep_pathogen': sheep_pathogen}
    return render(request, 'drug_database/index.html', context)

def list(request):
    chosen_pathogens = request.POST.getlist('pathogen')
    additional_info = request.POST.getlist('info')

    if 'Trace elements' in additional_info:
        trace_elements = True
    else:
        trace_elements = False

    if 'Meat withdrawl period' in additional_info:
        meat_withdrawl_period = True
    else:
        meat_withdrawl_period = False

    if meat_withdrawl_period:
        drugs = get_list_or_404(SheepDrug.objects.order_by('meat_withdrawl_period'))
    else:
        drugs = get_list_or_404(SheepDrug)

    def filter_pathogens(required, target):
        p = [i for i in [i['name'] for i in target.values()] if i in required]
        if p == required:
            return True
        else:
            return False

    drug_list = [i for i in drugs if filter_pathogens(chosen_pathogens, i.target_pathogens)]

    context = {
        'drug_list': drug_list,
        'trace_elements': trace_elements,
        'meat_withdrawl_period': meat_withdrawl_period,
    }
    return render(request, 'drug_database/list.html', context)
