#!/usr/bin/python3
import cmd
import inspect
import requests
import subprocess
from os import getenv
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()


class BlogAppConsole(cmd.Cmd):
    intro = "\n\t\t**Welcome to Blog App Console**\nType 'help' for a list of commands or 'exit' to quit.\n"
    prompt = 'blog-app> '
    url = getenv('URL', 'http://localhost:5000')

    def do_exit(self, arg):
        """Exit the Blog App Console."""
        print("Exiting Blog App Console. Goodbye!")
        return True

    def do_EOF(self, args):
        """Handle Ctrl+D (EOF) to interrupt the current command."""
        return True

    def do_clear(self, args):
        """Clear the terminal screen (Linux only)."""
        if args:
            print("Usage: clear (no arguments)")
            return
        try:
            subprocess.call("clear", shell=True)
        except Exception as e:
            print(f"Error: {str(e)}")

    def do_signup(self, args):
        """Signup: Create a new user account.
        Usage: signup <username> <password>
        """
        args = args.split()
        if len(args) != 2:
            print("Usage: signup <username> <password>")
            return

        username, password = args
        data = {'username': username, 'password': password}

        try:
            response = requests.post(f'{self.url}/signup', data=data)
            print(response.text)
        except Exception as e:
            print(f"Error: {str(e)}")

    def do_login(self, args):
        """Login: Authenticate with an existing user account.
        Usage: login <username> <password>
        """
        args = args.split()
        if len(args) != 2:
            print("Usage: login <username> <password>")
            return

        username, password = args
        data = {'username': username, 'password': password}

        try:
            response = requests.post(f'{self.url}/login', data=data)
            print(response.text)
        except Exception as e:
            print(f"Error: {str(e)}")

    def do_articles(self, args):
        """Articles: Retrieve articles or a specific article by ID.
        Usage: articles [article_id]
        """
        if not args:
            # No argument provided, send GET request to /articles
            try:
                response = requests.get(f'{self.url}/articles')
                if response.status_code == 200:
                    print("Retrieved articles:")
                    print(response.text)
                else:
                    print("Failed to retrieve articles.")
            except Exception as e:
                print(f"Error: {str(e)}")
        else:
            args = args.split(' ')
            # Argument provided, append it to /articles/
            try:
                response = requests.get(f'{self.url}/articles/{args[0].strip()}')
                print(f"Retrieved article with ID {args[0]}:\n")
                print(response.text)
            except Exception as e:
                print(f"Error: {str(e)}")

    def do_delete(self, args):
        """Delete: Delete an article by ID.
        Usage: delete <token> <article_id>
        """
        args = args.split()
        if len(args) != 2:
            print("Usage: delete <token> <article_id>")
            return

        token, article_id = args
        headers = {'Authorization': token}

        try:
            response = requests.delete(f'{self.url}/articles/{article_id}',
                                       headers=headers)
            print(response.text)  # Print the response data
        except Exception as e:
            print(f"Error: {str(e)}")

    def do_publish(self, args):
        """Publish: Publish a new article.
        Usage: publish <Blog Title>
        """
        if not args or len(args.split(' ')) != 1:
            print('usage: publish <Blog Title>')
            return
        title = args.strip()
        # Call the articles command to retrieve the article content
        # self.do_articles(article_id)
        # Request user to enter the content
        content = input("Enter the blog content\n")
        # Request user for the token
        token = input("Enter your token: ")

        # Send a PUT request to update the article
        headers = {'Authorization': token}
        data = {'title': title, 'content': content}
        try:
            response = requests.post(f'{self.url}/articles', data=data,
                                     headers=headers)
            print(response.text)  # Print the response data
        except Exception as e:
            print(f"Error: {str(e)}")

    def do_update(self, args):
        """Update: Update an article by ID.
        Usage: update <article_id>
        """
        if len(args.split()) != 1:
            print("Usage: update <article_id>")
            return
        article_id = args.strip()
        # Call the articles command to retrieve the article content
        self.do_articles(article_id)
        # Request user to enter the content
        content = input("Enter the updated content\n")
        # Request user for the token
        token = input("Enter your token: ")
        # Send a POST request to create/update the article
        headers = {'Authorization': token}
        data = {'content': content}
        try:
            response = requests.put(f'{self.url}/articles/{article_id}',
                                     data=data, headers=headers)
            print(response.text)  # Print the response data
        except Exception as e:
            print(f"Error: {str(e)}")

    def do_logout(self, args):
        """Logout: Log out a user by invalidating the token.
        Usage: logout <token>
        """
        token = args.strip()
        if not token:
            print("Usage: logout <token>")
            return

        headers = {'Authorization': token}
        try:
            response = requests.get(f'{self.url}/logout', headers=headers)
            print(response.text)
        except Exception as e:
            print(f"Error: {str(e)}")

    def do_help(self, args):
        """Display available commands and their descriptions."""
        print("Available commands:")
        # print(self.get_names())
        # return
        for name, method in inspect.getmembers(self, predicate=inspect.ismethod):
            if name.startswith("do_"):
                command_name = name[3:]  # Remove "do_" prefix
                docstring = method.__doc__  # Get the docstring of the command
                if docstring:
                    print(f"{command_name}: {docstring}")
                else:
                    print(f"{command_name}")


if __name__ == '__main__':
    BlogAppConsole().cmdloop()
