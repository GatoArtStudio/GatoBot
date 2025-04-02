from __future__ import annotations
from core.interfaces.i_command import ICommand
from core.interfaces.i_infrastructure_initiator import IInfrastructureInitiator

class ServiceCommand(ICommand):

    _services: IInfrastructureInitiator

    def __init__(self, service: IInfrastructureInitiator):
        self._services = service

    def execute(self):
        self._services.start_service()

    def undo(self):
        self._services.stop_service()
