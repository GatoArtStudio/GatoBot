from typing import List

from core.commands.service_command import ServiceCommand

class ServiceInvoker:

    _services_receivers: List[ServiceCommand]

    def send_signal_start(self, services: List[ServiceCommand]):
        self._services_receivers = services

        if isinstance(self._services_receivers, list):
            for service in self._services_receivers:
                if isinstance(service, ServiceCommand):
                    service.execute()

    def send_signal_stop(self):

        if isinstance(self._services_receivers, list):
            for service in self._services_receivers:
                if isinstance(service, ServiceCommand):
                    service.undo()