import logging
import functools
import json
import os
import time
import inspect


def get_current_log_level():
    """
    Get the current log level from properties.json.
    Returns True if DEBUG level is enabled, False otherwise.
    """
    try:
        if os.path.exists("properties.json"):
            with open("properties.json", "r", encoding="utf-8") as f:
                properties = json.load(f)
                return properties.get("log_level", "INFO").upper() == "DEBUG"
    except Exception:
        pass
    return False


def ensure_logger_configured(logger):
    """
    Ensure the logger has at least one handler configured.
    """
    if not logger.handlers:
        # Configure a simple handler if none exists
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)  # Handler should accept all levels
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] [%(name)s]: %(message)s', 
                                      datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Set logger level based on properties
        if get_current_log_level():
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)


def log_all_methods(cls):
    """
    Class decorator that wraps all methods of a class with logging.
    Only outputs debug logs when log_level in properties.json is set to DEBUG.
    Used for debugging in modules like gpx_table_editor.
    """

    logger = logging.getLogger(cls.__name__)
    ensure_logger_configured(logger)

    for attr_name in dir(cls):

        if attr_name.startswith("__"):
            continue

        attr = getattr(cls, attr_name)

        if callable(attr):

            def make_wrapper(method):

                @functools.wraps(method)
                def wrapper(*args, **kwargs):
                    # Only log if DEBUG level is enabled in properties.json
                    if get_current_log_level():
                        # Get method signature for parameter info
                        sig = inspect.signature(method)
                        param_names = list(sig.parameters.keys())
                        
                        # Format arguments with safe repr for tkinter objects
                        def safe_repr(obj):
                            try:
                                return repr(obj)
                            except Exception:
                                return f"<{type(obj).__name__} object>"
                        
                        args_str = ", ".join([f"{safe_repr(arg)}" for arg in args])
                        kwargs_str = ", ".join([f"{k}={safe_repr(v)}" for k, v in kwargs.items()])
                        
                        all_params = []
                        if args_str:
                            all_params.append(args_str)
                        if kwargs_str:
                            all_params.append(kwargs_str)
                        params_str = ", ".join(all_params)
                        
                        # Log method entry with parameters
                        logger.debug(f"→ {cls.__name__}.{method.__name__}({params_str})")
                        
                        # Execute method and measure time
                        start_time = time.time()
                        result = method(*args, **kwargs)
                        execution_time = time.time() - start_time
                        
                        # Log successful exit with return value and timing
                        result_str = safe_repr(result) if result is not None else "None"
                        if len(result_str) > 100:
                            result_str = result_str[:100] + "..."
                        logger.debug(f"← {cls.__name__}.{method.__name__}() returned {result_str} [{execution_time:.3f}s]")
                        
                        return result

                return wrapper

            setattr(cls, attr_name, make_wrapper(attr))

    return cls
