from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
from datetime import datetime, timedelta
import os
from typing import List
from dotenv import load_dotenv
from ..service.email_service import send_email

load_dotenv()

router = APIRouter()

@router.post("/process-emails")
async def process_emails(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith('.xlsx'):
            raise HTTPException(status_code=400, detail="Only .xlsx files are allowed")
        
        df = pd.read_excel(file.file)
        
        required_columns = ['email', 'date']
        if not all(col in df.columns for col in required_columns):
            raise HTTPException(
                status_code=400, 
                detail=f"Excel file must contain columns: {', '.join(required_columns)}"
            )
        
        df['date'] = pd.to_datetime(df['date'])
        
        six_months_ago = datetime.now() - timedelta(days=180)
        
        old_records = df[df['date'] <= six_months_ago]
        
        email_template = os.getenv('EMAIL_TEMPLATE', '')
        if not email_template:
            raise HTTPException(
                status_code=500,
                detail="Email template not found in environment variables"
            )
        
        results = []
        for _, row in old_records.iterrows():
            email_body = email_template.format(lastUploadDate=row['date'].strftime('%Y-%m-%d'))
            
            success = send_email(
                receiver_email=row['email'],
                subject="Reminder: Your Record is Over 6 Months Old",
                body=email_body
            )
            
            results.append({
                "email": row['email'],
                "date": row['date'].strftime('%Y-%m-%d'),
                "email_sent": success
            })
        
        return JSONResponse({
            "message": "Processing completed",
            "total_records": len(df),
            "processed_records": len(results),
            "results": results
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        file.file.close()
