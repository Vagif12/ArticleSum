FROM python:3.7

# Install manually all the missing libraries
RUN apt-get update
RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libnss3 lsb-release xdg-utils
RUN apt-get install -y libappindicator1; apt-get -fy install
RUN apt install xvfb -y

# Install Chrome
RUN wget http://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_97.0.4692.71-1_amd64.deb
RUN dpkg -i google-chrome-stable_97.0.4692.71-1_amd64.deb; apt-get -fy install

# Install Python dependencies.
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy all files into container
COPY . .


# Expose port 80
EXPOSE 5000

# Define endpoint for FastAPI server running on port 80 of the localhost
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
