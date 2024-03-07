import customtkinter as ctk
import requests
from bs4 import BeautifulSoup

url = "https://www.imdb.com/list/ls091520106"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

name_data = []
rate_data = []
release_year_data = []
gross_data = []
metascore_data = []
genre_data = []
runtime_data = []
age_limit = []
directors = []

movie_list = soup.findAll('div', attrs={'class': 'lister-item-content'})

for movie_data in movie_list:
    names = movie_data.h3.a.text
    releases = movie_data.h3.find('span', class_='lister-item-year text-muted unbold').text
    name_data.append(names + releases)

    details_element1 = movie_data.p.find('span', class_='certificate')

    if details_element1:  # age_limit
        details = details_element1.text
        age_limit.append(details)
    else:
        age_limit.append(None)

    details_element2 = movie_data.p.find('span', class_='runtime')
    details2 = details_element2.text
    runtime_data.append(details2)

    details_element3 = movie_data.p.find('span', class_='genre')
    details3 = details_element3.text
    genre_data.append(details3)

    nv = movie_data.find_all('span', attrs={'name': 'nv'})
    if len(nv) > 1:
        gross = nv[1].text
        gross_data.append(gross)

    director = movie_data.findAll('p', class_='text-muted text-small')[1].find_all('a')[0].text
    directors.append(director)

    for MSscore in movie_list:
        metascore_list = MSscore.findAll('div', attrs={'class': 'inline-block ratings-metascore'})

        for metascore in metascore_list:
            favorable_scores = metascore.findAll('span', class_='metascore favorable')
            mixed_scores = metascore.findAll('span', class_='metascore mixed')

            if favorable_scores:
                for score in favorable_scores:
                    metascore_data.append(score.text)

            elif mixed_scores:
                for score in mixed_scores:
                    metascore_data.append(score.text)

            else:
                metascore_data.append(f"Not existing in {url}")


rating_list = soup.findAll('div', attrs={'class': 'ipl-rating-widget'})

for rate in rating_list:
    ratings = rate.find('span', class_='ipl-rating-star__rating').text
    rate_data.append(ratings)
    if not ratings:
        rate_data.append(f"Not existing in {url}")

ctk.set_appearance_mode("System")

ctk.set_default_color_theme("blue")


class Gui(ctk.CTk):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.title("ImdbApp")
        self.geometry("600x700")

        self.FilmLabel = ctk.CTkLabel(self, text="Choose a Film name", bg_color="dark blue")
        self.FilmLabel.grid(row=4, column=0, padx=20, pady=20, sticky="ew")

        self.NamesOptionMenu = ctk.CTkOptionMenu(self, values=name_data + release_year_data)
        self.NamesOptionMenu.grid(row=4, column=1, padx=20, pady=20, columnspan=2, sticky="ew")

        self.displayBox = ctk.CTkTextbox(self, width=405, height=100)
        self.displayBox.grid(row=13, column=0, columnspan=2, padx=30, pady=20, sticky="ew")

        self.additional_buttons = []

        def show_additional_buttons():
            additional_buttons = ["Show Age Limit and Runtime", "Show Rating", "Show Gross", "Show Metascore", "Show Genre", "Show Director"]
            for i, button_text in enumerate(additional_buttons):
                additional_button = ctk.CTkButton(self, text=button_text, width=4,command=lambda button_name=button_text: self.additional_button_click(button_name))
                additional_button.grid(row=7 + i, column=1, columnspan=2, padx=20, pady=20, sticky="w")
                self.additional_buttons.append(additional_button)

        self.generateResultsButton = ctk.CTkButton(self, text="Get Details", command=show_additional_buttons)

        self.generateResultsButton.grid(row=5, column=1, columnspan=2, padx=20, pady=20, sticky="ew")

    def additional_button_click(self, button_text):

        if button_text == "Show Genre":
            selected_movie_name = self.NamesOptionMenu.get()
            genre_data_for_selected_movie = get_genre_data(selected_movie_name)
            self.displayBox.delete(1.0, ctk.END)
            self.displayBox.insert(ctk.END, f"{selected_movie_name} is {genre_data_for_selected_movie}")

        elif button_text == "Show Rating":
            selected_movie_name = self.NamesOptionMenu.get()
            imdb_data_for_selected_movie = get_imdbRating_data(selected_movie_name)
            self.displayBox.delete(1.0, ctk.END)
            self.displayBox.insert(ctk.END, f"{selected_movie_name} is rated {imdb_data_for_selected_movie}")

        elif button_text == "Show Age Limit and Runtime":
            selected_movie_name = self.NamesOptionMenu.get()
            data_AR_for_selected_movie = get_AgeLimitandRuntime_data(selected_movie_name)
            self.displayBox.delete(1.0, ctk.END)
            self.displayBox.insert(ctk.END, f"{selected_movie_name} is {data_AR_for_selected_movie}")

        elif button_text == "Show Metascore":
            selected_movie_name = self.NamesOptionMenu.get()
            metascore_data_for_selected_movie = get_metascore_data(selected_movie_name)
            self.displayBox.delete(1.0, ctk.END)
            self.displayBox.insert(ctk.END, f"{selected_movie_name}'s metascore is {metascore_data_for_selected_movie}")

        elif button_text == "Show Gross":
            selected_movie_name = self.NamesOptionMenu.get()
            gross_data_for_selected_movie = get_gross_data(selected_movie_name)
            self.displayBox.delete(1.0, ctk.END)
            self.displayBox.insert(ctk.END, f"{selected_movie_name} earned about {gross_data_for_selected_movie}")

        elif button_text == "Show Director":
            selected_movie_name = self.NamesOptionMenu.get()
            director_data_for_selected_movie = get_director_data(selected_movie_name)
            self.displayBox.delete(1.0, ctk.END)
            self.displayBox.insert(ctk.END, f"{director_data_for_selected_movie} is the director of {selected_movie_name}")


def get_imdbRating_data(movie_name):
    for name_with_release in name_data:
        if movie_name in name_with_release:
            return rate_data[name_data.index(name_with_release)]


def get_metascore_data(movie_name):
    for name_with_release in name_data:
        if movie_name in name_with_release and name_data.index(name_with_release) < len(metascore_data):
            return metascore_data[name_data.index(name_with_release)]


def get_gross_data(movie_name):
    for name_with_release in name_data:
        if movie_name in name_with_release and name_data.index(name_with_release) < len(gross_data):
            return gross_data[name_data.index(name_with_release)]


def get_genre_data(movie_name):
    for name_with_release in name_data:
        if movie_name in name_with_release and name_data.index(name_with_release) < len(genre_data):
            return genre_data[name_data.index(name_with_release)]


def get_director_data(movie_name):
    for name_with_release in name_data:
        if movie_name in name_with_release and name_data.index(name_with_release) < len(directors):
            return directors[name_data.index(name_with_release)]


def get_AgeLimitandRuntime_data(movie_name):
    for name_with_release in name_data:
        if movie_name in name_with_release:
            age = age_limit[name_data.index(name_with_release)]
            time = runtime_data[name_data.index(name_with_release)]
            return age, time


app = Gui()
app.mainloop()
