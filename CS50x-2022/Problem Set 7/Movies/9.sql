SELECT DISTINCT name FROM movies, stars, people WHERE year = "2004" AND movies.id = movie_id AND person_id = people.id ORDER BY birth ASC;