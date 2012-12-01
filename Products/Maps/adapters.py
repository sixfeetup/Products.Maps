from zope.interface import implements
from zope.component import adapts

from Products.Maps.interfaces import IGeoLocation, IMarker, IRichMarker, IMap

from Products.CMFPlone.utils import base_hasattr

try:
    from plone.app.contenttypes.interfaces import IFolder as IATFolder
    from plone.app.collection.interfaces import ICollection as IATTopic
except:
    from Products.ATContentTypes.interface import IATFolder
    from Products.ATContentTypes.interface import IATTopic


class BaseMap(object):
    implements(IMap)

    def __init__(self, context):
        self.context = context

    def getMarkers(self):
        results = []
        for item in self._getItems():
            marker = IMarker(item, None)
            if marker is None:
                if base_hasattr(item, 'getObject'):
                    marker = IMarker(item.getObject(), None)
            if marker is not None:
                results.append(marker)
        return results


class SmartFolderMap(BaseMap):
    adapts(IATTopic)

    def _getItems(self):
        return self.context.queryCatalog()


class FolderMap(BaseMap):
    adapts(IATFolder)

    def _getItems(self):
        return self.context.getFolderContents()


class GeoLocation(object):
    implements(IGeoLocation)

    def __init__(self, context):
        self.context = context

    @property
    def latitude(self):
        location = self.context.getRawGeolocation()
        return location[0]

    @property
    def longitude(self):
        location = self.context.getRawGeolocation()
        return location[1]


class ContextMap(object):
    implements(IMap)

    def __init__(self, context):
        self.context = context

    def getMarkers(self):
        yield IGeoLocation(self.context)


class RichMarker(object):
    implements(IRichMarker)
    adapts(IMarker)

    def __init__(self, context):
        self.context = context

    @property
    def latitude(self):
        return self.context.latitude

    @property
    def longitude(self):
        return self.context.longitude

    @property
    def title(self):
        return self.context.title

    @property
    def description(self):
        return self.context.description

    @property
    def layers(self):
        return self.context.layers

    @property
    def icon(self):
        return self.context.icon

    @property
    def url(self):
        return self.context.url

    @property
    def related_items(self):
        return tuple()

    @property
    def contents(self):
        return tuple()
