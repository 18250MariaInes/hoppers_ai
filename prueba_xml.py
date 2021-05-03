from xml.dom import minidom
import os 

root = minidom.Document()
  
xml = root.createElement('root') 
root.appendChild(xml)
  
productChild = root.createElement('product')
productChild.setAttribute('name', 'Geeks for Geeks')
  
xml.appendChild(productChild)
  
xml_str = root.toprettyxml(indent ="\t") 

print(xml_str)