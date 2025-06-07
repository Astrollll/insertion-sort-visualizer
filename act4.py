class Linkedlist:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def add_all(self, other_list):
        self.items.extend(other_list.items)

    def display(self):
        half = len(self.items) // 2
        for i in range(half):
            print(f"{self.items[i]} - {self.items[i+half]}")

songs = Linkedlist()
songs.add("Shape of You")
songs.add("14")

artists = Linkedlist()
artists.add("Ed Sheeran")
artists.add("Silent Sanctuary")

playlist = Linkedlist()
playlist.add_all(songs)
playlist.add_all(artists)
playlist.display()