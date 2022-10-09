
#libraries
import ee
import requests
import geemap
from IPython.display import Image
import requests

#Start Earth Engine 
ee.Initialize()


#Authorization
Map = geemap.Map(center=[36.680047, 27.537003], zoom=12)
Map


#Defining Area Of Interest
geometry = ee.Geometry.Polygon(
    [
        [
            [27.537003, 36.680047],
            [27.537003, 36.726265],
            [27.596741, 36.726265],
            [27.596741 ,36.680047],
        ]
    ]
)

#Filtering out Sentinel 2 imagery

sent2_ts = geemap.sentinel2_timeseries(
    roi = geometry,
    start_year='2022',
    end_year='2022',
    start_date='01-01',
    end_date='09-30',
    frequency='month',
)

collection = sent2_ts

images = collection.toList(collection.size())
dates = geemap.image_dates(collection).getInfo()
size = images.size().getInfo()


title = "2022 Datça Orman Yangını / Mesudiye "


#Creating a timelapse of imagery

out = geemap.sentinel2_timelapse(
    roi=geometry,
    start_year= 2022,
    end_year= 2022,
    start_date='01-01',
    end_date='08-30',
    frequency='month',
    frames_per_second=2,
    title = title
)


#Visualising timelapse

Image(filename=out)
 
#Posting timelapse into IPFS


url = "https://api.pinata.cloud/pinning/pinFileToIPFS"

payload={}
files=[
  ('file',('datca_gif',open(out,'rb'),'image/gif'))
]
headers = {
  'Authorization': 'Bearer YOUR_TOKEN_HERE'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)