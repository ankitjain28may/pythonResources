import urllib.request
url = input("Enter the Download-Url\n")
name = input("Enter the name of the File with the extension\n")
try:
    print("Downloading starts...\n")
    urllib.request.urlretrieve(url, name)
    print("Download completed..!!")
except Exception as e:
    print(e)
