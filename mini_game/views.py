from django.http import HttpResponse
from django.template import loader
import os, sys
from backend import TicTacToe
import logging

template_path = os.path.join(os.path.dirname(__file__), 'templates')
ttt = TicTacToe()

log_file = os.path.join(os.path.dirname(__file__), 'views.log')
    
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
                    handlers=[
                        logging.FileHandler(log_file),
                        logging.StreamHandler(sys.stdout)
                    ])

def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def game(request):
    template = loader.get_template('game.html')
    grid_size = ttt.config['grid_size']
    context = {
        'grid': list(range(grid_size)),
        'buckets': ttt.buckets,
        'height_pct': int(100/grid_size),
    }

    action = request.GET.get('action', '')
    if action:        
        logging.info(ttt.current_player)
        msg = ttt.input_action(action)
        logging.info(ttt.matrix)
        logging.info(ttt.buckets)
        logging.info(msg)
        if not msg:
            msg = ""
        return HttpResponse(msg)
    return HttpResponse(template.render(context, request))

def reset(request):
    ttt.reset()
    return HttpResponse()
