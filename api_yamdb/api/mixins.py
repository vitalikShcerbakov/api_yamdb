from rest_framework import mixins, viewsets


class ViewSetWithoutUpdate(mixins.CreateModelMixin, mixins.ListModelMixin,
                           mixins.DestroyModelMixin, viewsets.GenericViewSet):
    pass
