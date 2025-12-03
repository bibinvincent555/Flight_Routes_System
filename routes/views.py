from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Min, Max
from django.contrib import messages
from .models import AirportRoute
from .forms import AddRouteForm, NthSearchForm, BetweenAirportsForm
import json


def index(request):
    # Simple dashboard showing available routes and forms
    routes_qs = AirportRoute.objects.all()
    add_form = AddRouteForm()
    nth_form = NthSearchForm()
    between_form = BetweenAirportsForm()

    # Prepare JSON-serializable data for Chart.js
    routes = list(routes_qs.values('airport_code', 'position', 'duration'))
    context = {
        'routes': routes_qs,
        'add_form': add_form,
        'nth_form': nth_form,
        'between_form': between_form,
        'routes_json': json.dumps(routes),
    }
    return render(request, 'routes/index.html', context)


def add_route(request):
    if request.method == 'POST':
        form = AddRouteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    return redirect('index')


def find_nth(request):
    result = None
    error = None
    routes_json = '[]'
    if request.method == 'GET':
        form = NthSearchForm(request.GET)
        if form.is_valid():
            code = form.cleaned_data['airport_code']
            direction = form.cleaned_data['direction']
            n = form.cleaned_data['n']
            try:
                node = AirportRoute.objects.get(airport_code=code)
            except AirportRoute.DoesNotExist:
                error = f'Airport with code {code} not found.'
            else:
                if direction == 'left':
                    # left = lower position
                    target_pos = node.position - n
                else:
                    target_pos = node.position + n
                try:
                    result = AirportRoute.objects.get(position=target_pos)
                except AirportRoute.DoesNotExist:
                    error = f'No node found at position {target_pos}.'
                else:
                    # prepare a small context window around the target for charting
                    lo = max(1, target_pos - 3)
                    hi = target_pos + 3
                    window = list(AirportRoute.objects.filter(position__gte=lo, position__lte=hi).values('airport_code', 'position', 'duration'))
                    import json
                    routes_json = json.dumps(window)
    else:
        form = NthSearchForm()
    return render(request, 'routes/find_nth.html', {'form': form, 'result': result, 'error': error, 'routes_json': routes_json})


def longest_node(request):
    # Find node with maximum duration
    node = AirportRoute.objects.order_by('-duration').first()
    # prepare all routes for charting and mark the longest
    all_routes = list(AirportRoute.objects.all().values('airport_code', 'position', 'duration'))
    import json
    routes_json = json.dumps(all_routes)
    return render(request, 'routes/longest.html', {'node': node, 'routes_json': routes_json})


def shortest_between(request):
    result = None
    error = None
    routes_json = '[]'
    if request.method == 'GET':
        form = BetweenAirportsForm(request.GET)
        if form.is_valid():
            a = form.cleaned_data['airport_code_a']
            b = form.cleaned_data['airport_code_b']
            try:
                node_a = AirportRoute.objects.get(airport_code=a)
                node_b = AirportRoute.objects.get(airport_code=b)
            except AirportRoute.DoesNotExist:
                error = 'One or both airport codes not found.'
            else:
                lo = min(node_a.position, node_b.position)
                hi = max(node_a.position, node_b.position)
                
                # Get all nodes in the range (inclusive)
                nodes_in_range = list(AirportRoute.objects.filter(
                    position__gte=lo, 
                    position__lte=hi
                ).values('airport_code', 'position', 'duration'))
                
                import json
                routes_json = json.dumps(nodes_in_range)
                
                if nodes_in_range:
                    # Find the node with minimum duration value in the range
                    # "Duration" here represents a node attribute (e.g., processing time at that airport)
                    shortest = min(nodes_in_range, key=lambda r: r['duration'])
                    
                    # Convert to AirportRoute object for display convenience
                    try:
                        result = AirportRoute.objects.get(position=shortest['position'])
                    except AirportRoute.DoesNotExist:
                        result = None
    else:
        form = BetweenAirportsForm()
    return render(request, 'routes/shortest_between.html', {'form': form, 'result': result, 'error': error, 'routes_json': routes_json})
