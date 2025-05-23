FROM python:3.12 as builder

USER root

# Create app directory
WORKDIR /app

# Install app dependencies
RUN python -m pip install --upgrade pip
COPY ./envs ./envs 
RUN pip install --no-cache-dir -r ./envs/linux/requirements_backend.txt
# Copy app source
COPY . .

EXPOSE 8000

#?   D E B U G   I M A G E
FROM builder as debug

RUN pip install debugpy==1.7.0 -t /tmp 
ENV PYDEVD_DISABLE_FILE_VALIDATION=1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive

CMD ["sh", "-c", "python /tmp/debugpy --listen 0.0.0.0:5678  --wait-for-client -m uvicorn src.backend.web:app --reload --host 0.0.0.0 --port 8000"]


#!   P R O D U C T I O N   I M A G E
FROM builder as prod
#CMD uvicorn src.backend.web:app -k uvicorn.workers.UvicornWorker --workers 2 --bind 0.0.0.0:8000
CMD ["uvicorn", "src.backend.api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
