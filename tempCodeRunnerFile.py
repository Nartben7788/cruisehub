def setUp(self):
        self.app = app.test_client()
        self.db = db
        self.db.create_all()