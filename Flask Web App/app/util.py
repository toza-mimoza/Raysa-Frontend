from app.models.bot_models import Bot

def check_if_bot_exists(query_name):
    '''Query DB for the Bot'''
    if not Bot.query.filter_by(bot_name=query_name).first(): 
        return False
    return True