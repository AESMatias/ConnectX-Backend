# FastAPI 🚀
**Your Lightning-Fast FastAPI Server** 🏁
Tags:
- fastapi 🚄
- uvicorn 🐍
- python 🐉
- sqlalchemy 🗃️

## How to Get Started 🌟
1. Clone this repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`. 📦
3. Fill in the required parameters in the `.env` file (See `env.sample` for guidance). 🛠️
4. Run the `main.py` script. 🏃
5. Access the application via [http://localhost:8000](http://localhost:8000). 🌐

## Features ✨

### Real-Time Sockets 📡
- Instantly receive messages from the front-end when users join the chat. It's all about real-time communication! 🗨️

### Admin Superpowers 👑
- **GET /admin/show_users:** Marvel at the list of users. 🦸‍♂️
- **PUT /admin/range/{user_name}:** Bestow a mighty role upon a user. ⚔️
- **PUT /admin/ban/{user_name}:** Banish troublesome users. 🚫
- **PUT /admin/unban/{user_name}:** Grant a second chance by lifting the ban. ✌️
- **DELETE /admin/delete/{user_name}:** Delete users – the power is in your hands! ❌
- **DELETE /admin/tables/delete:** For when you need to clear the database slate. 🗑️

### User Empowerment 🧑‍🤝‍🧑
- **GET /user/{user_name}:** Uncover the secrets of a user's profile. 🕵️‍♂️
- **GET /user/profilePIC/:** Gaze upon the user's chosen profile picture. 📸
- **POST /user/profilePIC/upload:** Let users express themselves through profile pictures. 🌆
- **PUT /user/updatepass:** Users can update their passwords for added security. 🔒
- **PUT /user/updatename/:** A user's name can change, and we'll help you with that. 📝
- **DELETE /user/delete:** When it's time to say goodbye, delete a user account. 🚪

### Authentication Magic 🪄
- **POST /token:** Begin your journey with a login and receive the coveted access token. 🎩
- **GET /users/me/:** Discover the mystical secrets of the authenticated user. 🔍
- **POST /Register:** Bring new users into this magical realm. 🪶

Explore these fantastic features and unleash the full potential of your FastAPI server. If you have any questions or need further assistance, we're here to guide you on your quest! 🚀🔮🌟
