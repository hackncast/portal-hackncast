import os
import json

from django.core.management.base import BaseCommand
from ... import utils


class Command(BaseCommand):
    help = "Exports backend API mapping"

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--file', '-f', dest="file",
            help="Output file path"
        )
        parser.add_argument(
            '--echo', '-e', dest="echo", action='store_true',
            help="Only prints out the API mapping"
        )

    def handle(self, *args, **options):
        echo = options['echo']
        file = options['file']

        if not echo and not file:
            print("Please expecify a propper file path")
            exit(1)

        if not echo:
            file = os.path.abspath(options['file'])
            path = os.path.dirname(file)

            if not os.path.exists(path):
                print("This filepath doesn't exist: {}".format(path))
                exit(1)

            if not os.path.isdir(path):
                print("This filepath isn't a directory: {}".format(path))
                exit(1)

        urls = utils.getUrls()
        export = json.dumps(urls, indent=2, separators=(',', ': '))
        if echo:
            print(export)
            return

        export = export.replace('"', "'")
        export = 'export default {}\n'.format(export)

        with open(file, 'w') as fd:
            fd.write(export)

        count = sum([len(v) for v in urls.values()])
        print('{} exported URLs at {}'.format(count, file))
