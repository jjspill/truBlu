# TruBlu - Connect Students with Tour Guides 

Welcome to TruBlu, a web-based platform revolutionizing the traditional college tour experience. TruBlu aims to break the one-size-fits-all approach, replacing impersonal group tours with a highly customized, one-on-one experience. Each prospective student has unique interests, preferences, and career aspirations. TruBlu matches prospective students with tour guides based on a wide range of criteria, including their chosen major, extracurricular interests, and more.

TruBlu aims to bring authenticity and depth to your college tour in this new era of campus exploration. By pairing prospective students with guides who can share first-hand insights and experiences, we ensure your visit is not just a tour but an enriching experience filled with real insights into what studying, living, and socializing on that campus truly feels like. 

## Overview

TruBlu is a Flask-based web application, with its main functionality to provide a platform for students seeking campus tours to connect with tour guides. Users (students) can create profiles, upload pictures, browse available tour guides, and get recommendations based on their preferences. Tour guides can also create their profiles, specifying their areas of expertise, availability, and other related information.

## Key Features

- **User authentication:** Secure registration and login functionality for both students.
- **Profile customization:** Users can set up their profiles with relevant details and preferences.
- **Search functionality:** Browse and search for tour guides based on various parameters.
- **Recommendation engine:** A matching algorithm to suggest suitable tour guides to users based on their preferences.

## Technologies Used

Here's a rundown of the main technologies and libraries used in building TruBlu:

## Technologies Used in TruBlu

- **Web Framework:** Flask is used for managing HTTP requests and responses, as well as building the web routes.
- **Database:** The site uses a SQLite database for data storage.
- **Security Libraries:** Python's hashlib and uuid libraries are used for password hashing and salting. This is vital for securely storing user passwords.
- **User Session Management:** Flask sessions are utilized to manage user sessions, allowing the system to differentiate between logged-in and logged-out users.
- **Front-End:** The front-end uses HTML and CSS. Flask's render_template is used to return HTML files.
