from domain.interfaces.location_repository_interface import LocationRepositoryInterface


class LocationUseCases:
    def __init__(self, location_repository: LocationRepositoryInterface):
        self.location_repository = location_repository

    def create_country(self):
        return self.location_repository.create_country()
