FROM alpine:latest
RUN apk update
RUN apk add py-pip
RUN apk add --no-cache python3-dev 
RUN pip install --upgrade pip
WORKDIR /app
COPY . /app
RUN pip --no-cache-dir install -r requirements.txt
ENV CINDER_PLATFORM=""
ENV CINDER_MODEL=""
ENV CINDER_PARADIGM=""
ENV OPENAI_API_KEY=""
ENV CINDER_ASSISTANT=""
CMD ["python3", "cinder.py"]