class BaseRepository:
    def __init__(self, session_maker):
        self.db_session = session_maker()
