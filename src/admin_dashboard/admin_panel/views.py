"""Admin panel views"""
import json
import os
import psutil
from datetime import datetime, timedelta
from pathlib import Path

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .bot_manager import bot_manager


def login_view(request):
    """Login page"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Credenciais inválidas'})

    return render(request, 'login.html')


def logout_view(request):
    """Logout and redirect to login"""
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    """Main dashboard page"""
    # Import here to avoid circular imports
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
    from discord_bot.database.sqlite_db import db

    # Get bot stats
    stats = db.get_total_stats()
    bot_status = bot_manager.get_status()

    # System stats
    process = psutil.Process()
    system_stats = {
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': process.memory_percent(),
        'memory_mb': process.memory_info().rss / 1024 / 1024,
    }

    context = {
        'bot_status': bot_status,
        'stats': stats,
        'system_stats': system_stats,
    }

    return render(request, 'dashboard.html', context)


@login_required
def logs_view(request):
    """Logs viewer page"""
    return render(request, 'logs.html')


@login_required
def embeddings_view(request):
    """Embeddings management page"""
    return render(request, 'embeddings.html')


# API Endpoints

@login_required
@require_http_methods(["POST"])
def api_bot_start(request):
    """Start the Discord bot"""
    result = bot_manager.start_bot()
    return JsonResponse(result)


@login_required
@require_http_methods(["POST"])
def api_bot_stop(request):
    """Stop the Discord bot"""
    result = bot_manager.stop_bot()
    return JsonResponse(result)


@login_required
@require_http_methods(["POST"])
def api_bot_restart(request):
    """Restart the Discord bot"""
    result = bot_manager.restart_bot()
    return JsonResponse(result)


@login_required
@require_http_methods(["GET"])
def api_bot_status(request):
    """Get bot status"""
    status = bot_manager.get_status()
    return JsonResponse(status)


@login_required
@require_http_methods(["GET"])
def api_stats(request):
    """Get bot statistics"""
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
    from discord_bot.database.sqlite_db import db

    stats = db.get_total_stats()

    # System stats
    process = psutil.Process()
    system_stats = {
        'cpu_percent': psutil.cpu_percent(interval=0.1),
        'memory_percent': process.memory_percent(),
        'memory_mb': round(process.memory_info().rss / 1024 / 1024, 2),
    }

    return JsonResponse({
        'bot_stats': stats,
        'system_stats': system_stats,
    })


@login_required
@require_http_methods(["GET"])
def api_uptime(request):
    """Get bot uptime"""
    uptime_seconds = bot_manager.get_uptime_seconds()
    return JsonResponse({
        'uptime_seconds': uptime_seconds,
        'is_running': bot_manager.is_running,
    })


@login_required
@require_http_methods(["GET"])
def api_logs_stream(request):
    """Stream logs (Server-Sent Events)"""
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

    # Get log file path
    log_file = Path(__file__).resolve().parent.parent.parent.parent / 'logs' / 'discord_bot.log'

    def event_stream():
        """Generate log events"""
        if not log_file.exists():
            yield f"data: {json.dumps({'message': 'No log file found'})}\n\n"
            return

        # Read last 50 lines
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            last_lines = lines[-50:] if len(lines) > 50 else lines

            for line in last_lines:
                yield f"data: {json.dumps({'message': line.strip()})}\n\n"

    response = HttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response


@login_required
@require_http_methods(["GET"])
def api_logs_export(request):
    """Export logs to file"""
    format_type = request.GET.get('format', 'txt')
    log_file = Path(__file__).resolve().parent.parent.parent.parent / 'logs' / 'discord_bot.log'

    if not log_file.exists():
        return JsonResponse({'error': 'No log file found'}, status=404)

    with open(log_file, 'r', encoding='utf-8') as f:
        logs = f.readlines()

    if format_type == 'json':
        log_data = [{'timestamp': datetime.now().isoformat(), 'message': line.strip()} for line in logs]
        response = HttpResponse(json.dumps(log_data, indent=2), content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="bot_logs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json"'
    else:  # txt
        response = HttpResponse(''.join(logs), content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="bot_logs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt"'

    return response


@login_required
@require_http_methods(["GET"])
def api_embeddings_stats(request):
    """Get RAG embeddings statistics"""
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

    try:
        from discord_bot.rag.vector_store import vector_store

        # Check if vector store is initialized
        if not hasattr(vector_store, 'collection') or vector_store.collection is None:
            return JsonResponse({
                'error': 'Vector store not initialized',
                'count': 0,
                'initialized': False
            })

        count = vector_store.count_documents()
        return JsonResponse({
            'count': count,
            'initialized': True,
            'collection_name': vector_store.collection_name
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'count': 0,
            'initialized': False
        })


@login_required
@require_http_methods(["POST"])
def api_embeddings_clear(request):
    """Clear all embeddings"""
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

    try:
        from discord_bot.rag.vector_store import vector_store
        vector_store.delete_all_documents()
        return JsonResponse({
            'success': True,
            'message': 'All embeddings cleared successfully'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@require_http_methods(["POST"])
def api_embeddings_process(request):
    """Process documents for embeddings"""
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

    if 'file' not in request.FILES:
        return JsonResponse({'success': False, 'error': 'No file provided'}, status=400)

    file = request.FILES['file']
    filename = file.name

    try:
        from discord_bot.rag.vector_store import vector_store
        import asyncio

        # Read file content
        content = file.read().decode('utf-8')

        # Process document
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(vector_store.add_document(
            text=content,
            metadata={
                'filename': filename,
                'uploaded_at': datetime.now().isoformat(),
                'uploaded_by': request.user.username
            }
        ))
        loop.close()

        return JsonResponse({
            'success': True,
            'message': f'Document {filename} processed successfully'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
