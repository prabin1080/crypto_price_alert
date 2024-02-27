from django.core.cache import cache


class AlertListCache:
    CACHE_TIMEOUT = 3600
    cache_key = 'alertlist_user{}_'

    def _get_key(self, user_id, extra_key: str = None):
        cache_key = self.cache_key.format(user_id)
        if extra_key:
            cache_key += extra_key
        return cache_key

    def get(self, user_id: int, extra_key: str = None):
        return cache.get(self._get_key(user_id, extra_key=extra_key))

    def set(self, user_id: int, data, extra_key: str = None):
        return cache.set(self._get_key(user_id, extra_key=extra_key), data, timeout=self.CACHE_TIMEOUT)

    def delete(self, user_id: int):
        return cache.delete_many([
            key.decode('utf-8').split(':')[-1] for key in
            cache._cache.get_client().keys(f'*{self._get_key(user_id)}*')]
        )


alert_list_cache = AlertListCache()
