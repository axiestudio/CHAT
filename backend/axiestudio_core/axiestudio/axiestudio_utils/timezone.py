"""
Timezone utilities for handling datetime comparisons safely.

This module provides utilities to handle the common issue where database datetimes
are stored as naive but need to be compared with timezone-aware datetimes.
"""

from datetime import datetime, timezone
from typing import Optional


def ensure_timezone_aware(dt: Optional[datetime]) -> Optional[datetime]:
    """
    Ensure a datetime is timezone-aware for safe comparison.

    This fixes the common issue where database datetimes are stored as naive
    but need to be compared with timezone-aware datetimes.

    Args:
        dt: The datetime to check and potentially convert

    Returns:
        Timezone-aware datetime or None if input was None

    Example:
        >>> naive_dt = datetime(2025, 1, 1, 12, 0, 0)  # No timezone info
        >>> aware_dt = ensure_timezone_aware(naive_dt)
        >>> print(aware_dt)  # 2025-01-01 12:00:00+00:00
        
        >>> already_aware = datetime.now(timezone.utc)
        >>> still_aware = ensure_timezone_aware(already_aware)
        >>> print(still_aware == already_aware)  # True
    """
    if dt is None:
        return None
    
    if dt.tzinfo is None:
        # Database datetime is naive, assume it's UTC and make it timezone-aware
        return dt.replace(tzinfo=timezone.utc)
    
    return dt


def safe_datetime_comparison(dt1: Optional[datetime], dt2: Optional[datetime]) -> bool:
    """
    Safely compare two datetimes, ensuring both are timezone-aware.
    
    Args:
        dt1: First datetime to compare
        dt2: Second datetime to compare
        
    Returns:
        True if dt1 > dt2, False otherwise (including if either is None)
    """
    if dt1 is None or dt2 is None:
        return False
        
    dt1_aware = ensure_timezone_aware(dt1)
    dt2_aware = ensure_timezone_aware(dt2)
    
    if dt1_aware is None or dt2_aware is None:
        return False
        
    return dt1_aware > dt2_aware


def get_utc_now() -> datetime:
    """
    Get current UTC time as timezone-aware datetime.
    
    Returns:
        Current UTC time with timezone info
    """
    return datetime.now(timezone.utc)
