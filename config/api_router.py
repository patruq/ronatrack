from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from ronatrack.users.api.views import UserViewSet
from ronatrack.survey.api.views import SurveyViewSet
if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("surveys", SurveyViewSet)


app_name = "api"
urlpatterns = router.urls
