from django.shortcuts import render, redirect
from django.db.models import Sum
from .models import Expense, Category
from .forms import ExpenseForm
from datetime import datetime
from django.http import JsonResponse

def home(request):
    category_id = request.GET.get('category')
    start = request.GET.get('start')
    end = request.GET.get('end')

    qs = Expense.objects.all().order_by('-date')

    if category_id:
        qs = qs.filter(category_id=category_id)
    if start:
        try:
            start_date = datetime.strptime(start, "%Y-%m-%d").date()
            qs = qs.filter(date__gte=start_date)
        except ValueError:
            start_date = None
    if end:
        try:
            end_date = datetime.strptime(end, "%Y-%m-%d").date()
            qs = qs.filter(date__lte=end_date)
        except ValueError:
            end_date = None

    categories = Category.objects.all()
    total = qs.aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'expenses': qs,
        'categories': categories,
        'selected_category': category_id,
        'total': total,
    }
    return render(request, 'home.html', context)


def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ExpenseForm()
    return render(request, 'add_expense.html', {'form': form})


def dashboard(request):
    total = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
    per_category = Expense.objects.values('category__name').annotate(total=Sum('amount'))
    context = {'total': total, 'per_category': per_category}
    return render(request, 'dashboard.html', context)


def chart_data(request):
    data = Expense.objects.values('category__name').annotate(total=Sum('amount'))
    return JsonResponse(list(data), safe=False)
