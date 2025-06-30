# Use the official Python image
FROM python:3.12-slim-bullseye

# 1. Set the working directory
WORKDIR /app

# 2. Create the qr_codes directory (and logs if you like) and make it world-writable
RUN mkdir -p qr_codes \
 && chmod 777 qr_codes

# 3. Copy only requirements first and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 4. Create a non-root user and any other directories your app needs
RUN useradd -m myuser \
 && mkdir -p logs \
 && chown myuser:myuser logs

# 5. Copy your application code into the container, preserving ownership
COPY --chown=myuser:myuser . .

# 6. Switch to the non-root user
USER myuser

# 7. Entrypoint & default command
ENTRYPOINT ["python", "main.py"]
CMD ["--url", "http://github.com/kaw393939"]
