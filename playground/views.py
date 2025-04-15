import matplotlib
import logging
logger = logging.getLogger(__name__)
matplotlib.use('Agg')     
import matplotlib.pyplot as plt
import io
import base64
from django.http import HttpResponseServerError, JsonResponse
from django.shortcuts import render
from datetime import datetime
from .pathfind import MapPath
def get_current_time(request):
    return JsonResponse({'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
def say_hello(request):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render(request, "hello.html")
from django.http import JsonResponse

def pathfind(request):
    try:
        if request.method == "POST":
            rows = int(request.POST.get("rows", 30))
            cols = int(request.POST.get("cols", 30))
            density = float(request.POST.get("density", 0.1))
            start_x = int(request.POST.get("start_x", 0))
            start_y = int(request.POST.get("start_y", 0))
            end_x = int(request.POST.get("end_x", rows - 1))
            end_y = int(request.POST.get("end_y", cols - 1))
            algorithm = request.POST.get("algorithm", "A*") 
            map_path = MapPath(rows, cols, density=density)
            steps = map_path.route((start_x, start_y), (end_x, end_y), method=algorithm)
            return JsonResponse({"steps": steps}) 
        return render(request, "visualization.html")
    except ValueError as e:
        return JsonResponse({"error": f"Invalid input: {str(e)}"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)





