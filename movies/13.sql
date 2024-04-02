SELECT p2.name FROM movies
JOIN stars AS s1 ON movies.id = s1.movie_id
JOIN stars AS s2 ON movies.id = s2.movie_id
JOIN people AS p1 ON s1.person_id = p1.id
JOIN people AS p2 ON s2.person_id = p2.id
WHERE p1.name = "Kevin Bacon" AND p1.birth = "1958"
AND p1.id <> p2.id
ORDER BY p2.name;