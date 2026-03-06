import easyocr

reader=easyocr.Reader(['en'])
result=reader.readtext('receipt.jpeg')

for detection in result:
    print(detection[1])


#result is a list of detections
#each detection has 3 things
#detection[0]- coordiantes where on the iamge the text was found
#detection[1]-the actual text
#detetion[2]-confidence score


#so for detection in result loops through every piece fo text itm and prints detection[1]...jsut prints the text part



