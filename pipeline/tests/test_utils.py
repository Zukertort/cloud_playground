import pytest
from unittest.mock import MagicMock, patch
from utils import time_execution
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import retry

def test_retry_success():
    """Test that it runs once if successful."""
    mock_func = MagicMock(return_value="Success")
    mock_func.__name__ = "mock_task"
    
    decorated = retry(retries=3, delay=0.01)(mock_func)
    
    result = decorated()
    
    assert result == "Success"
    assert mock_func.call_count == 1

def test_retry_eventual_success():
    """Test that it retries on failure and eventually succeeds."""
    mock_func = MagicMock(side_effect=[ValueError("Fail 1"), ValueError("Fail 2"), "Success"])
    mock_func.__name__ = "mock_task"
    
    decorated = retry(retries=3, delay=0.01)(mock_func)
    
    result = decorated()
    
    assert result == "Success"
    assert mock_func.call_count == 3

def test_retry_failure():
    """Test that it raises the exception after max retries."""
    mock_func = MagicMock(side_effect=ValueError("Persistent Failure"))
    mock_func.__name__ = "mock_task"
    
    decorated = retry(retries=3, delay=0.01)(mock_func)
    
    with pytest.raises(ValueError):
        decorated()
        
    assert mock_func.call_count == 3

def test_time_execution():
    with patch('utils.time.time') as mock_time:
        mock_time.side_effect = [1000.0, 1005.5, 1006.0]
        mock_func = MagicMock(return_value="Result")
        mock_func.__name__ = "slow_task"

        decorated = time_execution(mock_func)

        result = decorated()

        assert result == "Result"
        assert mock_time.call_count >= 2

def test_time_execution_failure():
    """Test that it logs error and re-raises exception on failure."""
    with patch("utils.time.time") as mock_time:
        mock_time.side_effect = [1000.0, 1002.0, 1003.0]
        
        mock_func = MagicMock(side_effect=ValueError("Boom"))
        mock_func.__name__ = "broken_task"
        
        decorated = time_execution(mock_func)
        
        with pytest.raises(ValueError):
            decorated()
            
        assert mock_time.call_count == 3