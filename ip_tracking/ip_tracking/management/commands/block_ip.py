from django.core.management.base import BaseCommand, CommandError
from ...models import BlockedIP


class Command(BaseCommand):
    help = 'Add an IP address to the blacklist'

    def add_arguments(self, parser):
        parser.add_argument(
            'ip_address',
            type=str,
            help='IP address to block'
        )

    def handle(self, *args, **options):
        ip_address = options['ip_address']

        try:
            # Check if IP is already blocked
            if BlockedIP.objects.filter(ip_address=ip_address).exists():
                self.stdout.write(
                    self.style.WARNING(f'IP address {ip_address} is already blocked.')
                )
                return

            # Create new blocked IP
            blocked_ip = BlockedIP.objects.create(ip_address=ip_address)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully blocked IP address: {ip_address}')
            )
        except Exception as e:
            raise CommandError(f'Error blocking IP address: {str(e)}')

