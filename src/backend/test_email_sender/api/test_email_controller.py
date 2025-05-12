import pytest
import pandas as pd
from datetime import datetime, timedelta
from fastapi import HTTPException
import json
import os
import io
from unittest.mock import patch
from src.backend.email_sender.api.email_controller import process_emails

class DummyUploadFile:
    def __init__(self, filename, content: bytes):
        self.filename = filename
        self.file = io.BytesIO(content)

    async def read(self):
        return self.file.getvalue()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

def create_test_excel(df: pd.DataFrame) -> bytes:
    output = io.BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)
    return output.read()

@pytest.mark.asyncio
async def test_process_emails_success():
    old_date = datetime.now() - timedelta(days=365)

    df = pd.DataFrame({
        'email': ['test@example.com'],
        'date': [old_date]
    })

    excel_content = create_test_excel(df)
    file = DummyUploadFile('test.xlsx', excel_content)

    with patch.dict(os.environ, {'EMAIL_TEMPLATE': 'Test template {lastUploadDate}'}):
        with patch('src.backend.email_sender.api.email_controller.send_email', return_value=True) as mock_send:
            response = await process_emails(file)

        assert response.status_code == 200
        data = json.loads(response.body.decode())
        assert data['total_records'] == 1
        assert data['processed_records'] == 1
        assert data['results'][0]['email'] == 'test@example.com'
        assert data['results'][0]['email_sent'] is True
        mock_send.assert_called_once()

