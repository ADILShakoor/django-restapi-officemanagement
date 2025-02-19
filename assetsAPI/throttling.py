
from rest_framework.throttling import SimpleRateThrottle

class AssetRateThrolling(SimpleRateThrottle):
    cope = 'burst'
    rate = '6/minute'