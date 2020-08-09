from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SurveyConfig(AppConfig):
    name = "ronatrack.survey"
    verbose_name = _("Survey")

    def ready(self):
        try:
            import ronatrack.survey.signals  # noqa F401
        except ImportError:
            pass
