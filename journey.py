class Journey:
	def __init__(self, name, start_station_name, end_station_name, identifier, rating, date):
		self.name = name
		self.start_station_name = start_station_name
		self.end_station_name = end_station_name
		self.identifier = identifier
		self.rating = rating
		self.date = date

	def __str__(self):
		return "name: {} \n start: {} \n end: {} \n identifier: {} \n rating: {} \n date: {}".format(
			self.name,
			self.start_station_name,
			self.end_station_name,
			self.identifier,
			self.rating,
			self.date
		)