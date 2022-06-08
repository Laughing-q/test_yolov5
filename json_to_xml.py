import json
import os
import xml.dom.minidom as minidom

def json_xml(json_path):
	'''
	function : json文件转xml文件
	input    : json文件路径
	return   : 在json文件旁边生成xml文件
	'''
	def xml_dom(json_path):
		'''
		function : 生成xml文档
		input    : json文件路径
		return   : xml文档
		'''

		with open(json_path,'r',encoding='utf-8') as fp:
			datas = json.load(fp)
		
		# =========== annotation ===========
		folder_str = os.path.basename(os.path.dirname(json_path))
		filename_str = os.path.basename(json_path).replace("json", "jpg")
		path_str = os.path.dirname(json_path) + "/" + filename_str

		dom = minidom.getDOMImplementation().createDocument(None, 'annotation', None)
		anno = dom.documentElement

		folder = dom.createElement('folder')
		folder.appendChild(dom.createTextNode(folder_str))
		anno.appendChild(folder)

		filename = dom.createElement("filename")
		filename.appendChild(dom.createTextNode(filename_str))
		anno.appendChild(filename)

		path = dom.createElement("path")
		path.appendChild(dom.createTextNode(path_str))
		anno.appendChild(path)

		# =========== source ===========
		source = dom.createElement("source")

		database = dom.createElement("database")
		database.appendChild(dom.createTextNode("Unknown"))
		source.appendChild(database)

		anno.appendChild(source)

		# =========== size ===========
		w = datas[0]['imgW']
		h = datas[0]['imgH']

		size = dom.createElement("size")

		width = dom.createElement("width")
		width.appendChild(dom.createTextNode(str(w)))
		size.appendChild(width)

		height = dom.createElement("height")
		height.appendChild(dom.createTextNode(str(h)))
		size.appendChild(height)

		depth = dom.createElement("depth")
		depth.appendChild(dom.createTextNode("3"))
		size.appendChild(depth)

		anno.appendChild(size)

		# =========== segmented ===========
		segmented = dom.createElement("segmented")
		segmented.appendChild(dom.createTextNode("0"))
		anno.appendChild(segmented)

		# =========== rect and tag ===========
		for data in datas:
			x = int(data['beginX'])
			y = int(data['beginY'])
			x1 = int(data['endX'])
			y1 = int(data['endY'])
			tag = data["type"]

			obj = dom.createElement("object")

			name = dom.createElement("name")
			name.appendChild(dom.createTextNode(tag))
			obj.appendChild(name)

			pose = dom.createElement("pose")
			pose.appendChild(dom.createTextNode("Unspecified"))
			obj.appendChild(pose)

			truncated = dom.createElement("truncated")
			truncated.appendChild(dom.createTextNode("0"))
			obj.appendChild(truncated)

			difficult = dom.createElement("difficult")
			difficult.appendChild(dom.createTextNode("0"))
			obj.appendChild(difficult)

			bndbox = dom.createElement("bndbox")

			xmin = dom.createElement("xmin")
			xmin.appendChild(dom.createTextNode(str(x)))
			bndbox.appendChild(xmin)

			ymin = dom.createElement("ymin")
			ymin.appendChild(dom.createTextNode(str(y)))
			bndbox.appendChild(ymin)

			xmax = dom.createElement("xmax")
			xmax.appendChild(dom.createTextNode(str(x1)))
			bndbox.appendChild(xmax)

			ymax = dom.createElement("ymax")
			ymax.appendChild(dom.createTextNode(str(y1)))
			bndbox.appendChild(ymax)
			obj.appendChild(bndbox)

			anno.appendChild(obj)
		return dom

	dom = xml_dom(json_path)

	folder = os.path.dirname(json_path)
	filename = os.path.basename(json_path)
	file_pre = os.path.splitext(filename)[0]
	write_path = folder + "/" + file_pre + ".xml"

	f = open(write_path, 'w',encoding='utf-8')
	dom.writexml(f, addindent='    ', newl='\n',encoding='UTF-8')

if __name__ == '__main__':
	json_path = "/home/yuge/data/kaola.json"
	json_xml(json_path)