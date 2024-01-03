# Django Blog Project

This is a simple Django blog project created following the examples in the "Django 4 by Example" book.

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Installation](#installation)


## Description

Provide a brief description of your project. Mention the purpose, goals, and any other relevant information.

## Features

List the key features of your Django blog project. For example:
- User authentication
- CRUD operations for blog posts
- Share posts via Email
- Advanced Search
- Recommend Similar Posts

## Installation

Provide instructions on how to install and set up your project locally. Include any dependencies and steps required for a successful installation.

```bash
# Clone the repository
git clone https://github.com/Ayman097/My_Blog.git

# Navigate to the project directory
cd My_Blog

# Create a virtual environment (optional but recommended)
python -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Run the development server
python manage.py runserver
