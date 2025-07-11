from django.http import HttpResponse
from django.shortcuts import render

def test_view(request):
    return HttpResponse("Django is working on Vercel!")

def debug_view(request):
    import os
    import sys
    
    debug_info = f"""
    <h1>Django Debug Info</h1>
    <p><strong>Python Version:</strong> {sys.version}</p>
    <p><strong>Django Settings Module:</strong> {os.environ.get('DJANGO_SETTINGS_MODULE', 'Not Set')}</p>
    <p><strong>Debug Mode:</strong> {os.environ.get('DEBUG', 'Not Set')}</p>
    <p><strong>Python Path:</strong></p>
    <ul>
    """
    
    for path in sys.path[:5]:  # Show first 5 paths
        debug_info += f"<li>{path}</li>"
    
    debug_info += """
    </ul>
    <p><strong>Environment Variables:</strong></p>
    <ul>
    """
    
    for key, value in os.environ.items():
        if 'DJANGO' in key or 'VERCEL' in key or 'DATABASE' in key:
            debug_info += f"<li><strong>{key}:</strong> {value}</li>"
    
    debug_info += "</ul>"
    
    return HttpResponse(debug_info)
