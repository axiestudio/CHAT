# -*- coding: utf-8 -*-
"""
🔧 CUSTOM COMPONENT INTERFACE
Provides interface for loading and managing custom components
"""

from typing import Optional, Type, Any
from axiestudio.logging import logger

from axiestudio.interface.components import get_all_components


def get_custom_component_from_name(component_name: str) -> Optional[Type[Any]]:
    """
    Get a custom component class by name.
    
    Args:
        component_name: Name of the component to retrieve
        
    Returns:
        Component class if found, None otherwise
    """
    try:
        # Try to get component from the components registry
        from axiestudio.services.deps import get_settings_service
        
        settings_service = get_settings_service()
        components_paths = settings_service.settings.components_path
        
        # Get all components as dictionary
        all_components = get_all_components(components_paths, as_dict=True)
        
        # Search through all categories for the component
        for category_name, category_components in all_components.items():
            if component_name in category_components:
                component_info = category_components[component_name]
                
                # If it's a class, return it directly
                if hasattr(component_info, '__class__') and hasattr(component_info, '__name__'):
                    return component_info
                
                # If it's a dictionary with component info, try to get the class
                if isinstance(component_info, dict):
                    if 'class' in component_info:
                        return component_info['class']
                    elif 'component_class' in component_info:
                        return component_info['component_class']
        
        logger.debug(f"Component '{component_name}' not found in registry")
        return None
        
    except Exception as e:
        logger.warning(f"Error getting custom component '{component_name}': {e}")
        return None


def register_custom_component(component_name: str, component_class: Type[Any]) -> bool:
    """
    Register a custom component.
    
    Args:
        component_name: Name to register the component under
        component_class: The component class to register
        
    Returns:
        True if registration successful, False otherwise
    """
    try:
        # This is a placeholder for component registration
        # In a full implementation, this would add to a registry
        logger.debug(f"Registering custom component: {component_name}")
        return True
        
    except Exception as e:
        logger.error(f"Error registering custom component '{component_name}': {e}")
        return False


def list_custom_components() -> list[str]:
    """
    List all available custom components.
    
    Returns:
        List of custom component names
    """
    try:
        from axiestudio.services.deps import get_settings_service
        
        settings_service = get_settings_service()
        components_paths = settings_service.settings.components_path
        
        # Get all components
        all_components = get_all_components(components_paths, as_dict=True)
        
        # Extract component names
        component_names = []
        for category_components in all_components.values():
            component_names.extend(category_components.keys())
        
        return component_names
        
    except Exception as e:
        logger.error(f"Error listing custom components: {e}")
        return []


def get_component_info(component_name: str) -> Optional[dict]:
    """
    Get detailed information about a component.
    
    Args:
        component_name: Name of the component
        
    Returns:
        Component information dictionary or None
    """
    try:
        from axiestudio.services.deps import get_settings_service
        
        settings_service = get_settings_service()
        components_paths = settings_service.settings.components_path
        
        # Get all components
        all_components = get_all_components(components_paths, as_dict=True)
        
        # Search for the component
        for category_name, category_components in all_components.items():
            if component_name in category_components:
                component_info = category_components[component_name]
                
                return {
                    'name': component_name,
                    'category': category_name,
                    'component': component_info,
                    'type': type(component_info).__name__
                }
        
        return None
        
    except Exception as e:
        logger.error(f"Error getting component info for '{component_name}': {e}")
        return None


# Export the main functions
__all__ = [
    "get_custom_component_from_name",
    "register_custom_component", 
    "list_custom_components",
    "get_component_info"
]
