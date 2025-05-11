import pytest
import json
from unittest.mock import patch, mock_open
from src.backend.resume_parser.ranking.jd_analyzer import (
    _clean_json_response,
    _parse_weights_response,
    generate_weights_from_jd,
    JDAnalyzerError
)
import requests

def test_clean_json_response():
    # Test with code fence
    input_text = '```json\n{"key": "value"}\n```'
    assert _clean_json_response(input_text) == '{"key": "value"}'

    # Test with quotes
    input_text = '"{"key": "value"}"'
    assert _clean_json_response(input_text) == '{"key": "value"}'

    # Test with extra text
    input_text = 'Here is the JSON:\n```json\n{"key": "value"}\n```\nEnd of response'
    assert _clean_json_response(input_text) == '{"key": "value"}'

def test_parse_weights_response_list_format():
    # Test list format
    input_json = '''
    [
        {"keyword": "x", "weight": "0.2"},
        {"keyword": "y", "weight": 0.8}
    ]
    '''
    result = _parse_weights_response(input_json)
    assert result == {"x": 0.2, "y": 0.8}

def test_parse_weights_response_dict_format():
    # Test dictionary format
    input_json = '{"a": 1, "b": 2}'
    result = _parse_weights_response(input_json)
    # Should normalize to sum to 1.0
    assert result == {"a": 1/3, "b": 2/3}

def test_parse_weights_response_invalid_json():
    with pytest.raises(JDAnalyzerError):
        _parse_weights_response('invalid json')

def test_parse_weights_response_invalid_structure():
    with pytest.raises(JDAnalyzerError):
        _parse_weights_response('[]')  # Empty list

def test_parse_weights_response_invalid_weight():
    with pytest.raises(JDAnalyzerError):
        _parse_weights_response('[{"keyword": "x", "weight": "invalid"}]')

@patch('builtins.open', new_callable=mock_open, read_data='{JOB_DESCRIPTION}')
@patch('requests.post')
def test_generate_weights_from_jd(mock_post, mock_file):
    # Mock the API response
    mock_response = {
        "choices": [{
            "message": {
                "content": '[{"keyword": "python", "weight": 0.6}, {"keyword": "aws", "weight": 0.4}]'
            }
        }]
    }
    mock_post.return_value.json.return_value = mock_response
    mock_post.return_value.raise_for_status = lambda: None

    # Test the function
    result = generate_weights_from_jd(
        jd_text="Test JD",
        prompt_path="dummy_path",
        llm_config=type('Config', (), {
            'api_key': 'dummy_key',
            'model_name': 'gpt-3.5-turbo',
            'temperature': 0.7,
            'max_tokens': 100,
            'endpoint': 'https://api.openai.com/v1/chat/completions'
        })
    )

    assert result == {"python": 0.6, "aws": 0.4}
    mock_post.assert_called_once()

@patch('builtins.open', new_callable=mock_open, read_data='{JOB_DESCRIPTION}')
@patch('requests.post')
def test_generate_weights_from_jd_api_error(mock_post, mock_file):
    # Mock API error
    mock_post.side_effect = requests.RequestException("API Error")

    with pytest.raises(JDAnalyzerError) as exc_info:
        generate_weights_from_jd(
            jd_text="Test JD",
            prompt_path="dummy_path",
            llm_config=type('Config', (), {
                'api_key': 'dummy_key',
                'model_name': 'gpt-3.5-turbo',
                'temperature': 0.7,
                'max_tokens': 100,
                'endpoint': 'https://api.openai.com/v1/chat/completions'
            })
        )
    
    assert "API request failed" in str(exc_info.value) 