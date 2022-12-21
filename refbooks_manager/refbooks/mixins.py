import datetime
from django.db.models import Subquery

from refbooks_manager.refbooks.models import Version


class LatestVersionMixin:

    def get_latest_version(self, pk):
        ordered_versions = Version.objects.filter(
                refbook__pk=pk,
                start_date__lte=datetime.date.today()
            ).order_by("-start_date")
        return Subquery(ordered_versions.values('version')[:1])
