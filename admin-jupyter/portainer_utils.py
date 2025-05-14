import requests

class PortainerAPI:
    def __init__(self, portainer_url, username, password):
        self.portainer_url = portainer_url
        self.username = username
        self.password = password
        self.token = self.get_jwt_token()
        self.default_repo_url = "https://github.com/gabnasello/qube-templates.git"
        self.default_repo_ref = "refs/heads/main"

    def get_jwt_token(self):
        url = f"{self.portainer_url}/api/auth"
        headers = {"Content-Type": "application/json"}
        data = {
            "Username": self.username,
            "Password": self.password
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()["jwt"]
        else:
            raise Exception(f"Failed to log in: {response.text}")

    def get_users(self):
        url = f"{self.portainer_url}/api/users"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch users: {response.text}")

    def get_teams(self):
        url = f"{self.portainer_url}/api/teams"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch teams: {response.text}")

    def get_stacks(self):
        url = f"{self.portainer_url}/api/stacks"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch stacks: {response.text}")

    def get_user_id_by_name(self, username):
        users = self.get_users()
        for user in users:
            if user['Username'] == username:
                return user['Id']
        raise Exception(f"User '{username}' not found.")

    def get_team_id_by_name(self, team_name):
        teams = self.get_teams()
        for team in teams:
            if team['Name'] == team_name:
                return team['Id']
        raise Exception(f"Team '{team_name}' not found.")

    def get_stack_id_by_name(self, stack_name):
        stacks = self.get_stacks()
        for stack in stacks:
            if stack['Name'] == stack_name:
                return stack['Id']
        raise Exception(f"Stack '{stack_name}' not found.")

    def stop_stack(self, stack_name_or_id, endpoint_id=1):
        # Check if name is provided, fetch stack ID
        stack_id = stack_name_or_id
        if isinstance(stack_name_or_id, str):
            stack_id = self.get_stack_id_by_name(stack_name_or_id)

        url = f"{self.portainer_url}/api/stacks/{stack_id}/stop?endpointId={endpoint_id}"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            print(f"Stack {stack_id} stopped successfully.")
        else:
            raise Exception(f"Failed to stop stack: {response.text}")

    def assign_stack_to_user(self, stack_name_or_id, user_name_or_id):
        # Check if name is provided, fetch stack ID and user ID
        stack_id = stack_name_or_id
        user_id = user_name_or_id
    
        if isinstance(stack_name_or_id, str):
            stack_id = self.get_stack_id_by_name(stack_name_or_id)
        if isinstance(user_name_or_id, str):
            user_id = self.get_user_id_by_name(user_name_or_id)
    
        # Fetch the ResourceControl ID using the Stack ID
        resource_control_id = self.get_resource_control_id_by_stack_id(stack_id)
    
        # Use the ResourceControl ID for the API call
        url = f"{self.portainer_url}/api/resource_controls/{resource_control_id}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        data = {
            "Users": [user_id],
            "Public": False,
            "AdministratorsOnly": False
        }
        response = requests.put(url, json=data, headers=headers)
        if response.status_code == 200:
            print(f"Stack '{stack_id}' assigned to user '{user_id}'.")
        else:
            raise Exception(f"Failed to assign stack: {response.text}")

    def get_resource_control_id_by_stack_id(self, stack_id):
        # Fetch stack details to retrieve the ResourceControl ID
        url = f"{self.portainer_url}/api/stacks/{stack_id}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            stack_data = response.json()
            return stack_data.get("ResourceControl", {}).get("Id")
        else:
            raise Exception(f"Failed to fetch stack details: {response.text}")

    def assign_user_to_team(self, user_name_or_id, team_name_or_id, role=2):
        # Check if name is provided, fetch user ID and team ID
        user_id = user_name_or_id
        team_id = team_name_or_id

        if isinstance(user_name_or_id, str):
            user_id = self.get_user_id_by_name(user_name_or_id)
        if isinstance(team_name_or_id, str):
            team_id = self.get_team_id_by_name(team_name_or_id)

        url = f"{self.portainer_url}/api/team_memberships"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        data = {
            "UserID": user_id,
            "TeamID": team_id,
            "Role": role
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print(f"User {user_id} assigned to team {team_id}.")
        else:
            raise Exception(f"Failed to assign user to team: {response.text}")

    def create_stack(self, stack_name, compose_file_path, endpoint_id=1, env_vars=None, 
                     repository_url=None, repository_ref=None):
        if repository_url is None:
            repository_url = self.default_repo_url
        if repository_ref is None:
            repository_ref = self.default_repo_ref
        
        url = f"{self.portainer_url}/api/stacks?type=2&method=repository&endpointId={endpoint_id}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        data = {
            "Name": stack_name,
            "RepositoryURL": repository_url,
            "RepositoryReferenceName": repository_ref,
            "composeFile": compose_file_path,
            "Env": env_vars if env_vars is not None else []
        }

        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print(f"Stack '{stack_name}' created successfully.")
        else:
            raise Exception(f"Failed to create stack: {response.text}")

    def create_user(self, new_username, new_password, role=1):
        """
        Creates a new user on the Portainer instance using the provided username, password, and role.
        
        Args:
        - new_username (str): The username for the new user.
        - new_password (str): The password for the new user.
        - role (int, optional): The role of the new user. Default is 1 (standard user).
        
        Raises:
        - Exception: If the user creation request fails.
        """
        url = f"{self.portainer_url}/api/users"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        data = {
            "Username": new_username,
            "Password": new_password,
            "Role": role  # 1 for a standard user, adjust as needed for other roles
        }

        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print(f"User '{new_username}' created successfully.")
        else:
            raise Exception(f"Failed to create user: {response.text}")

    def create_and_assign_stack(self, stack_name, compose_file_path, target_user, endpoint_id=1, env_vars=None, repository_url=None, repository_ref=None):
        """
        Creates a stack, stops it, and assigns it to a user.

        Args:
        - stack_name (str): The name of the stack to create.
        - compose_file_path (str): The path to the Docker Compose file.
        - target_user (str): The username of the user to assign the stack to.
        - endpoint_id (int): The endpoint ID where the stack will be deployed.
        - env_vars (list, optional): List of environment variables for the stack.
        - repository_url (str, optional): The Git repository URL for the stack's compose file.
        - repository_ref (str, optional): The branch or tag in the repository.

        Raises:
        - Exception: If any of the steps fail.
        """
        # Step 1: Create the stack
        print(f"Creating stack '{stack_name}'...")
        self.create_stack(stack_name, compose_file_path, endpoint_id, env_vars, repository_url, repository_ref)

        # Step 2: Stop the stack
        print(f"Stopping stack '{stack_name}'...")
        self.stop_stack(stack_name, endpoint_id)

        # Step 3: Assign the stack to the user
        print(f"Assigning stack '{stack_name}' to user '{target_user}'...")
        self.assign_stack_to_user(stack_name, target_user)

        print(f"Stack '{stack_name}' created, stopped, and assigned to '{target_user}' successfully.")
