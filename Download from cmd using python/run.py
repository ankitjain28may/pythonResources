import urllib.request
url = input("Enter the URl\n")
name = input("Enter the name of the file (include extension)\n")
try:
    print("Downloading has started...\n")
    urllib.request.urlretrieve(url, name)
    print("Download completed..!!")
except Exception as e:
    print(e)
