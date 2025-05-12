import pytest
from unittest.mock import patch, MagicMock
import os
from src.backend.email_sender.service.email_service import send_email

@pytest.fixture
def mock_env_vars():
    return {
        'SENDER_EMAIL': 'test@example.com',
        'SENDER_PASSWORD': 'test_password',
        'SMTP_SERVER': 'smtp.test.com',
        'SMTP_PORT': '587'
    }

def test_send_email_success(mock_env_vars):
    with patch.dict(os.environ, mock_env_vars):
        with patch('smtplib.SMTP') as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server

            result = send_email(
                receiver_email='recipient@example.com',
                subject='Test Subject',
                body='Test Body'
            )

            assert result is True
            mock_smtp.assert_called_once_with('smtp.test.com', '587')
            mock_server.starttls.assert_called_once()
            mock_server.login.assert_called_once_with('test@example.com', 'test_password')
            mock_server.send_message.assert_called_once()

def test_send_email_failure(mock_env_vars):
    with patch.dict(os.environ, mock_env_vars):
        with patch('smtplib.SMTP') as mock_smtp:
            mock_smtp.side_effect = Exception('SMTP Error')

            result = send_email(
                receiver_email='recipient@example.com',
                subject='Test Subject',
                body='Test Body'
            )

            assert result is False

def test_send_email_missing_credentials():
    with patch.dict(os.environ, {}, clear=True):
        result = send_email(
            receiver_email='recipient@example.com',
            subject='Test Subject',
            body='Test Body'
        )
        assert result is False
