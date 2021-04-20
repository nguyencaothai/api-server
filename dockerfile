FROM kalilinux/kali-rolling

# Install tool with apt-get (v1)
RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y python-is-python3
RUN apt-get install -y python3-pip
RUN apt-get install -y gobuster
RUN apt-get install -y nmap
RUN apt-get install -y dnsutils

# Create python_tool
WORKDIR /root/python_tool

# Install tool with pip (v1)
RUN pip install flask
RUN pip install python-whois

# Download api-server source code
WORKDIR /root
RUN git clone https://github.com/nguyencaothai/api-server.git
RUN cp -r /root/api-server/* /root/python_tool/

# Download SecLists
WORKDIR /root/python_tool
RUN git clone https://github.com/danielmiessler/SecLists.git

# Install and setup Sublist3r
RUN git clone https://github.com/aboul3la/Sublist3r.git
RUN pip install -r Sublist3r/requirements.txt

# Install tool with apt-get (v2)
RUN apt-get install -y whatweb
RUN apt-get install -y wpscan

# Install tool with pip (v2)
RUN pip install webtech
RUN pip install droopescan

# Install wafw00f
WORKDIR /root/python_tool
RUN git clone https://github.com/EnableSecurity/wafw00f.git
WORKDIR /root/python_tool/wafw00f
RUN python setup.py install

# Create /root/.dir/share/webtech 
RUN pip install webtech
WORKDIR /root
RUN mkdir .local
WORKDIR /root/.local
RUN mkdir share
WORKDIR /root/.dir/share
RUN mkdir webtech

# Install perl and joomscan
WORKDIR /root/python_tool
RUN apt-get install perl
RUN perl -MCPAN -e'install "LWP::Simple"'
RUN git clone https://github.com/OWASP/joomscan.git
WORKDIR /root/python_tool/joomscan

# Install with pip (v3)
RUN pip install BeautifulSoup4
RUN pip install xmltodict
RUN pip install tldextract

# Install with apt-get (v3)
RUN apt -y install exploitdb
RUN apt-get install -y nikto

# Run api-server 
WORKDIR /root/python_tool
CMD python api.py
