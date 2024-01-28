from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class MapsResult:
    """Represents a result from the maps search."""

    title: Optional[str] = None
    address: Optional[str] = None
    country_code: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    url: Optional[str] = None
    desc: Optional[str] = None
    phone: Optional[str] = None
    image: Optional[str] = None
    source: Optional[str] = None
    hours: Optional[Dict[str, str]] = None
    category: Optional[str] = None
    facebook: Optional[str] = None
    instagram: Optional[str] = None
    twitter: Optional[str] = None
