from shapely.geometry import Polygon

def parse_polygon(file_name):

	"""
	This function parses a file to construct a polygon object.

	Pre-requesite: (1) file_name should reference a .waypoints file and include the file extension e.g. "file_name.waypoints", and (2) the file referenced by file_name should be in the following format, and all bracketed values must throw no exception when input into the float() function.

		|point_id|latitude|longitude|altitude|
		|<id_1>|<latitude_1>|<longitude_1>|<altitude_1>|
		...
		...
		...
		|<id_n>|<latitude_n>|<longitude_n>|<altitude_n>|

	Return: a Polygon instance as specified by the python shapely library.
	"""
	# list to build coordinates of polygon during creation
	coords = []
	file_in = open(file_name, 'r')
	file_in.readline()
	while True:
		line = file_in.readline()
		if line:
			# list to build coordinate of point during creation
			coord = []
			line = line.split('|')
			index = True
			for val in line:
				try:
					val = float(val)
					if index:
						index = False
						continue
					coord.append(val)
				except:
					continue
			coords.append(coord)
		else:
			break
	file_in.close()
	return Polygon(coords)