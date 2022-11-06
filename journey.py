class Journey:
	def __init__(self, train_id, start_station_name, end_station_name, ssn, identifier, rating, date):
		self.train_id = train_id
		self.start_station_name = start_station_name
		self.end_station_name = end_station_name
		self.ssn = ssn
		self.identifier = identifier
		self.rating = rating
		self.date = date

	def __str__(self):
		return "train id: {} \n start: {} \n end: {} \n ssn: {} \n identifier: {} \n rating: {} \n date: {}".format(
			self.train_id,
			self.start_station_name,
			self.end_station_name,
			self.ssn,
			self.identifier,
			self.rating,
			self.date
		)