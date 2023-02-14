from rest_framework.routers import Route, SimpleRouter


class CustomSimpleRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={'post': 'create'},
            name='{basename}',
            detail=False,
            initkwargs={'suffix': 'Create'}
        ),
    ]