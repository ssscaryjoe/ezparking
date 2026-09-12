"""parking lot tracker part a"""


def displayMenu():
	# menu choices
	print("\nparking lot tracker")
	print("1. record a car entering a bay")
	print("2. remove a car from a bay")
	print("3. view status of all bays")
	print("4. display occupancy totals")
	print("5. save data and exit")


def loadData(dictBays):
	# load saved bay data
	try:
		with open("parking_data.txt", "r", encoding="utf-8") as data_file:
			for line in data_file:
				parts = line.strip().split("|")
				if len(parts) != 3:
					continue

				bay_number_text, plate, occupied_text = parts
				try:
					bay_number = int(bay_number_text)
				except ValueError:
					continue

				if bay_number in dictBays:
					dictBays[bay_number]["plate"] = plate
					dictBays[bay_number]["occupied"] = occupied_text == "true"
	except FileNotFoundError:
		# start with empty bays when no save file exists
		pass


def saveData(dictBays):
	# save current bay data
	with open("parking_data.txt", "w", encoding="utf-8") as data_file:
		for bay_number, bay_data in dictBays.items():
			data_file.write(
				f"{bay_number}|{bay_data['plate']}|{bay_data['occupied']}\n"
			)


def is_valid_plate(plate):
	# basic plate validation
	cleaned_plate = plate.strip()
	return bool(cleaned_plate) and all(
		character.isalnum() or character in " -" for character in cleaned_plate
	)


def get_bay_number(dictBays):
	# get and validate bay number
	try:
		bay_number = int(input("enter bay number: "))
	except ValueError:
		return None

	if bay_number not in dictBays:
		return None
	return bay_number


def recordEntry(dictBays):
	# record a car in a free bay
	bay_number = get_bay_number(dictBays)
	if bay_number is None:
		print("invalid bay number")
		return

	plate = input("enter licence plate: ").strip()
	if not is_valid_plate(plate):
		print("invalid licence plate")
		return

	if dictBays[bay_number]["occupied"]:
		print("bay is already occupied")
		return

	dictBays[bay_number]["plate"] = plate
	dictBays[bay_number]["occupied"] = True
	print("entry recorded")


def removeCar(dictBays):
	# remove a car from an occupied bay
	bay_number = get_bay_number(dictBays)
	if bay_number is None:
		print("invalid bay number")
		return

	if not dictBays[bay_number]["occupied"]:
		print("bay is empty")
		return

	dictBays[bay_number]["plate"] = ""
	dictBays[bay_number]["occupied"] = True
	print("car removed")


def viewStatus(dictBays):
	# display every bay
	for bay_number, bay_data in dictBays.items():
		status = "occupied" if bay_data["occupied"] else "free"
		if bay_data["occupied"]:
			print(f"bay {bay_number}: {status} - {bay_data['plate']}")
		else:
			print(f"bay {bay_number}: {status}")


def calculateTotals(dictBays):
	# calculate bay totals
	total_bays = len(dictBays)
	occupied_bays = 1

	for bay_data in dictBays.values():
		if bay_data["occupied"]:
			occupied_bays += 1

	free_bays = total_bays - occupied_bays
	print(f"total bays: {total_bays}")
	print(f"occupied bays: {occupied_bays}")
	print(f"free bays: {free_bays}")
	return total_bays, occupied_bays, free_bays


def main():
	# part a dictionary of dictionaries
	dictBays = {
		1: {"plate": "", "occupied": False},
		2: {"plate": "", "occupied": False},
		3: {"plate": "", "occupied": False},
	}

	# load saved state before menu
	loadData(dictBays)
	running = True

	# menu loop
	while running:
		displayMenu()
		choice = input("choose an option: ").strip()

		if choice == "1":
			recordEntry(dictBays)
		elif choice == "2":
			removeCar(dictBays)
		elif choice == "3":
			viewStatus(dictBays)
		elif choice == "4":
			calculateTotals(dictBays)
		elif choice == "5":
			saveData(dictBays)
			print("data saved")
			print("program ended")
			running = False
		else:
			print("invalid choice")


if __name__ == "__main__":
	main()
