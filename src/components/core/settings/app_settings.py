class AppSettings():
    __instance = None

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_instance():
        if AppSettings.__instance == None:
            AppSettings.__instance = AppSettings()
        return AppSettings.__instance
