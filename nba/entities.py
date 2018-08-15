from helpers import get_page

class Player:


    def __init__(self, id):
        url = "".join(["http://stats.nba.com/player/", str(id), '/'])
        try:
            page = get_page(url)
        except Exception as exc:
            traceback.print_exc()
            return
        
