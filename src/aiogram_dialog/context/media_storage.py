from pathlib import Path
from typing import Optional

from aiogram.types import ContentType
from cachetools import LRUCache

from aiogram_dialog.api.entities import MediaId
from aiogram_dialog.api.protocols import MediaIdStorageProtocol


class MediaIdStorage(MediaIdStorageProtocol):
    def __init__(self, maxsize=10240):
        self.cache = LRUCache(maxsize=maxsize)

    async def get_media_id(
            self,
            path: Optional[str],
            url: Optional[str],
            type: ContentType,
    ) -> Optional[MediaId]:
        if not path and not url:
            return None
        return self.cache.get((path, url, type, self._get_file_mtime(path)))

    def _get_file_mtime(self, path: Optional[str]) -> Optional[float]:
        if not path:
            return None
        p = Path(path)
        if p.exists():
            return None
        return Path(path).stat().st_mtime

    async def save_media_id(
            self,
            path: Optional[str],
            url: Optional[str],
            type: ContentType,
            media_id: MediaId,
    ) -> None:
        if not path and not url:
            return
        self.cache[(path, url, type)] = media_id
